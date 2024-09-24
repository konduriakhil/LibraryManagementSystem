import json
import xml.etree.ElementTree as ET

# Load the JSON data
with open('trivy-report.json') as json_file:
    data = json.load(json_file)

# Function to convert JSON to XML
def dict_to_xml(tag, d):
    elem = ET.Element(tag)
    for key, val in d.items():
        child = ET.Element(key)
        child.text = str(val)
        elem.append(child)
    return elem

root = dict_to_xml('trivyReport', data)
tree = ET.ElementTree(root)

# Save the XML output
with open('trivy-report.xml', 'wb') as xml_file:
    tree.write(xml_file)
