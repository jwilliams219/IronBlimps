from queue import PriorityQueue

import time

# Modified from an example at https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
# Improved to use priority queues and sets for overall faster operation.
# The naive implementation in the article uses a ton of memory and is just overall time and space inefficient. It also doesn't prune children correctly.
# This example also uses the same obstacle course used by https://github.com/AtsushiSakai/PythonRobotics/tree/master/PathPlanning

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    start_node = Node(None, start)
    end_node = Node(None, end)

    open = {}
    next_up = PriorityQueue()
    closed = set()

    open[start_node.position] = start_node
    next_up.put((start_node.f, start_node.position))
    current_node = start_node

    while len(open) > 0:
        next_index = next_up.get()[1]
        while next_index not in open:
            next_index = next_up.get()[1]
        current_node = open[next_index]

        closed.add(current_node.position)
        if current_node.position in open:
            del open[current_node.position]

        if current_node == end_node:
            # Backtrack
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        nextNodes = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # 8 cardinal directions

            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            if maze[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Node(current_node, node_position)

            nextNodes.append(new_node)

        # Loop through children
        for node in nextNodes:

            # node is on the closed list
            if node.position in closed:
                continue

            # Create the f, g, and h values
            node.g = current_node.g + 1
            node.h = ((node.position[0] - end_node.position[0]) ** 2) + ((node.position[1] - end_node.position[1]) ** 2)
            node.f = node.g + node.h

            # node is already in the open list
            if node.position in open and open[node.position].g < node.g:
                continue

            # Add the node to the open list
            open[node.position] = node

            next_up.put((node.f, node.position))


def main():
    maze = []
    for i in range(0, 71):
        row = []
        for j in range(0,71):
            row.append(0)
        maze.append(row)
    for i in range(0, 70):
        maze[i][0] = 1
    for i in range(0, 70):
        maze[70][i] = 1

    for i in range(0, 71):
        maze[i][70] = 1

    for i in range(0, 71):
        maze[0][i] = 1

    for i in range(0, 50):
        maze[40][i] = 1
        
    for i in range(0, 50):
        maze[50][70-i] = 1

    start = (20, 20)
    end = (60, 60)

    startTime = time.time()
    path = astar(maze, start, end)
    totalTime = time.time() - startTime
    print("Path: " + str(path))
    print("Total Time: " + str(totalTime))
    print("Path Length: " + str(len(path)))

    averageTime = 0
    for i in range(10):
        startTime = time.time()
        path = astar(maze, start, end)
        totalTime = time.time() - startTime
        averageTime += totalTime
    averageTime /= 10
    print("Average Time to Run (10 times): " + str(averageTime))


if __name__ == '__main__':
    main()
