"""
This file is in charge of building a constellation map given a pre-processed signal
(Noise removal, filtering, etc, has already been performed)
"""

def build_constellation_map(signal, fs):
    """Builds a constellation mpa from a signal

     Parameters
     ----------
     signal : 1d float array
         Signal of sound in time domain.
     fs: float,
         Sampling frequency of the signal.

     Returns
     -------
     list of tuples
        Constellation map representation. Each entry in our list corresponds to a peak,
        and it is represented as a tuple with two entries. The first entry corresponds to the time.
        The second entry corresponds to the frequency at which the peak happens.
        The time is relative to the signal inputted to this function.
        The list of tuples is ordered in chronologically. In case of a tie in the time axis, they are ordered in ascending
        order based on frequency.

        As an example. We have a signal of 3000 observations sampled at 1000Hz.
        HEnce, we have a 3 seconds long snippet. The constellation map has peaks in points:

        1.235 seconds at 80 Hz
        1.235 seconds at 20 Hz
        2.7689 seconds at 45 Hz

        Then the output will be:
        [(1.235, 20),(1.235, 80),(2.7689, 45)]

     """
