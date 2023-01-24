UPPER_FREQ = 23_000
FREQ_BITS = 10


def create_hash_shazam(t_0, freq_0, t_1, freq_1):
    td = int(t_1 - t_0)
    freq_0_bin = int(freq_0 / UPPER_FREQ * (2**FREQ_BITS))
    freq_1_bin = int(freq_1 / UPPER_FREQ * (2**FREQ_BITS))

    hash = freq_0_bin | (freq_1_bin << FREQ_BITS) | (td << 2 * FREQ_BITS)

    return hash
