import pyaudio
import wave
import wavio
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
    recorded_so_far =[]

def  read_segment(seconds):
    fs = Parameters_IO.fs

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=Parameters_IO.channels)
    sd.wait()  # Wait until recording is finished
    write('output.wav', fs, myrecording)  # Save as WAV file
    return myrecording




def do_something():
    print('Sleeping 5 second')
    time.sleep(5)
    print('Done sleeping')

if __name__ == '__main__':
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
