"""
This file is in charge of building a constellation map given a pre-processed signal
(Noise removal, filtering, etc, has already been performed)
"""

import numpy as np
from scipy import signal

def build_constellation_map(frequencies, times, stft, fs):
    """Builds a constellation map from a signal
    Method is based on an existing method implementation by Michael C Strauss.
    Author: Michael C Strauss
    Title: shazam-python: create_constellation.py
    Date: 2021
    Type: Source Code
    Availability: https://github.com/MichaelCStrauss/shazam-python

     Parameters
     ----------
     frequencies: ndarray,
        Array of sample frequencies.
     times: ndarray,
        Array of segment times.
     stft: ndarray,
        Short-Term Fourier Transform, last axis corresponds to the segment times.
     fs: float,
         Sampling frequency of the signal.

     Returns
     -------
     list of tuples
        Constellation map representation. Each entry in our list corresponds to a peak,
        and it is represented as a tuple with two entries. The first entry corresponds to the index of the time sample.
        The second entry corresponds to the frequency at which the peak happens.
        The time index is relative to the signal inputted to this function.
        The list of tuples is ordered in chronologically. In case of a tie in the time axis, they are ordered in
        ascending order based on frequency.

        As an example. We have a signal of 3000 observations sampled at 1000Hz.
        Hence, we have a 3 seconds long snippet. The constellation map has peaks in points:

        1.235 seconds at 80 Hz
        1.235 seconds at 20 Hz
        2.769 seconds at 45 Hz

        so their corresponding index, frequency tuples would be:

        (1.235 * Fs, 20.0)
        (1.235 * Fs, 80.0)
        (2.769 *  Fs, 45.0)

        Then the output will be:
        [(1.235 * Fs, 20),(1.235 * Fs, 80),(2.769 * Fs, 45)]

     """
    # Maximum number of peaks to retrieve in each window.
    num_peaks = 15

    constellation_map = []

    # Iterate over the time slices
    for time_idx, window in enumerate(stft.T):
        # Spectrum is by default complex. We want real values only
        spectrum = abs(window)
        # Find peaks - these correspond to interesting features. Note the distance - want an even spread across the
        # spectrum (minimum distance between two neighbouring peaks)
        peaks, props = signal.find_peaks(spectrum, prominence=0, distance=200)

        # Only want the most prominent peaks, With a maximum of 15 per time slice
        n_peaks = min(num_peaks, len(peaks))

        # Get the n_peaks largest peaks from the prominences

        # This is an argpartition, Useful explanation with example but there is a quick overview below the link:
        # https://kanoki.org/2020/01/14/find-k-smallest-and-largest-values-and-its-indices-in-a-numpy-array/

        # Quick overview: partitions the array into portions of size l-n and n, then retrieves the indexes of the
        # desired maximum peaks in the last n indexes. before appending that length n array to the length l-n array of
        # remaining indexes. To retrieve the indexes of the n most prominent peaks we just retrieve the elements
        # corresponding to the indexes in the last n positions of the output of the argpartition.
        largest_peaks = np.argpartition(props["prominences"], -n_peaks)[-n_peaks:]
        largest_peaks = np.flip(largest_peaks, axis=None)
        for peak in peaks[largest_peaks]:
            frequency = frequencies[peak]
            constellation_map.append([time_idx, frequency])

    return constellation_map
