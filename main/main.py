from Signal_Processing.IO.Audio_IO import Parameters_IO
from Uttilities.Generator_segments import Generator_segments_recorded
from scipy.io.wavfile import read
from Signal_Processing.signal_plotting import plot_signal
from Uttilities.pipelines import *

if __name__ == '__main__':

    # Read the input WAV files, they need to have 1 channel, NOT STEREO
    Fs, ref_song = read("../data/imagine_john_lennon_PIANO_1_channel.wav")
    Parameters_IO.fs = Fs

    #aply the entire signal proccessing pipeline to the reference song to obtain a constellation map
    ref_segments_map_time = ref_signal_pipeline(ref_song, secs_per_segment = 3, non_overlap_seconds=2)



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
        Fs, rec_song = read("../data/imagine_john_lennon_PIANO_1_channel.wav")



        #now I will partition the song into song snippets of a chosen length
        #for each song snippet I will compute its contellation_map
        #then we will try to match that signal to the the reference constellation
        #map by means of the shazam algorithm
        count=1
        generator_semnets = Generator_segments_recorded(rec_song,seconds_per_segment=2, non_overlap_seconds=2)
        song_segment = generator_semnets.next()
        while song_segment is not None:
            plot_signal(song_segment)
            sp_pipeline(song_segment, Fs, denoise=True)
            #TODO include matching algorithm here
            #here we would compare histograms

            song_segment = generator_semnets.next()
            count+=1








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
