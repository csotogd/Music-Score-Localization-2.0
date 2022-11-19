import pyaudio
import wave
import wavio
import numpy as np
from abc import  abstractmethod
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



if __name__ == '__main__':
    Parameters_IO.fs = 45000
    read_segment(5)


