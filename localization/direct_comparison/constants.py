import numpy as np

# A constant that defines the thresholds for comparing two tuples of the form
# (freq_0, freq_1, td) to account for frequency and time distortion.
RANGES = np.array((2, 2, 1))
