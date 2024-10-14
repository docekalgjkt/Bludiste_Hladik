import numpy as np
from collections import deque

class Maze:
    def __init__(self):
        self.maze = np.array([
            [0, 1, 1, 3, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 8, 1, 0],
            [0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1]
        ])

        filename = 'maze_file.npz'

        np.savez(filename, maze=self.maze)

        loaded_data = np.load(filename)
        self.maze = loaded_data['maze']

maze = Maze()


class FloodFill:
    def __init__(self,maze):
        self.maze = maze
        self.start = np.where(maze == 8)[0][0],np.where(maze == 8)[1][0]
        self.finish = np.where(maze == 3)[0][0], np.where(maze == 3)[1][0]
        self.directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        self.transformed = self.maze_transform()

    def maze_transform(self):
        transformed = self.maze.astype(float)
        transformed[transformed == 1] = np.inf
        transformed[transformed == 8] = 0
        transformed[transformed == 3] = 0
        return transformed

    def flood(self, position=None):
        queue = deque([self.finish])  # Start BFS with the finish point
        self.transformed[self.finish[0], self.finish[1]] = 1  # Start with 1 at the finish point

        while queue:
            current = queue.popleft()  # Get the current position
            current_value = self.transformed[current[0], current[1]]

            # Explore neighbors
            for dir in self.directions:
                new_x = current[0] + dir[0]
                new_y = current[1] + dir[1]

                # Check if the new position is within bounds
                if 0 <= new_x < self.transformed.shape[0] and 0 <= new_y < self.transformed.shape[1]:
                    # If the neighboring cell is unvisited (i.e., 0 or infinity), fill it with current_value + 1
                    if self.transformed[new_x, new_y] == 0:
                        self.transformed[new_x, new_y] = current_value + 1
                        queue.append((new_x, new_y))  # Add the new position to the queue for further exploration


algo = FloodFill(maze.maze)
algo.flood()
print(algo.transformed)
