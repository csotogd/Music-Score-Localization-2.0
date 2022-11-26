from Signal_Processing.noise_filter import FIR_noise_filter
from Signal_Processing.spectrogram_builder import STFT_spectrogram
from Uttilities.Generator_segments import Generator_segments_recorded
from Signal_Processing.IO.Audio_IO import Parameters_IO
from Signal_Processing.constellation_map_builder import build_constellation_map


def ref_signal_pipeline(ref_song, secs_per_segment, non_overlap_seconds):
    """
    Parameters
    ----------
    ref_song: np.array (1,N)
        full song which is used as reference
    secs_per_segment: float
        nr of seconds in each segment
    non_overlap_seconds: float
        nr of secons in each new segment that are non overlapping with the previous one

    Returns
    -------
        A list of tuples which is tuple is the contellation map and times of one segment.
        Imagine we partition the referene song in 10 segments, then the returned list will havae 10 elements, each of them
        being the constellation map and (start, end time) of each segment

    """
    segments_map_time=[] #this list will contain tuple (time, map)
                        #the firs element id a segment contellation map, and the second element is a tuple
                        #containing the start and end times

    generator_semnets = Generator_segments_recorded(ref_song, secs_per_segment, non_overlap_seconds)
    song_segment = generator_semnets.next()
    times = generator_semnets.get_start_end_times()

    while song_segment is not None:
        #we generate segments and apply the signal proccesing pipeline to it
        constellation_map = sp_pipeline(song_segment, Parameters_IO.fs, denoise=False)
        segments_map_time.append((constellation_map, times))

        song_segment = generator_semnets.next()
        times = generator_semnets.get_start_end_times()

    return segments_map_time

def sp_pipeline(raw_signal, fs, denoise=False):
    #denoised
    if denoise:
        filter = FIR_noise_filter(length=20)
        denoised = filter.filter_noise(raw_signal, fs)
    else:
        #the reference song does not have to be denoised
        denoised = raw_signal

    #spectrogram
    spectr_builder = STFT_spectrogram()
    #spectr_builder.spectrogram_calculate_plot(denoised, fs)
    f, t, Zxx =spectr_builder.spectrogram(denoised, fs)

    #constellation_map
    constellation_map = build_constellation_map(f, t, Zxx, fs)
    print(constellation_map)
    return  constellation_map