import random
from numpy import arange
import numpy as np
from matplotlib import pyplot as plt
from localization.decay_distribution import decay_dist
class montecarlo_robot_localization:
    def __init__(self, nr_particles, length_ref_initial_subset, length_entire_ref):
        """
        Parameters
        ----------
         nr_particles int
        length_ref_subset int. This is in seconds. Either the length of the refernece song (if we are to compute it fully) or the size of the
                            subset we are going to consider
        length_entire_ref float, length of entire ref song in seconds
        """
        self.set_of_particles =self.__create_initial_set_of_particles(nr_particles, length_ref_initial_subset) #these always need to be ordered by time in ascending order
        self.length_entire_ref= length_entire_ref
    def iterate(self, length_ref, time_diff_snippets, predictions):
        """
        Performs one iteration of the montecarlo localization strategy, i.e. updates the set of particles
        Parameters
        ----------
        length_ref: length of the subset/whole reference song used in this iteration
        time_diff_snippets: time differnece between this snippet and the previous one
        predictions: interpretations of current measurements used to adjust the weights for particles

        """
        S_prime_k= self.__prediction_phase(S_k_minus_1=self.set_of_particles, length_ref=length_ref, time_diff_snippets= time_diff_snippets)
        self.set_of_particles= self.__update_phase(S_prime_k, predictions)
        self.set_of_particles= np.sort(self.set_of_particles)


    def get_most_likely_point(self, length_intervals=0.5, offset_intervals=0.15) :
        """
        Computes the most likely point in time of the reference song the musician is in given the current set of particles.
        This is done by using a sliding interval approach.


        offset_intervals: referes to how much we move the sliding interval each time.

        Returns
        -------
        the time point in time which is more likely to happen
        """
        start_idx=0
        end_idx= 0
        end_idx= self.__find_next_end_idx(start_idx,end_idx,length_intervals)

        center_intervals=[] #to be indexed at the same time as density_intervals
        density_intervals=[] #to be indexed at the same time as center_intervals


        while not (end_idx>=len(self.set_of_particles)-1 and start_idx ==end_idx):

            #first compute density for the current interval and store it
            density = end_idx - start_idx +1
            density_intervals.append(density)
            center = (self.set_of_particles[end_idx] + self.set_of_particles[start_idx])/2
            center_intervals.append(center)

            #second shift interval by offset_intervals seconds
            start_idx, end_idx = self.__find_next_interval(start_idx, length_intervals, offset_intervals)

        indx_max_density = np.argmax(density_intervals)
        return center_intervals[indx_max_density]


    """==========================   PRIVATE METHODS FROM HERE ONWARDS  ========================="""

    def __find_next_interval(self, start_indx, length_intervals, offset_intervals):
        start_indx= self.__find_next_start_idx(start_indx, offset_intervals)
        end_indx=start_indx
        end_indx= self.__find_next_end_idx(start_indx, end_indx, length_intervals)
        return start_indx, end_indx


    def __find_next_start_idx(self, start_idx, offset_intervals):
        previous_start_idx = start_idx
        while self.set_of_particles[start_idx] - self.set_of_particles[previous_start_idx] < offset_intervals:
            start_idx += 1
            if start_idx >= len(self.set_of_particles):
                start_idx-=1
                break
        return start_idx

    def __find_next_end_idx(self, start_idx, end_idx, length_intervals):
        # move end_index up until we get to n seconds
        while self.set_of_particles[end_idx] - self.set_of_particles[start_idx] < length_intervals:
            end_idx += 1
            if end_idx >= len(self.set_of_particles):
                end_idx-=1
                break
        # once it reaches that bit I need to substract 1 from the end index such that it does not exceed the length we want
        if self.set_of_particles[end_idx] - self.set_of_particles[start_idx] > length_intervals:
            end_idx-=1
        return end_idx



    def __create_initial_set_of_particles(self, nr_particles, length_ref_subset, initial_time=0):
        """
        Creates and return an initial set of particles S_0. This is done by uniformly selecting
        points in time between the start time and the length of the reference song plus the start time.
        Parameters
        ----------
        nr_particles int
        length_ref_subset int. This is in seconds. Either the length of the refernece song (if we are to compute it fully) or the size of the
                                subset we are going to consider

        Returns
        -------
        a 1d np array of time points in seconds.
        """

        particles = np.arange(initial_time, initial_time+length_ref_subset, length_ref_subset/nr_particles)

        return particles

    def __prediction_phase(self, S_k_minus_1, length_ref, time_diff_snippets):
        """
        Performs the prediction phase as specified in the paper
        Parameters
        ----------
        S_k_minus_1: 1d np array containing the particles (times in seconds) as floats
        length_ref: length of reference song/subset in seconds
        time_diff_snippets: float, time difference in seconds that elpases between consecutive calls to the prediction phase method, offset between snippets to localize

        Returns
        a new np array of the same shape and type as the one given as input
        -------

        """
        S_prime_k=np.zeros(shape=S_k_minus_1.shape, dtype=float)
        #first we need to add the time difference between the previous observation (song snippet) and the current one.
        S_k_minus_1= S_k_minus_1+time_diff_snippets

        for i in range(len(S_k_minus_1)):
            particle = S_k_minus_1[i]
            probs_x= self.__generate_prob_xk_of_prediction_phase(particle, length_ref)
            new_particle = self.__generate_new_particle_prediction_phase(probs_x)
            S_prime_k[i]=new_particle

        return S_prime_k

    def __update_phase(self, S_prime_k, predictions):
        """
        Update Phase of the monte carlo approach, updates the weights according to new sensor measurements and generates
         a new set of particles

        Parameters
        ----------
        S_prime_k: set of particles calculated in prediction phase. 2d np array of floats
        predictions: predicted positions from new sensor measurements
        Returns
        -------
        np array of floats of dimensions (N,2), where N represents the number of particles.
        [i,0] accesses the weight of particle i
        [i,1] accesses the time of particle 1
        """
        weights_M_k = self.__generate_weights_M_k(S_prime_k, predictions)
        return self.__generate_new_set_of_particles_update_phase(weights_M_k)

    def __generate_prob_xk_of_prediction_phase(self, particle, length_ref, length_side=3, step_size=0.1, fake_score = 0.1):
        """
        Here we are calculating the probability of being in a certain point knowing the resulting set of particles in the previous phase and
        not knowing the input at time k. This is the probability distribution that is calculated under the prediction phase of the paper.

       In order to calculate the probability, we do the following:
        Each particle '*' has an interval [a, b] centered around it. If an estimation position lands within the interval
        it receives a score relative to it's proximity to '*'. The score linearly decreases from the particle to the
        interval endpoints a and b. Every other point still gets a non score. An illustration is provided below:

              |                    *
        score |                   / \
              |                  /   \
              |                 /     \
              | ---------------        -----------------
              |_____________________________________
                   time        a        b

        Anything between a and b would get a score


        So the proccess works as follows:
        1.- We take steps of step_size seconds. For each step we calculate a score for that position as explained above.
        2.- We sum the scores of each position and we normalize. This way we get a probability distribution between 0 and 1

        Parameters
        ----------
        particle: a time point in seconds (float)
        length_side: float length in seconds of each side of the interval
        length_ref: length of reference song in seconds.
        step_size: float step size in seconds. We will generate the probability of selecting timepoints every step_size seconds
        fake_score: float which represents the probability to all those points that are different

        Returns
        -------
        A np array of dimensions [nr_steps in the entire song, where for each entry i,
                the first element [i][0] is a time point and the second element is the probability of selecting that time point.
                If the probability for a value is 0 there will be no entry for it
        """
        interval_nr_indices = int(self.length_entire_ref/step_size)
        probs_x= np.zeros([interval_nr_indices , 2], dtype=float)
        probs_x[:, 1] = np.ones([interval_nr_indices]) * fake_score
        probs_x[:, 0] = np.arange(0, self.length_entire_ref-step_size, step_size)

        start_second = max(0, particle- length_side)
        end_second = min(particle+ length_side, length_ref-step_size)


        slope = 1/length_side
        i=int(start_second/step_size)
        for time in arange(start_second, min(particle,length_ref-step_size), step_size): #first lenght of the interval
            probs_x[i][0]=time
            probs_x[i][1]=(time-start_second)*slope
            i+=1

        for time in arange(particle,end_second, step_size): #first lenght of the interval
            probs_x[i][0]= time
            probs_x[i][1]    = 1 + (time- particle)* - slope
            i += 1

        #now we normalize the probability
        probs_x[:,1] /=sum(probs_x[:,1])
        return probs_x

    def __generate_new_particle_prediction_phase(self, probs_x):
        """
        Generates a new particle knowing the probabilities of x given a particle and the previous input. This is part of the prediction phase

        Parameters
        ----------
        probs_x: conditional probability of having a particle at state x calculated previously in this prediciton phase
                A np array of dimensions [length_entire_song/step_size ,2], where for each entry i,
                the first element [i][0] is a time point and the second element is the probability of selecting that time point.
                If the probability for a value is 0 there will be no entry for it

        Returns
        -------
        a new particle (float), which represents a time point.
        """
        new_particle = None
        cum_sum = np.cumsum(probs_x[:, 1])
        random_limit = random.random()

        for i in range(len(cum_sum)):
            prob = cum_sum[i]
            if prob>= random_limit:
                new_particle= probs_x[i][0]
                break

        return new_particle


    def __generate_weights_M_k(self, S_prime_k, predictions, fake_weight=0.1):
        """
        For each particle calculates the probability of the observation given the particle.
        This is done in the following way:
            1. Use panako/hashing sliding window, to obtain a score for all the times in the song.
            2. Get the score given by 1 at the time of the particle, that would be the weight
            3. normalize all weights to add up to one

        Parameters
        ----------
        S_prime_k: set of particles calculated in prediction phase. 2d np array of floats
        predictions: predicted positions from new sensor measurements
        fake_weight: float that represents the score that we will give to points where the matching algorithm finds no matching

        Returns
        -------
        np array of floats of dimensions (N,2), where N represents the number of particles.
        [i,0] accesses the weight of particle i
        [i,1] accesses the time of particle 1
        """
        weight_list = np.zeros(shape=(len(S_prime_k), 2) , dtype=float)
        weight_list[:,1]= S_prime_k

        for i in range(len(S_prime_k)):
            particle = S_prime_k[i]
            #get localization score for that particle time
            weight= self.__get_localization_score(particle=particle, predictions=predictions, fake_score=fake_weight)
            weight_list[i, 0]= weight

        #normalize scores
        if np.sum(weight_list[:,0]) != 0:
            weight_list[:,0]= weight_list[:,0]/sum(weight_list[:,0]) ##TODO this line is causing a NaN value in the weight of the first particle during initialisation
        return weight_list


    def __get_localization_score(self, particle, predictions, length_center =0.5, length_side=0.25, fake_score=0.1):
        """
        Outputs a localisation score for each particle.

        Score is 1*score in predictions in an interval of length length center where the is one prediction in the center.
        Then it gets a score of 0.5* score in predictions if it is within 0.5 and 0.25s to the center of the inteval.

        Parameters
        ----------
        particle: particle object containing a time and weight
        predictions: predicted positions from new sensor measurements
        Returns
        -------
        a score between 1 and 0.
        """
        score = fake_score

        times_key = (list(predictions.keys()))

        for actual_time in times_key:

            if (particle>actual_time-length_center/2) and (particle< actual_time+length_center/2):
                score+= predictions[actual_time]* 1

            elif (particle<actual_time-length_center/2) and (particle>actual_time-length_center/2 - length_side):
                score+= predictions[actual_time]* 0.5

            elif (particle>actual_time+length_center/2) and (particle<actual_time+length_center/2 + length_side):
                score+= predictions[actual_time] * 0.5

        return score


    def __get_fuzzy_localization_score(self, particle, predictions, tolerance=1):
        """
        Outputs a localisation score for each particle. Tolerance around the prediction value for which a 1 is still
        returned as the weight for the particle. Example shown below

                    ____tol____|___tol____
                    |                     |
        score       |                     |
                    |                     |
         ___________|          /\         |_______________
                               |
                            prediction

                          <-time->

        Parameters
        ----------
        particle: particle object containing a time and weight
        predictions: predicted positions from new sensor measurements
        tolerance: the tolerance to either side of the prediction for which a value of 1 is returned

        Returns
        -------
        a score between 1 and 0.
        """

        score = 0
        for prediction in predictions:
            if abs(prediction - particle) <= tolerance:
                score += 1




    def __get_weighted_localization_score(self, particle, predictions, future_decay = 1):
        """
        Decayed weight of the particles time instance to predicted points

                     /\
                   /   \
               a /      \  b  ---- exponential rise (with rate a) and decay (with rate b). future_decay = b/a
               /         \
        ______/           \______________________

        Parameters
        ----------
        particle: particle object containing a time and weight
        predictions: predicted positions from new sensor measurements
        future_decay: decay factor of future predictions to past predictions

        Returns
        -------
        weight as sum of the decayed weights from all predictions to the particle time.
        """
        dec_dist = decay_dist.Decay_Dist(future_decay)
        score = 0
        for prediction in predictions:
            score += dec_dist(prediction - particle)
        return score

    def __generate_new_set_of_particles_update_phase(self, weights_M_k):
        """
        Generates a new set of particles, of the same length as the previous one, where the sampling is weighted
        according to the weights previously calculated in the update phase

        Parameters
        ----------
        weights_M_k: np array of floats of dimensions (N,2), where N represents the number of particles.
        [i,0] accesses the weight of particle i . the weight is a valid probability (they all sum up to one)
        [i,1] accesses the time of particle 1

        Returns
        -------
        1d float np array. New set of particles, where each entry in the np array represents the times of the particles.
        """

        new_set_particles = np.zeros(shape=weights_M_k[:,0].shape, dtype=float)
        cum_sum= np.cumsum(weights_M_k[:,0])
        random_sorted = np.sort(np.random.random(cum_sum.shape))


        #we will traverse the cum_sum and random_choices_Sorted simultaneously to keep the complexity of he loop linear. (it is O(nlogn) as there was sorting done before)
        idx_cumsum=0
        idx_random_sorted=0
        while idx_random_sorted< len(random_sorted) and idx_cumsum<len(cum_sum):
            random_sorted_value = random_sorted[idx_random_sorted]

            if idx_cumsum==0:#base case, done separately to avoid index out of bounds error
                if random_sorted_value <= cum_sum[idx_cumsum]:
                    new_particle = weights_M_k[idx_cumsum, 1]
                    new_set_particles[idx_random_sorted] = new_particle
                    idx_random_sorted+=1
                else:
                    idx_cumsum+=1
            else:
                ##TODO suspected index out of bounds error, when cum_sum array is size 1*2 (seen during initialisation) still present. Seems to have been accounted for before but not working
                if random_sorted_value> cum_sum[idx_cumsum-1] and random_sorted_value<= cum_sum[idx_cumsum]:
                    new_particle = weights_M_k[idx_cumsum, 1]
                    new_set_particles[idx_random_sorted] = new_particle
                    idx_random_sorted+=1

                else:
                    idx_cumsum += 1

        return new_set_particles





if __name__ == '__main__':
    #probs_x= (generate_prob_xk_of_prediction_phase(particle=5, length_side=3, length_ref=10, step_size=0.1))
    #generate_new_particle_prediction_phase(probs_x)

    """
    S_k_minus_1= np.random.random(size=(5,1))*9
    length_ref = 10
    time_diff_snippets= 1
    print(S_k_minus_1)
    print()
    print()
    s_k_prime = prediction_phase(S_k_minus_1, length_ref, time_diff_snippets)
    print(s_k_prime)
    """

    """
    set_of_particles = np.array([0, 2, 2.5, 3.4, 5.9,6.7, 8.7, 8.9, 9, 9.6])
    mc = montecarlo_robot_localization(nr_particles=10, length_ref_initial_subset=10)
    mc.set_of_particles= set_of_particles

    most_likely_time = mc.get_most_likely_point(length_intervals=2, offset_intervals=0.1)
    print(most_likely_time)
    """

    """
        predictions = {0.1:1, 0.2:1, 0.7: 3, 0.83:2, 3.2: 1, 4.1: 7, 5: 3, 7.5: 1}
        for particle in [0, 0.5,1,1.5, 2, 2.5,3, 3.5,4, 4.5,5, 5.5,6, 6.5,7, 7.5,8]:
            score = mc.get_localization_score(particle, predictions)
            print("particle: ", particle, " ------> score: ", score)
    """
    length_ref = 30
    time_step = 3
    #we are goin to simulate an iteration without taking the hashing/panako part into account to see how th emthod performs
    mc = montecarlo_robot_localization(nr_particles=1000, length_ref_initial_subset=length_ref, length_entire_ref=length_ref)



    for i in range(20):
        print(i)
        #create random prediction dict
        times = list(np.random.rand(100)* length_ref+ time_step*i)
        scores = list(np.random.rand(100)*4)
        predictions= dict(zip(times, scores))

        mc.iterate(length_ref=length_ref,predictions= predictions, time_diff_snippets=3)
        mc.get_most_likely_point()
        print("mean of particles: ", mc.set_of_particles.mean())
        print("std of particles: ", mc.set_of_particles.std())



