#! /usr/bin/python

from mrjob.job import MRJob
from mrjob.step import MRStep
import Operation_system_path as ops
import configparser
import random
import Greedy


class InitializationPhase(MRJob):

    def steps(self):
        return [
            MRStep(mapper_init=self.mapper_init,
                   mapper=self.mapper,
                   mapper_final=self.mapper_final,
                   reducer=self.reducer)
        ]

    # Initialize variables
    def mapper_init(self):
        self.id = 0
        self.data_set = {}

    # Allow a percentage of the data through
    def mapper(self, _, line):
        change = random.randint(1, 100)
        # Change to pass through equals to  A*(medoids_number)
        if change <= 100:
            self.data_set[self.id] = [int(axes) for axes in line.split('\t')]
            self.id += 1    # count the data points that pass through

    # Yield only the points that the greedy will produce
    def mapper_final(self):
        config = configparser.ConfigParser()
        config_file = ops.get_local_path('ConfigFile.ini')
        config.read(config_file)
        yield 1, Greedy.greedy(self.data_set, int(config['DEFAULT']['GREEDY_1']))

    def reducer(self, key, dataset):
        config = configparser.ConfigParser()
        config_file = ops.get_local_path('ConfigFile.ini')
        config.read(config_file)
        i = 0
        data_set = {}
        # Prepare the data for the greedy
        for data in dataset:
            i += 1
            for axe in data:
                data_set[i] = data[axe]
                i += 1
        medoids = Greedy.greedy(data_set, int(config['DEFAULT']['GREEDY_2']))

        # Yield all the medoids
        for medoid in medoids.values():
            data_str = ""
            for axe in medoid:
                if data_str == "":
                    data_str = str(axe)
                else:
                    data_str = data_str + " " + str(axe)

            yield "", data_str


