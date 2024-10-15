import time
import numpy as np
import tkinter as tk
from flood_fill_algorithm import FloodFill


class Maze:
    def __init__(self):
        self.maze = None
        self.size = None
        self.start = None
        self.finish = None
        self.load_maze()
        self.get_info()
        self.alg = FloodFill(self.maze)
        self.alg.flood()
        self.transformed = self.alg.transformed
        print(f"Flooded maze:\n{self.transformed}")


    def load_maze(self):
        self.maze = np.array([
            [0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
            [8, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [0, 0, 0, 1, 3, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])

        filename = 'maze_file.npz'

        np.savez(filename, maze=self.maze)

        loaded_data = np.load(filename)
        self.maze = loaded_data['maze']

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


class Robot:
    def __init__(self):
        self.maze = maze
        self.posx = maze.start[1]
        self.posy = maze.start[0]
        self.start_position = (maze.start[0],maze.start[1])
        # rightward, forward, leftward, backward
            # normalized (x,y)
        self.directions = [(1,0),(0,-1),(-1,0),(0,1)]
        self.status = True

    def move(self):
        window.label.config(text="...")
        transformed = maze.alg.transformed
        current_position = self.start_position
        start_time = time.time()

        while True:
            # if reached the goal
            if transformed[current_position[0], current_position[1]] == 1:
                print("Reached the destination!")
                window.label.config(text=f"{time.time()-start_time:.1f}s")
                break

            next_position = None
            min_value = np.inf

            # checks neighboring cells for the next move
            for dir in self.directions:
                new_y = current_position[0] + dir[0]
                new_x = current_position[1] + dir[1]

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

            canvas.character_draw()
            canvas.root.update()

            time.sleep(0.2)



class MazeView:
    def __init__(self,root):
        self.root = root
        self.root.title("Maze")

        self.width = (100/maze.size[0]*50)
        self.height = (100/maze.size[1]*50)
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="white", relief="solid", border=5)
        self.canvas.pack(side="left")

        self.character_rectangle = None
        self.character_label = None

        self.maze_creation()

    def maze_creation(self):
        for row in range(len(maze.maze)):
            for col in range(len(maze.maze[row])):
                color = "black" if maze.maze[row][col] == 1 else "white"
                x1, y1 = col * self.width/maze.size[1]+5, row * self.height/maze.size[0]+5
                x2, y2 = x1 + self.width/maze.size[1]+5, y1 + self.height/maze.size[0]+5
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        posy = maze.finish[1]
        posx = maze.finish[0]
        x1, y1 = (posy * self.width/maze.size[1]+(self.width/maze.size[1]/5),
                  posx * self.height/maze.size[0]+(self.height/maze.size[0]/5))
        x2, y2 = (x1 + (self.width/maze.size[1])-(self.width/maze.size[1]/5),
                  y1 + (self.height/maze.size[1])-(self.height/maze.size[1]/5))
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="lightgreen")


    def character_draw(self):
        if self.character_rectangle is not None:
            self.canvas.delete(self.character_rectangle)
            self.canvas.delete(self.character_label)

        character = robot
        posx = character.posy
        posy = character.posx
        x1, y1 = (posy * self.width / maze.size[1] + (self.width / maze.size[1] / 5),
                  posx * self.height / maze.size[0] + (self.height / maze.size[0] / 5))
        x2, y2 = (x1 + (self.width / maze.size[1]) - (self.width / maze.size[1] / 5),
                  y1 + (self.height / maze.size[1]) - (self.height / maze.size[1] / 5))
        self.character_rectangle = self.canvas.create_oval(x1, y1, x2, y2, fill="red", outline="darkred")


class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze")

        canvas.character_draw()

        self.label = tk.Label(root, text="...", font=("Helvetica", 16))
        self.label.pack(side="top")

        self.frame = tk.Frame(root)
        self.frame.pack(side="right")

        self.button = tk.Button(self.frame, text="Start", width=10, height=4, command=robot.move)
        self.button.pack()

        self.character_rectangle = None
        self.character_label = None


if __name__ == "__main__":
    maze = Maze()
    robot = Robot()
    root = tk.Tk()
    canvas = MazeView(root)
    window = MazeApp(root)
    root.mainloop()
