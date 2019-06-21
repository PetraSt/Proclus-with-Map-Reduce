#! /usr/bin/python

from mrjob.job import MRJob
from mrjob.step import MRStep
import math
import operator
import Operation_system_path as ops
import configparser
import Manhattan_segmental_dist


class IterativePhase(MRJob):

    def steps(self):
        return [
            MRStep(mapper_init=self.mapper_init,
                   mapper=self.mapper,
                   reducer=self.reducer)
        ]

    # Initialize variables and calculate the minimum delta distance between medoids
    def mapper_init(self):
        # read config file with local path
        self.config = configparser.ConfigParser()
        config_file = ops.get_local_path('ConfigFile.ini')
        self.config.read(config_file)

        self.medoids_min_delta_distance = {}
        number_of_dimensions = 0
        # Read the starting medoids from file
        file = ops.get_local_path(self.config['FILES']['CURRENT_MEDOIDS'])
        with open(file) as medoids_file:
            i = 0
            for line in medoids_file:  # read rest of lines
                clean_line = line.replace('[', '')  # remove '[' from string
                clean_line = clean_line.replace(']', '')  # remove ']' from string
                value = [int(x) for x in clean_line.split(",")]
                self.medoids_min_delta_distance[tuple(value)] = 0
                number_of_dimensions = len(value)
                i += 1
        medoids_file.close()

        dimensions = list(range(number_of_dimensions))

        # Calculate the minimum delta distance between medoids
        for medoid_key in self.medoids_min_delta_distance:
            for key in self.medoids_min_delta_distance:
                if medoid_key != key:
                    distance = Manhattan_segmental_dist.manhattan_segmental_dist(medoid_key, key, dimensions)
                    if self.medoids_min_delta_distance[medoid_key] == 0 or self.medoids_min_delta_distance[medoid_key] > distance:
                        self.medoids_min_delta_distance[medoid_key] = distance

    def mapper(self, _, line):
        data_point = [int(axes) for axes in line.split('\t')]
        dimensions = list(range(len(data_point)))

        # Find all the medoids the point belongs to
        for medoid_key in self.medoids_min_delta_distance:
            distance = Manhattan_segmental_dist.manhattan_segmental_dist(medoid_key, data_point, dimensions)

            # A point belongs to a medoid if the distance between the medoid and the point
            # is smaller or equal to the minimum delta distance of the medoid
            if distance <= self.medoids_min_delta_distance[medoid_key]:
                key_str = ""
                for axe in medoid_key:
                    if key_str == "":
                        key_str = str(axe)
                    else:
                        key_str = key_str + " " + str(axe)
                yield key_str, data_point

    def reducer(self, key, dataset):
        config = configparser.ConfigParser()
        config_file = ops.get_local_path('ConfigFile.ini')
        config.read(config_file)
        avg_dimension_distance_X = ""   # medoid's average distance for each dimension
        date_count = 0
        for data in dataset:
            # create a list of zeroes with the length of the axes
            if avg_dimension_distance_X == "":
                avg_dimension_distance_X = [0] * len(data)
            # sum the distance of each point for each of its dimensions
            for i in range(len(data)):
                avg_dimension_distance_X[i] += data[i]
            date_count += 1

        mean_Y = 0  # medoid's dimension mean
        standard_deviation_S = 0    # medoid's standard deviation
        correlation_of_dimensions_Z = {}

        # compute the avg distance for each dimension
        for i in range(len(avg_dimension_distance_X)):
            avg_dimension_distance_X[i] = avg_dimension_distance_X[i]/date_count
            # sum the avg distance of each dimension
            mean_Y += avg_dimension_distance_X[i]

        # compute the medoid's mean
        mean_Y = mean_Y / len(avg_dimension_distance_X)

        # sum the square for each dimension
        for avg_dist in avg_dimension_distance_X:
            standard_deviation_S += (avg_dist - mean_Y)**2

        # Division with the dimension number sub track one
        standard_deviation = standard_deviation_S/(int(config['DEFAULT']['DIMENSION'])-1)

        # Calculate the square
        standard_deviation = math.sqrt(standard_deviation)

        # Calculate the correlation of each dimension with the medoid
        for i in range((int(config['DEFAULT']['DIMENSION']))):
            correlation_of_dimensions_Z[i] = (avg_dimension_distance_X[i] - mean_Y)/standard_deviation

        # Sort the list in ascending order
        correlation_of_dimensions_Z = sorted(correlation_of_dimensions_Z.items(), key=operator.itemgetter(1))
        return_value = " | " + str(correlation_of_dimensions_Z)
        yield key, return_value
