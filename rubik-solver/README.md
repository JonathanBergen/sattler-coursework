# 2x2 Rubik's Cube solver

## Added:
- solver.py: This is the only file I modified: I wrote all of the code in this file

## The technique used to solve this problem:
- Implemented a two-way breadth-first search, searching from both the scrambled position and the solved position simultaneously

### Data Structures
- Created a queue and hash table for each search-direction. 
- Each queue contains novel cube positions whose child positions will be checked in the next level of search
- Each hash table contains cube arrangments as the keys, and the paths as values: (A list of moves representing the shortest path to the position)

### The searching algorithm
- Created two loops to step through the levels of search, alternating the direction of the search.
- Each loop begins by checking the length of the queue, and storing that number ensure the algorithm switches directions after searching one level
- Each cube position is popped from the queue, and all 6 possible child positions are checked for novelty. If the position exists in the parallel hash table, the child is discarded. If the child exists in the antiparallel hash table, a path has been found and the algorithm returns the appropiate path. If the child is merely novel, its hashed position is added to the parallel hash table, and it also added to the queue, to have its children searched in the next level of searching.

### Complexity managment
- Using a hash table allows for constant-time lookups, giving us an advantage over something like a linked-list representation of the searched nodes
- Using a queue rather than a list allows for O(1) constant-time popping and pushing rather than O(n) linear-time complexity.
- Storing the parents rather than children in the queue allows for 6x slower growth in space complexity. This was crucial, as the queue would grow much faster than the hash table if children were stored.
