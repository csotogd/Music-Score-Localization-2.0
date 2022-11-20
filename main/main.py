import multiprocessing
import time
import pyaudio
import wave
# import wavio

from Signal_Processing.IO.Audio_reader import PyAudio_reader


if __name__ == '__main__':
    seconds_total = 10
    seconds_per_segment = 2
    audio_reader = PyAudio_reader(fs=45000,
                                  seconds_per_segment=seconds_per_segment)
    recorded_so_far=[]

    for i in range(int(seconds_total/seconds_per_segment -1)):
        if i ==0:
            audio_reader.read_audio_segment(recorded_so_far)
            #nothing to proccess yet
        else:
            audio_reader = PyAudio_reader(fs=45000,
                                          seconds_per_segment=seconds_per_segment)
            p1 = multiprocessing.Process(target=audio_reader.read_audio_segment, args=[recorded_so_far])
            p2 = multiprocessing.Process(target=print, args=["preproccesing data"])
            p1.start()
            p2.start()
            p2.join()
            p1.join()
            p1.close()
            p2.close()


    p2 = multiprocessing.Process(target=print, args=["preproccesing data"])
