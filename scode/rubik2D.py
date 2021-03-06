"""
Name of the author(s):
- Louis Navarre <louis.navarre@uclouvain.be>
"""
import time
import sys
from search import *


#################
# Problem class #
#################
class Rubik2D(Problem):

    def actions(self, state):
        ActionsList = []
        (shape_x,shape_y)=state.shape
        #passe par toutes les lignes
        for i in range(0, shape_x):
            for j in range(0, shape_y):
                ActionsList.append((i, "down", j)) #Row #i Down #j
        #passe par toutes les col
        for i in range(0, shape_y):
            for j in range(0, shape_x):
                ActionsList.append((i, "right", j)) #Col #i Right #j
        
        return ActionsList

    def result(self, state, action):
        my_test_grid=state.grid
        if action[1]=="right":      
            for x in state.grid[action[0]]:
                pos=int(state.shape[0]-(int(x)+1))
                if (state.grid[action[0]].index(x)+action[2])<=state.shape[0]:
                    my_test_grid[action[0]][int(x)+action[2]]=state.grid[action[0]][int(x)]
                else:
                    my_test_grid[action[0][0+pos-1]]=state.grid[action[0]][x]
        else:
            for y in state.grid[action[0]]:
                if (state.grid[action[0]].index(y)+action[2])<=state.shape[1]:
                    my_test_grid[int(y)+action[2]][action[0]]=state.grid[int(y)][action(0)]
                else:
                    my_test_grid[action[0+pos-1]][action[0]]=state.grid[y][action[0]]
        return my_test_grid

    def goal_test(self, state):
        pass


###############
# State class #
###############
class State:

    def __init__(self, shape, grid, answer=None, move="Init"):
        self.shape = shape
        self.answer = answer
        self.grid = grid
        self.move = move

    def __str__(self):
        s = self.move + "\n"
        for line in self.grid:
            s += "".join(line) + "\n"
        return s


def read_instance_file(filepath):
    with open(filepath) as fd:
        lines = fd.read().splitlines()

    shape_x, shape_y = tuple([int(i) for i in lines[0].split(" ")])
    initial_grid = list()
    for row in lines[1:1 + shape_x]:
        initial_grid.append(tuple([i for i in row]))

    goal_grid = list()
    for row in lines[1 + shape_x + 1:]:
        goal_grid.append(tuple([i for i in row]))

    return (shape_x, shape_y), initial_grid, goal_grid


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: ./rubik2D.py <path_to_instance_file>")
    filepath = sys.argv[1]

    shape, initial_grid, goal_grid = read_instance_file(filepath)

    init_state = State(shape, tuple(initial_grid), tuple(goal_grid), "Init")
    problem = Rubik2D(init_state)

    # Example of search
    start_timer = time.perf_counter()
    node, nb_explored, remaining_nodes = breadth_first_tree_search(problem)
    end_timer = time.perf_counter()

    # Example of print
    path = node.path()

    for n in path:
        # assuming that the __str__ function of state outputs the correct format
        print(n.state)

    print("* Execution time:\t", str(end_timer - start_timer))
    print("* Path cost to goal:\t", node.depth, "moves")
    print("* #Nodes explored:\t", nb_explored)
    print("* Queue size at goal:\t",  remaining_nodes)
