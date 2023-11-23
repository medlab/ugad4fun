import ismrmrd

import numpy as np
import matplotlib.pyplot as plt


class DummyConn:
    def __init__(self, dataset_path, save_path=None):
        """A dummy connection for reconstructing radial rawdata locally

        Parameters
        ----------
        dataset_path : str | pathlib.Path
            ismrmrd dataset path (should be a .h5 file)
        save_path : str | pathlib.Path, optional
            recon result output path, by default None
            if None, plot images

        Raises
        ------
        NameError
            wrong input file format
        FileNotFoundError
            input file not exists
        """
        self.dataset_path = dataset_path
        self.save_path = save_path
        self.plot_mode = False if save_path else True
        self.filter_data = list()
        self.save_dataset = None

        # check dataset path
        if not str(dataset_path).endswith('.h5'):
            raise NameError("File format should be exactly .h5")
        if not self.dataset_path.exists():
            raise FileNotFoundError(rf"{self.dataset_path} Not Found")
        print(f'Loading {self.dataset_path}...')
        self.dataset = ismrmrd.Dataset(self.dataset_path)
        print(f'Extracting Header info...')
        # self.header = ismrmrd.xsd.CreateFromDocument(self.dataset.read_xml_header())

    def filter(self, predicate, **kwargs):
        if not isinstance(predicate, type):
            raise ValueError(rf"predicate should be type ,get {predicate}")
        print(rf"Filtering {predicate}")
        if predicate is ismrmrd.Acquisition:
            print(f'{self.dataset.number_of_acquisitions()} acquisitions included')
            acquisition = []
            for acq_num in range(self.dataset.number_of_acquisitions()):
                acq = self.dataset.read_acquisition(acq_num)
                acquisition.append(acq)
            print(f'{len(acquisition)} raw data extracted')
            self.filter_data = iter(acquisition)
        elif predicate is ismrmrd.Waveform:
            print(f'{self.dataset.number_of_waveforms()} waveforms included')
            waveform = []
            for waveform_num in range(self.dataset.number_of_waveforms()):
                wave = self.dataset.read_waveform(waveform_num)
                waveform.append(wave)
            print(f'{len(waveform)} waveform data extracted')
            self.filter_data = iter(waveform)
        elif predicate is ismrmrd.Image:
            print(f'{self.dataset.number_of_images(**kwargs)} images included')
            image = []
            for image_num in range(self.dataset.number_of_images(**kwargs)):
                kwargs['imnum'] = image_num
                img = self.dataset.read_image(**kwargs)
                image.append(img)
            print(f'{len(image)} image data extracted')
            self.filter_data = iter(image)
        else:
            print(f'{predicate} unsupported')

    def send(self, image):
        if self.plot_mode:
            print('Plotting images...')
            image_data = image.data.squeeze()

            fig, ax = plt.subplots(1, 1, dpi=150)
            ax.imshow(image_data, 'gray')
            ax.set_aspect(image_data.shape[0] / image_data.shape[1])
            ax.set_title('image')
            ax.axis('off')
            plt.show()
        else:
            print('Saving images...')
            self.save_dataset = ismrmrd.Dataset(self.save_path)
            self.save_dataset.append_image('image', image)

    def close(self):
        self.dataset.close()
        if self.save_dataset:
            self.save_dataset.close()
        print('Dataset closed')

    def __next__(self):
        try:
            return next(self.filter_data)
        except StopIteration:
            print('Iterating data finished by next')
            raise StopIteration("Length too big")

    def __iter__(self):
        while True:
            try:
                yield next(self)
            except StopIteration:
                print('Iterating data finished by iteration')
                return
