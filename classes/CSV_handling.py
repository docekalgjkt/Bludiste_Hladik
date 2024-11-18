import csv
import numpy as np
from abc import ABC, abstractmethod

class MazeDAO(ABC):
    # creation of main DAO class
    @abstractmethod
    def __init__(self, database, filename):
        self.database = database
        self.filename = filename

    @abstractmethod
    def save_maze(self, input_maze):
        pass

    @abstractmethod
    def load_maze(self, level):
        return np.array([])

    @abstractmethod
    def get_all_levels(self):
        return []

class MazeDAOCSV(MazeDAO):
    def __init__(self, database, filename):
        self.database = database
        self.filename = filename

    def save_maze(self, input_maze):
        # loads csv file
        filepath = f"../{self.database}/{self.filename}"
        maze_name = input("Enter maze name:\n> ")
        maze_level = input("Enter maze level:\n> ")


        with open(filepath, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # writes metadata: maze name and level
            writer.writerow([f"maze_name={maze_name}", f"level={maze_level}"])

            # writes maze cells row by row
            for row in input_maze:
                writer.writerow(row)

            # adds a blank row to separate mazes
            writer.writerow([])

    def load_maze(self, level):
        # loads csv file
        filepath = f"{self.database}/{self.filename}"
        try:
            with open(filepath, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                maze_found = False
                maze_data = []

                # reads through all rows:
                for row in reader:
                    # skips blank rows
                    if not row:
                        continue
                    # if it finds maze its goes to reading cells
                    if row[0].startswith("maze_name=") and row[1] == f"level={level}":
                        maze_found = True
                        continue
                    # if it encounters another maze after one was found, it breaks
                    elif row[0].startswith("maze_name="):
                        if maze_found:
                            break
                        continue

                    # reads cells
                    if maze_found:
                        maze_data.append([int(cell) for cell in row])

                if maze_data:
                    return np.array(maze_data)
                else:
                    raise ValueError(f"Maze with level {level} not found.")

        except FileNotFoundError:
            print("File not found.")

    def get_all_levels(self):
        data = f"{self.database}/{self.filename}"
        try:
            with open(data, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)

                # extracts levels from metadata lines
                levels = [row[1].split('=')[1] for row in reader if row and row[1].startswith("level=")]
                return levels
        except Exception as e:
            print(f"Error while retrieving levels: {e}")

        # if file is empty, returns empty
        return []

if __name__ == "__main__":
    maze = np.array([
        [0, 1, 1, 1, 1],
        [8, 0, 0, 1, 0],
        [1, 1, 0, 1, 3],
        [0, 0, 0, 0, 0],
        [0, 1, 0, 1, 1]
    ])
    dao = MazeDAOCSV("saved_levels", "levels.csv")
    dao.save_maze(maze)
