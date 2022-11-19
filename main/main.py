import multiprocessing
import time
import pyaudio
import wave
import wavio

from Signal_Processing.IO.Audio_IO import Parameters_IO
import scipy
import numpy as np
import matplotlib.pyplot as plt
from Signal_Processing.IO.Audio_IO import Generator_segments_recorded
from scipy.io.wavfile import read
from Signal_Processing.signal_plotting import plot_signal
from Signal_Processing.sp_pipeline import sp_pipeline



if __name__ == '__main__':

    # Read the input WAV files
    Fs, ref_song = read("../data/imagine_john_lennon_PIANO.wav")
    Parameters_IO.fs = Fs

    #TODO remove this line of code, only hear to get a 1D array instead of a 2D array.
    ref_song = ref_song[:, 1]

    #aply the entire signal proccessing pipeline to the reference song to obtain a constellation map
    const_map_ref = sp_pipeline(ref_song, Fs)


    #now we focus on the signal that is recorded by the microphone. There are two posibilities:
    #we either have the song stored because it is a past recording and we need to load it or we
    #will record the sound in real time. This will be controlled by the variable from_mic
    from_mic = False
    path_to_recording = "../data/imagine_john_lennon_PIANO.wav"
    #since we have not recorded Diyon playing piano, we will match the signal with itself

    if from_mic:
        a= "NEEDS TO BE IMPLEMENTED"

    else:
        # Read the input WAV files
        Fs, rec_song = read("../data/imagine_john_lennon_PIANO.wav")
        # TODO remove this line of code, only hear to get a 1D array instead of a 2D array.
        rec_song = rec_song[:, 1]


        #now I will partition the song into song snippets of a chosen length
        #for each song snippet I will compute its contellation_map
        #then we will try to match that signal to the the reference constellation
        #map by means of the shazam algorithm


        generator_semnets = Generator_segments_recorded(rec_song)
        song_segment = generator_semnets.next()
        while song_segment is not None:
            plot_signal(song_segment)
            sp_pipeline(song_segment, Fs, denoise=True)
            #TODO include matching algorithm here
            #here we would compare histograms

            song_segment = generator_semnets.next()









    """
           p1 = multiprocessing.Process(target=read_segment())
                p2 = multiprocessing.Process(target=print, args=["preproccesing data"])
                p1.start()
                p2.start()
                p2.join()
                p1.join()
                p1.close()
                p2.close()
    
    
    """
