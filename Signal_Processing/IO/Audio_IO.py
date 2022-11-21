# import pyaudio
import wave
# import wavio
import numpy as np
from abc import  abstractmethod
import multiprocessing
import threading
import time
import sounddevice as sd
from scipy.io.wavfile import write

class Parameters_IO:

    channels = 1 # is normally 2, one for each speaker, we set it to one as it would be quite complex otherwise.
    fs = None #to be initialized


class Segment_reader:
    """
    Class in charge of reading subsequent sound bits (or segments) from the microhphone
    """
    def __init__(self, total_seconds_to_record):
        self.__recorded_so_far = []
        #list of np arrayss where each np array correpsonds to a recording. They are ordered

        self.seconds_recorded_so_far = 0
        #nr of seconds that have been recorded so far

        self.total_seconds_to_record = total_seconds_to_record
        #nr of seconds to record in total, lenght of recording

        self.last_read_segment = np.array([])
        #last recorded segment

    def  read_segment(self, seconds):
        """"
        Reads #seconds from the mic and stores them as an np array in the
        self parameter last_read_segment
        """

        fs = Parameters_IO.fs

        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=Parameters_IO.channels)
        sd.wait()  # Wait until recording is finished
        self.recorded_so_far.append(myrecording)
        #write('output.wav', fs, myrecording)  # Save as WAV file
        self.last_read_segment= myrecording.T


    def get_recorded_so_far(self):
        """"
        Returns a numpy array with the recorded signal so far up to now.
        """
        return np.concatenate(self.__recorded_so_far, axis=0)


def do_something():
    print('Sleeping 5 second')
    time.sleep(5)
    print('Done sleeping')

if __name__ == '__main__':
    """"
    Parameters_IO.fs = 45000
    read_segment(2)

    start = time.perf_counter()

    t1 = threading.Thread(target=do_something)
    t2 = threading.Thread(target=read_segment, args=[5])

    t1.start()
    t2.start()

    t1.join()
    t2.join()



    finish = time.perf_counter()
    print(f'Finished in {round(finish - start, 2)} seconds')
    """