from classes.flood_fill_algorithm import FloodFill
from classes.helper_file import init
mazeDAO = init.mazeDAO
import numpy as np


class Maze:
    def __init__(self, level):
        # init of parameters, used for further referencing
        self.maze = mazeDAO.load_maze(level)
        self.size = None
        self.start = None
        self.finish = None
        self.get_info()
        self.alg = FloodFill(self.maze)
        self.alg.flood()
        self.transformed = self.alg.transformed
        print(f"Flooded maze:\n{self.transformed}")
        self.alg_values = self.alg.get_values()

    def get_info(self):
        self.size = self.maze.shape
        self.start = (np.where(self.maze == 8)[0][0],np.where(self.maze == 8)[1][0])
        self.finish = (np.where(self.maze == 3)[0][0],np.where(self.maze == 3)[1][0])

    def check_bounds(self, new_y, new_x):
        return 0 <= new_y < self.transformed.shape[0] and 0 <= new_x < self.transformed.shape[1]

    def check_walls(self, min_value, cell_value):
        return min_value > cell_value > 0

    def check_finish(self, current_position):
        return self.transformed[current_position[0], current_position[1]] == 1