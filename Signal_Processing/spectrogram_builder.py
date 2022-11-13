from scipy import signal as sig
import numpy as np
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt

from Signal_Processing.signal_plotting import plot_signal


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
    def spectrogram(signal, fs):
        return "to be implemented"

class STFT_spectrogram(Spectrogram_builder):
    """Builds a spectrogram using wavelet STFT. It just calls the function in the library
    scipy.signal"""

    def spectrogram(self, signal, fs):
        """

        Parameters
         ----------
         signal : 1d numpy float array
             Signal of sound in time domain.
         fs: float,
             Sampling frequency of the signal.


        Returns
        -------
        f: ndarray
            Array of sample frequencies.

        t:  ndarray
            Array of segment times.

        Zxx: xndarray
             STFT of x. By default, the last axis of Zxx corresponds to the segment times. Non normalized

        """
        f, t, Zxx = sig.stft(signal, fs=fs, window='hann',noverlap=100, nperseg=500)
        #size of frequencies array output: H = nperseg - noverlap
        #the f array will have evenly spaced values form 0 to fs/2 where H is the interval between values

        return f, t, Zxx #TODO Sree, If you have any questions about this, send me a text

    def spectrogram_calculate_plot(self, signal, fs):
        """
        Calculates spectrogram using stft and plots it

        Parameters
         ----------
         signal : 1d numpy float array
             Signal of sound in time domain.
         fs: float,
             Sampling frequency of the signal.

        """
        f, t, Zxx = self.spectrogram(signal, fs)
        plt.figure()
        plt.pcolormesh(t, f, np.abs(Zxx), vmin= 0, vmax=1, shading='gouraud')
        plt.title('STFT magnitude')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.grid()
        plt.show()

if __name__ == '__main__':

    x1 = np.linspace(500 * -np.pi, 500 * np.pi, 5001)
    signal_no_noise_1 = np.sin(x1)
    plot_signal(signal_no_noise_1)
    #plt.show()

    x2 = np.linspace(150 * -np.pi, 150 * np.pi, 5001)
    signal_no_noise_2 = np.sin(x2)

    x3 = np.linspace(2 * -np.pi, 2 * np.pi, 5001)
    signal_no_noise_3 = np.sin(x3)

    signal_no_noise = signal_no_noise_1 + signal_no_noise_2 + signal_no_noise_3


    #plot_signal(noisy_signal)
    #plt.show()

    fs=5000

    spectr_builder= STFT_spectrogram()
    spectr_builder.spectrogram_calculate_plot(signal_no_noise, fs)


