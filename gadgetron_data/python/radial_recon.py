"""
    three level of self proven
    1. dummy conn test
    2. gadgetron_ismrmrd_client -f xxx.h5 -c your_radial_pipline.xml
    3. uih online process
    external work(how to deploy):
        input layout:
            1. Docker file below
            2. something.py
            3. something.xml
        output:
            a docker file runnable
        Docker file:
            1. base_on: gadgetron_dev_no_cuda
            2. run copy something.py /opt/conda/envs/gadgetron/share/gadgetron/python/
            3. run copy something.xml /opt/conda/envs/gadgetron/share/gadgetron/config/
part 1:
def recon(conn):
    header=conn.header
    x=header.encoding.acq.matrix.x
    # collect line to a raw. + traj.buffer?
    # build om buffer by traj.buffer
    # build raw data buffer by raw.buffer
    # images=nufft(traj.buffer, recon_matrix, acq_matrix, some_factor).plan().execute(raw.buffer)
    # sos
    # send images
    pass
if __main__:
    # data_path (sys.argv[0]): h5.path
    # save_path (sys.argv[1]: if None then plot
    conn=dummy_conn(data_path, save_path, plot=True if save_path is None else False)
    recon(conn)
    
tip:
# extracting kspace line data to reconstruct images
for now, the method to extract line data, for reconstructing images, is not very reliable
what we do is 
1. find raw data has the flag ismrmrd.ACQ_FIRST_IN_SLICE
2. set append_acq = True
3. if the flag is ismrmrd.ACQ_LAST_IN_SLICE, append once, then stop
4. in this case, some data are gonna dropped(for now, not needed), be careful with that
"""
import time
import argparse
import itertools
import ismrmrd
import pathlib

import numpy as np
from pynufft import NUFFT
# from gadgetron.util.cfft import cfftn, cifftn

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
            traj_buffer[:, acq.idx.kspace_encode_step_1, acq.idx.kspace_encode_step_2, :] = acq.traj

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

    def combine_channels(image_data):
        # The buffer contains complex images, one for each channel. We combine these into a single image
        # through a sum of squares along the channels (axis 2).

        return np.sqrt(np.sum(np.square(np.abs(image_data)), axis=2))
        # return image_data[0]

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
        print("image_index = " + str(indices))
        yield ismrmrd.image.Image.from_array(
            reconstruct_image(data),
            acquisition=reference,
            image_index=next(indices),
            image_type=ismrmrd.IMTYPE_MAGNITUDE,
            # data_type=ismrmrd.DATATYPE_FLOAT,
            data_type=ismrmrd.DATATYPE_CXFLOAT,
            field_of_view=(field_of_view.x, field_of_view.y, field_of_view.z),
            transpose=True,
            matrix_size=(matrix.x, matrix.y, matrix.z)
        )
        
def do_work(conn):
    print("Python reconstruction running - reconstructing images from acquisitions.")
    conn.filter(ismrmrd.acquisition.Acquisition)
    acquisitions = iter(conn)
    buffers = accumulate_acquisitions(acquisitions, conn.header)
    images = reconstruct_images(buffers, conn.header)

    for image in images:
        print("Sending image back to client.")
        print(f"image.matrix_size = '{image.matrix_size}'")
        conn.send(image)
    
    print("Python reconstruction done.")
