import time
import argparse
import itertools
import ismrmrd
import pathlib
import warnings

import numpy as np
import matplotlib.pyplot as plt

from pynufft import NUFFT
from ugad4fun.utils.dummy_conn import DummyConn



warnings.filterwarnings("ignore")

def accumulate_acquisitions(acquisitions, header):
    accumulated_acquisitions = []
    
    k_space_size = header.encoding[0].encodedSpace.matrixSize
    num_of_samples, number_of_pe_lines, num_of_slices = k_space_size.x, k_space_size.y, k_space_size.z
    print("-" * 50)
    print(rf"{'num_of_samples'.ljust(20)}{num_of_samples}")
    print(rf"{'number_of_pe_lines'.ljust(20)}{number_of_pe_lines}")
    print(rf"{'num_of_slices'.ljust(20)}{num_of_slices}")
    print("-" * 50)

    def assemble_buffer(acqs):
        print(f"assembling buffers from {len(acqs)} acquisitions.")
        
        num_of_channels = acqs[0].data.shape[0]
        print(rf"{'num_of_channels'.ljust(20)}{num_of_channels}")
        
        num_of_traj_dims = acqs[0].trajectory_dimensions
        print(rf"{'num_of_traj_dims'.ljust(20)}{num_of_traj_dims}")
        print("-" * 50)
    

        raw_buffer = np.zeros(
            (num_of_samples,
             number_of_pe_lines,
             num_of_slices,
             num_of_channels,
             ),
            dtype=np.complex64
        )

        traj_buffer = np.zeros(
            (num_of_samples,
             number_of_pe_lines,
             num_of_slices,
             num_of_traj_dims
             ),
            dtype=np.float32
        )

        for acq in acqs:
            data = acq.data
            traj = acq.traj
            
            raw_buffer[:, acq.idx.kspace_encode_step_1, acq.idx.kspace_encode_step_2, :] = acq.data.transpose(1, 0)
            
            # pynufft needs traj to be in the range of [-pi, pi]
            # traj = (traj - traj.min()) / (traj.max() - traj.min()) * 2 * np.pi - np.pi
            traj_buffer[:, acq.idx.kspace_encode_step_1, acq.idx.kspace_encode_step_2, :] = traj
        return raw_buffer, traj_buffer[:, :, 0, :]  # every slice has the same traj, so we just use the traj of the first slice

    for acquisition in acquisitions:
        accumulated_acquisitions.append(acquisition)
        if acquisition.is_flag_set(ismrmrd.ACQ_LAST_IN_SLICE):
            yield acquisition, assemble_buffer(accumulated_acquisitions)
            accumulated_acquisitions = []


def reconstruct_images(buffers, header):

    indices = itertools.count(start=1)
    field_of_view = header.encoding[0].reconSpace.fieldOfView_mm
    k_space_size = header.encoding[0].encodedSpace.matrixSize
    matrix = header.encoding[0].reconSpace.matrixSize
    
    num_of_samples, num_of_pe_lines, num_of_slices = k_space_size.x, k_space_size.y, k_space_size.z

    def combine_channels(img):
        # The buffer contains complex images, one for each channel. We combine these into a single image
        # through a sum of squares along the channels (axis 2).

        # return np.sqrt(np.sum(np.square(np.abs(img)), axis=2))
        combined_complex_img = np.zeros_like(img[:, :, :, 0])
        
        for z in range(img.shape[2]):
            start_time = time.time()
            print("-" * 50)
            print("combining channels...")
            print(f"slice: {z}")
            print("-" * 50)
            for x in range(img.shape[0]):
                for y in range(img.shape[1]):
                    mag = 0
                    phase = 0
                    for ch in range(img.shape[3]):
                        img_data = img[x, y, z, ch]
                        mag_tmp = img_data.real ** 2 + img_data.imag ** 2
                        phase += mag_tmp * np.angle(img_data)
                        mag += mag_tmp
                    combined_complex_img[x, y, z] = np.sqrt(mag) * np.exp(complex(0, phase / mag))
            end_time = time.time()
            print(f"time cost: {end_time - start_time}s")
        return combined_complex_img
        
    def reconstruct_image(data):
        # Reconstruction is a pynufft fft in this case.
        kspace_data = data[0]
        traj = data[1]   
        print("-" * 50)
        print('K space data shape: ', kspace_data.shape)
        print('Trajectory shape: ', traj.shape)
        print("-" * 50)
        
        num_of_channels = kspace_data.shape[0]
        
        kspace_data_reshape = kspace_data.reshape(-1, num_of_slices, kspace_data.shape[-1])
        traj_reshape = traj.reshape(-1, traj.shape[2])

        # image size
        Nd = (matrix.x, matrix.y)
        print('setting image dimension Nd...', Nd)
        # k-space size
        Kd = (num_of_samples, num_of_pe_lines)
        print('setting spectrum dimension Kd...', Kd)
        # interpolation size
        Jd = (6, 6)
        print('setting interpolation size Jd...', Jd)
        print("-" * 50)

        NufftObj = NUFFT()
        NufftObj.plan(traj_reshape, Nd, Kd, Jd)
        img = np.empty((Nd[0], Nd[1], num_of_slices, num_of_channels), dtype=np.complex128)
        print(f"image shape {img.shape}")
        print("-" * 50)
        
        print("Recontructing...")
        for slice_num in range(num_of_slices):
            for ch_num, current_raw_data in enumerate(kspace_data_reshape[:, slice_num, :].transpose(1, 0)):
                print(f"slice: {slice_num}\t chan: {ch_num}")
                img[:, :, slice_num, ch_num] = NufftObj.solve(current_raw_data, solver='cg', maxiter=25)
                
        image_final = combine_channels(img)
        print('reconstructing images finished!')
        return image_final

    for reference, data in buffers:
        print(rf"image_index = {indices}")
        yield ismrmrd.image.Image.from_array(
            reconstruct_image(data),
            acquisition=reference,
            image_index=next(indices),
            image_type=ismrmrd.IMTYPE_MAGNITUDE,
            # data_type=ismrmrd.DATATYPE_FLOAT,
            data_type=ismrmrd.DATATYPE_CXFLOAT,
            field_of_view=(field_of_view.x, field_of_view.y, field_of_view.z),
            transpose=True, # this will transpose the image data
        )
        
def recon(conn):
    print("Python reconstruction running - reconstructing images from acquisitions.")
    conn.filter(ismrmrd.acquisition.Acquisition)
    acquisitions = iter(conn)
    buffers = accumulate_acquisitions(acquisitions, conn.header)
    images = reconstruct_images(buffers, conn.header)

    for image in images:
        print("Sending image back to client.")
        print(f"image.matrix_size = '{image.matrix_size}'")
        conn.send(image)
    
    print("radial image recon done.")
    


if __name__ == '__main__':

    help_msg = "Radial recon using dummy connection"

    parser = argparse.ArgumentParser(description=help_msg)
    parser.add_argument('input_path', type=str,
                        help='the input path of an ismrmrd data')
    parser.add_argument('-o', '--out_path', type=str,
                        help='the output path of recon')
    
    args = parser.parse_args()
    input_path = pathlib.Path(args.input_path).absolute()
    output_path = pathlib.Path(args.out_path).absolute() if args.out_path else None

    start_time = time.time()
    dummy_conn = DummyConn(input_path, output_path)
    recon(dummy_conn)
    dummy_conn.close()

    print(f'time costed {round(time.time() - start_time, 2)}s')
 
