import xml.etree.ElementTree as ET
import numpy as np
from abc import ABC, abstractmethod

class MazeDAO(ABC):
    # creation of main DAO class
    @abstractmethod
    def __init__(self, database, filename):
        self.database = database

    @abstractmethod
    def save_maze(self, input_maze):
        pass

    @abstractmethod
    def load_maze(self, level):
        pass

class MazeDAOXML(MazeDAO):
    def __init__(self, database, filename):
        self.database = database
        self.filename = filename

    def save_maze(self, input_maze):
        # checks if old file is present
            # loads xml file
        data = f"{self.database}/{self.filename}"

        try:
            ET.parse(data)
        except FileNotFoundError:
            print("data is none")
            # creates the root element if file not present
            levels = ET.Element('levels')
        else:
            # reads the xml file
            tree = ET.parse(data)
            # accesses the levels element
            levels = tree.getroot()

        # user input for maze customization
        maze_name = str(input("Enter maze name:\n> "))
        maze_level = str(input("Enter maze level:\n> "))

        # creates maze element with an attribute
        maze = ET.SubElement(levels, 'maze', name=maze_name)

        # creates the level element
        level = ET.SubElement(maze, "level", number=maze_level)

        # iterates over rows and its cells
        for i, row in enumerate(input_maze):
            row_element = ET.SubElement(maze, 'row', id=str(i))
            for cell in row:
                ET.SubElement(row_element, 'cell', number=str(cell))

        # converts the tree to a byte string and writes it to a file
        tree = ET.ElementTree(levels)
        tree.write(f"{self.database}/{self.filename}", encoding="utf-8", xml_declaration=True)

        # for pretty-printing
        import xml.dom.minidom

        # converts xml tree to string, goes through elements and adds indentations and line breaks
        xml_str = ET.tostring(levels, encoding="unicode")
        dom = xml.dom.minidom.parseString(xml_str)
        pretty_xml_str = dom.toprettyxml()

        # writes the pretty-printed xml to a file
        with open(f"{self.database}/{self.filename}", "w") as f:
            f.write(pretty_xml_str)

    def load_maze(self, level):
        # loads xml file
        data = f"{self.database}/{self.filename}"
        # reads the xml file
        tree = ET.parse(data)
        root = tree.getroot()

        # find right maze, then row and reads number attribute of all elements named cell
        maze = [maze for maze in root.findall('maze') if maze.find('level').get('number') == str(level)]
        rows = []
        for row_element in maze[0].findall('row'):
            row = [int(cell.get('number')) for cell in row_element.findall('cell')]
            rows.append(row)

        # converts the indented list to an array
        maze = np.array(rows)
        return maze

if __name__ == "__main__":
    maze = np.array([
        [0, 1, 1, 1, 1],
        [8, 0, 0, 1, 0],
        [1, 1, 0, 1, 3],
        [0, 0, 0, 0, 0],
        [0, 1, 0, 1, 1]
    ])
    dao = MazeDAOXML("saved_levels","levels.xml")
    dao.save_maze(maze)

