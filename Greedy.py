import random
import Manhattan_segmental_dist


# Greedy
#   s: dictionary of points
#   k: number of medoids
# returns
#   k medoids from sample set s
def greedy(s, k):
    # print("Hello Word!")
    m_1 = random.choice(list(s.keys()))
    medoids = {m_1: s[m_1]}
    dimensions = list(range(len(s[m_1])))
    s.pop(m_1)
    dist = {}
    # compute distance between each point and medoid m1
    for x in s:
        dist[x] = Manhattan_segmental_dist.manhattan_segmental_dist(medoids[m_1], s[x], dimensions)
    for i in range(1, k):
        m_i = max(dist, key=lambda x: dist.get(x))
        medoids[m_i] = s[m_i]
        dist.pop(m_i)
        s.pop(m_i)
        for x in s:
            dist[x] = min(dist[x], Manhattan_segmental_dist.manhattan_segmental_dist(medoids[m_i], s[x], dimensions))
    return medoids
