class Maze(object):
    def __init__(self, rows, cols):
        # store dimensions
        self.rows = rows
        self.cols = cols

        # store cells as double buffer
        self.cells1 = [0] * rows * cols
        self.cells2 = self.cells1[0:]
        self.current = True

    def get_index(self, row, col):
        # resolve (row, col) to index
        return (row % self.rows)*self.cols + (col % self.cols)

    def set_cells(self, row, col, val):
        index = self.get_index(row, col)
        self.cells1[index] = self.cells2[index] = val

    def get_current_cell(self, row, col):
        # get cell value
        index = self.get_index(row, col)
        if self.current:
            return self.cells1[index]
        else:
            return self.cells2[index]

    def set_other_cell(self, row, col, val):
        # set cell value
        index = self.get_index(row, col)
        if not self.current:
            self.cells1[index] = val
        else:
            self.cells2[index] = val

    def simulate(self):
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                # store new value (default dead)
                new_value = False

                # get neighbors
                values = []
                count = 0
                for d1 in range(-1, 2):
                    for d2 in range(-1, 2):
                        if i+d1 < 0 or i+d1 >= self.rows or j+d2 < 0 or j+d2 >= self.cols:
                            v = False
                        else:
                            v = self.get_current_cell(i+d1, j+d2)
                        values.append(v)

                        if v and len(values) != 5:
                            count += 1

                # check birth
                if not values[4] and count == 3:
                    new_value = True
                # check survival
                elif values[4] and 1 <= count < 5:
                    new_value = True
                # fix patterns
                if values[4]:
                    if values[0] and not values[1] and values[2]:
                        new_value = False
                    if values[6] and not values[7] and values[8]:
                        new_value = False
                    if values[0] and not values[3] and values[6]:
                        new_value = False
                    if values[2] and not values[5] and values[8]:
                        new_value = False

                # set new value
                self.set_other_cell(i, j, new_value)

        # swap buffers
        self.current = not self.current

    def __repr__(self):
        s = ''
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                k = '#'
                if self.get_current_cell(i, j):
                    k = ' '
                s = '{0}{1}'.format(s, k)
            s = '{0}\n'.format(s)

        return s