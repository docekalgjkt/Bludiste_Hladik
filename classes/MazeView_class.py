from init_objects import maze, robot
import tkinter as tk

class MazeView:
    # draws maze onto a canvas in root (MazeApp)
    def __init__(self, root):
        self.maze = maze
        self.root = root
        self.root.title("Maze")

        # creates canvas, sized according to maze size (complex calculus by og chat)
        max_canvas_size = 600  # maximum size for the canvas (square)
        rows, cols = self.maze.size
        self.cell_size = min(max_canvas_size // cols, max_canvas_size // rows)
        self.width = self.cell_size * cols
        self.height = self.cell_size * rows

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="white", relief="solid", border=5)
        self.canvas.pack(side="left")

        self.character_rectangle = None

        self.maze_creation()

    def maze_creation(self):
        # draws maze as a grid of black and white squares
        for row in range(len(self.maze.maze)):
            for col in range(len(self.maze.maze[row])):
                color = "black" if self.maze.maze[row][col] == 1 else "white"
                x1, y1 = col * self.cell_size + 7, row * self.cell_size + 7
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        # draws finish on canvas
        finish_x, finish_y = self.maze.finish
        x1, y1, x2, y2 = self.get_xy(finish_x, finish_y)
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="lightgreen")


    def character_draw(self):
        # places robot on canvas, and deletes it if its present for new draw
        if self.character_rectangle is not None:
            self.canvas.delete(self.character_rectangle)
        x1, y1, x2, y2 = self.get_xy(robot.posy, robot.posx)
        self.character_rectangle = self.canvas.create_oval(x1, y1, x2, y2, fill="red", outline="darkred")

    def get_xy(self, posx, posy):
        # helper function for x and y
        x1, y1 = posy * self.cell_size + self.cell_size * 0.2 + 7, posx * self.cell_size + self.cell_size * 0.2 + 7
        x2, y2 = x1 + self.cell_size * 0.6, y1 + self.cell_size * 0.6
        return x1, y1, x2, y2
