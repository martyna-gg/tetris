import numpy as np
import random

global decision_letter
global state
global score
decision_grid = [10, 5]
state = 0
decision = ''
score = 0

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

def check_scores():
    best_score = open('scores.txt', 'r')
    if int(best_score.read()) >= score:
        best_score.close()
    else:
        best_score.close()
        best_score = open('scores.txt', 'w')
        best_score.write(str(score))
        best_score.close()


letters = {'O': [[4, 14, 15, 5], [4, 14, 15, 5]],
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

    def break_line(self):
        check = 0
        global score
        global grid
        new_grid = []
        for x in range(int(decision_grid[1])):
            if all([a == '0' for a in np.reshape(grid, (int(decision_grid[1]), int(decision_grid[0])))[x]]):
                new_grid = ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'] + new_grid
                check += 1
            else:
                new_grid = new_grid + list(np.reshape(grid, (int(decision_grid[1]), int(decision_grid[0])))[x])
        if check:
            if check == 1:
                score += 100
            if check == 2:
                score += 400
            if check == 3:
                score += 900
            if check == 4:
                score += 2000
            grid = np.array(new_grid)
            grid_print()


    def check_top(self):
        global state
        if any([(grid[x] == '0') for x in top]):
            return False
        elif state == 2 and decision == 'p' and any([grid[x] == '0'  for x in letter.coordinates[0]]):
            return False
        else:
            return True

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
            self.break_line()
        

    def rotate(self):
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
        if self.check_left():
            self.coordinates = list([map(lambda x:  x - 1, self.coordinates[y]) for y in range(len(self.coordinates))])
            self.coordinates = [list(self.coordinates[x]) for x in range(len(self.coordinates))]
            for x in self.position:
                grid[x] = '-'
            self.position = self.coordinates[0]
            self.down()
        else:
            self.down()


while state != 4:
    if state == 0:
        decision = input("select g for game, b for best score or e for exit ")
        while decision not in ['g', 'b', 'e']:
            decision = input("select g for game, b for best score or e for exit ")
        if decision == 'b':
            best_score = open('scores.txt', 'r')
            print(best_score.read())
            best_score.close()
            state = 0
        if decision == 'g':
            state = 1
        if decision == 'e':
            check_scores()
            state = 4
    if state == 1:
        decision_grid = [10, input("select the number of rows ")]
        try:
            if int(decision_grid[1]) < 5:
                state = 1
            else:
                left_border = [x * int(decision_grid[0]) for x in range(0, int(decision_grid[1]))]
                right_border = [x * int(decision_grid[0]) - 1 for x in range(1, int(decision_grid[1]) + 1)]
                bottom = [int(decision_grid[1]) * int(decision_grid[0]) - x for x in range(1, int(decision_grid[0]) + 1)]
                top = [x for x in range(0, int(decision_grid[0]))]
                grid_reset()
                grid_print()
                state = 2
        except ValueError:
            state = 1
    if state == 2:
        decision = input("select p for piece, s for your score or e for exit ")
        while decision not in ['p', 's', 'e']:
            decision = input("select p for piece, s for your score or e for exit ")
        if decision == 's':
            print(score)
            state = 2
        if decision == 'p':
            decision_letter = random.choice(['I', 'S', 'Z', 'L', 'J', 'T', 'O'])
            letter = Letter()
            if letter.check_top() and letter.check_bottom():
                letter.print_position()
                state = 3
            else:
                letter.print_position()
                check_scores()
                print('Game over!')
                state = 4
        if decision == 'e':
            check_scores()
            state = 4
    if state == 3:
        if letter.check_bottom():
            decision = input("select e for exit, d for down, rt for rotate, l for left or r for right ")
            while decision not in ['e', 'd', 'rt', 'l', 'r']:
                decision = input("select e for exit, d for down, rt for rotate, l for left or r for right ")
            if decision == 'd':
                letter.down()
                if letter.check_top() and letter.check_bottom():
                    state = 3
                if not letter.check_top():
                    check_scores()
                    print('Game over!')
                    state = 4
                if not letter.check_bottom():
                    letter.break_line()
                    state = 2
            if decision == 'rt':
                letter.rotate()
                if letter.check_top() and letter.check_bottom():
                    state = 3
                if not letter.check_top():
                    check_scores()
                    print('Game over!')
                    state = 4
                if not letter.check_bottom():
                    letter.break_line()
                    state = 2
            if decision == 'l':
                letter.left()
                if letter.check_top() and letter.check_bottom():
                    state = 3
                if not letter.check_top():
                    check_scores()
                    print('Game over!')
                    state = 4
                if not letter.check_bottom():
                    letter.break_line()
                    state = 2
            if decision == 'r':
                letter.right()
                if letter.check_top() and letter.check_bottom():
                    state = 3
                if not letter.check_top():
                    check_scores()
                    print('Game over!')
                    state = 4
                if not letter.check_bottom():
                    letter.break_line()
                    state = 2
            if decision == 'e':
                check_scores()
                state = 4
        else:
            letter.break_line()
            state = 2

   









