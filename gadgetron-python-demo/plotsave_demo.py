import gadgetron
import ismrmrd
from PIL import Image as PILImage
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import numpy as np
import logging
import multiprocessing
import typing
import faulthandler

def gen_image_to_send(header: ismrmrd.xsd.ismrmrdHeader,
                      acqs: typing.List[ismrmrd.Acquisition]=None,
                      connection: gadgetron.external.Connection=None):
    # target picture size, should get get from header in the future
    recon_matrix=header.encoding[0].reconSpace.matrixSize
    ic=1 # channel
    iz=1 # z size
    iy=recon_matrix.y # height
    ix=recon_matrix.x # width
    dpi=100 # data per inch
    figure=plt.gcf() # type: Figure
    figure.set_size_inches(ix/dpi,iy/dpi)

    print(rf'--------------------plot begin-----------------------')
    t = np.arange(0.0, 2.0, 0.01)
    s = np.sin(2 * np.pi * t)

    plt.plot(t, s)
    plt.title(r'$\alpha_i > \beta_i$', fontsize=20)
    plt.text(1, -0.6, r'$\sum_{i=0}^\infty x_i$', fontsize=20)
    plt.text(0.6, 0.6, r'$\mathcal{A}\mathrm{sin}(2 \omega t)$',
             fontsize=20)
    plt.xlabel('time (s)')
    plt.ylabel('volts (mV)')

    plt.savefig("result.png", dpi=dpi) # 3x100, 2x100
    print(rf'--------------------plot end-----------------------')

    h=ismrmrd.ImageHeader()# type: ismrmrd.ImageHeader
    #h.data_type = ismrmrd.DATATYPE_USHORT
    h.data_type = ismrmrd.DATATYPE_FLOAT
    h.image_type= ismrmrd.IMTYPE_MAGNITUDE
    h.channels=ic
    h.matrix_size=(ix,iy,iz)

    i=ismrmrd.Image(h)

    gray_scale_img=PILImage.open('result.png').convert('L') # gray scale image uint 8
    img_data=np.array(gray_scale_img)

    #TODO how to stand this code?
    #i.data[:] = img_data[:, ::-1].data[:]
    i.data[:]=img_data.data[:]
    return i

def do_work(connection:gadgetron.external.Connection):
    print('-----------------------begin------------------------')

    acqs=[] # type: typing.List[ismrmrd.Acquisition]

    for index, acq in enumerate(connection): # type: ismrmrd.Acquisition
        #do what you want todo?
        acqs.append(acq)
        pass

    print(rf'-------------------acq end-------------------')
    header=connection.header # type: ismrmrd.xsd.ismrmrdHeader
    image=gen_image_to_send(header, acqs, connection)

    print('  --begin-- try to send image')
    connection.send(image)
    print('  --end-- try to send image')

    print('-----------------------end------------------------')

if __name__ == "__main__":
    faulthandler.enable()
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    def spawn_process(*args):
        child = multiprocessing.Process(target=do_work, args=args)
        child.start()

    while True:
        gadgetron.external.listen(18000, spawn_process)
