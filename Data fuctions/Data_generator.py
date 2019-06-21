# It creates a file with a dataset that has a specific number of clusters
#
# Input parameters: None
# Return value: None

import random
import os

DIMENSIONS = 20
POINTS = 1000
CLUSTERS = 3
SIZE = 30
SPACE = 10


def main():
    file_name = os.getcwd() + "\\dataset_CP" + str(POINTS) + "_D" + str(DIMENSIONS) + "_C" + str(CLUSTERS) + ".txt"
    f = open(file_name, "w+")

    # create data points
    for i in range(0, POINTS):
        data_point = ""
        for j in range(0, DIMENSIONS):
            if data_point == "":
                data_point = str(random.randint(0, 35))
            else:
                data_point += "\t" + str(random.randint(0, 35))
        data_point += "\n"
        f.write(data_point)

        data_point = ""
        for j in range(0, DIMENSIONS):
            if data_point == "":
                data_point = str(random.randint(65, 100))
            else:
                data_point += "\t" + str(random.randint(65, 100))
        data_point += "\n"
        f.write(data_point)

        data_point = ""
        lower = 0
        upper = 0
        for j in range(0, DIMENSIONS):
            if j%2 == 0:
                lower = 65
                upper = 100
            else:
                lower = 0
                upper = 35
            if data_point == "":
                data_point = str(random.randint(lower, upper))
            else:
                data_point += "\t" + str(random.randint(lower, upper))
        data_point += "\n"
        f.write(data_point)
    f.close()


if __name__ == "__main__":
    main()
