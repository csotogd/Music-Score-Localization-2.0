from Signal_Processing.noise_filter import FIR_noise_filter
from Signal_Processing.spectrogram_builder import STFT_spectrogram


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
    #TODO implement
    constellation_map =[]
    return  constellation_map