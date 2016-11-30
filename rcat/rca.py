import os
from osgeo import gdal
from osgeo import ogr
import shutil
from projectxml import ProjectXML

class RCAproject:
    """class to create and populate a project structure for RCA projects"""

    def __init__(self, projectName, projPath, ex_veg, hist_veg, network, frag_valley, rca, lrp='', thiessen='',
                 hucid='', hucname='', width_thresh=''):

        self.projectName = projectName
        self.ToolName = 'RCA'
        self.ToolVersion = '0.1'

        self.hucid = hucid
        self.hucname = hucname

        self.projPath = projPath
        self.ex_veg = ex_veg
        self.hist_veg = hist_veg
        self.network = network
        self.frag_valley = frag_valley
        self.rca = rca
        self.lrp = lrp
        self.thiessen = thiessen
        self.width_thresh = width_thresh

        self.xmlpath = self.projPath + '/rca.xml'

        newxml = ProjectXML(self.xmlpath, self.ToolName, self.ToolVersion, self.projectName)

        if not self.hucid == '':
            newxml.addMeta('HUCID', self.hucid, newxml.project)
        if not self.hucname == '':
            newxml.addMeta('HUCName', self.hucname, newxml.project)

        newxml.addRCARealization('RCA Realization 1', 1)

        if not self.width_thresh == '':
            newxml.addParameter("width_thresh", self.width_thresh, newxml.RCArealizations[0])

        self.set_structure(projPath)
        self.copy_datasets(projPath, ex_veg, hist_veg, network, frag_valley, rca, lrp, thiessen, newxml)

        newxml.write()

    def set_structure(self, projPath):
        """Sets up the folder structure for an RCA project"""

        if not os.path.exists(projPath):
            os.mkdir(projPath)

        if os.getcwd() is not projPath:
            os.chdir(projPath)

        os.mkdir('01_Inputs')
        os.mkdir('02_Analyses')
        os.chdir('01_Inputs')
        os.mkdir('01_Ex_Veg')
        os.mkdir('02_Hist_Veg')
        os.mkdir('03_Network')
        os.mkdir('04_VB_Accessibility')
        os.mkdir('05_LRP')
        os.chdir('01_Ex_Veg')
        os.mkdir('Ex_Veg_001')
        os.chdir('Ex_Veg_001')
        os.mkdir('Ex_Rip')
        os.mkdir('Ex_LUI')
        os.chdir(projPath + '/01_Inputs/02_Hist_Veg')
        os.mkdir('Hist_Veg_001')
        os.chdir('Hist_Veg_001')
        os.mkdir('Hist_Rip')
        os.chdir(projPath + '/01_Inputs/03_Network')
        os.mkdir('Network_001')
        os.chdir('Network_001')
        os.mkdir('Thiessen')
        os.chdir(projPath + '/01_Inputs/04_VB_Accessibility')
        os.mkdir('Frag_VB_001')
        os.chdir(projPath + '/01_Inputs/05_LRP')
        os.mkdir('LRP_001')
        os.chdir(projPath + '/02_Analyses')
        os.mkdir('Outputs_001')
        os.chdir(projPath)

    def copy_datasets(self, projPath, ex_veg, hist_veg, network, frag_valley, rca, lrp, thiessen, newxml):
        """Copies the existing data sets used to run RVD into the RCA project structure"""

        if os.getcwd() is not projPath:
            os.chdir(projPath)

        shutil.copytree(ex_veg, '01_Inputs/01_Ex_Veg/Ex_Veg_001/' + os.path.basename(ex_veg))

        newxml.addInput("Raster", "Existing Vegetation", newxml.project,
                        path='01_Inputs/01_Ex_Veg/Ex_Veg_001/' + os.path.basename(ex_veg), iid='EXVEG001')
        newxml.addInput("Raster", "Existing Vegetation", newxml.RCArealizations[0], inputref='EXVEG001')

        shutil.copytree(hist_veg, '01_Inputs/02_Hist_Veg/Hist_Veg_001/' + os.path.basename(hist_veg))

        newxml.addInput("Raster", "Historic Vegetation", newxml.project,
                        path='01_Inputs/02_Hist_Veg/Hist_Veg_001/' + os.path.basename(hist_veg), iid='HISTVEG001')
        newxml.addInput("Raster", "Historic Vegetation", newxml.RCArealizations[0], inputref='HISTVEG001')

        network_copy = '01_Inputs/03_Network/Network_001/' + os.path.basename(network)
        inNetwork = ogr.GetDriverByName('ESRI Shapefile').Open(network)
        ogr.GetDriverByName('ESRI Shapefile').CopyDataSource(inNetwork, network_copy)

        newxml.addInput("Vector", "Network", newxml.project, path=network_copy, iid='NETWORK001')
        newxml.addInput("Vector", "Network", newxml.RCArealizations[0], inputref='NETWORK001')

        frag_valley_copy = '01_Inputs/04_Valley/Valley_001/' + os.path.basename(frag_valley)
        inFragValley = ogr.GetDriverByName('ESRI Shapefile').Open(frag_valley)
        ogr.GetDriverByName('ESRI Shapefile').CopyDataSource(inFragValley, frag_valley_copy)

        newxml.addInput("Vector", "Valley Bottom Accessibility", newxml.project, path=frag_valley_copy, iid="VALLEY001")
        newxml.addInput("Vector", "Valley Bottom Accessibility", newxml.RCArealizations[0], inputref='VALLEY001')

        rca_copy = '02_Analyses/Outputs_001/' + os.path.basename(rca)
        inRca = ogr.GetDriverByName('ESRI Shapefile').Open(rca)
        ogr.GetDriverByName('ESRI Shapefile').CopyDataSource(inRca, rca_copy)

        newxml.addOutput("Analysis 001", "Vector", "RCA 001", rca_copy, newxml.RCArealizations[0])

        if not lrp == '':
            lrp_copy = '01_Inputs/05_LRP/LRP_001/' + os.path.basename(lrp)
            inLrp = ogr.GetDriverByName('ESRI Shapefile').Open(lrp)
            ogr.GetDriverByName('ESRI Shapefile').CopyDataSource(inLrp, lrp_copy)

            newxml.addInput("Vector", "Large River Polygon", newxml.project, path=lrp_copy, iid='LRP001')
            newxml.addInput("Vector", "Large River Polygon", newxml.RCArealizations[0], inputref='LRP001')

        if not thiessen == '':
            thiessen_copy = '01_Inputs/03_Network/Network_001/Thiessen/' + os.path.basename(thiessen)
            inThiessen = ogr.GetDriverByName('ESRI Shapefile').Open(thiessen)
            ogr.GetDriverByName('ESRI Shapefile').CopyDataSource(inThiessen, thiessen_copy)

            newxml.addInput("Vector", "Thiessen Polygons", newxml.RCArealizations[0], path=thiessen_copy)