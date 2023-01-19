# Append root to path
import random
import sys
import os
import time

import numpy as np

from localization.montecarlo_robot.montecarlo import montecarlo_robot_localization
from localization.panako_sh.get_mc_scores_panako_sh import get_mc_scores_panako_sh

sys.path.append(os.getcwd())

from Utilities.pipelines import *
from scipy.io.wavfile import read

from utils import *

# Import methods for testing
from localization.direct_comparison.localize_sample_d import localize_sample_d
from localization.hashing.localize_sample_h import localize_sample_h
from localization.sliding_hashes.localize_sample_sh import localize_sample_sh
from localization.panako_sh.localize_sample_panako_sh import localize_sample_panako_sh
from localization.panako_h.localize_sample_panako_h import localize_sample_panako_h

METHODS = [
    localize_sample_d,
    localize_sample_h,
    localize_sample_sh,
    localize_sample_panako_sh,
    localize_sample_panako_h,
]


Fs_ref, ref_song = read(
    "../data/Clair_de_lune_original_1channel.wav"
    #"../data/bach_prelude_c_major/Bach_prelude_original_1channel.wav"
)

# paths to songs we will compare
path1_rec = "../data/claire_de_lune_record1_kris_1channel.wav"
#path1_rec = ("../data/bach_prelude_c_major/mic/Bach_prelude_first_version_1channel.wav")
#path2_rec = ("../data/bach_prelude_c_major/mic/Bach_prelude_second_version_1channel.wav")
#path3_rec = ("../data/bach_prelude_c_major/mic/BAch_prelude_Background_plus_mistake_1_channel.wav")

# paths to labeled data of songs
path1_labels = "../data/extensive_labelled_data/claire_de_lune_record1_kris.txt"
#path1_labels = ("../data/labelled_data/Bach_prelude_first_version_1channel.txt")
#path2_labels = "../data/labelled_data/Bach_prelude_second_version_1channel.txt"
#path3_labels = ("../data/labelled_data/BAch_prelude_Background_plus_mistake_1_channel.txt")

paths = [
    (path1_rec, path1_labels)
    #(path2_rec, path2_labels),
    #(path3_rec, path3_labels)
]

length_snippets_in_secs = [3]


def evaluation_main(evaluation_method, localization_method):
    # now we evaluate all songs
    start_time = time.time()
    print()
    print(f"Evaluation method: {evaluation_method.__name__}")
    print(f"Localization method: {localization_method.__name__}")
    print()
    scores = []
    for path_rec, path_labels in paths:
        labelled_data = get_labeled_data(path_labels)
        Fs_record, record_song = read(path_rec)

        # for each song try different lengths of snippets:
        for length_snippet in length_snippets_in_secs:

            score = evaluation_method(
                localization_method=localization_method,
                raw_ref=ref_song,
                fs_ref=Fs_ref,
                raw_recording=record_song,
                fs_record=Fs_record,
                recording_labels=labelled_data,
                length_snippet_secs=length_snippet,
            )
            print("done with snippets of length: ", length_snippet)
            scores.append(score)
        print("done with one version. moving onto the next.")
    names = ["first version"]#, "second version", "third version"]
    print()
    print()
    print()
    end_time = time.time()
    print("Total time taken: ", end_time - start_time)
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
    scores = []
    for path_rec, path_labels in paths:
        labelled_data = get_labeled_data(path_labels)
        for i in range(len(labelled_data)):
            labelled_data[i] = (labelled_data[i][1], labelled_data[i][1])
        Fs_record, record_song = read(path_rec)

        # for each song try different lengths of snippets:
        for length_snippet in length_snippets_in_secs:
            score = evaluation_method(
                localization_method=localization_method,
                raw_ref=ref_song,
                fs_ref=Fs_ref,
                raw_recording=ref_song,
                fs_record=Fs_ref,
                recording_labels=labelled_data,
                length_snippet_secs=length_snippet,
            )
            print("done with snippets of length: ", length_snippet)
            scores.append(score)
        print("done with one version. moving onto the next.")
    names = ["first version"]#, "second version", "third version"]
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




def evaluate_mc(
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
    length_ref_subset = 30
    previous_time = 0
    current_time = 0
    time_elapsed = 0

    # calculate constellation map for each
    constellation_ref = sp_pipeline(raw_ref, fs_ref, denoise=False)
    mc_localizer = montecarlo_robot_localization(nr_particles = 3000, length_ref_initial_subset= 30, length_entire_ref=len(raw_ref)/fs_ref)


    score = 0
    for time_recording, true_label in recording_labels:
        print('time recording: ', time_recording )
        previous_time= current_time
        current_time= time_recording
        time_elapsed= current_time - previous_time

        # get subset of the constellation map
        """
        const_ref_subset = get_fraction_of_ref_song(
            ref_song_cons_map=constellation_ref,
            fs_ref=fs_ref,
            indication_time=true_label,
            length_seconds_ref_song=len(raw_ref) / fs_ref,
            length_subset=length_ref_subset,
        )
        """

        # get an interval of the song around the point in the recording
        recording_interval = get_song_interval(
            raw_recording, time_recording, fs_record, length_sec=length_snippet_secs
        )
        constellation_record = sp_pipeline(recording_interval, fs_record, denoise=True)

        predictions =get_mc_scores_panako_sh(sample_constellation_map= constellation_record, song_constellation_map= constellation_ref, ref_freq=fs_ref)

        ##perform the iteration of the montecarlo
        mc_localizer.iterate(length_ref=30, time_diff_snippets=time_elapsed, predictions=predictions) #check the time diff snippets, filled with a random value
        prediction = mc_localizer.get_most_likely_point(length_intervals=2, offset_intervals=0.2)

        score_point = evaluate_localization(true_label, np.array([prediction]))
        print('score point: ', score_point)
        print()
        score += score_point

    score_normalized = score / len(recording_labels)
    return score_normalized




if __name__ == "__main__":
    score = evaluation_main(
        evaluation_method=evaluate_mc,
        localization_method=localize_sample_sh,
    )

    print('score: ', score)
