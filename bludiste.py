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
            if self.maze[self.posy + dir[1], self.posx + dir[0]] == 1 or self.posx+dir[0] < 0 or self.posy+dir[1] < 0:
                window.label.config(text="Cant go there")
            else:
                if self.maze[self.posy + dir[1], self.posx + dir[0]] == 3:
                    window.label.config(text="You won!")
                    global status
                    status = False

                self.maze[self.posy + dir[1], self.posx + dir[0]] = 8
                self.maze[self.posy, self.posx] = 0
                self.posx +=dir[0]
                self.posy +=dir[1]

                window.player_draw()


class Window:
    def __init__(self,root):
        self.root = root
        self.root.title("Maze")

        width = len(maze.maze[0])*100-10
        height = len(maze.maze)*100-10
        self.canvas = tk.Canvas(root, width=width, height=height, bg="white", relief="solid", border=5)
        self.canvas.pack(side="left")

        self.label = tk.Label(root, text="...", font=("", 16))
        self.label.pack(side="top")

        self.frame = tk.Frame(root)
        self.frame.pack(side="right")

        self.button = tk.Button(self.frame, text="W", width=10, height=4, command=lambda: player.move("w"))
        self.button.grid(row=1,column=1)

        self.button = tk.Button(self.frame, text="A", width=10, height=4, command=lambda: player.move("a"))
        self.button.grid(row=2,column=0)

        self.button = tk.Button(self.frame, text="S", width=10, height=4, command=lambda: player.move("s"))
        self.button.grid(row=2,column=1)

        self.button = tk.Button(self.frame, text="D", width=10, height=4, command=lambda: player.move("d"))
        self.button.grid(row=2,column=3)

        self.player_rec = None

        self.maze_creation()
        self.player_draw()

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

    def player_draw(self):
        if self.player_rec is not None:
            self.canvas.delete(self.player_rec)
        posx = player.posy
        posy = player.posx
        x1, y1 = posy * 100+10, posx * 100+10
        x2, y2 = x1 + 80, y1 + 80
        self.player_rec = self.canvas.create_oval(x1, y1, x2, y2, fill="red", outline="darkred")


maze = Maze()
player = Player(maze.maze)

status = False
while status:
    player.move(str(input("> ")))

if __name__ == "__main__":
    root = tk.Tk()
    window = Window(root)
    root.mainloop()
