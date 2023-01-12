# Append root to path
import sys
import os
import time

sys.path.append(os.getcwd())


from Uttilities.pipelines import *
from localization.sliding_hashes.localize_sample_sh import localize_sample_sh
from scipy.io.wavfile import read

"""
This file handles the evaluation of our method.
"""


def evaluate(
    raw_ref, fs_ref, raw_recording, fs_record, recording_labels, length_snippet_secs=3
):
    """

    Parameters
    ----------
    raw_ref: np array of the reference song, before any processing
    raw_recording: np array of the recording, before any processing
    recording_labels: data structure to be defined
            This stores our (X,Y), where the X represents a time point (in seconds)
            in the recorded song, and the Y represent the time at which that bit appears.
    fs_ref: int sampling frequency of the reference song in Hz
    fs_record: int sampling frequency of the recorded song in Hz

    Returns
    -------
    a score (to be defined)

    """
    # calculate constellation map for each
    constellation_ref = sp_pipeline(raw_ref, fs_ref, denoise=False)

    score = 0
    for time_recording, true_label in recording_labels:

        # get an interval of the song around the point in the recording
        recording_interval = get_song_interval(
            raw_recording, time_recording, fs_record, length_sec=length_snippet_secs
        )
        constellation_record = sp_pipeline(recording_interval, fs_record, denoise=True)

        predictions, _ = localize_sample_sh(
            constellation_record, constellation_ref, fs_record
        )

        score_point = evaluate_localization(true_label, predictions)
        score += score_point

    score_normalized = score / len(recording_labels)
    return score_normalized


def evaluate_reduced_search_space(
    raw_ref, fs_ref, raw_recording, fs_record, recording_labels, length_snippet_secs=3
):
    """
    This functions evaluates how good our matching algorithm is, but it  is assumed that we can reduce the search space, i.e only take a fraction
    of the reference song to look into. In practice, the information needed to reduce the search space would be provided by the user.

    Parameters
    ----------
    raw_ref: np array of the reference song, before any processing
    raw_recording: np array of the recording, before any processing
    recording_labels: data structure to be defined
            This stores our (X,Y), where the X represents a time point (in seconds)
            in the recorded song, and the Y represent the time at which that bit appears.
    fs_ref: int sampling frequency of the reference song in Hz
    fs_record: int sampling frequency of the recorded song in Hz

    Returns
    -------
    a score (to be defined)

    """
    # calculate constellation map for each
    constellation_ref = sp_pipeline(raw_ref, fs_ref, denoise=False)


    score = 0
    for time_recording, true_label in recording_labels:
        #get subset of the constellation map
        const_ref_subset = get_fraction_of_ref_song(ref_song_cons_map=constellation_ref, fs_ref=fs_ref, indication_time=true_label,lenght_seconds_ref_song=len(ref_song)/fs_ref,
                                 length_subset=30)


        # get an interval of the song around the point in the recording
        recording_interval = get_song_interval(
            raw_recording, time_recording, fs_record, length_sec=length_snippet_secs
        )
        constellation_record = sp_pipeline(recording_interval, fs_record, denoise=True)

        predictions, _ = localize_sample_sh(
            constellation_record, constellation_ref, fs_record
        )

        score_point = evaluate_localization(true_label, predictions)
        score += score_point

    score_normalized = score / len(recording_labels)
    return score_normalized



def get_fraction_of_ref_song(ref_song_cons_map, fs_ref, indication_time, length_subset, lenght_seconds_ref_song):
    """
    Gets a subset of the constellation map of the reference song.

    Parameters
    ----------
    ref_song_cons_map: constellation map of reference song
    fs_ref: sampling frequency (Hz) of ref song
    indication_label: time in seconds which is used as a central point (approcimation) of the subset to be returned.
    length_subset: legnth in seconds of the suibset to be returned.  the subset must be of that length, so the indication time will be placed
                in the extreme points if no other alternatives exist. MUST BE SMALLER THAN THE LENGHT IN SECONDS OF THE REFERENCE SONG
    lenght_seconds_ref_song: length of ref song
    Returns
    -------
    subset of ref_song_cons_map.   same data type
    """
    if lenght_seconds_ref_song< length_subset:
        raise Exception("Length of subset must be smaller than length of reference song")

    #First of all we will compute the seconds at which our interval should theoretically start at and its corresponding index

    seconds_start = indication_time-length_subset/2
    seconds_end =  indication_time + length_subset / 2
    #now we check for edge cases
    if (length_subset - (seconds_end- seconds_end)) > 0.1: #the interval is not of desired length
        if seconds_start<0: # we are at the beginning of the song
            seconds_start= 0
            seconds_end = length_subset
        else:# we are at the end.
            seconds_end = lenght_seconds_ref_song
            seconds_start= seconds_end- length_subset

    desired_obs_start = seconds_start*fs_ref
    desired_obs_end = seconds_end* fs_ref

    # The constellation map is a list of tuples ordered by time, hence finding a time interval in it can be done in linear time
    # We will compute a subset as close as possible to the target one. In case of disambiguation we make the subset smaller.
    for i in range(len(ref_song_cons_map)):
        obs = ref_song_cons_map[i][0]
        if obs>= desired_obs_start:
            index_start = i
            break

    for i in range(index_start, len(ref_song_cons_map)):
        obs = ref_song_cons_map[i][0]
        if obs >= desired_obs_end:
            index_end = i
            break

    subset_cons_map = ref_song_cons_map[index_start: index_end]
    return subset_cons_map

def evaluate_localization(
    true_label,
    predictions,
    interval_side_perfect_length=1,
    interval_side_relevant_length=2,
):
    """

    This functions evaluate how good/bad our estimated localization for one point is. the returned score lies between 0 and 1

    More specifically this function works as follows:

    -   The score will be 1 (the max) if
        the prediction lies in the interval [true_label +- interval_side_perfect_length]

    -   The score will decrease linearly from 1 to 0 in the intervals
        [ true_label - interval_side_perfect_length - interval_side_relevant_length ]   &
        [ true_label + interval_side_perfect_length + interval_side_relevant_length ]

    -   The score will be 0 everywhere else

    Here is a drawing of how a score looks like

    1                       -------------------
    .                      /                     \
                          /                       \
    .                    /                         \
    .                   /                           \
    0 ------------------                              ......................................

    (vertical axis represents score and horizontal axis represents match)

    x axis:            a    b

    where b = true_label - interval_side_perfect_length
          a =  true_label - interval_side_perfect_length - interval_side_relevant_length


    Parameters
    ----------
    true_label: float which represents the time in seconds of the ideal match. (our ground truth)
    prediction: float which represents the time in seconds of the predicted time at which the localization happens
                according to our localization algorithm

    Returns
    -------
    float, score of our match, must be between 0 and 1
    """
    scores = []
    for prediction in predictions:
        if (
            true_label - interval_side_perfect_length
            <= prediction
            <= true_label + interval_side_perfect_length
        ):
            scores.append(1)

        elif (
            true_label - interval_side_perfect_length - interval_side_relevant_length
            <= prediction
            <= true_label - interval_side_perfect_length
        ):
            distance_from_0_score = prediction - (
                true_label
                - interval_side_perfect_length
                - interval_side_relevant_length
            )
            score = distance_from_0_score / interval_side_relevant_length
            scores.append(score)

        elif (
            true_label + interval_side_perfect_length
            <= prediction
            <= true_label + interval_side_perfect_length + interval_side_relevant_length
        ):
            distance_from_0_score = (
                true_label
                + interval_side_perfect_length
                + interval_side_relevant_length
            ) - prediction
            score = distance_from_0_score / interval_side_relevant_length
            scores.append(score)

        else:
            scores.append(0)

    return max(scores)


def get_song_interval(raw_recording, time_recording, fs, length_sec=3):
    """

    Parameters
    ----------
    raw_recording np.array of the song for which we want to obtain a subset (in the time domain)
    time_recording: float second ([0, inf]) which is the beginning of the interval we want to obtain. Watch out, now we do the beginning instead of the center.
    length_sec: float length of the interval we want to return.

    Returns
    -------
    a np array of a subset of the raw_recording parameter

    """

    seconds_start = time_recording
    seconds_end = time_recording + length_sec

    index_start = max(0, int(seconds_start * fs))
    index_end = min(len(raw_recording), int(seconds_end * fs))

    return raw_recording[index_start:index_end]


def get_labeled_data(path_to_file):
    """
    Parameters
    ----------
    path_to_file txt file where the labeled data is stored

    Returns
    -------
    a list of tuples, where the first element represents a second in the recorded song and the second element represents
    where that point is in the actual reference song, also in seconds
    """
    # list to return
    labeled_list = []

    # Using readlines()
    file1 = open(path_to_file, "r")
    Lines = file1.readlines()

    # Strips the newline character
    for line in Lines:
        split_string = line.split(":")
        point = (float(split_string[0]), float(split_string[1].split("\n")[0]))
        labeled_list.append(point)

    return labeled_list


if __name__ == "__main__":

    Fs_ref, ref_song = read(
        "../data/Clair_de_lune_original_1channel.wav"
        # "../data/bach_prelude_c_major/Bach_prelude_original_1channel.wav"
    )

    # paths to songs we will compare
    path1_rec = (
        "../data/claire_de_lune_record1_kris_1channel.wav"
    )
    # path1_rec = ("../data/bach_prelude_c_major/mic/Bach_prelude_first_version_1channel.wav")
    # path2_rec = (
    #    "../data/bach_prelude_c_major/mic/Bach_prelude_second_version_1channel.wav"
    # )
    # path3_rec = "../data/bach_prelude_c_major/mic/BAch_prelude_Background_plus_mistake_1_channel.wav"

    # paths to labeled data of songs
    path1_labels = "../data/claire_de_lune_record1_kris.txt"
    # path1_labels = ../data/labelled_data/Bach_prelude_first_version_1channel.txt
    # path2_labels = "../data/labelled_data/Bach_prelude_second_version_1channel.txt"
    # path3_labels = (
    #    "../data/labelled_data/BAch_prelude_Background_plus_mistake_1_channel.txt"
    # )

    paths = [
        (path1_rec, path1_labels),
        #(path2_rec, path2_labels),
        #(path3_rec, path3_labels),
    ]


    length_snippets_in_secs = [3, 5, 10]
    scores = []

    # now we evaluate all songs
    start_time = time.time()
    for path_rec, path_labels in paths:
        labelled_data = get_labeled_data(path_labels)
        Fs_record, record_song = read(path_rec)

        # for each song try different lengths of snippets:
        for length_snippet in length_snippets_in_secs:

            score = evaluate_reduced_search_space(
                raw_ref=ref_song,
                fs_ref=Fs_ref,
                raw_recording=record_song,
                fs_record=Fs_record,
                recording_labels=labelled_data,
                length_snippet_secs=length_snippet,
            )
            print('done with snippets of length: ', length_snippet)
            scores.append(score)
        print('done with one version. moving onto the next.')
    names = ["first version"] #, "second version", "third version"]
    print()
    print()
    print()
    end_time = time.time()
    print("Total time taken: ", end_time-start_time)
    print("----------------EVALUATION RESULTS ---------------------")
    for i in range(len(names)):
        for j in range(len(length_snippets_in_secs)):
            print(
                "score for ",
                names[i],
                " and snippet of ",
                length_snippets_in_secs[j],
                " seconds ---->",
                scores[i * len(length_snippets_in_secs) + j],
            )
        print()

    print()
    print()
    print()
    print("----------COMPARING A SONG TO ITSELF--------")
    scores=[]
    for path_rec, path_labels in paths:
        labelled_data = get_labeled_data(path_labels)
        for i in range(len(labelled_data)):
            labelled_data[i] = (labelled_data[i][1], labelled_data[i][1])
        Fs_record, record_song = read(path_rec)

        # for each song try different lengths of snippets:
        for length_snippet in length_snippets_in_secs:
            score = evaluate_reduced_search_space(
                raw_ref=ref_song,
                fs_ref=Fs_ref,
                raw_recording=ref_song,
                fs_record=Fs_ref,
                recording_labels=labelled_data,
                length_snippet_secs=length_snippet,
            )
            print('done with snippets of length: ', length_snippet)
            scores.append(score)
        print('done with one version. moving onto the next.')
    names = ["first version"]  # , "second version", "third version"]
    print()
    print()
    print()
    end_time = time.time()
    print("Total time taken: ", end_time - start_time)
    print("----------------EVALUATION RESULTS FOR SONG TO ITSELF---------------------")
    for i in range(len(names)):
        for j in range(len(length_snippets_in_secs)):
            print(
                "score for ",
                names[i],
                " and snippet of ",
                length_snippets_in_secs[j],
                " seconds ---->",
                scores[i * len(length_snippets_in_secs) + j],
            )
        print()

