import random
from numpy import arange
import numpy as np
from matplotlib import pyplot as plt
class montecarlo_robot_localization:
    def __init__(self, nr_particles, length_ref_initial_subset):
        """
        Parameters
        ----------
         nr_particles int
        length_ref_subset int. This is in seconds. Either the length of the refernece song (if we are to compute it fully) or the size of the
                            subset we are going to consider
        """
        self.set_of_particles =self.create_initial_set_of_particles(nr_particles, length_ref_initial_subset)

    def iterate(self, length_ref, time_diff_snippets):
        """
        Performs one iteration of the montecarlo localization strategy, i.e. updates the set of particles
        Parameters
        ----------
        length_ref: length of the subset/whole reference song used in this iteration
        time_diff_snippets: time differnece between this snippet and the previous one

        """
        S_prime_k= self.prediction_phase(self, S_k_minus_1=self.set_of_particles, length_ref=length_ref, time_diff_snippets= time_diff_snippets)
        self.set_of_particles= self.update_phase(S_prime_k)


    def get_most_likely_point:
        
        """
        Returns
        -------
        the time point in time which is more likely to happen
        """


    def create_initial_set_of_particles(self, nr_particles, length_ref_subset):
        """
        Creates and return an initial set of particles S_0. This is done by uniformly randomly selecting
        points in time between 0 and the length of the reference song.
        Parameters
        ----------
        nr_particles int
        length_ref_subset int. This is in seconds. Either the length of the refernece song (if we are to compute it fully) or the size of the
                                subset we are going to consider

        Returns
        -------
        A list of time points in seconds.
        """

        particles = [((random.random()+0) *length_ref_subset) for _ in range(nr_particles)]

        return particles

    def prediction_phase(self, S_k_minus_1, length_ref, time_diff_snippets):
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
            probs_x= self.generate_prob_xk_of_prediction_phase(particle, length_ref)
            new_particle = self.generate_new_particle_prediction_phase(probs_x)
            S_prime_k[i]=new_particle

        return S_prime_k

    def update_phase(self, S_prime_k):
        weights_M_k = self.generate_weights_M_k(S_prime_k)
        return self.generate_new_set_of_particles_update_phase(weights_M_k)

    def generate_prob_xk_of_prediction_phase(self, particle,length_ref, length_side=1 ,step_size=0.1):
        """
        Here we are calculating the probability of being in a certain point knowing the resulting set of particles in the previous phase and
        not knowing the input at time k. This is the probability distribution that is calculated under the prediction phase of the paper.

       In order to calculate the probability, we do the following:
        Each particle '*' has an interval [a, b] centered around it. If an estimation position lands within the interval
        it receives a score relative to it's proximity to '*'. The score linearly decreases from the particle to the
        interval endpoints a and b. An illustration is provided below:

              |                    *
        score |                   / \
              |                  /   \
              |                 /     \
              |________________/_______\______________
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

        Returns
        -------
        A np array of dimensions [nr_steps in interval, where for each entry i,
                the first element [i][0] is a time point and the second element is the probability of selecting that time point.
                If the probability for a value is 0 there will be no entry for it
        """
        interval_nr_indices = int((length_side*2)/step_size)+1
        probs_x= np.zeros([interval_nr_indices , 2], dtype=float)

        start_second = max(0, particle- length_side)
        end_second = min(particle+ length_side, length_ref)

        slope = 1/length_side
        i=0
        for time in arange(start_second, particle, step_size): #first lenght of the interval
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

    def generate_new_particle_prediction_phase(self, probs_x):
        """
        Generates a new particle knowing the probabilities of x given a particle and the previous input. This is part of the prediction phase

        Parameters
        ----------
        probs_x: conditional probability of having a particle at state x calculated previously in this prediciton phase
                A np array of dimensions [step_size* 2*length_Side][2], where for each entry i,
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
            if random_limit>= prob:
                new_particle= probs_x[i][0]
                break

        return new_particle




    def generate_weights_M_k(self, S_prime_k):
        """
        For each particle calculates the probability of the observation given the particle.
        This is done in the following way:
            1. Use panako/hashing sliding window, to obtain a score for all the times in the song.
            2. Get the score given by 1 at the time of the particle, that would be the weight
            3. normalize all weights to add up to one

        Parameters
        ----------
        S_prime_k: set of particles calculated in prediction phase. 2d np array of floats

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
            weight= get_localization_score(time= particle) #TODO: integrate with panako part
            weight_list[i, 0]= weight

        #normalize scores
        weight_list[:,0]= weight_list[:,0]/sum(weight_list[:,0])
        return weight_list


    def generate_new_set_of_particles_update_phase(self, weights_M_k):
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
        while idx_random_sorted< len(random_sorted):
            random_sorted_value = random_sorted[idx_random_sorted]

            if idx_cumsum==0:#base case, done separately to avoid index out of bounds error
                if random_sorted_value <= cum_sum[idx_cumsum]:
                    new_particle = weights_M_k[idx_cumsum, 1]
                    new_set_particles[idx_random_sorted] = new_particle
                    idx_random_sorted+=1
                else:
                    idx_cumsum+=1
            else:

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
    weights_M_k= np.random.random((5,2))
    generate_new_set_of_particles_update_phase(weights_M_k)
