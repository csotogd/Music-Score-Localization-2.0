import unittest
from Signal_Processing.IO.Audio_reader import PyAudio_reader
import numpy as np

class Test_Audio_Reader(unittest.TestCase):

    def test_py_audio_correct_length(self):
        """

        we test the recorded signal is of the desired length
        """
        audio_reader = PyAudio_reader(fs= 1000,
                                      seconds_per_segment= 2, total_seconds=10)
        ok = True
        while ok:
            segment, ok = audio_reader.read_audio_segment()

        desired_len = audio_reader.total_seconds *audio_reader.fs
        recorded_len = len(audio_reader.recorded_so_far)
        self.assertEqual(desired_len, recorded_len)