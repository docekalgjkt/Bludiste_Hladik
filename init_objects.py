from XML_handling import MazeDAOXML
mazeDAO = MazeDAOXML("saved_levels", "levels.xml")
from Maze_class import Maze
maze = Maze(level=3)
from Robot_flood_class import Robot
robot = Robot()
import tkinter as tk
root = tk.Tk()
from MazeView_class import MazeView
canvas = MazeView(root)
from MazeApp_class import MazeApp
window = MazeApp(root)
