from localization.sliding_hashes.create_hashes import create_hashes
from localization.sliding_hashes.match import match
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from math import ceil
import time


class global_hashes:
    song_array = None
    song_idx_dict = None


def localize_sample_sh(
    sample_constellation_map: list, song_constellation_map: list, sample_freq=1
):
    """
    A function to perform sample localization. The function first
    creates the hash arrays from the sample and the song constellation
    maps and then finds the indices at which they match. The function then
    looks up the corresponding times in the song index dictionary. The function
    finally returns:
        - A list of the times at which the sample is found to match the song.
            NOTE: Each time in the list is to be interpreted as the STARTING time at
            which the sample matches the song. To get the CURRENT time, the recording time
            needs to be added to the time returned by this function.
        - The matching score for the times in the list.
    """

    start = time.time()

    if global_hashes.song_array is None:
        song_array, song_idx_dict = create_hashes(song_constellation_map)
        global_hashes.song_array = song_array
        global_hashes.song_idx_dict = song_idx_dict
        print("created new song hashes")

    else:
        song_array = global_hashes.song_array
        song_idx_dict = global_hashes.song_idx_dict

    sample_array, _ = create_hashes(sample_constellation_map)

    threads = 10
    ref_subdivision_length = int(len(song_array) / threads)
    snippet_half = ceil(len(sample_array) / 2)

    coords = []

    for thread in range(threads):
        if thread == 0:
            coords.append((0, ref_subdivision_length+snippet_half))
        elif thread != threads-1:
            coords.append((thread*ref_subdivision_length-snippet_half, (thread+1)*ref_subdivision_length+snippet_half))
        else:
            coords.append((thread*ref_subdivision_length-snippet_half, len(song_array)))

    ref_segments = [song_array[coord[0]:coord[1]] for coord in coords]

    with ProcessPoolExecutor() as executor:

        # args = [[sample_array, ref_segments[thread], thread, ref_subdivision_length] for thread in range(thread)]
        results = executor.map(match, [sample_array]*10, ref_segments, [thread for thread in range(threads)], [ref_subdivision_length]*10)

    matching_indices, matching_score = max(results, key=lambda x: x[1])
    matching_times = [song_idx_dict[i] / sample_freq for i in matching_indices]

    print("match found with seconds: ", matching_times)

    done = time.time()
    print(done-start)

    return matching_times, matching_score
