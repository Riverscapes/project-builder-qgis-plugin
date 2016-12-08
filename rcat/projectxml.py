import xml, os
import uuid
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

class ProjectXML:
    """creates an instance of a project xml file"""

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
        self.project.set('xsi:noNamespaceSchemaLocation', 'https://raw.githubusercontent.com/Riverscapes/Program/master/Project/XSD/V1/Project.xsd')

        # Set up the <Name> and <ProjectType> tags
        self.name = ET.SubElement(self.project, "Name")
        self.name.text = name
        self.projectType = ET.SubElement(self.project, "ProjectType")
        self.projectType.text = projType

        # Add some containers we will fill out later
        self.Inputs = ET.SubElement(self.project, "Inputs")
        self.realizations = ET.SubElement(self.project, "Realizations")
        self.VBETrealizations = []
        self.RVDrealizations = []
        self.RCArealizations = []

    def addMeta(self, name, value, parentNode):
        """adds metadata tags to the project xml document"""
        metaNode = parentNode.find("MetaData")
        if metaNode is None:
            metaNode = ET.SubElement(parentNode, "MetaData")

        node = ET.SubElement(metaNode, "Meta")
        node.set("name", name)
        node.text = str(value)

    def addProjectInput(self, itype, name, path, project='', iid='', guid='', ref=''):
        typeNode = ET.SubElement(self.Inputs, itype)
        if iid is not '':
            typeNode.set('id', iid)
        if guid is not '':
            typeNode.set('guid', guid)
        if ref is not '':
            typeNode.set('ref', ref)
        nameNode = ET.SubElement(typeNode, "Name")
        nameNode.text = str(name)
        pathNode = ET.SubElement(typeNode, "Path")
        pathNode.text = str(path)
        if project is not '':
            projectNode = ET.SubElement(typeNode, "Project")
            projectNode.text = str(project)

    def addVBETInput(self, parentNode, type, name='', path='', project='', iid='', guid='', ref=''):
        """adds input tags to the project xml documuent"""
        inputsNode = parentNode.find("Inputs")
        if inputsNode is None:
            inputsNode = ET.SubElement(parentNode, "Inputs")
        if type == 'DEM':
            topoNode = inputsNode.find("Topography")
            if topoNode is None:
                topoNode = ET.SubElement(inputsNode, "Topography")
            demNode = ET.SubElement(topoNode, "DEM")
            if name is not '':
                nameNode = ET.SubElement(demNode, "Name")
                nameNode.text = str(name)
            if path is not '':
                pathNode = ET.SubElement(demNode, "Path")
                pathNode.text = str(path)
            if project is not '':
                projectNode = ET.SubElement(demNode, "Project")
                projectNode.text = str(project)
            if iid is not '':
                demNode.set('id', iid)
            if guid is not '':
                demNode.set('guid', guid)
            if ref is not '':
                demNode.set('ref', ref)
        if type == 'Flow':
            topoNode = inputsNode.find("Topography")
            if topoNode is None:
                topoNode = ET.SubElement(inputsNode, "Topography")
            flowNode = ET.SubElement(topoNode, "Flow")
            if name is not '':
                nameNode = ET.SubElement(flowNode, "Name")
                nameNode.text = str(name)
            if path is not '':
                pathNode = ET.SubElement(flowNode, "Path")
                pathNode.text = str(path)
            if project is not '':
                projectNode = ET.SubElement(flowNode, "Project")
                projectNode.text = str(project)
            if iid is not '':
                flowNode.set('id', iid)
            if guid is not '':
                flowNode.set('guid', guid)
            if ref is not '':
                flowNode.set('ref', ref)
        if type == 'Slope':
            topoNode = inputsNode.find("Topography")
            if topoNode is None:
                topoNode = ET.SubElement(inputsNode, "Topography")
            slopeNode = ET.SubElement(topoNode, "Slope")
            if name is not '':
                nameNode = ET.SubElement(slopeNode, "Name")
                nameNode.text = str(name)
            if path is not '':
                pathNode = ET.SubElement(slopeNode, "Path")
                pathNode.text = str(path)
            if project is not '':
                projectNode = ET.SubElement(slopeNode, "Project")
                projectNode.text = str(project)
            if iid is not '':
                slopeNode.set('id', iid)
            if guid is not '':
                slopeNode.set('guid', guid)
            if ref is not '':
                slopeNode.set('ref', ref)
        if type == 'Network':
            dnNode = inputsNode.find("DrainageNetworks")
            if dnNode is None:
                dnNode = ET.SubElement(inputsNode, "DrainageNetworks")
            networkNode = ET.SubElement(dnNode, "Network")
            if name is not '':
                nameNode = ET.SubElement(networkNode, "Name")
                nameNode.text = str(name)
            if path is not '':
                pathNode = ET.SubElement(networkNode, "Path")
                pathNode.text = str(path)
            if project is not '':
                projectNode = ET.SubElement(networkNode, "Project")
                projectNode.text = str(project)
            if iid is not '':
                networkNode.set('id', iid)
            if guid is not '':
                networkNode.set('guid', guid)
            if ref is not '':
                networkNode.set('ref', ref)
        if type == 'Buffer':
            dnNode = inputsNode.find("DrainageNetworks")
            if dnNode is None:
                dnNode = ET.SubElement(inputsNode, "DrainageNetworks")
            networkNode = dnNode.find("Network")
            if networkNode is None:
                networkNode = ET.SubElement(dnNode, "Network")
            buffersNode = networkNode.find("Buffers")
            if buffersNode is None:
                buffersNode = ET.SubElement(networkNode, "Buffers")
            bufferNode = ET.SubElement(buffersNode, "Buffer")
            if name is not '':
                nameNode = ET.SubElement(bufferNode, "Name")
                nameNode.text = str(name)
            if path is not '':
                pathNode = ET.SubElement(bufferNode, "Path")
                pathNode.text = str(path)
            if project is not '':
                projectNode = ET.SubElement(bufferNode, "Project")
                projectNode.text = str(project)
            if iid is not '':
                bufferNode.set('id', iid)
            if guid is not '':
                bufferNode.set('guid', guid)
            if ref is not '':
                bufferNode.set('ref', ref)

    def addParameter(self, name, value, parentNode):
        """adds parameter tags to the project xml document"""
        paramNode = parentNode.find("Parameters")
        if paramNode is None:
            paramNode = ET.SubElement(parentNode, "Parameters")

        node = ET.SubElement(paramNode, "Param")
        node.set("name", name)
        node.text = str(value)

    def addOutput(self, aname, otype, name, path, parentNode, project='', oid='', guid='', ref=''):
        """adds an output tag to an analysis tag in the project xml document"""
        analysisNode = parentNode.find("Analysis")
        if analysisNode is None:
            analysisNode = ET.SubElement(parentNode, "Analysis")
            ET.SubElement(analysisNode, "Name").text = str(aname)
        outputsNode = analysisNode.find("Outputs")
        if outputsNode is None:
            outputsNode = ET.SubElement(analysisNode, "Outputs")

        typeNode = ET.SubElement(outputsNode, otype)
        if oid is not '':
            typeNode.set('id', oid)
        if guid is not '':
            typeNode.set('guid', guid)
        if ref is not '':
            typeNode.set('ref', ref)
        nameNode = ET.SubElement(typeNode, "Name")
        nameNode.text = str(name)
        pathNode = ET.SubElement(typeNode, "Path")
        pathNode.text = str(path)

        if project is not '':
            projectNode = ET.SubElement(typeNode, "Project")
            projectNode.text = str(project)

    def addVBETRealization(self, name, promoted='', dateCreated='', productVersion='', guid=''):
        """adds a VBET realization tag to the project xml document"""
        node = ET.SubElement(self.realizations, "VBET")
        if promoted is not '':
            node.set('promoted', promoted)
        if dateCreated is not '':
            node.set('dateCreated', dateCreated)
        if productVersion is not '':
            node.set('productVersion', productVersion)
        if guid is not '':
            node.set('guid', guid)
        nameNode = ET.SubElement(node, "Name")
        nameNode.text = str(name)

        self.VBETrealizations.append(node)

    def addRVDRealization(self, name, id):  # will need to update like VBET
        """adds an RVD realization tag to the project xml document"""
        node = ET.SubElement(self.realizations, "RVD")
        node.set("id", str(id))
        node.set("Guid", self.getUUID())
        nameNode = ET.SubElement(node, "Name")
        nameNode.text = str(name)
        self.RVDrealizations.append(node)

    def addRCARealization(self, name, id):  # will need to update like VBET
        """adds an RCA realization tag to the project xml document"""
        node = ET.SubElement(self.realizations, "RCA")
        node.set("id", str(id))
        node.set("Guid", self.getUUID())
        nameNode = ET.SubElement(node, "Name")
        nameNode.text = str(name)
        self.RCArealizations.append(node)

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