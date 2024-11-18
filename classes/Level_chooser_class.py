import tkinter as tk
from tkinter import simpledialog

class LevelChooser:
    def __init__(self, title="Popup"):
        # sets up the main window (hidden)
        self.root = tk.Tk()
        self.root.withdraw()  # hides the root window
        self.title = title

    def message_popup(self, levels):
        # creates a popup message box with radio buttons for each level (og chat cooked this one)
        if not levels:
            print("Level database is empty")
        # custom dialog class for radio button popup
        class RadioDialog(simpledialog.Dialog):
            def body(self, master):
                self.selection = tk.StringVar(value=levels[0])  # Default value
                tk.Label(master, text="Choose a level:").pack(anchor="w")
                for level in levels:
                    tk.Radiobutton(master, text=str(level), variable=self.selection, value=level).pack(anchor="w")
                return master

            def apply(self):
                self.result = self.selection.get()

        # launches the popup
        return RadioDialog(self.root, title=self.title).result

# Example usage
if __name__ == "__main__":
    popup = LevelChooser(title="Select Difficulty Level")
    selected_level = popup.message_popup(["Easy", "Medium", "Hard"])
    print(f"You selected: {selected_level}")