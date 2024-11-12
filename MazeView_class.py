from Maze_class import Maze
from init_objects import maze, robot
import tkinter as tk

class MazeView:
    # draws maze onto a canvas in root (MazeApp)
    def __init__(self, root):
        self.maze = maze
        self.root = root
        self.root.title("Maze")

        # creates canvas, sized according to maze size
        self.width = (100/self.maze.size[0]*50)
        self.height = (100/self.maze.size[1]*50)
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="white", relief="solid", border=5)
        self.canvas.pack(side="left")

        self.character_rectangle = None
        self.character_label = None

        self.maze_creation()

    def maze_creation(self):
        # draws maze as black and white squares
        for row in range(len(self.maze.maze)):
            for col in range(len(self.maze.maze[row])):
                color = "black" if self.maze.maze[row][col] == 1 else "white"
                x1, y1 = col * self.width/self.maze.size[1]+5, row * self.height/self.maze.size[0]+5
                x2, y2 = x1 + self.width/self.maze.size[1]+5, y1 + self.height/self.maze.size[0]+5
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        # places finish on canvas
        posy = self.maze.finish[1]
        posx = self.maze.finish[0]
        x1, y1 = (posy * self.width/self.maze.size[1]+(self.width/self.maze.size[1]/5),
                  posx * self.height/self.maze.size[0]+(self.height/self.maze.size[0]/5))
        x2, y2 = (x1 + (self.width/self.maze.size[1])-(self.width/self.maze.size[1]/5),
                  y1 + (self.height/self.maze.size[1])-(self.height/self.maze.size[1]/5))
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="lightgreen")


    def character_draw(self):
        # places robot on canvas, and deletes it if its present for new draw
        if self.character_rectangle is not None:
            self.canvas.delete(self.character_rectangle)
            self.canvas.delete(self.character_label)

        character = robot

        posx = character.posy
        posy = character.posx
        x1, y1 = (posy * self.width / self.maze.size[1] + (self.width / self.maze.size[1] / 5),
                  posx * self.height / self.maze.size[0] + (self.height / self.maze.size[0] / 5))
        x2, y2 = (x1 + (self.width / self.maze.size[1]) - (self.width / self.maze.size[1] / 5),
                  y1 + (self.height / self.maze.size[1]) - (self.height / self.maze.size[1] / 5))
        self.character_rectangle = self.canvas.create_oval(x1, y1, x2, y2, fill="red", outline="darkred")
