# manhattan_segmental_dist
# distance function
#   x1: set of multi-dimension coordinates
#   x2: set of multi-dimension coordinates
#   d: set of the dimensions that we need to calculate the distance
# returns
#   the manhattan segmental distance
def manhattan_segmental_dist(x1, x2, d):
    summation = 0
    for i in range(0, len(d)):
        # We need the absolute value of the difference of the two points
        summation = summation + abs(x1[d[i]] - x2[d[i]])
    #
    summation = summation / len(d)
    return summation
