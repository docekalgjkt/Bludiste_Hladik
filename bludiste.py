import time
import numpy as np
import tkinter as tk
from flood_fill_algorithm import FloodFill


class Maze:
    def __init__(self):
        self.maze = np.array([
            [0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
            [8, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [0, 0, 0, 1, 3, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])

        filename = 'maze_file.npz'

        np.savez(filename, maze=self.maze)

        loaded_data = np.load(filename)
        self.maze = loaded_data['maze']


class Robot:
    def __init__(self,maze):
        self.maze = maze
        self.posx = np.where(maze == 8)[1][0]
        self.posy = np.where(maze == 8)[0][0]
        self.start_position = (np.where(maze == 8)[0][0],np.where(maze == 8)[1][0])
        # rightward, forward, leftward, backward
            # normalized (x,y)
        self.directions = [(1,0),(0,-1),(-1,0),(0,1)]
        self.status = True

    def move(self):
        window.label.config(text="...")
        alg = FloodFill(self.maze)
        alg.flood()
        transformed = alg.transformed
        print(transformed)
        current_position = self.start_position
        start_time = time.time()

        while True:
            # if reached the goal
            if transformed[current_position[0], current_position[1]] == 1:
                print("Reached the destination!")
                window.label.config(text=f"{time.time()-start_time:.1f}s")
                break

            next_position = None
            min_value = np.inf

            # checks neighboring cells for the next move
            for dir in self.directions:
                new_y = current_position[0] + dir[0]
                new_x = current_position[1] + dir[1]

                # checks bounds
                if 0 <= new_y < transformed.shape[0] and 0 <= new_x < transformed.shape[1]:
                    cell_value = transformed[new_y, new_x]

                    # searching for the lowest non-infinity value
                    if min_value > cell_value > 0:  # avoids walls (inf.) and only considers cells filled with legal number
                        min_value = cell_value
                        next_position = (new_y, new_x)

            if next_position is None:  # If no valid moves are available, we're stuck
                window.label.config(text=f"Can't solve this maze")
                break

            current_position = next_position  # Move to the next position
            self.posx = next_position[1]
            self.posy = next_position[0]

            window.character_draw()
            window.root.update()

            time.sleep(0.2)



class Window:
    def __init__(self,root):
        self.root = root
        self.root.title("Maze")

        self.width = (100/len(maze.maze[0]))*50
        self.height = (100/len(maze.maze))*50
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="white", relief="solid", border=5)
        self.canvas.pack(side="left")

        self.label = tk.Label(root, text="...", font=("Helvetica", 16))
        self.label.pack(side="top")

        self.frame = tk.Frame(root)
        self.frame.pack(side="right")

        self.button = tk.Button(self.frame, text="Start", width=10, height=4, command=robot.move)
        self.button.pack()

        self.character_rectangle = None
        self.character_label = None

        self.maze_creation()
        self.character_draw()

    def maze_creation(self):
        print(self.width/len(maze.maze[0]))
        print(self.height/len(maze.maze))
        for row in range(len(maze.maze)):
            for col in range(len(maze.maze[row])):
                color = "black" if maze.maze[row][col] == 1 else "white"
                x1, y1 = col * self.width/len(maze.maze[0])+5, row * self.height/len(maze.maze)+5
                x2, y2 = x1 + self.width/len(maze.maze[0])+5, y1 + self.height/len(maze.maze)+5
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        posy = np.where(maze.maze == 3)[1][0]
        posx = np.where(maze.maze == 3)[0][0]
        x1, y1 = (posy * self.width/len(maze.maze[0])+5,
                  posx * self.height/len(maze.maze)+5)
        x2, y2 = (x1 + self.width/len(maze.maze[0]),
                  y1 + self.height/len(maze.maze))
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="lightgreen")
        self.canvas.create_window(x1+self.width/len(maze.maze[0])/2.3, y2-self.width/len(maze.maze)/2.3,
                                  window=tk.Label(self.canvas, text="Finish", bg="green", fg="white",
                                                                  font=("Helvetica",int(self.width/len(maze.maze)/10))))

    def character_draw(self):
        if self.character_rectangle is not None:
            self.canvas.delete(self.character_rectangle)
            self.canvas.delete(self.character_label)

        character = robot
        posx = character.posy
        posy = character.posx
        x1, y1 = (posy * self.width / len(maze.maze[0]) + 5,
                  posx * self.height / len(maze.maze) + 5)
        x2, y2 = (x1 + self.width / len(maze.maze[0]),
                  y1 + self.height / len(maze.maze))
        self.character_rectangle = self.canvas.create_oval(x1, y1, x2, y2, fill="red", outline="darkred")
        self.character_label = self.canvas.create_window(x1+self.width/len(maze.maze[0])/2.3, y2-self.width/len(maze.maze)/2.3,
                                                         window=tk.Label(self.canvas, text="Character", bg="red", fg="white",
                                                  font=("Helvetica", int(self.width/len(maze.maze)/10))))


maze = Maze()
robot = Robot(maze.maze)

if __name__ == "__main__":
    root = tk.Tk()
    window = Window(root)
    root.mainloop()
