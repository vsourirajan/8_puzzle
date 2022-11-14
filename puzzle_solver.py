
from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q
import resource
import heapq

#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def __lt__(self, other):
        order = ["Up", "Down", "Left", "Right"]
        return order.index(self.action) < order.index(other.action)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        
        '''zeroIndex = 0
        for count in range(len(self.config)):
          if(self.config[count] == 0):
            break
          zeroIndex+=1'''
        
        if(self.blank_index >= self.n):
            config = list(self.config)
            temp = config[self.blank_index]
            config[self.blank_index] = config[self.blank_index- self.n]
            config[self.blank_index- self.n] = temp
            child = PuzzleState(config, self.n, self, 'Up', self.cost+1)
            
            return child

        return None
        
        #pass
      
    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        
        if(self.blank_index <= self.n*self.n - self.n - 1):
            config = list(self.config)
            temp = config[self.blank_index]
            config[self.blank_index] = config[self.blank_index+self.n]
            config[self.blank_index+self.n] = temp
            child = PuzzleState(config, self.n, self, 'Down', self.cost+1)

            return child

        return None


        #pass
      
    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """

        if(self.blank_index%3 > 0):
            config = list(self.config)
            temp = config[self.blank_index]
            config[self.blank_index] = config[self.blank_index-1]
            config[self.blank_index-1] = temp
            child = PuzzleState(config, self.n, self, 'Left', self.cost+1)
            
            return child

        return None

        #pass

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """

        
        if(self.blank_index%self.n < self.n-1):
            config = list(self.config)
            temp = config[self.blank_index]
            config[self.blank_index] = config[self.blank_index+1]
            config[self.blank_index+1] = temp
            child = PuzzleState(config, self.n, self, 'Right', self.cost+1)

            return child

        return None

        #pass
      
    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]
        

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(current_state, expanded, time, max_cost, ram):
    ### Student Code Goes here

    pathList = []
    #pathList.insert(0, current_state.action)
    current = current_state
    while(current.parent is not None):
        pathList.insert(0, current.action)
        current = current.parent

    f = open("output.txt", "w")
    f.write("path_to_goal: ")
    f.write(str(pathList))

    f.write("\ncost_of_path: ")
    f.write(str(current_state.cost))

    f.write("\nnodes_expanded: ")
    f.write(str(expanded))

    f.write("\nsearch_depth: ")
    f.write(str(len(pathList)))

    f.write("\nmax_search_depth: ")
    f.write(str(max_cost))


    f.write("\nrunning_time: ")
    #val = '%.8f'%(time)
    f.write(str('%.8f'%(time)))

    f.write("\nmax_ram_usage: ")
    f.write(str(ram))
    f.write("\n")

    f.close()

    #pass

def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###

    bfs_start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    start_time  = time.time()

    q = Q.Queue()
    q.put(initial_state)

    fringe = set()
    fringe.add(''.join(map(str,initial_state.config)))
    explored = set()

    while(q.empty() == False):
        current_state = q.get()
        #print(current_state.config)
        explored.add(''.join(map(str,current_state.config)))
        if(test_goal(current_state) == True):
            max_cost = current_state.cost
            while(q.empty() == False):
                c = q.get().cost
                if(c > max_cost):
                    max_cost = c
            
            bfs_ram = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - bfs_start_ram)/(2**20)
            end_time = time.time()
            return writeOutput(current_state, len(explored) - 1, end_time-start_time, max_cost, bfs_ram)

        children = current_state.expand()

        for child in children:
            if(child != None and ''.join(map(str,child.config)) not in explored and ''.join(map(str,child.config)) not in fringe):
                q.put(child)
                fringe.add(''.join(map(str,child.config)))
        
        fringe.remove(''.join(map(str,current_state.config)))
        

    return None

    #pass

def dfs_search(initial_state):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###

    dfs_start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    start_time  = time.time()

    stack = Q.LifoQueue()
    stack.put(initial_state)

    fringe = set()
    fringe.add(''.join(map(str,initial_state.config)))

    explored = set()

    max_cost = 0

    while(stack.empty() == False):

        current_state = stack.get()
        fringe.remove(''.join(map(str,current_state.config)))
        #print(current_state.config)
        explored.add(''.join(map(str,current_state.config)))

        if(current_state.cost > max_cost):
            max_cost = current_state.cost

        if(test_goal(current_state) == True):
            
            dfs_ram = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - dfs_start_ram)/(2**20)
            end_time = time.time()
            return writeOutput(current_state, len(explored) - 1, end_time-start_time, max_cost, dfs_ram)

        children = current_state.expand()

        for child in children[::-1]:
            if(child != None and ''.join(map(str,child.config)) not in explored and ''.join(map(str,child.config)) not in fringe):
                stack.put(child)
                fringe.add(''.join(map(str,child.config)))

    return None

    #pass

def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###

    dfs_start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    start_time  = time.time()

    heap = []
    heapq.heappush(heap, (calculate_total_cost(initial_state), initial_state))

    fringe = set()
    fringe.add(''.join(map(str,initial_state.config)))
    
    explored = set()
    
    while(len(heap) > 0):
        
        current_state = heapq.heappop(heap)[1]
        #print(current_state.config)

        fringe.remove(''.join(map(str, current_state.config)))
        explored.add(''.join(map(str,current_state.config)))
        
        if(test_goal(current_state) == True):
            max_cost = current_state.cost
            
            bfs_ram = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - dfs_start_ram)/(2**20)
            end_time = time.time()
            return writeOutput(current_state, len(explored) - 1, end_time-start_time, max_cost, bfs_ram)

        children = current_state.expand()

        for child in children:
            if(child != None and ''.join(map(str,child.config)) not in explored and ''.join(map(str,child.config)) not in fringe):
                heapq.heappush(heap, (calculate_total_cost(child), child))
                fringe.add(''.join(map(str,child.config)))
            elif(child != None and ''.join(map(str,child.config)) not in explored and ''.join(map(str,child.config)) in fringe):
                for tup in heap:
                    if(tup[1].config == child.config):
                        tup = (min(calculate_total_cost(child), tup[0]), tup[1])
                        
    return None
    #pass

def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###

    total_cost = state.cost

    for count in range(len(state.config)):
        total_cost += calculate_manhattan_dist(count, state.config[count], state.n)

    #print(state.config, total_cost)
    return total_cost

    #pass

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###

    start_row = idx/n
    final_row = value/n

    start_col = idx%n
    final_col = value%n

    return abs(final_row-start_row) + abs(final_col-start_col)

def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###

    goalState = list(puzzle_state.config)
    goalState.sort()

    if(goalState == puzzle_state.config):
        return True
    return False

    #pass

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    
    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
        
    end_time = time.time()
    print("Program completed in %.3f second(s)"%(end_time-start_time))

if __name__ == '__main__':
    main()
