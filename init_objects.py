from classes.XML_handling import MazeDAOXML
mazeDAO = MazeDAOXML("saved_levels", "levels.xml")
from classes.Maze_class import Maze
maze = Maze(level=3)
from classes.Robot_flood_class import Robot
robot = Robot()
import tkinter as tk
root = tk.Tk()
from classes.MazeView_class import MazeView
canvas = MazeView(root)
from classes.MazeApp_class import MazeApp
window = MazeApp(root)
