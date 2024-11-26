import tkinter as tk


class MazeApp:
    # draws the GUI
    def __init__(self, root, levels):
        self.root = root
        self.root.title("Maze")
        self.level = None

        # draws character for the first time
        # robot_view.character_draw()

        # draws GUI
        self.label = tk.Label(root, text="...", font=("Helvetica", 16))
        self.label.pack(side="top")

        self.frame = tk.Frame(root)
        self.frame.pack(side="right")

        self.button_start = tk.Button(self.frame, text="Start", width=10, height=4)
        self.button_start.pack()

        # Level chooser
        self.level_label = tk.Label(self.frame, text="Select Level:")
        self.level_label.pack(anchor="w")

        self.level_var = tk.StringVar(value=levels[0] if levels else None)
        self.level_buttons = []

        for index, level in enumerate(levels, start=1):
            rb = tk.Radiobutton(
                self.frame,
                text=f"{level} ({index})",
                variable=self.level_var,
                value=index
            )
            rb.pack(anchor="w")
            self.level_buttons.append(rb)

        # Confirm button
        self.confirm_button = tk.Button(self.frame, text="Confirm Selection", command=self.confirm_selection)
        self.confirm_button.pack(pady=5)

        self.character_rectangle = None

        self.update_button()

    def update_button(self):
        try:
            from init_objects import canvas
        except ImportError:
            pass
        else:
            if canvas.can_run:
                self.button_start.config(state=tk.NORMAL, bg="light green")
            else:
                self.button_start.config(state=tk.DISABLED)

            self.root.after(100, self.update_button)

    def confirm_selection(self):
        self.level = self.level_var.get()
        print(f"Confirmed Level: {self.level_var.get()}")
        try:
            from init_objects import robot
        except ImportError:
            pass
        else:
            self.button_start.config(command=robot.move)

