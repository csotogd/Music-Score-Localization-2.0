
import time

# Append root to path
import sys
import os

sys.path.append(os.getcwd())


from Utilities.pipelines import *

# from localization.montecarlo_robot import montecarlo as MC


"""
This file handles the evaluation of our method.
"""


def evaluate(
    localization_method,
    raw_ref,
    fs_ref,
    raw_recording,
    fs_record,
    recording_labels,
    length_snippet_secs=3,
):
    """

    Parameters
    ----------
    localization_method: the localization method to be tested
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

        predictions, _ = localization_method(
            constellation_record, constellation_ref, print_times=False
        )

        score_point = evaluate_localization(true_label, predictions)
        score += score_point

    score_normalized = score / len(recording_labels)
    return score_normalized


def evaluate_reduced_search_space(
    localization_method,
    raw_ref,
    fs_ref,
    raw_recording,
    fs_record,
    recording_labels,
    length_snippet_secs=3,
):
    """
    This functions evaluates how good our matching algorithm is, but it is assumed that we can reduce the search space, i.e only take a fraction
    of the reference song to look into. In practice, the information needed to reduce the search space would be provided by the user.

    Parameters
    ----------
    localization_method: the localization method to be tested
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

    ##TODO instantiate the MC object with the number of particles.
    # mc = MC.montecarlo_robot_localization(nr_particles=50, length_ref_initial_subset=30)

    score = 0
    scores = []
    for time_recording, true_label in recording_labels:
        # get subset of the constellation map
        const_ref_subset = get_fraction_of_ref_song(
            ref_song_cons_map=constellation_ref,
            fs_ref=fs_ref,
            indication_time=true_label,
            length_seconds_ref_song=len(raw_ref) / fs_ref,
            length_subset=30,
        )

        # get an interval of the song around the point in the recording
        recording_interval = get_song_interval(
            raw_recording, time_recording, fs_record, length_sec=length_snippet_secs
        )
        constellation_record = sp_pipeline(recording_interval, fs_record, denoise=True)

        predictions, _ = localization_method(
            constellation_record, const_ref_subset, print_times=False
        )

        # print("Constref: " + str(const_ref_subset[0][0]))
        # print("Constref end: " + str(const_ref_subset[-1][0]))
        # print("Prediction:" + str(predictions))

        ##TODO perform the itteration of the montecarlo
        # mc.iterate(length_ref=30, time_diff_snippets=1, predictions=predictions) #check the time diff snippets, filled with a random value
        # prediction = mc.get_most_likely_point(length_intervals=2, offset_intervals=0.2)
        # score_point = evaluate_localization_single(true_label, prediction)

        score_point = evaluate_localization(true_label, predictions)
        scores.append(round(score_point, 2))
        score += score_point

    score_normalized = score / len(recording_labels)
    return score_normalized, scores


def get_fraction_of_ref_song(
    ref_song_cons_map, fs_ref, indication_time, length_subset, length_seconds_ref_song
):
    """
    Gets a subset of the constellation map of the reference song.

    Parameters
    ----------
    ref_song_cons_map: constellation map of reference song
    fs_ref: sampling frequency (Hz) of ref song
    indication_label: time in seconds which is used as a central point (approximation) of the subset to be returned.
    length_subset: length in seconds of the subset to be returned.  the subset must be of that length, so the indication time will be placed
                in the extreme points if no other alternatives exist. MUST BE SMALLER THAN THE LENGTH IN SECONDS OF THE REFERENCE SONG
    length_seconds_ref_song: length of ref song
    Returns
    -------
    subset of ref_song_cons_map.   same data type
    """
    if length_seconds_ref_song < length_subset:
        raise Exception(
            "Length of subset must be smaller than length of reference song"
        )

    # First of all we will compute the seconds at which our interval should theoretically start at and its corresponding index

    seconds_start = indication_time - length_subset / 2
    seconds_end = indication_time + length_subset / 2
    # now we check for edge cases

    if seconds_start < 0:  # we are at the beginning of the song
        seconds_start = 0
        seconds_end = length_subset
    elif seconds_end > length_seconds_ref_song:  # we are at the end.
        seconds_end = length_seconds_ref_song
        seconds_start = seconds_end - length_subset

    desired_obs_start = seconds_start * fs_ref
    desired_obs_end = seconds_end * fs_ref

    # The constellation map is a list of tuples ordered by time, hence finding a time interval in it can be done in linear time
    # We will compute a subset as close as possible to the target one. In case of disambiguation we make the subset smaller.
    for i in range(len(ref_song_cons_map)):
        obs = ref_song_cons_map[i][0] * fs_ref
        if obs >= desired_obs_start:
            index_start = i
            break

    index_end = None
    for i in range(index_start, len(ref_song_cons_map)):
        obs = ref_song_cons_map[i][0] * fs_ref
        if obs >= desired_obs_end:
            index_end = i
            break
    if index_end is None:
        index_end = len(ref_song_cons_map) - 1

    subset_cons_map = ref_song_cons_map[index_start:index_end]
    return subset_cons_map


def evaluate_localization(
    true_label,
    predictions,
    interval_side_perfect_length=3,
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
    if len(predictions) == 0:
        return 0
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

    # print("True Label: ", true_label)
    # for i in range(len(predictions)):
    #     print(predictions[i], scores[i])
    # print()

    return max(scores)


def evaluate_localization_single(
    true_label,
    prediction,
    interval_side_perfect_length=3,
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
    if len(prediction) == 0:
        return 0

    if (
        true_label - interval_side_perfect_length
        <= prediction
        <= true_label + interval_side_perfect_length
    ):
        return 1

    elif (
        true_label - interval_side_perfect_length - interval_side_relevant_length
        <= prediction
        <= true_label - interval_side_perfect_length
    ):
        distance_from_0_score = prediction - (
            true_label - interval_side_perfect_length - interval_side_relevant_length
        )
        score = distance_from_0_score / interval_side_relevant_length
        return score

    elif (
        true_label + interval_side_perfect_length
        <= prediction
        <= true_label + interval_side_perfect_length + interval_side_relevant_length
    ):
        distance_from_0_score = (
            true_label + interval_side_perfect_length + interval_side_relevant_length
        ) - prediction
        score = distance_from_0_score / interval_side_relevant_length
        return score

    else:
        return 0


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