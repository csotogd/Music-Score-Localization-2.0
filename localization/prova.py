import numpy as np
import time
import random

dict = {1: "bella", 2: "ciao", 3: "spada", 4: "scudo", 5: "drago", 6: "lupo", 7: "chitarra"}

print("doing it with basic python")
start = time.time()
for i in range(1):
    key = random.choice([1, 2, 3, 4, 5, 6, 7])
    elem = dict[key]
    print(key, elem)
done = time.time()
print(done - start)
print()

print("doing it with numpy and lambda")

map = lambda x, y: x[0] == y
hash_map = np.array([(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)])

start = time.time()
for i in range(1):
    hash = random.choice([1, 2, 3, 4, 5, 6, 7])
    elem = np.array([i[1:] for i in hash_map if i[0] == hash])
    print(hash, elem)
done = time.time()
print(done - start)

import numpy as np

'''
def create_hashes(constellation_map, time_ahead):
    hashes = {[hash1]: [0, 1, 2], [hash2] : []}
    upper_frequency = 23_000
    frequency_bits = 10

    for idx, current_freq in np.ndenumerate(constellation_map):

        current_index = idx[0]
        current_time = idx[1]

        for future_peak in constellation_map[current_index:, :]:

            if future_peak[0] > current_time + time_ahead:
                break

            time_diff = future_peak[0] - current_time

            freq_binned = current_freq / upper_frequency * (2**frequency_bits)
            other_freq_binned = future_peak[1] / upper_frequency * (2**frequency_bits)

            hash = (
                int(freq_binned)
                | (int(other_freq_binned) << 10)
                | (int(time_diff) << 20)
            )
            if hash not in hashes:
                hashes[hash] = np.array([])
            np.vstack
            hashes[hash].append(current_time)

    return hashes
'''