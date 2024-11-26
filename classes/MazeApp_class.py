from init_objects import robot, canvas, robot_view
import tkinter as tk


class MazeApp:
    # draws the GUI
    def __init__(self, root):
        self.root = root
        self.root.title("Maze")
        self.level = None

        # draws character for the first time
        robot_view.character_draw()

        # draws GUI
        self.label = tk.Label(root, text="...", font=("Helvetica", 16))
        self.label.pack(side="top")

        self.frame = tk.Frame(root)
        self.frame.pack(side="right")

        self.button = tk.Button(self.frame, text="Start", width=10, height=4, command=robot.move)
        self.button.pack()

        self.character_rectangle = None
        self.character_label = None

        self.update_button()

    def update_button(self):
        if canvas.can_run:
            self.button.config(state=tk.NORMAL, bg="light green")
        else:
            self.button.config(state=tk.DISABLED)

        self.root.after(100, self.update_button)
