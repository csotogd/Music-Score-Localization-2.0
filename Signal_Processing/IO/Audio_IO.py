import pyaudio
import wave
import wavio
import numpy as np
from abc import  abstractmethod

class Parameters_IO:


    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1 # is normally 2, one for each speaker, we set it to one as it would be quite complex otherwise.
    fs = None #to be initialized
    chunk_size = 1024
    recorded_so_far =[]
    frames= []




"""

def read_segment():
    
    
    Handles reading of audio segments.
    Reads a segement of audio using Pyaudio library. Works for PC. It may need to be changed for an Ipad
"""

"""
    ##inititalizes pyaudioobject
    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    stream = p.open(format=Parameters_IO.sample_format,
                    channels=Parameters_IO.channels,
                    rate=Parameters_IO.fs,
                    frames_per_buffer=Parameters_IO.chunk_size,
                    input=True)

    frames=[]

    for i in range(0, int(Parameters_IO.fs / Parameters_IO.chunk_size * Parameters_IO.seconds_per_segment)):
        data = stream.read(Parameters_IO.chunk_size)
        numpydata = np.frombuffer(data, dtype=np.int16)
        Parameters_IO.recorded_so_far += (list(numpydata))
        Parameters_IO.frames.append(data)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    return frames









def store_recorded_signal(filename ='output.wav'):
"""
"""
    stores the recorded signal as a wav file

     Parameters
    ----------
     filename: string
        relative path to the file in which the sound will be stored.
        must be a ".wav" file
"""
"""
    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    stream = p.open(format=Parameters_IO.sample_format,
                    channels=Parameters_IO.channels,
                    rate=Parameters_IO.fs,
                    frames_per_buffer=Parameters_IO.chunk_size,
                    input=True)

    wf = wave.open(filename, 'wb')
    wf.setnchannels(Parameters_IO.channels)
    wf.setsampwidth(p.get_sample_size(Parameters_IO.sample_format))
    wf.setframerate(Parameters_IO.fs)
    wf.writeframes(b''.join(Parameters_IO.frames))
    wf.close()

if __name__ == '__main__':


    data = read_segment()
    a=0
    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=4500,
                    frames_per_buffer=1024,
                    input=True)

    wf = wave.open('output.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(4500)
    wf.writeframes(b''.join(data))
    wf.close()
"""