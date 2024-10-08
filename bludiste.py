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
            print("Cant go there")
        else:
            if self.maze[self.posy + dir[1], self.posx + dir[0]] == 1 or self.posx+dir[0] < 0 or self.posy+dir[1] < 0:
                print("Cant go there")
            elif self.maze[self.posy + dir[1], self.posx + dir[0]] == 3:
                print("You won!")
                global status
                status = False
            else:
                self.maze[self.posy + dir[1], self.posx + dir[0]] = 8
                self.maze[self.posy, self.posx] = 0
                self.posx +=dir[0]
                self.posy +=dir[1]

                for row in self.maze:
                    print(" ".join(f"{i:2d}" for i in row))


class Window:
    def __init__(self,root):
        self.root = root
        self.root.title("Maze")

        self.canvas = tk.Canvas(root, width=400, height=400, bg="white", borderwidth=5, relief="solid")
        self.canvas.pack()

    def maze_creation(self):
        for i in maze.maze:
            if i == 1:
                color = "black"
            else:
                color = "white"
            self.canvas.create_rectangle(1,1,1,1, fill=color)

maze = Maze()
player = Player(maze.maze)

print("Init maze:")
for row in maze.maze:
    print(" ".join(f"{i:2d}" for i in row))
print("")

status = False
while status:
    player.move(str(input("> ")))

if __name__ == "__main__":
    root = tk.Tk()
    window = Window(root)
    root.mainloop()
    window.maze_creation()
