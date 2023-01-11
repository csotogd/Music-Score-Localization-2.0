import numpy as np

# Constants for hash creation
UPPER_FREQ = 23_000
FREQ_BITS = 4

"""
Constants required for Panako:

- Frequency sector size: The audible spectrum is divided into sectors. In the panako algorithm, the sector in which a
                        frequency lies is of importance. For example, A spectrum of 1000Hz divided into 4 sectors, will
                        mean that a frequency of 300Hz lies in sector 2. This is a rough estimation of their locations
                        in the spectrum
                        
- Frequency shift: The percentage by which the frequencies should be shifted

- Time dilation: The percentage by which the time should be dilated
"""
FREQ_SECTOR_SIZE = UPPER_FREQ / 8
# FREQ_SHIFT = 0.9
# TIME_DILATION = 0.95


def create_hashes(constellation_map: list):
    """
    A function that creates an array containing the hashes representing the diagonals in the constellation map.

    This function first shifts the frequency and dilates time by the desired amount.

    Frequency differences and frequencies are normalised, and stored as 4-bit integers
    The time difference, time ratio and frequency sectors are also stored as a 4-bit integer

    The resulting hash is a 32-bit integer

    The function returns:
        - A numpy array (vector) containing the hashes;
        - A dictionary in which each index in the numpy array is associated with the time in the song at which
        the corresponding hash is encountered.
    """

    index_dict = {}
    hashes_list = []

    arr_ind = 0

    for i, (t_0, freq_0) in enumerate(constellation_map):
        for j, (t_1, freq_1) in enumerate(constellation_map[i : i + 10]):
            for t_2, freq_2 in constellation_map[j : j + 10]:

                # 4 bits
                freq_diff_1 = ((freq_0 - freq_1) / UPPER_FREQ) * (2**FREQ_BITS)
                # 4 bits
                freq_diff_2 = ((freq_1 - freq_2) / UPPER_FREQ) * (2**FREQ_BITS)
                # 4 bits
                f0_tilde = int(freq_0 / FREQ_SECTOR_SIZE)
                # 4 bits
                f2_tilde = int(freq_2 / FREQ_SECTOR_SIZE)

                # Shifting the starting time/origin has no effect, therefore will always present a division by 0 error
                # 4 bits
                t_ratio = 0 if t_2 - t_0 == 0 else (abs(t_1 - t_0) / abs(t_2 - t_0))
                # 4 bits
                td = t_2 - t_0

                # 4 bits
                freq_0_binned = freq_0 / UPPER_FREQ * (2**FREQ_BITS)

                # 32-bit hash
                hash = (
                    int(freq_diff_1)
                    | int(freq_diff_2) << 4
                    | f0_tilde << 8
                    | f2_tilde << 12
                    | int(t_ratio) << 16
                    | int(t_0) << 20
                    | int(freq_0_binned) << 24
                    | int(td) << 28
                )

                hashes_list.append(hash)
                index_dict[arr_ind] = t_0
                arr_ind += 1

    return np.asarray(hashes_list).astype(np.uint64), index_dict
