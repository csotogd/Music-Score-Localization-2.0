# Append root to path
import sys
import os

sys.path.append(os.getcwd())


from Uttilities.pipelines import *
from localization.direct_comparison.localize_sample_d import localize_sample_d
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

        predictions, _ = localize_sample_d(
            constellation_record, constellation_ref, fs_record
        )

        score_point = evaluate_localization(true_label, predictions)
        score += score_point

    score_normalized = score / len(recording_labels)
    return score_normalized


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
    time_recording: float second ([0, inf]) which is the center of the interval we want to obtain
    length_sec: float length of the interval we want to return

    Returns
    -------
    a np array of a subset of the raw_recording parameter

    """

    seconds_start = time_recording - length_sec / 2
    seconds_end = time_recording + length_sec / 2

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
        "data/bach_prelude_c_major/Bach_prelude_original_1channel.wav"
    )

    # paths to songs we will compare
    path1_rec = "data/bach_prelude_c_major/mic/Bach_prelude_first_version_1channel.wav"
    path2_rec = "data/bach_prelude_c_major/mic/Bach_prelude_second_version_1channel.wav"
    path3_rec = "data/bach_prelude_c_major/mic/BAch_prelude_Background_plus_mistake_1_channel.wav"

    # paths to labeled data of songs
    path1_labels = "data/labelled_data/Bach_prelude_first_version_1channel.txt"
    path2_labels = "data/labelled_data/Bach_prelude_second_version_1channel.txt"
    path3_labels = (
        "data/labelled_data/BAch_prelude_Background_plus_mistake_1_channel.txt"
    )

    paths = [
        (path1_rec, path1_labels),
        (path2_rec, path2_labels),
        (path3_rec, path3_labels),
    ]
    length_snippets_in_secs = [3, 5, 10]
    scores = []

    # now we evaluate all songs
    for path_rec, path_labels in paths:
        labelled_data = get_labeled_data(path_labels)
        Fs_record, record_song = read(path_rec)

        # for each song try different lengths of snippets:
        for length_snippet in length_snippets_in_secs:

            score = evaluate(
                raw_ref=ref_song,
                fs_ref=Fs_ref,
                raw_recording=record_song,
                fs_record=Fs_record,
                recording_labels=labelled_data,
                length_snippet_secs=length_snippet,
            )
            scores.append(score)

    names = ["first version", "second version", "third version"]
    print()
    print()
    print()
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
