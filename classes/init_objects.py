class Init_objects:
    def __init__(self):
        # xml, csv, txt
        self.file_type = "csv"
        # num = numbers, sq = colored squares, none = no display
        self.draw_flood = "sq"
        self.database = "saved_levels"
        self.filename = "levels"
        from classes.FactoryDAO import FactoryDAO
        self.factory_dao = FactoryDAO(self.database, self.filename)
        self.mazeDAO = self.factory_dao.create_dao(self.file_type)
        # from classes.Level_chooser_class import LevelChooser
        # popup = LevelChooser("Level selector")
        import tkinter as tk
        self.root = tk.Tk()
        from classes.MazeApp_class import MazeApp
        self.window = MazeApp(self.root, levels=self.mazeDAO.get_all_levels())

        self.maze = None
        self.robot = None
        self.canvas = None
        self.robot_view = None

        self.check_level_and_run()

    def check_level_and_run(self):
        """
        Checks if a level has been selected. If so, proceeds to initialize the rest of the program.
        """
        if self.window.level is not None:
            from classes.Maze_class import Maze
            self.maze = Maze(level=self.window.level)
            from classes.Robot_flood_class import Robot
            self.robot = Robot()
            from classes.MazeView_class import MazeView
            self.canvas = MazeView(self.root)
            from classes.RobotView_class import RobotView
            self.robot_view = RobotView(self.canvas.canvas)
            if self.draw_flood == "none":
                self.robot_view.character_draw()
        else:
            # Keep checking until a level is selected
            self.root.after(100, self.check_level_and_run)
