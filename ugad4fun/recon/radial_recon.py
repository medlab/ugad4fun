import time
import argparse
import itertools
import ismrmrd
import pathlib

import numpy as np
import matplotlib.pyplot as plt

from pynufft import NUFFT
from ugad4fun.utils.dummy_conn import DummyConn


def accumulate_acquisitions(acquisitions, header):
    accumulated_acquisitions = []
    matrix_size = header.encoding[0].encodedSpace.matrixSize
    print("matrix_size.x=" + str(matrix_size.x))
    print("matrix_size.y=" + str(matrix_size.y))
    print("matrix_size.z=" + str(matrix_size.z))

    def assemble_buffer(acqs):
        print(f"Assembling buffer from {len(acqs)} acquisitions.")

        number_of_channels, number_of_samples = acqs[0].data.shape
        trajectory_dimensions = acqs[0].trajectory_dimensions
        print("number_of_channels=" + str(number_of_channels))
        print("number_of_samples=" + str(number_of_samples))
        print("trajectory_dimensions=" + str(trajectory_dimensions))

        raw_buffer = np.zeros(
            (matrix_size.x,
             matrix_size.y,
             matrix_size.z,
             number_of_channels,
             ),
            dtype=np.complex64
        )

        traj_buffer = np.zeros(
            (matrix_size.x,
             matrix_size.y,
             matrix_size.z,
             trajectory_dimensions
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
        return raw_buffer, traj_buffer

    for acquisition in acquisitions:
        accumulated_acquisitions.append(acquisition)
        if acquisition.is_flag_set(ismrmrd.ACQ_LAST_IN_SLICE):
            yield acquisition, assemble_buffer(accumulated_acquisitions)
            accumulated_acquisitions = []


def reconstruct_images(buffers, header):

    indices = itertools.count(start=1)
    field_of_view = header.encoding[0].reconSpace.fieldOfView_mm
    kspace_size = header.encoding[0].encodedSpace.matrixSize
    matrix = header.encoding[0].reconSpace.matrixSize

    def combine_channels(img):
        # The buffer contains complex images, one for each channel. We combine these into a single image
        # through a sum of squares along the channels (axis 2).

        # return np.sqrt(np.sum(np.square(np.abs(img)), axis=2))
        combined_complex_img = np.zeros_like(img[:, :, 0])
        for x in range(img.shape[0]):
            for y in range(img.shape[1]):
                mag = 0
                phase = 0
                for ch in range(img.shape[2]):
                    img_data = img[x, y, ch]
                    mag_tmp = img_data.real ** 2 + img_data.imag ** 2
                    phase += mag_tmp * np.angle(img_data)
                    mag += mag_tmp
                combined_complex_img[x, y] = np.sqrt(mag) * np.exp(complex(0, phase / mag))
        return combined_complex_img
        
    def reconstruct_image(data):
        # Reconstruction is a pynufft fft in this case.
        kspace_data = data[0].squeeze()
        traj = data[1].squeeze()    
        print('Trajectory shape: ', traj.shape)
        print('K space data shape: ', kspace_data.shape)
        kspace_data_reshape = kspace_data.reshape(-1, kspace_data.shape[2])

        traj_reshape = traj.reshape(-1, traj.shape[2])

        # image size
        Nd = (matrix.x, matrix.y)
        print('setting image dimension Nd...', Nd)
        # k-space size
        Kd = (kspace_size.x, kspace_size.y)
        print('setting spectrum dimension Kd...', Kd)
        # interpolation size
        Jd = (6, 6)
        print('setting interpolation size Jd...', Jd)

        NufftObj = NUFFT()
        NufftObj.plan(traj_reshape, Nd, Kd, Jd)
        img = np.empty((Nd[0], Nd[1], kspace_data_reshape.shape[1]), dtype=np.complex128)
        for index, current_raw_data in enumerate(kspace_data_reshape.transpose(1, 0)):
            img[:, :, index] = NufftObj.solve(current_raw_data, solver='cg', maxiter=25)
        image_final = combine_channels(img)
        print('reconstruct images finished!')
        return image_final

    for reference, data in buffers:
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
 