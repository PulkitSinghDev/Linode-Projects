from Maze import Maze
from PIL import Image
import StringIO
import random
import base64
import cgi
import cgitb

cgitb.enable()

form = cgi.FieldStorage()

rows = 55
cols = 110
iterations = 50

m = Maze(rows, cols)

pattern = form['initial'].value
if pattern == 'rand':
    for i in range(0, rows):
        for j in range(0, cols):
            m.set_cells(i, j, random.random() <= 0.5)
elif pattern == 'line1':
    for i in range(0, rows):
        m.set_cells(i, cols/2, True)
elif pattern == 'line2':
    for i in range(0, cols):
        m.set_cells(rows/2, i, True)

for i in range(0, iterations):
    m.simulate()

img = Image.new('L', (cols, rows))
if m.current:
    img.putdata([255*x for x in m.cells1])
else:
    img.putdata([255*x for x in m.cells2])
buf = StringIO.StringIO()
img.save(buf, 'PNG')

print(base64.b64encode(buf.getvalue()))