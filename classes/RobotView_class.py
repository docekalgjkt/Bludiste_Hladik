from classes.helper_file import init
robot = init.robot
maze_view = init.canvas

class RobotView:
    def __init__(self, canvas):
        self.canvas = canvas
        self.character_rectangle = None

    def character_draw(self):
        # places robot on canvas, and deletes it if its present for new draw
        if self.character_rectangle is not None:
            self.canvas.delete(self.character_rectangle)
        x1, y1, x2, y2 = maze_view.get_xy(robot.posy, robot.posx)
        self.character_rectangle = self.canvas.create_oval(x1, y1, x2, y2, fill="purple", outline="darkred")
