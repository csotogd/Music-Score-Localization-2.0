from Uttilities.pipelines import *
from localization.localization_pipe import localization_pipeline

"""
This file handles the evaluation of our method.
"""

def evaluate(raw_ref, raw_recording, recording_labels):
    """

    Parameters
    ----------
    raw_ref: np array of the reference song, before any processing
    raw_recording: np array of the recording, before any proccesing
    recording_labels: data structure to be defined
            This stores our (X,Y), where the X represents a time point (in seconds)
            in the recorded song, and the Y represent the time at which that bit appears.     
        
    Returns
    -------
    a score (to be defined)
        
    """
    #calculate constellation map for each
    constellation_ref = sp_pipeline(raw_ref, Parameters_IO.fs, denoise=False)
    constellation_record = sp_pipeline(raw_recording, Parameters_IO.fs, denoise=True)


    score= 0
    for time_recording, true_labels in recording_labels:
        #get an interval of the song around the point in the recording
        recording_interval = get_song_interval(time_recording) #TODO implement

        #use shazam algorithm to localize snippet:
        prediction =localization_pipeline(constellation_ref, constellation_record, time_ahead= 10, sample_freq= Parameters_IO.fs)


        score += metric(time_recording, true_labels, prediction)

    score_normalized = score/ len(recording_labels)
    return score_normalized



def metric(time_recording, true_labels, prediction):#TODO implement
    return "a score"

def get_song_interval(time_recording, length_sec=3): #TODO implement
    return "a np array containing length_sec seconds of recording in the recorded song," \
           " where time_recording is in the middle of the interval"

