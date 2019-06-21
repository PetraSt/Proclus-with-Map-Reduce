import Operation_system_path as ops
import configparser

config = configparser.ConfigParser()
config_file = ops.get_local_path('ConfigFile.ini')
config.read(config_file)


def create_structures():
    final_data_file_path = ops.get_local_path(config['FILES']['FINAL_CENTROIDS'])
    medoid_file_path = ops.get_local_path(config['FILES']['BEST_MEDOIDS'])

    medoid_with_centroid = {}
    data_with_medoid = {}
    medoid_with_cluster = {}
    i = 0
    j = 0
    with open(final_data_file_path) as final_data:
        for line in final_data:
            line = line.replace("\"", "")
            line = line.replace("\n", "")
            line = line.replace("[", "")
            line = line.replace("]", "")
            line = line.split("\t")

            part0 = line[0].replace(" ", "\t")
            part1 = line[1].replace(", ", "\t")
            if "-" in part1:
                medoid_with_centroid[part0] = part1
                j += 1
            else:
                data_with_medoid[part1] = part0
                i += 1
    with open(medoid_file_path) as medoid_file:
        for line in medoid_file:
            line = line.replace("\n", "")
            line = line.replace("[", "")
            line = line.replace("]", "")
            line = line.replace(", ", "\t")
            medoid_with_cluster[line] = [0] * (int(config['DEFAULT']['CLUSTER_NUMBER']) + 1)
    medoid_file.close()

    return medoid_with_centroid, data_with_medoid, medoid_with_cluster


def calculate_accuracy_better_approach():
    data_file_path = ops.get_local_path(config['FILES']['DATA_FILE'])
    cluster_file_path = ops.get_local_path(config['FILES']['DATA_FILE_CLUSTERS'])

    data_list = []
    cluster_list = []
    original_data_with_clusters = {}

    with open(data_file_path) as data_file:  # read data file
        for data_line in data_file:
            data_line = data_line.replace("\n", "")
            data_list.append(data_line)
    data_file.close()

    with open(cluster_file_path) as cluster_file:
        for cluster_str in cluster_file:  # read every data line
            cluster_str = cluster_str.replace("\n", "")
            cluster_list.append(cluster_str)
    cluster_file.close()

    for i in range(0, len(data_list)):
        original_data_with_clusters[data_list[i]] = cluster_list[i]

    cluster_data_original = [0] * (int(config['DEFAULT']['CLUSTER_NUMBER']) + 1)
    medoid_with_centroid, data_with_medoid, medoid_with_cluster = create_structures()

    for datum in data_list:
        cluster = original_data_with_clusters[datum]
        m_data = data_with_medoid[datum]
        medoid_with_cluster[m_data][int(cluster)] += 1
        cluster_data_original[int(cluster)] += 1

    # clean confusion matrix
    for key, value in medoid_with_cluster.items():
        medoid_with_cluster[key].pop(0)
    cluster = ""
    # create header
    for i in range(0, int(config['DEFAULT']['CLUSTER_NUMBER'])):
        if cluster == "":
            cluster = "\t\t" + chr(65)
        else:
            cluster = cluster + "  " + chr(65 + i)

    wrong = 0
    correct = 0
    cluster_data_original.pop(0)
    print("-------------------- Confusion Matrix ---------------------")
    print(cluster)
    i = 0
    for key, value in medoid_with_cluster.items():
        count = 0
        for j in value:
            count += j
        if count > cluster_data_original[i]:
            wrong += count - cluster_data_original[i]
            correct += cluster_data_original[i]
        else:
            correct += count

        print(" {}\t| {} |{}".format(chr(65 + i), value, count))
        i += 1

    line = ""
    for cluster in cluster_data_original:
        if line == "":
            line = "\t  " + str(cluster)
        else:
            line = line + " " + str(cluster)
    print(line)

    print("GREEDY_1: {}".format(config['DEFAULT']['GREEDY_1']))
    print("GREEDY_2: {}".format(config['DEFAULT']['GREEDY_2']))
    print("GREEDY_2: {}".format(config['DEFAULT']['GREEDY_2']))
    print("MIN_DEVIATION: {}".format(config['DEFAULT']['MIN_DEVIATION']))
    print("AVG_DIMENSION: {}".format(config['DEFAULT']['AVG_DIMENSION']))
    print("DIMENSIONS: {}\n".format(config['DEFAULT']['DIMENSION']))
    print("wrong: {}".format(wrong))
    print("correct: {}".format(correct))
    print("total: {}".format(config['DEFAULT']['DATA_SIZE']))
    print("accuracy: {}%".format((correct / int(config['DEFAULT']['DATA_SIZE'])) * 100))


calculate_accuracy_better_approach()

