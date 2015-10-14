import math
import random
import cStringIO
import cgi
import cgitb
cgitb.enable()

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '({0}, {1})'.format(self.x, self.y)

# store best cost and network
best_cost = None
best_network = []

# define points
form = cgi.FieldStorage()
n = 40
try:
    n = int(form['size'].value)
except KeyError:
    pass
points = []
for i in range(0, n):
    x = random.random()
    y = random.random()
    points.append(Point(x, y))

# calculate cost of connection
def cost(p1, p2):
    return math.pow(p1.x-p2.x, 2) + math.pow(p1.y-p2.y, 2)

# generate optimal network
def generate(points):
    global best_cost

    best_cost = float('inf')
    # generate_best(points, {points[0]}, [], 0)
    generate_best_greedy(points)

def closest_pair_single(points):
    p, q = points[0], points[1]
    for p1 in points:
        for q1 in points:
            if p1 == q1:
                continue

            if cost(p1, q1) < cost(p, q):
                p, q = p1, q1

    return p, q

def closest_pair_double(points1, points2):
    p, q = random.sample(points1, 1)[0], random.sample(points2, 1)[0]
    for p1 in points1:
        for q1 in points2:
            if cost(p1, q1) < cost(p, q):
                p, q = p1, q1

    return p, q

def generate_best_greedy(points):
    global best_cost, best_network

    # stats
    best_cost = 0
    best_network = []
    # start from closest pair
    p, q = closest_pair_single(points)
    marked = { p, q }
    spoints = set(points)
    # as long as not all points have been marked
    while len(marked) < len(points):
        # find closest pair (p1, p2) where p1 in marked and p2 in points-marked
        p1, p2 = closest_pair_double(marked, spoints.difference(marked))

        # update cost
        best_cost += cost(p1, p2)

        # add point to marked
        marked.add(p2)
        # add connection
        best_network.append((p1, p2))

def generate_best(points, marked, current_network, current_cost):
    global best_cost, best_network

    # base case: network completed
    if len(marked) == len(points):
        # check cost
        if current_cost < best_cost:
            # update best cost and network
            best_cost = current_cost
            best_network = current_network[0:]
    else:
        # extend network
        for p1 in points:
            # check mark
            if p1 in marked:
                continue

            for p2 in marked:
                # calculate cost
                c = cost(p1, p2)

                # bounding criterion
                if best_cost is not None and current_cost + c >= best_cost:
                    continue

                # add connection to network
                current_network.append((p1, p2))
                # update cost
                current_cost += c
                # mark point
                marked2 = marked.copy()
                marked2.add(p1)
                # go deeper
                generate_best(points, marked2, current_network[0:], current_cost)
                # update cost
                current_cost -= c
                # remove connection from network
                current_network.pop()

# generate network and plot result
generate(points)
for p1, p2 in best_network:
    plt.plot([p1.x, p2.x], [p1.y, p2.y], color='k', linestyle='-', linewidth=2)
    plt.plot([p1.x, p2.x], [p1.y, p2.y], 'ro')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Network cost: {0}'.format(best_cost))

# export plot
format = "png"
sio = cStringIO.StringIO()
fig = plt.gcf()
fig.savefig(sio, format=format)
print("Content-Type: image/{0}\n".format(format))
print(sio.getvalue().encode("base64").strip())