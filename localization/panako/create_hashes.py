import numpy as np

# Constants for hash creation
UPPER_FREQ = 23_000
FREQ_BITS = 8


def create_hashes(constellation_map: list):

    index_dict = {}
    hashes_list = []

    arr_ind = 0
    for i, (t_0, freq_0) in enumerate(constellation_map):
        for j, (t_1, freq_1) in enumerate(constellation_map[i : i + 10]):
            for t_2, freq_2 in constellation_map[j : j + 10]:
                # freq_diff_0_binned = (
                #     (freq_0 - freq_1) / UPPER_FREQ * (2**FREQ_BITS)
                # )  # 10 bits
                # freq_diff_1_binned = (
                #     (freq_1 - freq_2) / UPPER_FREQ * (2**FREQ_BITS)
                # )  # 10 bits
                freq_0_binned = freq_0 / UPPER_FREQ * (2**FREQ_BITS)  # 10 bits
                freq_1_binned = freq_1 / UPPER_FREQ * (2**FREQ_BITS)  # 10 bits
                freq_2_binned = freq_2 / UPPER_FREQ * (2**FREQ_BITS)  # 10 bits
                # time_ratio = (t_1 - t_0) / (t_2 - t_0) * 2**8  # 8 bits
                td = t_1 - t_0

                hash = (
                    int(freq_0_binned)
                    + (int(freq_1_binned) << FREQ_BITS)
                    # | (int(freq_2_binned) << (2 * FREQ_BITS))
                    # | (int(time_ratio) << (3 * FREQ_BITS))
                    + (int(td) << (2 * FREQ_BITS))
                )

                hashes_list.append(hash)
                index_dict[arr_ind] = t_0
                arr_ind += 1

    print(hashes_list)
    return np.asarray(hashes_list).astype(np.uint64), index_dict
