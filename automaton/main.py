import cgi
import cgitb
from PIL import Image
import random
import StringIO
import base64

cgitb.enable()
width = 640
height = 480

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

def to_image(states):
    global width, height

    img = Image.new('L', (width, height))
    img.putdata(states)

    buf = StringIO.StringIO()
    img.save(buf, 'PNG')

    return base64.b64encode(buf.getvalue())

form = cgi.FieldStorage()

n = int(form['rule'].value)
k = form['initial'].value

initial = []
if k == 'single':
    initial = [0] * width
    initial[int(width)/2] = 1
else:
    for i in range(0, width):
        initial.append(random.randrange(0, 2))

a = Automaton(n)
s = a.transformFor(initial, height-1)
pixels = []
for state in s:
    for b in state:
        pixels.append(255*b)

print(to_image(pixels))