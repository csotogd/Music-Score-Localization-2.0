UPPER_FREQ = 23_000
FREQ_SECTOR_SIZE = UPPER_FREQ / 8
FREQ_BITS = 4
TR_BITS = 4


def create_hash_panako(t_0, freq_0, t_1, freq_1, t_2, freq_2):
    # 4 bits
    freq_diff_1 = ((freq_0 - freq_1) / UPPER_FREQ) * (2**FREQ_BITS)
    # 4 bits
    freq_diff_2 = ((freq_1 - freq_2) / UPPER_FREQ) * (2**FREQ_BITS)
    # 4 bits
    f0_tilde = freq_0 / FREQ_SECTOR_SIZE
    # 4 bits
    f2_tilde = freq_2 / FREQ_SECTOR_SIZE

    # Shifting the starting time/origin has no effect, therefore will always present a division by 0 error
    # 4 bits
    t_ratio = (
        0 if t_2 - t_0 == 0 else ((abs(t_1 - t_0) / abs(t_2 - t_0))) * (2**TR_BITS)
    )
    # 4 bits
    td = t_2 - t_0

    # 4 bits
    freq_0_binned = freq_0 / UPPER_FREQ * (2**FREQ_BITS)

    # 32-bit hash
    hash = (
        int(freq_diff_1)
        | int(freq_diff_2) << FREQ_BITS
        | int(freq_0_binned) << 2 * FREQ_BITS
        | int(f0_tilde) << 3 * FREQ_BITS
        | int(f2_tilde) << 3 * FREQ_BITS + 3
        | int(t_ratio) << 3 * FREQ_BITS + 6
        | int(td) << 3 * FREQ_BITS + 6 + TR_BITS
    )

    return hash
