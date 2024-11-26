# xml, csv, txt
file_type = "csv"
database = "saved_levels"
filename = "levels"
from classes.FactoryDAO import FactoryDAO
factory_dao = FactoryDAO(database, filename)
mazeDAO = factory_dao.create_dao(file_type)
from classes.Level_chooser_class import LevelChooser
popup = LevelChooser("Level selector")
from classes.Maze_class import Maze
maze = Maze(level=popup.message_popup(mazeDAO.get_all_levels()))
from classes.Robot_flood_class import Robot
robot = Robot()
import tkinter as tk
root = tk.Tk()
from classes.MazeView_class import MazeView
canvas = MazeView(root)
from classes.RobotView_class import RobotView
robot_view = RobotView(canvas.canvas)
from classes.MazeApp_class import MazeApp
window = MazeApp(root)
level = window.level
