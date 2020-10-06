import numpy as np
from EightPuzzleGame_State import State

# This class implement one of the Uinformed Search algorithm
# You may choose to implement the Breadth-first or Depth-first or Iterative-Deepening search algorithm


class UninformedSearchSolver:
    current = State()
    goal = State()
    openlist = []
    closed = []
    depth = 0

    def __init__(self, current, goal):
        self.current = current
        self.goal = goal
        self.openlist.append(current)

    def check_inclusive(self, s):
        in_open = 0
        in_closed = 0
        ret = [-1, -1]

        for item in self.openlist:
            if item.equals(s):
                in_open = 1
                ret[1] = self.openlist.index(item)
                break

        for item in self.closed:
            if item.equals(s):
                in_closed = 1
                ret[1] = self.closed.index(item)
                break

        if in_open == 0 and in_closed == 0:
            ret[0] = 1  # the child is not in open or closed
        elif in_open == 1 and in_closed == 0:
            ret[0] = 2  # the child is already in open
        elif in_open == 0 and in_closed == 1:
            ret[0] = 3  # the child is already in closed
        return ret

    # To check if a number has been repeated in the input sequence
    def chk_inputstate_correct(self, node):
        arr_of_node = np.reshape(node, 9)
        for c in range(9):
            rep = 0
            e = arr_of_node[c]
            for r in range(9):
                if e == arr_of_node[r]:
                    rep += 1
            if rep >= 2:
                print("Invalid input sequence. Same number is entered twice")
                exit(0)

    # To check if the input state has a solution or not
    def chk_state_solvable(self, node):
        arr_of_node = np.reshape(node, 9)
        state_count = 0
        for c in range(9):
            if not arr_of_node[c] == 0:
                chk_e = arr_of_node[c]
                for r in range(c + 1, 9):
                    if chk_e < arr_of_node[r] or arr_of_node[r] == 0:
                        continue
                    else:
                        state_count += 1
        if state_count % 2 == 0:
            print("The puzzle is solvable through Uninformed Search, generating path")
        else:
            print("The puzzle is insolvable, still creating nodes")

    def get_zeroindex(self, node):
        i, j = np.where(node == 0)
        i = int(i)
        j = int(j)
        return i, j

    def move_left(self, data, i, j):
        if j == 0:
            return None
        else:
            temp_state = np.copy(data)
            temp = temp_state[i, j - 1]
            temp_state[i, j] = temp
            temp_state[i, j - 1] = 0
            return temp_state

    def move_right(self, data, i, j):
        if j == 2:
            return None
        else:
            temp_state = np.copy(data)
            temp = temp_state[i, j + 1]
            temp_state[i, j] = temp
            temp_state[i, j + 1] = 0
            return temp_state

    def move_up(self, data, i, j):
        if i == 0:
            return None
        else:
            temp_state = np.copy(data)
            temp = temp_state[i - 1, j]
            temp_state[i, j] = temp
            temp_state[i - 1, j] = 0
            return temp_state

    def move_down(self, data, i, j):
        if i == 2:
            return None
        else:
            temp_state = np.copy(data)
            temp = temp_state[i + 1, j]
            temp_state[i, j] = temp
            temp_state[i + 1, j] = 0
            return temp_state

    def add_child_to_open(self, node_seq):
        if node_seq is not None:
            child = State(np.array(node_seq), self.depth, 0)

        flag, index = self.check_inclusive(child)

        if flag == 1:
            self.openlist.append(child)
        elif flag == 2:
            if child.depth < self.openlist[index].depth:
                self.openlist[index] = child
        elif flag == 3:
            if child.depth < self.closed[index].depth:
                self.closed.pop(index)
                self.openlist.append(child)

    # BFS - implements 4 types of walks - ↑ ↓ ← → (move up, move down, move left, move right)
    # Blank tile is represent by '0'

    def state_walk(self):
        self.closed.append(self.current)

        if self.current in self.openlist:
            self.openlist.remove(self.current)

        walk_state = self.current.tile_seq
        row, col = self.get_zeroindex(walk_state)

        self.depth += 1

        if (row - 1) >= 0:
            child_seq = self.move_up(walk_state, row, col)
            self.add_child_to_open(child_seq)
        if (row + 1) < len(walk_state):
            child_seq = self.move_down(walk_state, row, col)
            self.add_child_to_open(child_seq)
        if (col - 1) >= 0:
            child_seq = self.move_left(walk_state, row, col)
            self.add_child_to_open(child_seq)
        if (col + 1) < len(walk_state):
            child_seq = self.move_right(walk_state, row, col)
            self.add_child_to_open(child_seq)

        self.current = self.openlist.pop(0)
    # Check the following to make it work properly

    def run(self):
        # output the start state
        print("start state !!!!!")
        print(self.current.tile_seq)

        self.chk_inputstate_correct(self.current.tile_seq)
        self.chk_state_solvable(self.current.tile_seq)

        path = 0

        while not self.current.equals(self.goal):

            self.state_walk()
            print(self.current.tile_seq)
            path += 1

        print("It took ", path, " iterations")
        print("The length of the path is: ", self.current.depth)
        # output the goal state
        target = self.goal.tile_seq
        print(target)
        print("Goal State !!!!!")
