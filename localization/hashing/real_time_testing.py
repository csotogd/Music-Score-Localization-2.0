import random
from localization.hashing.localize_snippet import localize_snippet
from localization.hashing.create_hashes import create_hashes
import cProfile, pstats, io
from pstats import SortKey
import time

time_ahead = 5

song_constellation_map_1 = [
    (time, random.randint(20, 20_000)) for time in range(3_000)
]
song_constellation_map_2 = [
    (time, random.randint(20, 20_000)) for time in range(3_000)
]
song_constellation_map = song_constellation_map_1 + song_constellation_map_2
song_constellation_map.sort()

idx = random.randint(0, 5_000)

sample_constellation_map_0 = song_constellation_map[idx : idx + 100]

sample_constellation_map = []
time_0 = sample_constellation_map_0[0][0]
for sample_time, freq in sample_constellation_map_0:
    sample_constellation_map.append((sample_time - time_0, round(freq + random.gauss(0, 10))))

print("yes")

song_hashes = create_hashes(song_constellation_map, time_ahead)
sample_hashes = create_hashes(sample_constellation_map, time_ahead)

print("yes")

start = time.time()
'''pr = cProfile.Profile()
pr.enable()'''
print(localize_snippet(song_hashes, sample_hashes, 1))
'''pr.disable()
s = io.StringIO()
sortby = SortKey.CUMULATIVE
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())'''
done = time.time()
elapsed = done - start
print(elapsed)

# print(localize_snippet(song_hashes, sample_hashes, 1))
print(song_constellation_map[idx][0])
