import numpy as np
from classes.AbstractDAO import MazeDAO


class MazeDAOText(MazeDAO):
    def __init__(self, database, filename):
        self.database = database
        self.filename = filename

    def save_maze(self, input_maze):
        # loads txt file
        data = f"../{self.database}/{self.filename}"

        maze_name = input("Enter maze name:\n> ")
        maze_level = input("Enter maze level:\n> ")

        # formats the maze as a string
        maze_string = f"Maze Name: {maze_name}\nMaze Level: {maze_level}\n"
        maze_string += "\n".join(" ".join(map(str, row)) for row in input_maze)

        # checks if the file exists and append or create it
        try:
            with open(data, "a") as file:
                file.write(maze_string + "\n\n")  # Append maze data with double blank lines
            print("Maze saved successfully.")
        except Exception as e:
            print(f"Error saving maze: {e}")

    def load_maze(self, level):
        # loads txt file
        data = f"{self.database}/{self.filename}"

        try:
            with open(data, "r") as file:
                content = file.read()

            # splits content into individual maze entries
            mazes = content.strip().split("\n\n")
            for maze_entry in mazes:
                lines = maze_entry.split("\n")
                maze_level = lines[1].split(":")[1].strip()  # extracts level number from first line
                if maze_level == str(level):
                    maze_data = lines[2:]  # extracts the maze rows
                    return np.array([[int(cell) for cell in row.split()] for row in maze_data])
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(f"Error loading maze: {e}")
        return None

    def get_all_levels(self):
        data = f"{self.database}/{self.filename}"
        levels = []

        try:
            with open(data, "r") as file:
                content = file.read()

            mazes = content.strip().split("\n\n")
            for maze_entry in mazes:
                lines = maze_entry.split("\n")
                level = lines[1].split(":")[1].strip()  # Extract level number
                levels.append(level)
        except Exception as e:
            print(f"Error while retrieving levels: {e}")

        return levels


if __name__ == "__main__":
    maze = np.array([
        [0, 1, 1, 1, 1],
        [8, 0, 0, 1, 0],
        [1, 1, 0, 1, 3],
        [0, 0, 0, 0, 0],
        [0, 1, 0, 1, 1]
    ])
    dao = MazeDAOText("saved_levels", "levels.txt")
    dao.save_maze(maze)
