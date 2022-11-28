import random
import time
from localize_sample import localize_sample

# First we create a constellation map with 10,000 time instances with two
# randomly chosen frequencies from the range (20, 20,000) at each sample time.
song_constellation_map_1 = [
    (time, random.randint(20, 20_000)) for time in range(10_000)
]
song_constellation_map_2 = [
    (time, random.randint(20, 20_000)) for time in range(10_000)
]
song_constellation_map = song_constellation_map_1 + song_constellation_map_2
song_constellation_map.sort()

# We now choose a random index from the constellation map and extract sample
# with 100 indices starting from said index.
idx = random.randint(0, 8_000)
extracted_sample = song_constellation_map[idx : idx + 100]

# We now shift the times from the extracted sample so that they start at 0
# and add some gaussian noise in each frequency.
sample_constellation_map = []
origin = extracted_sample[0][0]
for t, freq in extracted_sample:
    sample_constellation_map.append((t - origin, round(freq + random.gauss(0, 3))))

# Finally, we perform the matching test.
print()
print("Match testing")
print()
print("Part sampled from constellation map (first 10 tuples):")
print(song_constellation_map[idx : idx + 10])
print()
print("Distorted sample (first 10 tuples):")
print(sample_constellation_map[:10])
print()

print("Testing results")
start = time.time()
matching_times, matching_score = localize_sample(
    sample_constellation_map, song_constellation_map
)
result = "success" if origin in matching_times else "failure"
end = time.time()
print(f"Sample origin time: {origin}")
print(f"Matching times: {matching_times} ({result})")
print(f"Matching score: {matching_score}")
print(f"Total calculation time: {end-start}")
