import hashlib
import cgi
import cgitb

cgitb.enable()

class Automaton(object):
    def __init__(self, rule):
        # store rule number as bitstring
        self.rule = '{:08b}'.format(rule)

    def transform(self, state):
        # store new state
        result = []

        # form new state
        for i in range(0, len(state)):
            # get surrounding bits
            left = state[(i-1) % len(state)]
            center = state[i]
            right = state[(i+1) % len(state)]

            # calculate result bit
            new_center = self.next_bit(left, center, right)

            # set new bit
            result.append(new_center)

        return result

    def transformFor(self, state, n):
        states = []
        states.append(state)
        for i in range(0, n):
            state = self.transform(state)
            states.append(state)

        return states

    def next_bit(self, left, center, right):
        # calculate index into bitstring
        index = 7 - (int(right) + 2*int(center) + 4*int(left))

        # check pattern
        return int(self.rule[index])

# get params
form = cgi.FieldStorage()
seed = int(hashlib.sha256(form['seed'].value.encode('utf-8')).hexdigest(), 16)
bits = int(form['bits'].value) % 33
count = int(form['count'].value) % 101

# init automaton
a = Automaton(30)
n = 255 # one bit less for odd window size
initial = [0] * n
for i in range(0, n):
    # bits of seed determine initial pattern
    initial[i] = (seed >> i) % 2

# accumulate results
results = []
for i in range(0, count):
    result = 0
    for j in range(0, bits):
        # transform row
        initial = a.transform(initial)
        # get middle bit
        result += initial[int(n/2)] * (2**j)
    results.append(result)

print('\n'.join([str(x) for x in results]))
