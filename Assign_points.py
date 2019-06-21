from mrjob.job import MRJob
from mrjob.step import MRStep
import Operation_system_path as ops
import configparser
import Manhattan_segmental_dist


class RefinementPhase(MRJob):
    MRJob.SORT_VALUES = True

    def steps(self):
        return [
            MRStep(mapper_init=self.init,
                   mapper=self.mapper,
                   reducer_init=self.init,
                   reducer=self.reducer)
        ]

    def init(self):
        # read config file with local path
        config = configparser.ConfigParser()
        config_file = ops.get_local_path('ConfigFile.ini')
        config.read(config_file)

        self.dimensions_per_medoid = {}

        file = ops.get_local_path(config['FILES']['L_MEDOID_DATA'])
        with open(file) as dimensions_per_medoid_file:
            for line in dimensions_per_medoid_file:
                clean_line = line.replace('[', '')  # remove '[' from string
                clean_line = clean_line.replace(']', '')  # remove ']' from string
                clean_line = clean_line.replace(' | ', '')  # remove '|' from string
                clean_line = clean_line.replace('"', '')  # remove '"' from string
                read_input = clean_line.split(' \', ')
                medoid = read_input[0]
                medoid = medoid.replace('\'', '')
                dimensions = [int(x) for x in read_input[1].split(",")]
                str_medoid = ''.join(medoid)
                self.dimensions_per_medoid[str_medoid] = dimensions
        dimensions_per_medoid_file.close()

    def mapper(self, _, line):
        data_readed = [int(axes) for axes in line.split('\t')]
        min_distance = -1
        key = 0
        # compute the manhattan distance for each medoid with the point that read the mapper
        for medoid, dimensions in self.dimensions_per_medoid.items():
            medoid_int = [int(x) for x in medoid.split(" ")]
            dist = Manhattan_segmental_dist.manhattan_segmental_dist(data_readed, medoid_int, dimensions)
            # if we find the closet medoid for this cluster we save it to return it later with the point
            if min_distance > dist or min_distance == -1:
                min_distance = dist
                key = medoid

        yield key, data_readed

    def reducer(self, key, dataset):
        centroid_sum = [0] * len(self.dimensions_per_medoid[key])
        centroid = [0] * len(self.dimensions_per_medoid[key])
        dataset_length = 0
        # we calculate the centroid of the cluster
        for data in dataset:
            i = 0
            for dimension in self.dimensions_per_medoid[key]:
                centroid_sum[i] = centroid_sum[i] + data[dimension]
                i = i + 1
            yield key, data
            dataset_length = dataset_length + 1
        number_of_dimensions = len(self.dimensions_per_medoid[key])
        # we return a negative value because we order the output so the next reducer will know this information
        for i in range(0, number_of_dimensions):
            centroid[i] = -centroid_sum[i] / dataset_length
        yield key, centroid


if __name__ == '__main__':
    RefinementPhase.run()
