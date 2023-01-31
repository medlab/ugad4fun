import time
import logging
import ismrmrd
import itertools
import numpy as np

from gadgetron.util.cfft import cfftn, cifftn

def remove_oversampling(acquisitions, header):
    print("Start remove_oversampling.")
    encoding_space = header.encoding[0].encodedSpace.matrixSize
    recon_space = header.encoding[0].reconSpace.matrixSize

    if encoding_space.x == recon_space.x:
        return acquisitions

    x0 = (encoding_space.x - recon_space.x) // 2
    x1 = (encoding_space.x - recon_space.x) // 2 + recon_space.x

    def crop_acquisition(acquisition):
        x_space = cifftn(acquisition.data, axes=[1])
        x_space = x_space[:, x0:x1]
        acquisition.resize(number_of_samples=x_space.shape[1], active_channels=x_space.shape[0])
        acquisition.center_sample = recon_space.x // 2
        acquisition.data[:] = cfftn(x_space, axes=[1])

        return acquisition

    print("End remove_oversampling.")
    return map(crop_acquisition, acquisitions)


def accumulate_acquisitions(acquisitions, header):
    print("Start accumulate_acquisitions.")
    accumulated_acquisitions = []
    matrix_size = header.encoding[0].encodedSpace.matrixSize
    print("matrix_size.x=" + str(matrix_size.x))
    print("matrix_size.y=" + str(matrix_size.y))
    print("matrix_size.z=" + str(matrix_size.z))

    def assemble_buffer(acqs):
        print("Start assemble_buffer.")
        number_of_channels = acqs[0].data.shape[0]
        number_of_samples = acqs[0].data.shape[1]

        buffer = np.zeros(
            (number_of_channels,
             number_of_samples,
             matrix_size.y,
             matrix_size.z),
            dtype=np.complex64
        )

        for acq in acqs:
            buffer[:, :, acq.idx.kspace_encode_step_1, acq.idx.kspace_encode_step_2] = acq.data

        print("End assemble_buffer.")
        return buffer

    for acquisition in acquisitions:
        accumulated_acquisitions.append(acquisition)
        if acquisition.is_flag_set(ismrmrd.ACQ_LAST_IN_SLICE):
            yield acquisition, assemble_buffer(accumulated_acquisitions)
            accumulated_acquisitions = []

    print("End accumulate_acquisitions.")

def reconstruct_images(buffers, header):
    print("Start reconstruct_images.")
    indices = itertools.count(start=1)
    field_of_view = header.encoding[0].reconSpace.fieldOfView_mm

    def reconstruct_image(kspace_data):
        return cifftn(kspace_data, axes=[1, 2, 3])

    def combine_channels(image_data):
        # return np.sqrt(np.sum(np.square(np.abs(image_data)), axis=0))
        return image_data[0]
        # return image_data

    for reference, data in buffers:
        print("image_index = " + str(indices))
        yield ismrmrd.image.Image.from_array(
            combine_channels(reconstruct_image(data)),
            acquisition=reference,
            image_index=next(indices),
            image_type=ismrmrd.IMTYPE_MAGNITUDE,
            # data_type=ismrmrd.DATATYPE_FLOAT,
            data_type=ismrmrd.DATATYPE_CXFLOAT,
            field_of_view=(field_of_view.x, field_of_view.y, field_of_view.z),
            transpose = False
        )
    
    print("End reconstruct_images.")


def recon_acquisitions(connection):
    print("Python reconstruction running - reconstructing images from acquisitions.")

    start = time.time()

    connection.filter(ismrmrd.Acquisition)

    acquisitions = iter(connection)
    acquisitions = remove_oversampling(acquisitions, connection.header)
    buffers = accumulate_acquisitions(acquisitions, connection.header)
    images = reconstruct_images(buffers, connection.header)

    for image in images:
        print("Sending image back to client.")
        print(f"image.matrix_size = '{image.matrix_size}'")
        connection.send(image)

    print("Python reconstruction done.")
