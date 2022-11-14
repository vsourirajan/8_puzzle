# 8-Puzzle Solver Using Breadth-First, Depth-First, and A-Star Search Methods

### How to Run:
bfs: breadth-first search<br />
dfs: depth-first search<br />
ast: a-star search (uses total Manhattan distance as heuristic)<br /> <br />

Run the solver as follows (python 3):<br />  `python3 8 puzzle_solver.py <solve_method> <comma_separated_board_of_numbers>`
<br /> <br />
For example:<br />
<sub>`python3 puzzle_solver.py ast 8,7,6,5,4,3,2,1`</sub>
<br /><br />
The above command solves the puzzle using a-star search and writes the solved order of moves to output.txt
<br /> <br />
The file output.txt also includes the following metrics regarding each solve:<br />
        -cost_of_path<br />
        -nodes_expanded<br />
        -search_depth<br />
        -running_time<br />
        -max_ram_usage
