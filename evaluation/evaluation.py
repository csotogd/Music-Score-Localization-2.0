# Append root to path
import sys
import os
import csv
import matplotlib.pyplot as plt

sys.path.append(os.getcwd())

from scipy.io.wavfile import read

from utils_eval import *

# Import methods for testing
from localization.methods import *

METHODS = [
    # localize_sample_d,
    localize_sample_h_shazam,
    localize_sample_h_panako,
    localize_sample_sw1_shazam,
    localize_sample_sw1_panako,
    localize_sample_sw2_shazam,
    localize_sample_sw2_panako,
]

GRAPH_FOLDER = "../data/graphs/"
CSV_FOLDER = "../data/csv_files/"

"""
All paths and their respective:
- original reference song (.wav)
- recorded attempt (.wav)
- labelled data (.txt)
"""

ALL_PATHS = [
    (
        "../data/reference_wave_files/Clair_de_lune_original_1channel.wav",
        "../data/recorded_wave_files/claire_de_lune_record1_kris_1channel.wav",
        "../data/labelled_data/claire_de_lune_record1_kris.txt",
    )
    ,
    (
        "../data/reference_wave_files/Bach_prelude_original_1channel.wav",
        "../data/recorded_wave_files/BAch_prelude_Background_plus_mistake_1_channel.wav",
        "../data/labelled_data/BAch_prelude_Background_plus_mistake_1_channel.txt"
     )
    ,

    (
        "../data/reference_wave_files/Bach_prelude_original_1channel.wav",
        "../data/recorded_wave_files/Bach_prelude_first_version_1channel.wav",
        "../data/labelled_data/Bach_prelude_first_version_1channel.txt"
     )
    ,

    (
        "../data/reference_wave_files/Bach_prelude_original_1channel.wav",
        "../data/recorded_wave_files/Bach_prelude_second_version_1channel.wav",
        "../data/labelled_data/Bach_prelude_second_version_1channel.txt"
     )
    ,

    (
        "../data/reference_wave_files/The_ballad_of_john_and_yoko_BASS_1_channel.wav",
        "../data/recorded_wave_files/The_Ballad_Of_John_And_Yoko_bass_diyon.wav",
        "../data/labelled_data/The_ballad_of_john_and_yoko_bass.txt"
     )
    ,

    (
        "../data/reference_wave_files/The_ballad_of_john_and_yoko_BASS_1_channel.wav",
        "../data/recorded_wave_files/The_Ballad_Of_John_And_Yoko_piano_diyon_mistakes.wav",
        "../data/labelled_data/The_ballad_of_john_and_yoko_piano_mistakes.txt"
     )
    ,

    (
        "../data/reference_wave_files/The_ballad_of_john_and_yoko_BASS_1_channel.wav",
        "../data/recorded_wave_files/The_Ballad_Of_John_And_Yoko_piano_diyon_take2.wav",
        "../data/labelled_data/The_ballad_of_john_and_yoko_piano_take2.txt"
     )
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


def write_csv_files(mode: str):
    """
    Writes CSV files for all localisation methods. Each CSV file contains the score and snippet matching time per song

    Parameters
    ----------
    mode: String indicating the mode of matching: reference to reference, or recording to reference

    Returns
    -------
    None
    """

    print("Writing CSV files...")

    sub_folder = ""
    if mode == "reference vs reference":
        sub_folder = "ref_vs_ref/"
    elif mode == "recording vs reference":
        sub_folder = "rec_vs_ref/"

    for loc_method in CSV_DICT:

        with open(
            CSV_FOLDER + sub_folder + loc_method + ".csv", "w", newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow([loc_method])

            # Create header row
            header = ["Song"]
            for i in range(len(SNIPPET_LENGTHS)):
                header.append(f"Score ({str(SNIPPET_LENGTHS[i])}s)")
                header.append(f"Match time ({str(SNIPPET_LENGTHS[i])}s)")

            writer.writerow(header)

            # Create rows for each song
            for song_name in CSV_DICT[loc_method]:

                row = [song_name]
                row.extend(CSV_DICT[loc_method][song_name])

                writer.writerow(row)

    print("Done")


def draw_time_series_graphs(mode: str):
    """
    Creates graphs for the performance of each localisation method (matching score) per song

    Parameters
    ----------
    mode: String indicating the mode of matching: reference to reference, or recording to reference

    Returns
    -------
    None
    """

    print("Drawing graphs...")

    for graph_group in GRAPH_DICT:

        # One figure for all localisation methods, per snippet length and song
        plt.figure()

        # Each element of the list is a list and looks like: [loc_method, [time_steps], [scores]]
        for graph in GRAPH_DICT[graph_group]:

            time_steps = graph[1]
            scores = graph[2]
            label = graph[0]
            plt.plot(time_steps, scores, label=label)

        split_string = graph_group.split("_")
        plt.title(
            f"Localised snippet ({split_string[0]}) scores for {split_string[1]} vs. time"
        )
        plt.xlabel("Time (seconds)")
        plt.ylabel("Score")
        plt.legend()

        sub_folder = ""
        if mode == "reference vs reference":
            sub_folder = "ref_vs_ref/"
        elif mode == "recording vs reference":
            sub_folder = "rec_vs_ref/"

        file_name = graph_group + ".png"
        plt.savefig(GRAPH_FOLDER + sub_folder + file_name)

    print("Done")


def evaluation_main(evaluation_method, localization_method, mode):
    """
    Evaluates a localisation method, based on a particular evaluation method

    Parameters
    ----------
    evaluation_method: Evaluation method
    localization_method: Localisation method
    mode: String indicating the mode of matching: reference to reference, or recording to reference

    Returns
    -------
    None
    """

    print(f"Evaluation method: {evaluation_method.__name__}")
    print(f"Localization method: {localization_method.__name__}")

    # For each song
    for path_ref, path_rec, path_labels in ALL_PATHS:

        print(f"Starting for: {path_rec}")

        times = []
        scores = []
        score_arrays = []

        fs_ref, ref_song, fs_record, record_song, labelled_data = get_eval_data(
            path_ref, path_rec, path_labels, mode
        )

        # for each song try different lengths of snippets:
        for length_snippet in SNIPPET_LENGTHS:
            start_time = time.time()

            score, score_array = evaluation_method(
                localization_method=localization_method,
                raw_ref=ref_song,
                fs_ref=fs_ref,
                raw_recording=record_song,
                fs_record=fs_record,
                recording_labels=labelled_data,
                length_snippet_secs=length_snippet,
            )

            end_time = time.time()
            times.append(end_time - start_time)
            print("done with snippets of length: ", length_snippet)

            time_steps = [x[0] for x in labelled_data]

            song_name = path_rec.split("/")[-1].replace(".wav", "").replace("_", "")
            key = f"{str(length_snippet)}s_{song_name}"
            GRAPH_DICT[key].append(
                [
                    localization_method.__name__.replace("localize_sample_", ""),
                    time_steps,
                    score_array,
                ]
            )

            score_arrays.append(score_array)
            scores.append(score)

        csv_row = []
        for i in range(len(scores)):
            csv_row.append(round(scores[i], 2))
            csv_row.append(round(times[i], 2))
        song_name = path_rec.split("/")[-1].replace(".wav", "").replace("_", "")
        CSV_DICT[localization_method.__name__.replace("localize_sample_", "")][
            song_name
        ] = csv_row

        print(f"Done with {path_rec}\n")
        print(f"Total time taken: {sum(times)}\n")
        print(f"----------------EVALUATION RESULTS ({mode}) ---------------------")
        for j in range(len(SNIPPET_LENGTHS)):
            print(
                f"score for {path_rec} and snippet of {SNIPPET_LENGTHS[j]} seconds --> {scores[j]}. All scores: {score_arrays[j]}"
            )
        print("\n")


"""
For every snippet length and song, a graph will consist of all localisation methods' performance 

The dictionary contains:

key - snippetLength_songName: str
value - []: list

each element of the list is a list and looks like: [loc_method: str, [time_steps]:list, [scores]:list]
"""
GRAPH_DICT = {}

"""
For every localisation method, a song's matching score and matching time will be noted

The dictionary contains:

key - localisation_method: str
value - {}

Each key in the value dictionary is a song name; each song name has a value: 

[s3s, t3s, s5s, t5s, s10s, t10s, ....] where s3s is the matching score for a snippet of 3s, and t3s is the matching
time of a snippet of 3s, and so on
"""
CSV_DICT = {}

if __name__ == "__main__":

    match_mode = "recording vs reference"

    # Populate graph dictionary
    for _, path_recording, _ in ALL_PATHS:

        song = path_recording.split("/")[-1].replace(".wav", "").replace("_", "")

        # Create different snippet lengths for each song
        for snippet_length in SNIPPET_LENGTHS:

            graph_key = str(snippet_length) + f"s_{song}"
            GRAPH_DICT[graph_key] = []

    # Populate csv dictionary
    for method in METHODS:
        for _, path_recording, _ in ALL_PATHS:

            song = path_recording.split("/")[-1].replace(".wav", "").replace("_", "")

            CSV_DICT[method.__name__.replace("localize_sample_", "")] = {}

    for method in METHODS:
        evaluation_main(
            evaluation_method=evaluate_reduced_search_space,
            localization_method=method,
            mode=match_mode,
        )

    draw_time_series_graphs(match_mode)

    write_csv_files(match_mode)