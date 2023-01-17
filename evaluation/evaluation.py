# Append root to path
import sys
import os
import time

from Utilities.pipelines import *
from scipy.io.wavfile import read

from utils import *

# Import methods for testing
from localization.direct_comparison.localize_sample_d import localize_sample_d
from localization.hashing.localize_sample_h import localize_sample_h
from localization.sliding_hashes.localize_sample_sh import localize_sample_sh
from localization.panako_sh.localize_sample_panako_sh import localize_sample_panako_sh
from localization.panako_h.localize_sample_panako_h import localize_sample_panako_h

sys.path.append(os.getcwd())

METHODS = [
    localize_sample_d,
    localize_sample_h,
    localize_sample_sh,
    localize_sample_panako_sh,
    localize_sample_panako_h,
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

all_paths = [

    ("../data/Clair_de_lune_original_1channel.wav",
     "../data/claire_de_lune_record1_kris_1channel.wav",
     "../data/labelled_data/claire_de_lune_record1_kris.txt"
     ),

    ("../data/bach_prelude_c_major/Bach_prelude_original_1channel.wav",
     "../data/bach_prelude_c_major/mic/BAch_prelude_Background_plus_mistake_1_channel.wav",
     "../data/labelled_data/BAch_prelude_Background_plus_mistake_1_channel.txt"
     ),

    ("../data/bach_prelude_c_major/Bach_prelude_original_1channel.wav",
     "../data/bach_prelude_c_major/mic/Bach_prelude_first_version_1channel.wav",
     "../data/labelled_data/Bach_prelude_first_version_1channel.txt"
     ),

    ("../data/bach_prelude_c_major/Bach_prelude_original_1channel.wav",
     "../data/bach_prelude_c_major/mic/Bach_prelude_second_version_1channel.wav",
     "../data/labelled_data/Bach_prelude_second_version_1channel.txt"
     )
]

length_snippets_in_secs = [3, 5, 10]


def evaluation_main(evaluation_method, localization_method):
    print(f"Evaluation method: {evaluation_method.__name__}")
    print(f"Localization method: {localization_method.__name__}")

    for path_ref, path_rec, path_labels in all_paths:

        print(f"Starting for: {path_rec}")

        start_time = time.time()
        scores = []

        labelled_data = get_labeled_data(path_labels)
        Fs_record, record_song = read(path_rec)
        Fs_ref, ref_song = read(path_ref)

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

        print(f"Done with {path_rec}\n")

        end_time = time.time()
        print(f"Total time taken: {end_time - start_time}\n")

        print("----------------EVALUATION RESULTS ---------------------")
        for j in range(len(length_snippets_in_secs)):
            print(
                "score for ",
                path_rec,
                " and snippet of ",
                length_snippets_in_secs[j],
                " seconds ---->",
                scores[j]
            )
        print("\n")

    print("----------COMPARING A SONG TO ITSELF--------")

    for path_ref, path_rec, path_labels in all_paths:

        print(f"Starting for: {path_rec}")
        start_time = time.time()
        scores = []
        labelled_data = get_labeled_data(path_labels)

        for i in range(len(labelled_data)):
            labelled_data[i] = (labelled_data[i][1], labelled_data[i][1])

        Fs_record, record_song = read(path_rec)
        Fs_ref, ref_song = read(path_ref)

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

        print(f"Done with {path_rec}\n")

        end_time = time.time()
        print(f"Total time taken: {end_time - start_time}\n")

        print("----------------EVALUATION RESULTS FOR SONG TO ITSELF---------------------")
        for j in range(len(length_snippets_in_secs)):
            print(
                "score for ",
                path_rec,
                " and snippet of ",
                length_snippets_in_secs[j],
                " seconds ---->",
                scores[j]
            )
        print("\n")


if __name__ == "__main__":

    for method in METHODS:
        evaluation_main(
            evaluation_method=evaluate_reduced_search_space,
            localization_method=method,
        )
