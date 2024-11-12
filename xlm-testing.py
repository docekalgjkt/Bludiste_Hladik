import xml.etree.ElementTree as ET

import numpy as np

maze = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

def save_to_xml(maze):
    # Create the root XML element
    root = ET.Element("Maze")

    # Iterate over each row in the array and create XML elements for each
    for i, row in enumerate(maze):
        # Create an XML element for the row
        row_element = ET.SubElement(root, "Row", id=str(i))  # 'id' attribute to distinguish rows
        for value in row:
            # Create an XML element for each cell in the row
            cell_element = ET.SubElement(row_element, "Cell")
            cell_element.text = str(value)  # Set the text of the cell element to the value

    # Convert the ElementTree to a string
    xml_data = ET.tostring(root, encoding="unicode")

    # Print or save the XML data
    print(xml_data)

    # Optional: Save to a file
    with open("maze.xml", "w") as file:
        file.write(xml_data)

save_to_xml(maze)