import xml.etree.ElementTree as ET

# load xml file to root element
xml_tree = ET.parse('country_data.xml')
xml_root = xml_tree.getroot()

# As an Element, root has children nodes over which we can iterate:
for child in xml_root:
    print(child.tag, child.attrib)

# Children are nested, and we can access specific child nodes by index:
print(xml_root[0][1].text)
