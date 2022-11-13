import pyaudio
import wave
import wavio
import numpy as np
from abc import  abstractmethod
class Audio_reader():

    def __init__(self, fs, seconds_per_segment, total_seconds ):
        """

        Parameters
        ----------
        fs: int
            sampling frequency
        seconds_per_segment: float
            number of seconds per segment to be analyzed
        total_seconds: float
            number of seconds of sound to recored in total from the piece.
            the remaininin total_seconds % seconds_per_segment will be ignored
        """
        self.fs = fs
        self.seconds_per_segment = seconds_per_segment
        self.total_seconds = total_seconds
        self.chunk_size = fs*seconds_per_segment


        self.recorded_so_far = []
        ##list to which the consecutive audio segment values will be appended as a list of floats.
        #contains all values recorded up to the 'present' time when executing the program

        self.segments_so_far= 0

    @abstractmethod
    def read_audio_segment(self):
        """
        Reads self.seconds_per_segment of audio from the microphone. It appends the values to self.recorded_so_far and returns the recoreded
        sound segment


        Returns:
        --------
        segment_read: 1d float numpy
            array containing the intensities of the sound segment recorded on the microphone

        check_correct: bool
            True if reading was correct, False if there was nothing more to read
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

    def __init__(self,fs, seconds_per_segment, total_seconds ):
        super().__init__(fs, seconds_per_segment, total_seconds )
        self.sample_format = pyaudio.paInt16  # 16 bits per sample
        self.channels = 1 #is normally 2, one for each speaker, we set it to one as it would be quite complex otherwise.

        self.p =  pyaudio.PyAudio()  # Create an interface to PortAudio
        self.stream =  self.p.open(format=self.sample_format,
                channels=self.channels,
                rate=fs,
                frames_per_buffer=self.chunk_size,
                input=True)
        self.frames =[]

    def read_audio_segment(self):
        """
        full method documentation in superclass

        """

        if self.segments_so_far >= (self.total_seconds/self.seconds_per_segment):
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
            return None, False

        else:
            self.segments_so_far+=1
            data = self.stream.read(self.chunk_size)
            self.frames.append(data)
            segment_data = np.frombuffer(data, dtype=np.int16)
            self.recorded_so_far+=(list(segment_data))

            return segment_data, True

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
                                  seconds_per_segment=2, total_seconds=10)

    ok = True
    while ok:
        segment, ok = audio_reader.read_audio_segment()

    audio_reader.store_recorded_signal()



