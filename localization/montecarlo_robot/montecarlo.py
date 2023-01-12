import random
from numpy import arange
import numpy as np
def create_initial_set_of_particles(nr_particles, length_ref_subset):
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

def prediction_phase(S_k_minus_1):
    for i in range(len(S_k_minus_1)):
        particle = S_k_minus_1[i]
        probs_x= generate_prob_xk_of_prediction_phase(particle)
        generate_new_particle_prediction_phase()

def update_phase():
    generate_weights_m_i_k()
    generate_new_set_of_particles_update_phase()

def generate_prob_xk_of_prediction_phase(particle,length_side ,length_ref,step_size=0.1):
    """
    Here we are calculating the probability of being in a certain point knowing the resulting set of particles in the previous phase and
    not knowing the input at time k. This is the probability distribution that is calculated under the prediction phase of the paper. 
    
    In order to calculate the probability, we do the following:
    Each particle has an associated interval for which there is a score. The particle is centered at the beggining of the interval and the score
    throughout the interval decreases linearly. Here is an example:

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

    print(sum(probs_x[:,1]))
    #now we normalize the probability
    probs_x[:,1] /=sum(probs_x[:,1])
    print(sum(probs_x[:,1]))
    return probs_x

def generate_new_particle_prediction_phase(probs_x):
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
    return ""




def generate_weights_m_i_k():
    return "implement"

def generate_new_set_of_particles_update_phase():
    return "implement"

if __name__ == '__main__':
    (generate_prob_xk_of_prediction_phase(particle=5, length_side=3, length_ref=10, step_size=0.1))
