from scipy import signal as sig
import numpy as np
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import pywt

class Noise_filter:
    """
    This class is an interface that defines a framework for filtering signals
    """

    #@abstractmethod
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
            filtered_signal:  1d float np array
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

    def filter_noise(self,signal, fs):
        """
        full docmentation in superclass

        Returned signal will be of size input-1 as the left padding is removed
        """
        b = (np.ones(self.length)) / self.length  # numerator co-effs of filter transfer function
        a = np.ones(1)  # denominator co-effs of filter transfer function

        y = sig.lfilter(b, a, signal)  # filter output using lfilter function
        return y[1:] #remove lefft padding

    def filter_and_plot(self, signal, fs):

        filtered_s = self.filter_noise(signal,fs)
        n = len(signal)

        #f = (np.array(range(0,n-1)) * fs) / n;
        x=np.array(range(0,n))
        plt.plot(x[1:], signal[1:])
        plt.plot(x[1:], filtered_s)
        plt.title("Noisy vs filtered")
        # plt.legend("noisy", "filtered")

        plt.show()


class Wavelet_shink_filter(Noise_filter):
    """
    Subclass of Noise_filter which will perform noise filtering by using Wavelet shinkrage with soft thresholding

    Denoising algorithm
    The denoising steps are the following :

    Apply the dwt to the signal
    Compute the threshold corresponding to the chosen level
    Only keep coefficients with a value higher than the threshold
    Apply the inverse dwt to retrieve the signal
    """

    def __init__(self, levels=2):
        """
         Parameters
         ----------
         levels : int
             nr of low pass and high pass filters to apply to the data before performing thresholding
        """
        self.levels = levels

    def __madev(self, d, axis=None):
        """ Mean absolute deviation of a signal """
        return np.mean(np.absolute(d - np.mean(d, axis)), axis)

    def __wavelet_denoising(self, x, wavelet='db4', level=1):
        coeff = pywt.wavedec(x, wavelet, mode="per")
        sigma = (1 / 0.6745) * self.__madev(coeff[-level])
        uthresh = sigma * np.sqrt(2 * np.log(len(x)))
        coeff[1:] = (pywt.threshold(i, value=uthresh, mode='hard') for i in coeff[1:])
        return pywt.waverec(coeff, wavelet, mode='per')

    def filter_noise(self, signal, fs):
        return self.__wavelet_denoising(signal, level=self.levels)

if __name__ == '__main__':

    

    #test_visual_testing.  Other tests in test suite class
    x = np.linspace(4 * -np.pi, 4 * np.pi, 501)
    signal_no_noise = np.sin(x)
    noisy_signal = signal_no_noise + np.random.normal(0, 1, len(signal_no_noise))

    denoiser= Wavelet_shink_filter(levels=2)

    denoised = denoiser.filter_noise(noisy_signal, fs = 'not necesary just here for completness')
    plt.plot(noisy_signal)
    plt.plot(denoised)
    plt.show()
    #filter = FIR_noise_filter(length=20)
    #filter.filter_and_plot(noisy_signal, 100)
    """
    filtered_s = filter.filter_noise(noisy_signal, 100)

    plt.plot(x[1:], noisy_signal[1:])
    plt.plot(x[1:], filtered_s)
    plt.title("Noisy vs filtered")
    #plt.legend("noisy", "filtered")



    plt.show()
    """