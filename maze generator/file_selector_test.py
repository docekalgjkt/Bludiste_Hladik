import tkinter as tk
from tkinter import filedialog

def select_file(file_types=None, title="Select a File"):
    if file_types is None:
        file_types = [("Numpy array", "*.npy")]
    root = tk.Tk()
    root.withdraw()

    # Open the file dialog
    file_path = filedialog.askopenfilename(filetypes=file_types, title=title)

    # Return the selected file path (or None if no file was selected)
    return file_path

# Example usage:
if __name__ == "__main__":
    selected_file = select_file(file_types=None, title="Select Your File")
    if selected_file:
        print(f"Selected file: {selected_file}")
    else:
        print("No file selected.")