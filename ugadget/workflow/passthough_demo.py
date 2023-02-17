import faulthandler
import logging
import multiprocessing

# from PIL import Image as PILImage
import gadgetron

def do_work(conn):
    print(rf'iam in')
    for index,acq in enumerate(conn):
        print(rf'{index}: data type: {type(acq)}')
        conn.send(acq)
        pass
    pass

if __name__ == "__main__":
    faulthandler.enable()
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    def spawn_process(*args):
        child = multiprocessing.Process(target=do_work, args=args)
        child.start()

    while True:
        gadgetron.external.listen(18000, spawn_process)
