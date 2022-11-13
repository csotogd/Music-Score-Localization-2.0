from Signal_Processing.noise_filter import FIR_noise_filter
from Signal_Processing.spectrogram_builder import STFT_spectrogram


def sp_pipeline(raw_signal, fs):
    #denoised
    filter = FIR_noise_filter(length=20)
    denoised = filter.filter_noise(raw_signal, fs)

    #spectrogram
    spectr_builder = STFT_spectrogram()
    f, t, Zxx =spectr_builder.spectrogram_calculate_plot(denoised, fs)

    #constellation_map
    #TODO