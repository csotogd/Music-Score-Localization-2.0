from Signal_Processing.IO.Audio_IO import Parameters_IO


class Generator_segments_recorded:
    """
    Generates sound segments for a recorded signal using the next method.
    """

    def __init__(self, recorded_song, seconds_per_segment, non_overlap_seconds):
        self.recorded_song = recorded_song
        self.seconds_per_segment = seconds_per_segment
        self.non_overlap_seconds = non_overlap_seconds # number of seconds in each segment of new content
        self.length_secs_rec = len(recorded_song) / Parameters_IO.fs
        self.start_id = -1
        self.end_id = -1


    def get_first_start_end_id(self):
        """
        Returns the start and the end id of the segment to be read from a reference song
        """
        start_segment_id = 0
        end_segment_id = start_segment_id + (self.seconds_per_segment * Parameters_IO.fs)
        if end_segment_id>= len(self.recorded_song):
            end_segment_id= len(self.recorded_song)-1

        return start_segment_id, end_segment_id

    def next(self):
        """

        Returns
        -------
        The next song segment (np.array) to proccess or None if there are no more song snippets to return

        """

        if self.start_id<0: #first song snippet
            self.start_id, self.end_id = self.get_first_start_end_id()


        elif self.end_id>= len(self.recorded_song)-1: #nothing else to read
            return None


        else:
            self.start_id+= self.non_overlap_seconds*Parameters_IO.fs
            self.end_id+= self.non_overlap_seconds*Parameters_IO.fs

            if self.end_id >= len(self.recorded_song):
                self.end_id = len(self.recorded_song) - 1




        return self.recorded_song[self.start_id: self.end_id]

    def get_time_average(self):
        """
        Gets the time in seconds of the center of the segment which was returned last.
        Assume, we have a song of 10 seconds. We call the method next()
        and get a song segment from second 6 to second 8,
        then the returned value will be 7, because it is the middle value inseoncds of the last segment
        relative to the whole song


        Returns
        -------

        """
        seconds_start = self.start_id/Parameters_IO.fs
        seconds_end = self.end_id/Parameters_IO.fs

        return (seconds_end+ (seconds_end-seconds_start))/2

    def get_start_end_times(self):
        """
        Gets the times in seconds of the  segment which was returned last.
        Assume, we have a song of 10 seconds. We call the method next()
        and get a song segment from second 6 to second 8,
        then the returned values will be 6 and 8
        """
        seconds_start = self.start_id/Parameters_IO.fs
        seconds_end = self.end_id/Parameters_IO.fs
        return (seconds_start, seconds_end)