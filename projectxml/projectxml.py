import xml, os
import uuid
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

class ProjectXML:

    def __init__(self, filepath, projType, name):
        self.logFilePath = filepath

        # File exists. Delete it.
        if os.path.isfile(self.logFilePath):
            os.remove(self.logFilePath)

        # Initialize the tree
        self.projectTree = ET.ElementTree(ET.Element("Project"))
        self.project = self.projectTree.getroot()

        # Set up a root Project node
        self.project.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        self.project.set('xsi:noNamespaceSchemaLocation', 'XSD/V1/Project.xsd')
        self.project.set("Guid", self.getUUID())

        # Set up the <Name> and <ProjectType> tags
        self.name = ET.SubElement(self.project, "Name")
        self.name.text = name
        self.projectType = ET.SubElement(self.project, "ProjectType")
        self.projectType.set('Version', '1')
        self.projectType.text = projType

        # Add some containers we will fill out later
        self.Inputs = ET.SubElement(self.project, "Inputs")
        self.realizations = ET.SubElement(self.project, "Realizations")

    def addMeta(self, name, value, parentNode):
        metaNode = parentNode.find("metadata")
        if metaNode is None:
            metaNode = ET.SubElement(parentNode, "metadata")

        node = ET.SubElement(metaNode, "Meta")
        node.set("Name", name)
        node.text = str(value)

    def addVBETRealization(self, name, id):
        node = ET.SubElement(self.realizations, "VBET")
        node.set("id", str(id))
        node.set("Guid", self.getUUID())
        nameNode = ET.SubElement(node, "Name")
        nameNode.text = str(name)

    def write(self):
        """
        Return a pretty-printed XML string for the Element.
        then write it out to the expected file
        """
        rough_string = ET.tostring(self.project, encoding='utf8', method='xml')
        reparsed = minidom.parseString(rough_string)
        pretty = reparsed.toprettyxml(indent="\t")
        f = open(self.logFilePath, "wb")
        f.write(pretty)
        f.close()

    def getUUID(self):
        return str(uuid.uuid4()).upper()