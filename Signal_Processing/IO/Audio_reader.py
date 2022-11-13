import pyaudio
import wave
import wavio
import numpy as np
from abc import  abstractmethod
class Audio_reader():

    def __init__(self, fs, seconds_per_segment):
        """

        Parameters
        ----------
        fs: int
            sampling frequency
        seconds_per_segment: float
            number of seconds per segment to be analyzed
        """
        self.fs = fs
        self.seconds_per_segment = seconds_per_segment
        self.chunk_size = 1024





    @abstractmethod
    def read_audio_segment(self, recorded_so_far):
        """
        Parameters:
        ---------
        recorded_so_far: []
            list to which the consecutive audio segment values will be appended as a list of floats.
            contains all values recorded up to the 'present' time when executing the program.
            natural decsion woule be to make this a class parameter, but we can not do it.


        Reads self.seconds_per_segment of audio from the microphone. It appends the values to self.recorded_so_far and returns the recoreded
        sound segment

        """
    @abstractmethod
    def store_recorded_signal(self, filename):
        """
        stores the recorded signal as a wav file

         Parameters
        ----------
         filename: string
            relative path to the file in which the sound will be stored.
            must be a ".wav" file
        """



class PyAudio_reader(Audio_reader):
    """
    Reads using Pyaudio library. Works for PC. It may need to be changed for an Ipad
    """

    def __init__(self,fs, seconds_per_segment):
        super().__init__(fs, seconds_per_segment)
        self.sample_format = pyaudio.paInt16  # 16 bits per sample
        self.channels = 1 #is normally 2, one for each speaker, we set it to one as it would be quite complex otherwise.
        self.recorded_so_far=[]

    def __create_pyaudio_object(self):
        self.p = pyaudio.PyAudio()  # Create an interface to PortAudio
        self.stream = self.p.open(format=self.sample_format,
                                  channels=self.channels,
                                  rate=self.fs,
                                  frames_per_buffer=self.chunk_size,
                                  input=True)
        self.frames = []



    def read_audio_segment(self, recorded_so_far):
        """
        full method documentation in superclass
        """
        self.__create_pyaudio_object()

        for i in range(0, int(self.fs / self.chunk_size * self.seconds_per_segment)):
            data = self.stream.read(self.chunk_size)
            self.frames.append(data)
            numpydata = np.frombuffer(data, dtype=np.int16)
            recorded_so_far+=(list(numpydata))

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        return numpydata

    def store_recorded_signal(self, filename ='output.wav'):
        """
        full method documentation in superclass
        """
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()

if __name__ == '__main__':
    audio_reader = PyAudio_reader(fs=45000,
                                  seconds_per_segment=10)


    audio_reader.read_audio_segment()
    ok=0

    audio_reader.store_recorded_signal()



