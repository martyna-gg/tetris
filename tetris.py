import numpy as np
import random

global decision_letter
decision_grid = [10, input("select the number of rows ")]

left_border = [x * int(decision_grid[0]) for x in range(0, int(decision_grid[1]))]
right_border = [x * int(decision_grid[0]) - 1 for x in range(1, int(decision_grid[1]) + 1)]
bottom = [int(decision_grid[1]) * int(decision_grid[0]) - x for x in range(1, int(decision_grid[0]) + 1)]
top = [x for x in range(0, int(decision_grid[0]))]


def grid_reset():
    global grid
    grid = np.array(['-'] * int(decision_grid[0]) * int(decision_grid[1]))


def grid_print():
    print()
    for x in range(int(decision_grid[1])):
        print(' '.join(map(str, np.reshape(grid, (int(decision_grid[1]), int(decision_grid[0])))[x])))
    print()


def break_line():
    global grid
    new_grid = []
    for x in range(int(decision_grid[1])):
        if all([a == '0' for a in np.reshape(grid, (int(decision_grid[1]), int(decision_grid[0])))[x]]):
            new_grid = ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'] + new_grid
        else:
            new_grid = new_grid + list(np.reshape(grid, (int(decision_grid[1]), int(decision_grid[0])))[x])
    grid = np.array(new_grid)
    grid_print()


grid_reset()
grid_print()


letters = {'O': [[4, 14, 15, 5]],
'I': [[4, 14, 24, 34], [3, 4, 5, 6]],
'S': [[5, 4, 14, 13], [4, 14, 15, 25]],
'Z': [[4, 5, 15, 16], [5, 15, 14, 24]],
'L': [[4, 14, 24, 25], [13, 14, 15, 23], [3, 4, 14, 24], [5, 13, 14, 15]],
'J': [[4, 14, 24, 23], [3, 13, 14, 15], [4, 5, 14, 24], [13, 14, 15, 25]],
'T': [[4, 14, 24, 15], [13, 14, 15, 24], [4, 14, 24, 13], [4, 13, 14, 15]]}


class Letter:
    def __init__(self):
        self.name = decision_letter
        self.coordinates = letters[self.name].copy()
        self.position = self.coordinates[0]

    def print_position(self):
        for x in self.position:
            grid[x] = '0'
        grid_print()

    def check_bottom(self):
        if any([(x in self.coordinates[0]) for x in bottom]):
            return False
        elif any([(grid[x + int(decision_grid[0])] == '0' and x + int(decision_grid[0]) not in self.position) for x in self.position]):
            return False
        else:
            return True
        
    def check_right(self):
        if any([(x in self.coordinates[0]) for x in right_border]):
            return False
        elif any([(grid[x + 1] == '0' and x + 1 not in self.position) for x in self.position]):
            return False
        else:
            return True
        
    def check_left(self):
        if any([(x in self.coordinates[0]) for x in left_border]):
            return False
        elif any([(grid[x - 1] == '0' and x - 1 not in self.position) for x in self.position]):
            return False
        else:
            return True
        
    def check_right_rotate(self):
        if any([(x - 1 in self.coordinates[0]) for x in right_border]):
            return False
        elif any([(grid[x + 2] == '0' and x + 2 not in self.position) for x in self.position]):
            return False
        else:
            return True
        
    def check_rotate(self):
        if any([(x in self.coordinates[1]) for x in left_border]) and any([(x in self.coordinates[1]) for x in right_border]):
            return False
        elif any([(grid[x] == '0' and x not in self.position) for x in self.coordinates[1]]):
            return False
        else:
            return True

    def down(self):
        if self.check_bottom():
            self.coordinates = list([map(lambda x: x + 10, self.coordinates[y]) for y in range(len(self.coordinates))])
            self.coordinates = [list(self.coordinates[x]) for x in range(len(self.coordinates))]
            for x in self.position:
                grid[x] = '-'
            self.position = self.coordinates[0]
            self.print_position()
        else:
            self.print_position()
            decision = input("select e for exit, p for new piece, d for down, rt for rotate, l for left, r for right or b for break ") #tutaj trzeba zablokować następny ruch!

    def rotate(self):
        if self.check_bottom():
            if not self.check_left():
                if not self.check_rotate():
                    if self.check_right():
                        self.coordinates = list([map(lambda x: x + 1, self.coordinates[y]) for y in range(len(self.coordinates))])
                        self.coordinates = [list(self.coordinates[x]) for x in range(len(self.coordinates))]
                        if not self.check_rotate():
                            self.coordinates = list([map(lambda x: x - 1, self.coordinates[y]) for y in range(len(self.coordinates))])
                            self.coordinates = [list(self.coordinates[x]) for x in range(len(self.coordinates))]
            elif not self.check_right() or not self.check_right_rotate():
                if not self.check_rotate():
                    if self.check_left():
                        self.coordinates = list([map(lambda x: x - 1, self.coordinates[y]) for y in range(len(self.coordinates))])
                        self.coordinates = [list(self.coordinates[x]) for x in range(len(self.coordinates))]
                        if not self.check_rotate():
                            self.coordinates = list([map(lambda x: x - 1, self.coordinates[y]) for y in range(len(self.coordinates))])
                            self.coordinates = [list(self.coordinates[x]) for x in range(len(self.coordinates))]
                            if not self.check_rotate():
                                self.coordinates = list([map(lambda x: x + 2, self.coordinates[y]) for y in range(len(self.coordinates))])
                                self.coordinates = [list(self.coordinates[x]) for x in range(len(self.coordinates))]
            for x in self.position:
                grid[x] = '-'
            if self.check_rotate():
                self.coordinates.append(self.coordinates.pop(0))
                self.position = self.coordinates[0]
            self.down()


    def right(self):
        if self.check_bottom():
            if self.check_right():
                self.coordinates = list([map(lambda x: x + 1, self.coordinates[y]) for y in range(len(self.coordinates))])
                self.coordinates = [list(self.coordinates[x]) for x in range(len(self.coordinates))]
                for x in self.position:
                    grid[x] = '-'
                self.position = self.coordinates[0]
                self.down()
            else:
                self.down()

    def left(self):
        if self.check_bottom():
            if self.check_left():
                self.coordinates = list([map(lambda x:  x - 1, self.coordinates[y]) for y in range(len(self.coordinates))])
                self.coordinates = [list(self.coordinates[x]) for x in range(len(self.coordinates))]
                for x in self.position:
                    grid[x] = '-'
                self.position = self.coordinates[0]
                self.down()
            else:
                self.down()

decision = input("select e for exit, p for new piece, d for down, rt for rotate, l for left, r for right or b for break ") #tutaj trzena zrobić zmianę menu

while decision != 'e':
    if decision not in ['e', 'p', 'd', 'r', 'l', 'rt', 'b']:
        decision = input("select e for exit, p for new piece, d for down, rt for rotate, l for left, r for right or b for break ")
    if decision == 'p':
        decision_letter = random.choice(['I', 'S', 'Z', 'L', 'J', 'T', 'O'])
        letter = Letter()
        letter.print_position()
        decision = input("select e for exit, p for new piece, d for down, rt for rotate, l for left, r for right or b for break ")
    if decision == 'd':
        letter.down()
        if any([(grid[x] == '0') for x in top]):
            print('Game Over!')
            break
        else:
            decision = input("select e for exit, p for new piece, d for down, rt for rotate, l for left, r for right or b for break ")
    elif decision == 'rt':
        letter.rotate()
        decision = input("select e for exit, p for new piece, d for down, rt for rotate, l for left, r for right or b for break ")
    elif decision == 'l':
        letter.left()
        decision = input("select e for exit, p for new piece, d for down, rt for rotate, l for left, r for right or b for break ")
    elif decision == 'r':
        letter.right()
        decision = input("select e for exit, p for new piece, d for down, rt for rotate, l for left, r for right or b for break ")
    elif decision == 'b':
        break_line()
        decision = input("select e for exit, p for new piece, d for down, rt for rotate, l for left, r for right or b for break ")









