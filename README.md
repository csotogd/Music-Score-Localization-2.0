# Music-Score-Localization-2.0

The absence of an automatic page turner that can
localise a musician performing to the appropriate section of
a music score poses problems. Particularly for musicians with
visual impairments who must zoom into the sheet music to
distinguish notes, greatly increasing the frequency of page turns.
The paper proposes a novel adaptation of the Shazam algorithm and its variations such as PANAKO.
These algorithms are used to map a subset of a song to the entire reference song, 
instead of finding a song in a database of songs. These methods are modified to account for pitch and speed dilations.

In order to disambiguate repetitions and take consecutive recordings into considerations, we use a
method used to localize a mobile robot in a known map. In our case the position of the robot in the map would
correspond to the time in a song we are in. The strategy chosen is the MonteCarlo localization method, which
estimates the posterior probability by maintaining and updating a set of particles (possible times).

We test our strategy in our self-built test set. Labelling data was time consuming.

Please read the report for a more in depth explanation
