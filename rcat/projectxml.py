import xml, os
import uuid
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

class ProjectXML:

    def __init__(self, filepath, projType, version, name):
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
        self.projectType.set('Version', version)
        self.projectType.text = projType

        # Add some containers we will fill out later
        self.Inputs = ET.SubElement(self.project, "Inputs")
        self.realizations = ET.SubElement(self.project, "Realizations")
        self.VBETrealizations = []
        self.RVDrealizations = []

    def addMeta(self, name, value, parentNode):
        metaNode = parentNode.find("MetaData")
        if metaNode is None:
            metaNode = ET.SubElement(parentNode, "MetaData")

        node = ET.SubElement(metaNode, "Meta")
        node.set("Name", name)
        node.text = str(value)

    def addInput(self, itype, name, parentNode, path='', iid='', iguid='', basepath='', inputref=''):
        if parentNode == self.project:
            typeNode = ET.SubElement(self.Inputs, itype)
            if iid is not '':
                typeNode.set('id', iid)
            if iguid is not '':
                typeNode.set('Guid', iguid)
            nameNode = ET.SubElement(typeNode, "Name")
            nameNode.text = str(name)
            if path is not '':
                pathNode = ET.SubElement(typeNode, "Path")
                pathNode.text = str(path)
            if basepath is not '':
                basepathNode = ET.SubElement(typeNode, "BasePath")
                basepathNode.text = str(basepath)
            if inputref is not '':
                filerefNode = ET.SubElement(typeNode, "InputRef")
                filerefNode.text = str(inputref)

        else:
            inputsNode = parentNode.find("Inputs")
            if inputsNode is None:
                inputsNode = ET.SubElement(parentNode, "Inputs")
            typeNode = ET.SubElement(inputsNode, itype)
            if iid is not '':
                typeNode.set('id', iid)
            if iguid is not '':
                typeNode.set('Guid', iguid)
            nameNode = ET.SubElement(typeNode, "Name")
            nameNode.text = str(name)
            if path is not '':
                pathNode = ET.SubElement(typeNode, "Path")
                pathNode.text = str(path)
            if basepath is not '':
                basepathNode = ET.SubElement(typeNode, "BasePath")
                basepathNode.text = str(basepath)
            if inputref is not '':
                filerefNode = ET.SubElement(typeNode, "InputRef")
                filerefNode.text = str(inputref)

    def addParameter(self, name, value, parentNode):
        paramNode = parentNode.find("Parameters")
        if paramNode is None:
            paramNode = ET.SubElement(parentNode, "Parameters")

        node = ET.SubElement(paramNode, "Param")
        node.set("Name", name)
        node.text = str(value)

    def addOutput(self, aname, otype, name, path, parentNode, basepath='', fileref=''):
        analysisNode = parentNode.find("Analysis")
        if analysisNode is None:
            analysisNode = ET.SubElement(parentNode, "Analysis")
            ET.SubElement(analysisNode, "Name").text = str(aname)
        outputsNode = analysisNode.find("Outputs")
        if outputsNode is None:
            outputsNode = ET.SubElement(analysisNode, "Outputs")

        typeNode = ET.SubElement(outputsNode, otype)
        nameNode = ET.SubElement(typeNode, "Name")
        nameNode.text = str(name)
        pathNode = ET.SubElement(typeNode, "Path")
        pathNode.text = str(path)

        if basepath is not '':
            basepathNode = ET.SubElement(typeNode, "BasePath")
            basepathNode.text = str(basepath)
        if fileref is not '':
            filerefNode = ET.SubElement(typeNode, "fileRef")
            filerefNode.text = str(fileref)

    def addVBETRealization(self, name, id):
        node = ET.SubElement(self.realizations, "VBET")
        node.set("id", str(id))
        node.set("Guid", self.getUUID())
        nameNode = ET.SubElement(node, "Name")
        nameNode.text = str(name)
        self.VBETrealizations.append(node)

    def addRVDRealization(self, name, id):
        node = ET.SubElement(self.realizations, "RVD")
        node.set("id", str(id))
        node.set("Guid", self.getUUID())
        nameNode = ET.SubElement(node, "Name")
        nameNode.text = str(name)
        self.RVDrealizations.append(node)

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