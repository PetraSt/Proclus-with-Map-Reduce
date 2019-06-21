import configparser
import Operation_system_path as ops


def choose_optimal_set_of_dimensions():
    config = configparser.ConfigParser()
    config_file = ops.get_local_path('ConfigFile.ini')
    config.read(config_file)

    medoid = []
    medoid_dimensions = []
    file = ops.get_local_path(config['FILES']['L_MEDOID_DATA'])
    with open(file) as l_medoid_data_file:
        for line in l_medoid_data_file:

            line = line.replace('"', '')  # remove '"' from string
            line = line.replace('\t', '')  # remove '\t' from string
            line = line.split('|')  # get the medoid
            medoid.append([line[0], []])
            line = line[1].split('\n')
            medoid_dimensions.append(line)
    l_medoid_data_file.close()

    # Calculate the number of medoids that are going to be returned
    # Minimum 2 dimensions for its medoid must be returned
    num_of_return_dimensions = int(config['FILES']['CLUSTER_NUMBER']) * int(config['FILES']['AVG_DIMENSION'])
    num_of_return_dimensions -= int(config['FILES']['CLUSTER_NUMBER']) * 2

    for i in range(0, len(medoid_dimensions)):
        medoid_dimensions[i] = medoid_dimensions[i][0]
        medoid_dimensions[i] = medoid_dimensions[i].replace("(", "")
        medoid_dimensions[i] = medoid_dimensions[i].replace(" [", "")
        medoid_dimensions[i] = medoid_dimensions[i].split("),")

        first_dimension = medoid_dimensions[i].pop(0)
        first_dimension = first_dimension.split(",")
        medoid[i][1].append(int(first_dimension[0]))

        first_dimension = medoid_dimensions[i].pop(0)
        first_dimension = first_dimension.split(",")
        medoid[i][1].append(int(first_dimension[0]))

    while num_of_return_dimensions > 0:
        m_num = 0
        min_value = 0
        m_dimensions = 0

        for i in range(0, len(medoid_dimensions)):
            if len(medoid_dimensions[i]) > 0:

                first_dimension = medoid_dimensions[i][0].replace(")", "")
                first_dimension = first_dimension.replace("]", "")
                first_dimension = first_dimension.split(",")
                if min_value == 0 or min_value > float(first_dimension[1]):
                    m_num = i
                    min_value = float(first_dimension[1])
                    m_dimensions = int(first_dimension[0])

        medoid_dimensions[m_num].pop(0)
        medoid[m_num][1].append(m_dimensions)
        num_of_return_dimensions -= 1

    ops.write_file(config['FILES']['L_MEDOID_DATA'], medoid)