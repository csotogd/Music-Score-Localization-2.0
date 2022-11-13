import unittest
from Signal_Processing.noise_filter import FIR_noise_filter
import numpy as np
import matplotlib.pyplot as plt
import random

class Test_FIR_Noise_filter(unittest.TestCase):

    def test_averaging(self):
        #assume
        signal = np.array([0, 0, 0 ,3, 3, 3, 6, 6 ,6])
        fs = 1
        filter = FIR_noise_filter(length=3)

        #perform filtering
        filtered_signal = filter.filter_noise(signal, fs).astype(int)

        #test the outocme is the same as the desired one
        desired= np.array([ 0 ,0, 1 , 2, 3, 4 , 5 ,6])
        self.assertTrue((filtered_signal==desired).all())


    def test_same_size_minus_one(self):
        #assume
        length = 100
        signal = np.ones(100)
        filter = FIR_noise_filter(length=7)

        #perform
        filtered_signal = filter.filter_noise(signal, fs=1)

        #assert both signals have same len
        self.assertTrue(len(filtered_signal)+1==len(signal))




