#!/usr/bin/python

import os
import time
import configparser
import Operation_system_path as ops
import Choose_optimal_set_of_dimensions as choose_psd


def proclus():
    start = time.time()

    ######################################
    # Initialization phase with Map-Reduce
    ######################################

    # read config file with local path
    config = configparser.ConfigParser()
    config_file = ops.get_local_path('ConfigFile.ini')
    config.read(config_file)

    filtering_criterion = (int(config['DEFAULT']['DATA_SIZE']) / int(config['DEFAULT']['CLUSTER_NUMBER'])) * float(
        config['DEFAULT']['MIN_DEVIATION'])

    map_reduce_file = ops.get_local_path(config['FILES']['INITIALIZATION_PHASE'])
    data_file = ops.get_local_path(config['FILES']['DATA_FILE'])
    output_file = ops.get_local_path(config['FILES']['STARTING_MEDOIDS'])
    command = "python {} {} > {}".format(map_reduce_file, data_file, output_file)

    # Execute the command to start  Initialization phase
    os.system(command)

    starting_medoids = []
    current_medoids = []
    best_medoids = []
    best_objective = -1
    i = 0

    # Read the starting medoid from file
    file = ops.get_local_path(config['FILES']['STARTING_MEDOIDS'])
    with open(file) as medoids_file:
        for line in medoids_file:  # read rest of lines
            clean_line = line.replace('"', '')  # remove '"' from string
            clean_line = clean_line.replace('\t', '')  # remove '\t' from string
            value = [int(x) for x in clean_line.split(" ")]
            if i < int(config['DEFAULT']['CLUSTER_NUMBER']):
                current_medoids.append(value)
                i += 1
            else:
                starting_medoids.append(value)
    medoids_file.close()
    ops.write_file(config['FILES']['CURRENT_MEDOIDS'], current_medoids)
    termination_criterion = False
    termination_counter = 0
    while not termination_criterion:
        ######################################
        # Iterative phase with Map-Reduce
        ######################################
        map_reduce_file = ops.get_local_path(config['FILES']['OPTIMAL_SET_OF_DIMENSIONS'])
        data_file = ops.get_local_path(config['FILES']['DATA_FILE'])
        output_file = ops.get_local_path(config['FILES']['L_MEDOID_DATA'])
        command = "python {} {} > {}".format(map_reduce_file, data_file, output_file)

        # Execute the command to find OptimalSetOfDimensions with MapReduce
        os.system(command)

        # Choose the best set of dimensions
        choose_psd.choose_optimal_set_of_dimensions()
        # --------------------------------------------------------------
        map_reduce_file = ops.get_local_path(config['FILES']['ASSIGN_POINTS_EVALUATE_CLUSTERS'])
        output_file = ops.get_local_path(config['FILES']['CLUSTERS_DATA'])
        command = "python {} {} > {}".format(map_reduce_file, data_file, output_file)

        # Execute the command to AssignPoints and EvaluateClusters
        os.system(command)
        medoids = []
        weight = []
        clustered_data_length = []
        file = ops.get_local_path(config['FILES']['CLUSTERS_DATA'])
        with open(file) as cluster_data_file:
            for line in cluster_data_file:
                clean_line = line.replace('[', '')  # remove '[' from string
                clean_line = clean_line.replace(']', '')  # remove ']' from string
                clean_line = clean_line.replace('"', '')  # remove '"' from string
                read_input = clean_line.split('\t')
                parse_input = read_input[0].split("|")
                medoids.append([int(x) for x in parse_input[0].split(" ")])
                weight.append(float(parse_input[1]))
                clustered_data_length.append(int(parse_input[2]))
        cluster_data_file.close()
        objective_function = 0
        bad_medoids = []
        min_cluster = min(clustered_data_length)

        ###########################################
        #       Find Objective function           #
        ###########################################
        for j in range(int(config['DEFAULT']['CLUSTER_NUMBER'])):
            objective_function += weight[j]*clustered_data_length[j]

            ###########################################
            #       We assume that the medoids        #
            #       with the less point is bad        #
            ###########################################
            if clustered_data_length[j] == min_cluster:
                bad_medoids.append(medoids[j])
        objective_function = objective_function / int(config['DEFAULT']['DATA_SIZE'])


        ###########################################
        #       Determine the bad medoids         #
        ###########################################
        for j in range(int(config['DEFAULT']['CLUSTER_NUMBER'])):
            if filtering_criterion > clustered_data_length[j]:
                if medoids[j] not in bad_medoids:
                    bad_medoids.append(medoids[j])

        ###########################################
        #       Determine Mbest                   #
        ###########################################
        if objective_function < best_objective or best_objective == -1:
            best_objective = objective_function
            best_medoids = current_medoids
            termination_counter = 0
            termination_criterion = False
        else:
            termination_counter = termination_counter + 1
            if termination_counter >= int(config['DEFAULT']['MAX_ITERATIONS']):
                termination_criterion = True
        temp_medoids = current_medoids
        current_medoids = []
        ###########################################
        #       Create a new Mcurrent             #
        ###########################################
        if not termination_criterion:
            for x in temp_medoids:
                if x not in bad_medoids:
                    current_medoids.append(x)
            for x in bad_medoids:
                if x not in starting_medoids:
                    starting_medoids.append(x)
            temp_medoids = []
            while len(current_medoids) < int(config['DEFAULT']['CLUSTER_NUMBER']):
                added_medoid = starting_medoids.pop(0)
                if added_medoid not in current_medoids:
                    current_medoids.append(added_medoid)
                temp_medoids.append(added_medoid)
        ops.write_file(config['FILES']['CURRENT_MEDOIDS'], current_medoids)

    ######################################
    # Refinement phase with Map-Reduce
    ######################################
    ops.write_file(config['FILES']['CURRENT_MEDOIDS'], best_medoids)

    map_reduce_file = ops.get_local_path(config['FILES']['OPTIMAL_SET_OF_DIMENSIONS'])
    data_file = ops.get_local_path(config['FILES']['DATA_FILE'])
    output_file = ops.get_local_path(config['FILES']['L_MEDOID_DATA'])
    command = "python {} {} > {}".format(map_reduce_file, data_file, output_file)

    # Execute the command to find OptimalSetOfDimensions
    os.system(command)

    # Choose the best set of dimensions
    choose_psd.choose_optimal_set_of_dimensions()
    # --------------------------------------------------------------
    map_reduce_file = ops.get_local_path(config['FILES']['ASSIGN_POINTS'])
    output_file = ops.get_local_path(config['FILES']['FINAL_CENTROIDS'])
    command = "python {} {} > {}".format(map_reduce_file, data_file, output_file)

    # Execute the command to AssignPoints and EvaluateClusters
    os.system(command)

    dimensions_per_medoid = {}
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
            dimensions_per_medoid[str_medoid] = dimensions
    dimensions_per_medoid_file.close()

    file_best_medoid = ops.get_local_path(config['FILES']['BEST_MEDOIDS'])
    with open(file_best_medoid, "w") as best_medoid_file:
        for medoid in best_medoids:
            best_medoid_file.write("%s\n" % medoid)
    best_medoid_file.close()
    file_final_dimensions = ops.get_local_path(config['FILES']['FINAL_DIMENSIONS'])
    with open(file_final_dimensions, "w") as best_final_dimensions:
        for key in dimensions_per_medoid.keys():
            best_final_dimensions.write("%s\n" % dimensions_per_medoid[key])
    best_final_dimensions.close()
    end = time.time()
    print("\nExecution time: " + str(end - start) + "\n")


if __name__ == '__main__':
    proclus()
