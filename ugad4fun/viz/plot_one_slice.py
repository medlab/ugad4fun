import argparse
import ismrmrd

import numpy as np
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser()
parser.add_argument('-r', '--raw_path', type=str, default='../../rawdata.h5')

args = parser.parse_args()
fpath = args.raw_path

mrd_data = ismrmrd.Dataset(fpath)
acq_num = mrd_data.number_of_acquisitions()

xml_header = ismrmrd.xsd.CreateFromDocument(mrd_data.read_xml_header())
matrix_size = xml_header.encoding[0].encodedSpace.matrixSize

acquisitions = []
for num in range(acq_num):
    acquisitions.append(mrd_data.read_acquisition(num))

raw_data = np.zeros((matrix_size.x, matrix_size.y, matrix_size.z, acquisitions[0].data.shape[0]), dtype=np.complex64)



for acq in acquisitions:
    raw_data[:, acq.idx.kspace_encode_step_1, acq.idx.kspace_encode_step_2, :] = acq.data.transpose(1, 0)

print(f'RO:\t\t{raw_data.shape[0]}')
print(f'PE:\t\t{raw_data.shape[1]}')
print(f'Slice:\t\t{raw_data.shape[2]}')
print(f'Channel:\t{raw_data.shape[3]}')


fig, axes = plt.subplots(2, 2)
axes[0, 0].imshow(np.abs(raw_data[:, :, 0, 0]).T, cmap='gray')
axes[0, 0].axis('off')
axes[0, 0].set_title('Amplitude')

axes[0, 1].imshow(np.angle(raw_data[:, :, 0, 0]).T, cmap='gray')
axes[0, 1].axis('off')
axes[0, 1].set_title('Phase')

axes[1, 0].imshow(np.real(raw_data[:, :, 0, 0]).T, cmap='gray')
axes[1, 0].axis('off')
axes[1, 0].set_title('Real')

axes[1, 1].imshow(np.imag(raw_data[:, :, 0, 0]).T, cmap='gray')
axes[1, 1].axis('off')
axes[1, 1].set_title('Imag')

plt.show()
