import time

# Append root to path
import sys
import os

sys.path.append(os.getcwd())

from Utilities.pipelines import *
from scipy.io.wavfile import read

from utils import *


# Import methods for testing
from localization import *

METHODS = [
    # localize_sample_d,
    localize_sample_h_shazam,
    localize_sample_h_panako,
    localize_sample_sw1_shazam,
    localize_sample_sw1_panako,
    localize_sample_sw2_shazam,
    localize_sample_sw2_panako,
]

# Fs_ref, ref_song = read(
#     "../data/Clair_de_lune_original_1channel.wav"
#     #"../data/bach_prelude_c_major/Bach_prelude_original_1channel.wav"
# )
#
# # paths to songs we will compare
# path1_rec = "../data/claire_de_lune_record1_kris_1channel.wav"
# #path1_rec = ("../data/bach_prelude_c_major/mic/Bach_prelude_first_version_1channel.wav")
# #path2_rec = ("../data/bach_prelude_c_major/mic/Bach_prelude_second_version_1channel.wav")
# #path3_rec = ("../data/bach_prelude_c_major/mic/BAch_prelude_Background_plus_mistake_1_channel.wav")
#
# # paths to labeled data of songs
# path1_labels = "../data/labelled_data/claire_de_lune_record1_kris.txt"
# #path1_labels = ("../data/labelled_data/Bach_prelude_first_version_1channel.txt")
# #path2_labels = "../data/labelled_data/Bach_prelude_second_version_1channel.txt"
# #path3_labels = ("../data/labelled_data/BAch_prelude_Background_plus_mistake_1_channel.txt")
#
# paths = [
#     (path1_rec, path1_labels)
#     #(path2_rec, path2_labels),
#     #(path3_rec, path3_labels)
# ]

"""
All paths and their respective:
- original reference song (.wav)
- recorded attempt (.wav)
- labelled data (.txt)
"""

ALL_PATHS = [
    (
        "./data/Clair_de_lune_original_1channel.wav",
        "./data/claire_de_lune_record1_kris_1channel.wav",
        "./data/labelled_data/claire_de_lune_record1_kris.txt",
    )
    # ,
    # ("../data/bach_prelude_c_major/Bach_prelude_original_1channel.wav",
    #  "../data/bach_prelude_c_major/mic/BAch_prelude_Background_plus_mistake_1_channel.wav",
    #  "../data/labelled_data/BAch_prelude_Background_plus_mistake_1_channel.txt"
    #  )
    #  ,
    #
    # ("../data/bach_prelude_c_major/Bach_prelude_original_1channel.wav",
    #  "../data/bach_prelude_c_major/mic/Bach_prelude_first_version_1channel.wav",
    #  "../data/labelled_data/Bach_prelude_first_version_1channel.txt"
    #  )
    #  ,
    #
    # ("../data/bach_prelude_c_major/Bach_prelude_original_1channel.wav",
    #  "../data/bach_prelude_c_major/mic/Bach_prelude_second_version_1channel.wav",
    #  "../data/labelled_data/Bach_prelude_second_version_1channel.txt"
    #  )
]

SNIPPET_LENGTHS = [3, 5, 10]


def get_eval_data(path_ref, path_rec, path_labels, mode):
    labelled_data = get_labeled_data(path_labels)
    fs_record, record_song = read(path_rec)
    fs_ref, ref_song = read(path_ref)

    if mode == "reference vs reference":
        labelled_data = [(label[1], label[1]) for label in labelled_data]
        return fs_ref, ref_song, fs_ref, ref_song, labelled_data

    elif mode == "recording vs reference":
        return fs_ref, ref_song, fs_record, record_song, labelled_data


def evaluation_main(evaluation_method, localization_method, mode):
    print(f"Evaluation method: {evaluation_method.__name__}")
    print(f"Localization method: {localization_method.__name__}")

    for path_ref, path_rec, path_labels in ALL_PATHS:

        print(f"Starting for: {path_rec}")

        start_time = time.time()
        scores = []

        fs_ref, ref_song, fs_record, record_song, labelled_data = get_eval_data(
            path_ref, path_rec, path_labels, mode
        )

        # for each song try different lengths of snippets:
        for length_snippet in SNIPPET_LENGTHS:
            score = evaluation_method(
                localization_method=localization_method,
                raw_ref=ref_song,
                fs_ref=fs_ref,
                raw_recording=record_song,
                fs_record=fs_record,
                recording_labels=labelled_data,
                length_snippet_secs=length_snippet,
            )

            print("done with snippets of length: ", length_snippet)
            scores.append(score)

        print(f"Done with {path_rec}\n")

        end_time = time.time()
        print(f"Total time taken: {end_time - start_time}\n")

        print(f"----------------EVALUATION RESULTS ({mode}) ---------------------")
        for j in range(len(SNIPPET_LENGTHS)):
            print(
                "score for ",
                path_rec,
                " and snippet of ",
                SNIPPET_LENGTHS[j],
                " seconds ---->",
                scores[j],
            )
        print("\n")


if __name__ == "__main__":

    for method in METHODS:
        evaluation_main(
            evaluation_method=evaluate_reduced_search_space,
            localization_method=method,
            mode="reference vs reference",
        )
