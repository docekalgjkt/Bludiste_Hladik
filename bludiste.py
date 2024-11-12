import time
import numpy as np
import tkinter as tk
from abc import ABC, abstractmethod
import ast
from classes.flood_fill_algorithm import FloodFill


class Maze:
    def __init__(self):
        # init of parameters, used for further referencing
        self.maze = mazaDAO.load_maze("maze_10x10.txt")
        self.size = None
        self.start = None
        self.finish = None
        self.get_info()
        self.alg = FloodFill(self.maze)
        self.alg.flood()
        self.transformed = self.alg.transformed
        print(f"Flooded maze:\n{self.transformed}")

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

class MazeDAO(ABC):
    # creation of main DAO class
    @abstractmethod
    def save_maze(self, maze):
        pass

    @abstractmethod
    def load_maze(self, maze):
        pass


class MazeDAOTXT(MazeDAO):
    def __init__(self, database):
        self.database = database

    def save_maze(self, maze):
        # saves maze to .txt
        maze_list = []

        # iterates over each element in matrix; creates a nested list
        for row in maze:
            maze_sublist = []
            for col in row:
                maze_sublist.append(col)
            maze_list.append(maze_sublist)

        # opens file
        with open("maze_10x10.txt", "w") as file:
            for sublist in maze_list:
                # converts each sublist to a string and writes it onto new line
                file.write(f"{sublist}\n")

    def load_maze(self, file):
        # loads the file and creates a matrix
        maze_list = []
        # reads the file
        with open(f"{file}", "r") as file:
            for line in file:
                # get rid of whitespace and evaluate the line as a list
                maze_list.append(ast.literal_eval(line.strip()))

        # convert loaded nested list to a NumPy array (maze)
        return np.array(maze_list)


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
        # move function using flood fill algorithm
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
    # draws maze onto a canvas in root (MazeApp)
    def __init__(self,root):
        self.root = root
        self.root.title("Maze")

        # creates canvas, sized according to maze size
        self.width = (100/maze.size[0]*50)
        self.height = (100/maze.size[1]*50)
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="white", relief="solid", border=5)
        self.canvas.pack(side="left")

        self.character_rectangle = None
        self.character_label = None

        self.maze_creation()

    def maze_creation(self):
        # draws maze as black and white squares
        for row in range(len(maze.maze)):
            for col in range(len(maze.maze[row])):
                color = "black" if maze.maze[row][col] == 1 else "white"
                x1, y1 = col * self.width/maze.size[1]+5, row * self.height/maze.size[0]+5
                x2, y2 = x1 + self.width/maze.size[1]+5, y1 + self.height/maze.size[0]+5
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        # places finish on canvas
        posy = maze.finish[1]
        posx = maze.finish[0]
        x1, y1 = (posy * self.width/maze.size[1]+(self.width/maze.size[1]/5),
                  posx * self.height/maze.size[0]+(self.height/maze.size[0]/5))
        x2, y2 = (x1 + (self.width/maze.size[1])-(self.width/maze.size[1]/5),
                  y1 + (self.height/maze.size[1])-(self.height/maze.size[1]/5))
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="lightgreen")


    def character_draw(self):
        # places robot on canvas, and deletes it if its present for new draw
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
    # draws the GUI
    def __init__(self, root):
        self.root = root
        self.root.title("Maze")

        # draws character for the first time
        canvas.character_draw()

        # draws GUI
        self.label = tk.Label(root, text="...", font=("Helvetica", 16))
        self.label.pack(side="top")

        self.frame = tk.Frame(root)
        self.frame.pack(side="right")

        self.button = tk.Button(self.frame, text="Start", width=10, height=4, command=robot.move)
        self.button.pack()

        self.character_rectangle = None
        self.character_label = None


if __name__ == "__main__":
    mazaDAO = MazeDAOTXT("database")
    maze = Maze()
    robot = Robot()
    root = tk.Tk()
    canvas = MazeView(root)
    window = MazeApp(root)
    root.mainloop()
