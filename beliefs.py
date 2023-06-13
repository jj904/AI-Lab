
"""
Module to track the belief distribution over all possible grid positions

Your task for homework 8 is to implement:
1.  update
2.  recommend_sensing
"""
import utils

class Belief(object):

    """
    Belief class used to track the belief distribution based on the
    sensing evidence we have so far.
    Arguments:
    size (int): the number of rows/columns in the grid

    Attributes:
    open (list of tuples): list containing all the positions that have not
        been observed so far.
    current_distribution (dictionary): probability distribution based on
        the evidence observed so far.
        The keys of the dictionary are the possible grid positions
        The values represent the (conditional) probability that the
        treasure is found at that position given the evidence
        (sensor data) observed so far.
    """

    def __init__(self, size):
        # Initially all positions are open - have not been observed
        self.open = [(x, y) for x in range(size)
                     for y in range(size)]
        # Initialize to a uniform distribution
        self.current_distribution = {pos: 1 / (size ** 2) for pos in self.open}


    def update(self, color, sensor_position, model):
        """
        Update the belief distribution based on new evidence:  our agent
        detected the given color at sensor location: sensor_position.
        :param color: (string) color detected
        :param sensor_position: (tuple) position of the sensor
        :param model (Model object) models the relationship between the
             treasure location and the sensor data
        :return: None
        """
        # Iterate over ALL positions in the grid and update the
        # probability of finding the treasure at that position - given
        # the new evidence.
        # The probability of the evidence given the Manhattan distance
        # to the treasure is given by calling model.pcolorgivendist.
        # Don't forget to normalize.
        # Don't forget to update self.open since sensor_position has
        # now been observed.

        for pos in self.current_distribution:
            distance = utils.manhattan_distance(pos,sensor_position)
            # P(C|T) probability of the given sonar color given the distance
            pct = model.pcolorgivendist(color, distance)
            self.current_distribution[pos] *= pct

        # normalize
        # Add the products computed for all pos
        sum_of_probs = sum(self.current_distribution.values())
        # divide each value by the sum computed above
        for pos in self.current_distribution:
            self.current_distribution[pos] /= sum_of_probs
        # test normalization
        # print("should add up to be 1:", sum(self.current_distribution.values()))

        # Update self.open since sensor_position has now been observed
        if sensor_position in self.open:
            self.open.remove(sensor_position)

    def recommend_sensing(self):
        """
        Recommend where we should take the next measurement in the grid.
        The position should be the most promising unobserved location.
        If all remaining unobserved locations have a probability of 0,
        return the unobserved location that is closest to the (observed)
        location with he highest probability.
        If there are no remaining unobserved locations return the
        (observed) location with the highest probability.

        :return: tuple representing the position where we should take
            the next measurement
        """
        # Enter your code and remove the statement below
        # Highest probability in observed positions
        observed_probs = {}
        for pos in self.current_distribution:
            if pos not in self.open:
                observed_probs[pos] = self.current_distribution[pos]

        max_observed = max(observed_probs, key=lambda pos: observed_probs[pos])

        # Highest probability in unobserved position
        unobserved_probs = {}
        if len(self.open) > 0:
            for pos in self.open:
                unobserved_probs[pos] = self.current_distribution[pos]
            max_unobserved = max(unobserved_probs, key=lambda pos: unobserved_probs[pos])

        if len(self.open) > 0:  # if there ARE remaining unobserved locations
            # if all remaining unobserved locations have a probability of 0,
            # return the unobserved location that is closest to the location
            # with the highest probability
            if all(probs == 0 for probs in unobserved_probs.values()):
                return utils.closest_point(max_observed, self.open)
            else:  # the most promising unobserved location
                return max_unobserved
        else:  # no remaining unobserved locations, return the location with the highest probability
            return max_observed
