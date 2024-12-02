from classes.helper_file import init
maze = init.maze
import time
import numpy as np


class Robot:
    def __init__(self):
        self.maze = maze
        self.posx = maze.start[1]
        self.posy = maze.start[0]
        # (y,x)
        self.start_position = (maze.start[0],maze.start[1])
        # rightward, forward, leftward, backward
            # normalized (x,y)
        self.directions = [(1,0),(0,-1),(-1,0),(0,1)]
        self.status = True

    def move(self):
        canvas = init.canvas
        if canvas.can_run:
            window = init.window
            # move function using flood fill algorithm
            window.label.config(text="...")
            transformed = maze.alg.transformed
            current_position = self.start_position
            start_time = time.time()

            while True:
                # if reached the goal
                if transformed[current_position[0], current_position[1]] == 1:
                    window.label.config(text=f"Finished in: {time.time()-start_time:.1f}s")
                    break

                next_position = None
                min_value = np.inf

                # checks neighboring cells for the next move
                for dir in self.directions:
                    new_y = current_position[0] + dir[1]
                    new_x = current_position[1] + dir[0]

                    # checks bounds
                    if maze.check_bounds(new_y, new_x):
                        cell_value = transformed[new_y, new_x]

                        # searching for the lowest non-infinity value
                        # avoids walls (inf.) and only considers cells filled with legal number
                        if maze.check_walls(min_value, cell_value):
                            min_value = cell_value
                            next_position = (new_y, new_x)

                if next_position is None:  # if no valid moves are available...
                    window.label.config(text=f"Can't solve this maze")
                    break

                current_position = next_position  # moves to the next position
                self.posx = next_position[1]
                self.posy = next_position[0]

                robot_view = init.robot_view
                robot_view.character_draw()
                robot_view.canvas.update()

                time.sleep(0.2)
