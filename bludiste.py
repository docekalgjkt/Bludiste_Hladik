import time
import numpy as np
import tkinter as tk


class Maze:
    def __init__(self):
        self.maze = np.array([
            [0, 1, 1, 3, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 8, 1, 0],
            [0, 0, 1, 0, 0],
            [1, 0, 0, 0, 1]
        ])

        filename = 'maze_file.npz'

        np.savez(filename, maze=self.maze)

        loaded_data = np.load(filename)
        self.maze = loaded_data['maze']


class Player:
    def __init__(self,maze):
        self.maze = maze
        self.posx = np.where(maze == 8)[1][0]
        self.posy = np.where(maze == 8)[0][0]

    def direction(self, input):
        # normalized (x,y)
        if input == "w":
            return 0, -1
        elif input == "a":
            return -1, 0
        elif input == "s":
            return 0, 1
        elif input == "d":
            return 1, 0

    def move(self, input):
        dir = self.direction(input)
        try:
            self.maze[self.posy + dir[1], self.posx + dir[0]]
        except IndexError:
            window.label.config(text="Cant go there")
        else:
            if self.maze[self.posy + dir[1], self.posx + dir[0]] == 1 or self.posx + dir[0] < 0 or self.posy + dir[1] < 0:
                window.label.config(text="Cant go there")
            else:
                window.label.config(text="...")

                if self.maze[self.posy + dir[1], self.posx + dir[0]] == 3:
                    can_win = True
                    window.label.config(text="You won!")

                self.maze[self.posy + dir[1], self.posx + dir[0]] = 8
                self.maze[self.posy, self.posx] = 0
                self.posx +=dir[0]
                self.posy +=dir[1]

                window.character_draw()


class Robot:
    def __init__(self,maze):
        self.maze = maze
        self.posx = np.where(maze == 8)[1][0]
        self.posy = np.where(maze == 8)[0][0]
        # rightward, forward, leftward, backward
            # normalized (x,y)
        self.directions = [(1,0),(0,-1),(-1,0),(0,1)]
        self.status = True

    def rotate(self):
        # shifts the tuples in directions one to the right (rotates the list as a loop)
        self.directions = self.directions[1:] + [self.directions[0]]

    def move(self):
        while self.status:
            to_go = []
            for dir in self.directions:
                try:
                    self.maze[self.posy + dir[1], self.posx + dir[0]]
                except IndexError:
                    continue
                else:
                    if (self.posx + dir[0] >= 0 and self.posy + dir[1] >= 0) and not self.maze[self.posy + dir[1], self.posx + dir[0]] == 1:
                        to_go.append(dir)

            for dir in to_go:
                window.label.config(text="...")

                if self.maze[self.posy + dir[1], self.posx + dir[0]] == 3:
                    window.label.config(text="You won!")
                    self.status = False

                self.maze[self.posy + dir[1], self.posx + dir[0]] = 8
                self.maze[self.posy, self.posx] = 0
                self.posx += dir[0]
                self.posy += dir[1]

                window.character_draw()
                window.root.update()

                altered_directions = self.directions[2:] + self.directions[:2]
                if dir == altered_directions[0] or dir == altered_directions[1] or dir == altered_directions[2]:
                    for i in range(altered_directions.index(dir)+1):
                        self.rotate()


                time.sleep(0.2)
                break




class Window:
    def __init__(self,root):
        self.root = root
        self.root.title("Maze")

        width = len(maze.maze[0])*100-10
        height = len(maze.maze)*100-10
        self.canvas = tk.Canvas(root, width=width, height=height, bg="white", relief="solid", border=5)
        self.canvas.pack(side="left")

        self.label = tk.Label(root, text="...", font=("Helvetica", 16))
        self.label.pack(side="top")

        self.frame = tk.Frame(root)
        self.frame.pack(side="right")

        if not robot_enabled:
            self.button = tk.Button(self.frame, text="W", width=10, height=4, command=lambda: player.move("w"))
            self.button.grid(row=1,column=1)

            self.button = tk.Button(self.frame, text="A", width=10, height=4, command=lambda: player.move("a"))
            self.button.grid(row=2,column=0)

            self.button = tk.Button(self.frame, text="S", width=10, height=4, command=lambda: player.move("s"))
            self.button.grid(row=2,column=1)

            self.button = tk.Button(self.frame, text="D", width=10, height=4, command=lambda: player.move("d"))
            self.button.grid(row=2,column=3)
        else:
            self.button = tk.Button(self.frame, text="Start", width=10, height=4, command=robot.move)
            self.button.pack()

        self.character_rectangle = None
        self.character_label = None

        self.maze_creation()
        self.character_draw()

    def maze_creation(self):
        for row in range(len(maze.maze)):
            for col in range(len(maze.maze[row])):
                color = "black" if maze.maze[row][col] == 1 else "white"
                x1, y1 = col * 100, row * 100
                x2, y2 = x1 + 100, y1 + 100
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        posy = np.where(maze.maze == 3)[1][0]
        posx = np.where(maze.maze == 3)[0][0]
        x1, y1 = posy * 100 + 10, posx * 100 + 10
        x2, y2 = x1 + 80, y1 + 80
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="lightgreen")
        self.canvas.create_window(x1+40, y2-40, window=tk.Label(self.canvas, text="Finish", bg="green", fg="white",
                                                                  font=("Helvetica",10)))

    def character_draw(self):
        if self.character_rectangle is not None:
            self.canvas.delete(self.character_rectangle)
            self.canvas.delete(self.character_label)

        character = robot if robot_enabled else False
        posx = character.posy
        posy = character.posx
        x1, y1 = posy * 100+10, posx * 100+10
        x2, y2 = x1 + 80, y1 + 80
        self.character_rectangle = self.canvas.create_oval(x1, y1, x2, y2, fill="red", outline="darkred")
        self.character_label = self.canvas.create_window(x1+40, y2-40, window=tk.Label(self.canvas, text="Character", bg="red", fg="white",
                                                  font=("Helvetica", 10)))


maze = Maze()
player = Player(maze.maze)
robot = Robot(maze.maze)
robot_enabled = True

if __name__ == "__main__":
    root = tk.Tk()
    window = Window(root)
    root.mainloop()
