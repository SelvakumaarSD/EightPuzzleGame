import numpy as np
from EightPuzzleGame_State import State

# This class implement the Best-First-Search (BFS) algorithm along with the Heuristic search strategies

# In this algorithm, an OPEN list is used to store the unexplored states and
# a CLOSE list is used to store the visited state. OPEN list is a priority queue.
# The priority is insured through sorting the OPEN list each time after new states are generated
# and added into the list. The heuristics are used as sorting criteria.

# In this informed search, reducing the state space search complexity is the main criterion.
# We define heuristic evaluations to reduce the states that need to be checked every iteration.
# Evaluation function is used to express the quality of informedness of a heuristic algorithm.


class InformedSearchSolver:
    current = State()
    goal = State()
    openlist = []
    closed = []
    depth = 0

    def __init__(self, current, goal):
        self.current = current
        self.goal = goal
        self.openlist.append(current)

    def sortFun(self, e):
        return e.weight

    # Check if Child Node is in Open / closed List - the purpose is to avoid a circle
    # @param s
    # @return array (flag and index)

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

    # Check and add child to open list
    # @param s
    def add_child_to_open(self, node):
        flag, index = self.check_inclusive(node)

        if flag == 1:
            self.heuristic_test(node)
            self.openlist.append(node)
        elif flag == 2:
            if node.depth < self.openlist[index].depth:
                self.openlist[index] = node
        elif flag == 3:
            if node.depth < self.closed[index].depth:
                self.closed.pop(index)
                self.openlist.append(node)

    # The following program does the state space walk using Best First Search
    # four types of walks - ↑ ↓ ← → (move up, move down, move left, move right)
    # Blank Tile is represent by '0'

    def state_walk(self):
        # add closed state
        self.closed.append(self.current)
        self.openlist.remove(self.current)
        # move to the next heuristic state
        walk_state = self.current.tile_seq
        row = 0
        col = 0

        for i in range(len(walk_state)):
            for j in range(len(walk_state[i])):
                if walk_state[i, j] == 0:
                    row = i
                    col = j
                    break

        self.depth += 1

        # ↑ move up
        if (row - 1) >= 0:
            if i == 0:
                return None
            else:
                temp_state = np.copy(walk_state)
                temp = temp_state[row - 1, col]
                temp_state[row, col] = temp
                temp_state[row - 1, col] = 0

                if temp_state is not None:
                    child = State(np.array(temp_state), self.depth, 0)

                self.add_child_to_open(child)

        # ↓ move down
        if (row + 1) < len(walk_state):

            if i == 0:
                return None
            else:
                temp_state = np.copy(walk_state)
                temp = temp_state[row + 1, col]
                temp_state[row, col] = temp
                temp_state[row + 1, col] = 0

                if temp_state is not None:
                    child = State(np.array(temp_state), self.depth, 0)

                self.add_child_to_open(child)

        # ← move left
        if (col - 1) >= 0:
            if i == 0:
                return None
            else:
                temp_state = np.copy(walk_state)
                temp = temp_state[row, col - 1]
                temp_state[row, col] = temp
                temp_state[row, col - 1] = 0

                if temp_state is not None:
                    child = State(np.array(temp_state), self.depth, 0)

                self.add_child_to_open(child)

        # → move right
        if (col + 1) < len(walk_state):
            if i == 0:
                return None
            else:
                temp_state = np.copy(walk_state)
                temp = temp_state[row, col + 1]
                temp_state[row, col] = temp
                temp_state[row, col + 1] = 0

                if temp_state is not None:
                    child = State(np.array(temp_state), self.depth, 0)

                # check if child is in open / closed and add appropriately
                self.add_child_to_open(child)

        # sort the open list first by h(n) then g(n)
        self.openlist.sort(key=self.sortFun)
        self.current = self.openlist[0]

    # Solving the game using heuristic search strategies
    # Three types of heuristic rules are used:
    # (1) Tiles out of place
    # (2) Sum of distances out of place
    # (3) 2 x the number of direct tile reversals

    # evaluation function
    # f(n) = g(n) + h(n)
    # g(n) = depth of path length to start state
    # h(n) = (1) + (2) + (3)

    def heuristic_test(self, current):
        curr_seq = current.tile_seq
        goal_seq = self.goal.tile_seq

        h1 = 0
        h2 = 0
        h3 = 0

        for r in range(len(curr_seq)):
            for c in range(len(curr_seq)):

                # (1) Tiles out of place
                # Checks for every single element in current == goal
                if curr_seq[r, c] != goal_seq[r, c]:
                    h1 += 1

                # (2) Sum of distances out of place
                # This function gets the absolute value of differences in current and goal (row and column)
                curr_val = curr_seq[r, c]
                curr_row = r
                curr_col = c
                goal_row, goal_col = np.where(goal_seq == curr_val)

                abs_row_dist = abs(curr_row - goal_row)
                abs_col_dist = abs(curr_col - goal_col)

                h2 += abs_row_dist + abs_col_dist

                # (3) 2 x the number of direct tile reversals
                if (abs_row_dist == 1 and abs_col_dist == 0) or (abs_row_dist == 0 and abs_col_dist == 1):
                    h3 += 1

        h3 *= 2

        # set the heuristic value for current state
        current.weight = current.depth + h1 + h2 + h3

    # You can choose to print all the states on the search path, or just the start and goal state

    def run(self):
        # output the start state
        print("start state !!!!!")
        print(self.current.tile_seq)

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
        print("goal state !!!!!")
