import numpy as np
from collections import deque

class FloodFill:
    def __init__(self,maze):
        # load components from maze
        self.maze = maze
        self.start = np.where(maze == 8)[0][0],np.where(maze == 8)[1][0]
        self.finish = np.where(maze == 3)[0][0], np.where(maze == 3)[1][0]
        self.directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        self.transformed = self.maze_transform()
        self.can_be_solved = True

    def maze_transform(self):
        # replaces all 1 with inf. and 8,3 with 0
        transformed = self.maze.astype(float)
        transformed[transformed == 1] = np.inf
        transformed[transformed == 8] = 0
        transformed[transformed == 3] = 0
        return transformed

    def flood(self, position=None):
        # creates queue and adds finish to it
        queue = deque([self.finish])
        # replaces finish with 1
        self.transformed[self.finish[0], self.finish[1]] = 1

        while queue:
            # gets the first to be explored position and removes it
            current = queue.popleft()
            current_value = self.transformed[current[0], current[1]]

            # explores neighbors
            for dir in self.directions:
                new_y = current[0] + dir[0]
                new_x = current[1] + dir[1]

                # checks bounds
                if 0 <= new_y < self.transformed.shape[0] and 0 <= new_x < self.transformed.shape[1]:
                    # if the neighboring cell is unvisited, fill it with current_value + 1
                    if self.transformed[new_y, new_x] == 0:
                        self.transformed[new_y, new_x] = current_value + 1
                        # add the new position to the queue for further exploration in next iteration
                        queue.append((new_y, new_x))
