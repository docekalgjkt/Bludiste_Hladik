import numpy as np
from random import randint


class Maze_generator:
    def __init__(self, size):
        self.y, self.x = size
        self.directions = [(1,0),(0,-1),(-1,0),(0,1)]   # y, x
        self.file = None

    def create_maze(self):
        # maze = [[randint(0, 9) for cell in range(self.x)] for row in range(self.y)]

        # creates a maze with walls only
        maze = []
        for row in range(self.y):
            row = []
            for cell in range(self.x):
                row.append('0')
            maze.append(row)

        # maze = np.array([[1,2,3],
        #                  [4,5,6],
        #                  [7,8,9]])

        # saves the wall only maze as np.array
        self.file = np.array(maze, dtype=int)

        # replaces wall with vacant cells if possible
        for y, row in enumerate(self.file):
            for x, cell in enumerate(row):
                print(f"cell: {cell} at ({y}, {x})")
                available_cells = 0
                unavailable_cells = 0

                # gets the value of cell's neighbors
                for dir in self.directions:
                    neighbor_row = y + dir[0]
                    neighbor_col = x + dir[1]

                    # checks bounds
                    if 0 <= neighbor_row < self.file.shape[0] and 0 <= neighbor_col < self.file.shape[1]:
                        neighbor = self.file[neighbor_row, neighbor_col]
                        print(f"Neighbor at ({neighbor_row}, {neighbor_col}): {neighbor}")
                        if neighbor == 0:
                            available_cells += 1
                        if neighbor == 1:
                            unavailable_cells += 1

                print(f"Available cells: {available_cells}")
                print(f"Unavailable cells: {unavailable_cells}")
                # Replace cell if conditions are met
                if available_cells >= 3 and 2 >= unavailable_cells:
                    print(self.file[y,x])
                    self.file[y, x] = 1
                print("\n")

        np.save("temp_maze.npy", self.file)
        print(self.file)


if __name__ == "__main__":
    generator = Maze_generator((5,5))
    generator.create_maze()

