from scipy import signal as sig
import numpy as np
from abc import ABC, abstractmethod

class Spectrogram_builder:
    """
    This class is an interface that defines a framework building Spectrograms
    """

    @abstractmethod
    def spectrogram(signal, fs):
        """
        Builds spectrogram from the inputted signal.

        Parameters
         ----------
         signal : 1d numpy float array
             Signal of sound in time domain.
         fs: float,
             Sampling frequency of the signal.

        Returns
        -------
        fndarray
            Array of sample frequencies.

        tndarray
            Array of segment times.

        Sxxndarray
            Spectrogram of x. By default, the last axis of Sxx corresponds to the segment times.


        this is similar to what can be found in:
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html
        """
        pass

class Wavelet_spectrogram(Spectrogram_builder):
    """Builds a spectrogram using wavelet transforms"""
    #TODO: probablly migrate to another file as this will be a large class
    return "to be implemented"

class STFT(Spectrogram_builder):
    """Builds a spectrogram using wavelet STFT. It just calls the function in the library
    scipy.signal"""

    def spectrogram(signal, fs):
        return signal.spectrogram(signal, fs=fs, window=('tukey', 0.25), noverlap=20)