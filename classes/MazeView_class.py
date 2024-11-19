from init_objects import maze, robot
import tkinter as tk
import time

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

        # used for graphical display of flood fill
        self.alg_values = self.maze.alg_values
        self.white_squares = {}  # dictionary to store values:coordinates
        self.maze_values = set()  # set to track unique values

        self.maze_creation(self.alg_values)

    def maze_creation(self, values):
        # draws maze as a grid of black and white squares
        for row in range(len(self.maze.maze)):
            for col in range(len(self.maze.maze[row])):
                value = self.maze.transformed[row][col]
                color = "black" if self.maze.maze[row][col] == 1 else "white"
                x1, y1 = col * self.cell_size + 7, row * self.cell_size + 7
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

                if color == "white":
                    # if the square is white, it adds its value to set, creates a dictionary value:coordinates(multiple)
                    self.maze_values.add(value)  # tracks unique values
                    if value not in self.white_squares:
                        # creates key with empty list as value
                        self.white_squares[value] = []
                    # stores center coordinates of the square as value into a list from above
                    text_x = (x1 + x2) / 2
                    text_y = (y1 + y2) / 2
                    self.white_squares[value].append((text_x, text_y))

                # draws finish on canvas
                finish_x, finish_y = self.maze.finish
                x1, y1, x2, y2 = self.get_xy(finish_x, finish_y)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="lightgreen")

        # starts the flood-fill animation
        self.maze_values = sorted(self.maze_values)  # sorts values set in ascending order
        self.animate_values(0)  # starts animation

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

    def animate_values(self, value_index):
        # stops if all values are drawn
        if value_index >= len(self.maze_values):
            return

        current_value = self.maze_values[value_index]
        if current_value in self.white_squares:
            # draws all values with the same current value
            for x, y in self.white_squares[current_value]:
                self.canvas.create_text(
                    x, y, text=str(int(current_value)), fill="black", font=("Helvetica", 20, "bold")
                )

        # schedules the next value group after 0.5 seconds, stops when the function return invalid argument
        self.canvas.after(500, self.animate_values, value_index + 1)
