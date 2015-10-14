import random
import cgi
import cgitb
import sys
cgitb.enable()

form = cgi.FieldStorage()
n = int(form['n'].value)
if n < 4 or n > 10:
    print(''.join(['0' * 8]))
    sys.exit(0)

board = [0 for i in range(0, n*n)]
sols = []

def set_cell(row, col, val):
    board[n*(row % n) + (col % n)] = val

def get_cell(row, col):
    return board[n*(row % n) + (col % n)]

def is_safe(row, col):
    # checking rows is superfluous since we will only place one queen per row
    # column only needs to be checked up to current row
    for i in range(0, row):
        if get_cell(i, col) == 1:
            return False
    # check diagonals
    for i in range(0, n):
        crow = row-i
        ccol = col-i
        if crow < 0 or ccol < 0:
            break
        if get_cell(crow, ccol) == 1:
            return False
    for i in range(0, n):
        crow = row-i
        ccol = col+i
        if crow < 0 or ccol >= n:
            break
        if get_cell(crow, ccol) == 1:
            return False
    # all clear
    return True

def place_queen(row):
    if row >= n:
        sols.append(board[0:])
    else:
        for i in range(0, n):
            if is_safe(row, i):
                set_cell(row, i, 1)
                place_queen(row+1)
                set_cell(row, i, 0)

place_queen(0)
sol = sols[random.randrange(0, len(sols))]
print(''.join([str(cell) for cell in sol]))