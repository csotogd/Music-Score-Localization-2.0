from localization.sliding_hashes.create_hashes import create_hashes
from localization.sliding_hashes.match import match
from concurrent.futures import ThreadPoolExecutor
from math import ceil


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

    if global_hashes.song_array is None:
        song_array, song_idx_dict = create_hashes(song_constellation_map)
        global_hashes.song_array = song_array
        global_hashes.song_idx_dict = song_idx_dict
        print("created new song hashes")

    else:
        song_array = global_hashes.song_array
        song_idx_dict = global_hashes.song_idx_dict

    sample_array, _ = create_hashes(sample_constellation_map)

    threads = 5
    ref_subdivision_length = int(len(song_array) / threads)
    snippet_half = ceil(len(sample_array) / 2)

    ref_segments = [song_array[:ref_subdivision_length + snippet_half],
                    song_array[ref_subdivision_length - snippet_half:2 * ref_subdivision_length + snippet_half],
                    song_array[2 * ref_subdivision_length - snippet_half:3 * ref_subdivision_length + snippet_half],
                    song_array[3 * ref_subdivision_length - snippet_half:4 * ref_subdivision_length + snippet_half],
                    song_array[4 * ref_subdivision_length - snippet_half:]
                    ]

    with ThreadPoolExecutor() as executor:

        thread_list = [executor.submit(match, *[sample_array, ref_segments[thread], thread, ref_subdivision_length]) for thread in range(threads)]
        results = [thread.result() for thread in thread_list]

        matching_indices, matching_score = max(results, key=lambda x: x[1])
        matching_times = [song_idx_dict[i] / sample_freq for i in matching_indices]

        print("match found with seconds: ", matching_times)

    return matching_times, matching_score
