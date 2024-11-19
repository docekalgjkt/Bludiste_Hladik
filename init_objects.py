# xml, csv
file_type = "xml"
if file_type == "xml":
    from classes.XML_handling import MazeDAOXML
    mazeDAO = MazeDAOXML("saved_levels", "levels.xml")
elif file_type == "csv":
    from classes.CSV_handling import MazeDAOCSV
    mazeDAO = MazeDAOCSV("saved_levels", "levels.csv")
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
from classes.MazeApp_class import MazeApp
window = MazeApp(root)
