from scipy import signal as sig
import numpy as np
from abc import ABC, abstractmethod

class Noise_filter:
    """
    This class is an interface that defines a framework for filtering signals
    """

    @abstractmethod
    def filter_noise(signal, fs):
        """
        Filters Noise from the inputted signal.

        Parameters
         ----------
         signal : 1d numpy float array
             Signal of sound in time domain.
         fs: float,
             Sampling frequency of the signal.

        Returns
        -------
            filtered_signal:  1d float array
             Signal of sound in time domain.

        """
        pass

class FIR_noise_filter(Noise_filter):
    """
    Subclass of Noise_filter which will perform noise filtering by using FIR averaging filter.
    """
    def __init__(self, length):
        """
         Parameters
         ----------
         length : int
             length of filter
        """
        self.length = length

    def filter_noise(signal, fs):
        b = (np.ones(self.length)) / self.length  # numerator co-effs of filter transfer function
        a = np.ones(1)  # denominator co-effs of filter transfer function
        x = np.random.randn(10)  # 10 random samples for x

        y = sig.lfilter(b, a, x)  # filter output using lfilter function


class Wavelet_shink_filter(Noise_filtering):
    """
    Subclass of Noise_filter which will perform noise filtering by using Wavelet shinkrage with soft thresholding
    """

    def __init__(self, levels=3):
        """
         Parameters
         ----------
         levels : int
             nr of low pass and high pass filters to apply to the data before performing thresholding
        """
        self.levels = levels

    def filter_noise(signal, fs):
        return "to be implemented"
