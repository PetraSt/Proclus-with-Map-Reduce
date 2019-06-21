# The purpose of this file is to plot the given data and the medoids that are provided to it.
# No files are created.
#
# Input parameters: None
# Return value: None

import matplotlib.pyplot as plt
import csv
import os

x = []
y = []

# with open(os.getcwd() + '\\Data\\test_small.txt', 'r') as csv_file:
with open(os.getcwd() + '\\test_small.txt', 'r') as csv_file:
    plots = csv.reader(csv_file, delimiter='\t')
    for row in plots:
        x.append(int(row[0]))
        y.append(int(row[1]))
x1 = []
y1 = []
# with open('./Data/medoids_small.txt', 'r') as csv_file:
with open('./medoids_small.txt', 'r') as csv_file:
    plots = csv.reader(csv_file, delimiter='\t')
    for row in plots:
        x1.append(int(row[0]))
        y1.append(int(row[1]))

plt.plot(x, y, 'ro', label='Data points')
plt.plot(x1, y1, 'bo', label='Medoids')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Data plot')
plt.legend()
plt.show()
