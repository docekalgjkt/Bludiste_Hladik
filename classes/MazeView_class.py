from classes.helper_file import init
maze = init.maze
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

        # used for graphical display of flood fill
        self.alg_values = self.maze.alg_values
        self.white_squares = {}  # dictionary to store values:coordinates
        self.maze_values = set()  # set to track unique values
        self.max_value = None

        self.can_run = False

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
                        # creates key with empty list as value (so one key can have more values)
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
        self.max_value = max(self.maze_values)  # finds maximum value for normalization
        self.animate_values(0)  # starts animation

    def get_xy(self, posx, posy):
        # helper function for x and y
        x1, y1 = posy * self.cell_size + self.cell_size * 0.2 + 7, posx * self.cell_size + self.cell_size * 0.2 + 7
        x2, y2 = x1 + self.cell_size * 0.6, y1 + self.cell_size * 0.6
        return x1, y1, x2, y2

    def value_to_color(self, value):
        # maps a value to a color in the gradient
        normalized_value = value / self.max_value
        red = int(255 * normalized_value)
        green = int(255 * (1 - normalized_value))
        return f'#{red:02x}{green:02x}00'

    def animate_values(self, value_index):
        # draws values on white squares from self.white_squares dictionary according to set maze_values
        # stops if all values are drawn
        if value_index >= len(self.maze_values):
            self.can_run = True
            return  # ends the animation loop

        if init.draw_flood == "none":
            self.can_run = True
        else:
            current_value = self.maze_values[value_index]
            if current_value in self.white_squares:
                # draws all values with the same current value
                for x, y in self.white_squares[current_value]:
                    color = self.value_to_color(current_value)
                    text_color = None

                    if init.draw_flood == "sq":
                        # calculates square coordinates
                        col = int((x - 7) // self.cell_size)  # reverse x calculation to column
                        row = int((y - 7) // self.cell_size)  # reverse y calculation to row
                        x1, y1 = col * self.cell_size + 7, row * self.cell_size + 7
                        x2, y2 = x1 + self.cell_size, y1 + self.cell_size

                        # draws colored square first
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                        text_color = "black"
                    elif init.draw_flood == "num":
                        text_color = color

                    # draws black text over the colored square if applicable
                    self.canvas.create_text(
                        x, y, text=str(int(current_value)), fill=text_color, font=("Helvetica", 20, "bold"))

                    if init.draw_flood == "none" or "num" and current_value == self.max_value:
                        robot_view = init.robot_view
                        robot_view.character_draw()

            # schedules the next value group after 0.5 seconds, stops when the function return invalid argument
            self.canvas.after(300, self.animate_values, value_index + 1)