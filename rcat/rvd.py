import os
from osgeo import gdal
from osgeo import ogr
from projectxml import ProjectXML

class RVDproject:
    """class to create and populate a project structure for RVD projects"""

    def __init__(self, projPath, ex_veg, hist_veg, network, valleybottom, rvd, conversion='', lrp='', hucid='', hucname=''):

        self.ProjectName = 'Sample RVD Project'
        self.ToolName = 'RVD'
        self.ToolVersion = '0.1'

        self.hucid = hucid
        self.hucname = hucname

        self.projPath = projPath
        self.ex_veg = ex_veg
        self.hist_veg = hist_veg
        self.network = network
        self.valleybottom = valleybottom
        self.rvd = rvd
        self.conversion = conversion
        self.lrp = lrp

        self.xmlpath = self.projPath + '/rvd.xml'

        newxml = ProjectXML(self.xmlpath, self.ToolName, self.ProjectName)

        if not self.hucid == '':
            newxml.addMeta('HUCID', self.hucid, newxml.project)
        if not self.hucname == '':
            newxml.addMeta('HUCName', self.hucname, newxml.project)

        newxml.addRVDRealization('RVD Realization 1', 1)

        self.set_structure(projPath)
        self.copy_datasets(projPath, ex_veg, hist_veg, network, valleybottom, rvd, conversion, lrp, newxml)

        newxml.write()

    def set_structure(self, projPath):
        """Sets up the folder structure for an RVD project"""

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
        os.mkdir('04_Valley')
        os.mkdir('05_LRP')
        os.chdir('01_Ex_Veg')
        os.mkdir('Ex_Veg_001')
        os.chdir('Ex_Veg_001')
        os.mkdir('Ex_Rasters')
        os.chdir(projPath + '/01_Inputs/02_Hist_Veg')
        os.mkdir('Hist_Veg_001')
        os.chdir('Hist_Veg_001')
        os.mkdir('Hist_Rasters')
        os.chdir(projPath + '/01_Inputs/03_Network')
        os.mkdir('Network_001')
        os.chdir('Network_001')
        os.mkdir('Thiessen')
        os.chdir(projPath + '/01_Inputs/04_Valley')
        os.mkdir('Valley_001')
        os.chdir(projPath + '/01_Inputs/05_LRP')
        os.mkdir('LRP_001')
        os.chdir(projPath + '/02_Analyses')
        os.mkdir('Outputs_001')
        os.chdir(projPath)

    def copy_datasets(self, projPath, ex_veg, hist_veg, network, valleybottom, rvd, conversion, lrp, newxml):
        """Copies the existing data sets used to run RVD into the RVD project structure"""

        if os.getcwd() is not projPath:
            os.chdir(projPath)

        ex_veg_copy = '01_Inputs/01_Ex_Veg/Ex_Veg_001/' + os.path.basename(ex_veg)
        inEx_veg = gdal.Open(ex_veg)
        driver = gdal.GetDriverByName('AAIGrid')
        driver.CreateCopy(ex_veg_copy, inEx_veg)

        newxml.addInput("Raster", "Existing Vegetation", newxml.project, path=ex_veg_copy, iid='EXVEG001')
        newxml.addInput("Raster", "Existing Vegetation", newxml.RVDrealizations[0], inputref='EXVEG001')

        hist_veg_copy = '01_Inputs/02_Hist_Veg/Hist_Veg_001/' + os.path.basename(hist_veg)
        inHist_veg = gdal.Open(hist_veg)
        driver = gdal.GetDriverByName('AAIGrid')
        driver.CreateCopy(hist_veg_copy, inHist_veg)

        newxml.addInput("Raster", "Historic Vegetation", newxml.project, path=hist_veg_copy, iid='HISTVEG001')
        newxml.addInput("Raster", "Historic Vegetation", newxml.RVDrealizations[0], inputref='HISTVEG001')

        network_copy = '01_Inputs/03_Network/Network_001/' + os.path.basename(network)
        inNetwork = ogr.GetDriverByName('ESRI Shapefile').Open(network)
        ogr.GetDriverByName('ESRI Shapefile').CopyDataSource(inNetwork, network_copy)

        newxml.addInput("Vector", "Network", newxml.project, path=network_copy, iid='NETWORK001')
        newxml.addInput("Vector", "Network", newxml.RVDrealizations[0], inputref='NETWORK001')

        valleybottom_copy = '01_Inputs/04_Valley/Valley_001/' + os.path.basename(valleybottom)
        inValleybottom = ogr.GetDriverByName('ESRI Shapefile').Open(valleybottom)
        ogr.GetDriverByName('ESRI Shapefile').CopyDataSource(inValleybottom, valleybottom_copy)

        newxml.addInput("Vector", "Valley Bottom", newxml.project, path=valleybottom_copy, iid="VALLEY001")
        newxml.addInput("Vector", "Valley Bottom", newxml.RVDrealizations[0], inputref='VALLEY001')

        rvd_copy = '02_Analyses/Outputs_001/' + os.path.basename(rvd)
        inRvd = ogr.GetDriverByName('ESRI Shapefile').Open(rvd)
        ogr.GetDriverByName('ESRI Shapefile').CopyDataSource(inRvd, rvd_copy)

        newxml.addOutput("Analysis 001", "Vector", "RVD 001", rvd_copy, newxml.RVDrealizations[0])

        if not conversion == '':
            conversion_copy = '02_Analyses/Outputs_001/' + os.path.basename(conversion)
            inConversion = gdal.Open(conversion)
            driver = gdal.GetDriverByName('GTiff')
            driver.CreateCopy(conversion_copy, inConversion)

            newxml.addOutput("Analysis 001", "Raster", "Conversion 001", conversion_copy, newxml.RVDrealizations[0])

        if not lrp == '':
            lrp_copy = '01_Inputs/05_LRP/LRP_001/' + os.path.basename(lrp)
            inLrp = ogr.GetDriverByName('ESRI Shapefile').Open(lrp)
            ogr.GetDriverByName('ESRI Shapefile').CopyDataSource(inLrp, lrp_copy)

            newxml.addInput("Vector", "Large River Polygon", newxml.project, path=lrp_copy, iid='LRP001')
            newxml.addInput("Vector", "Large River Polygon", newxml.RVDrealizations[0], inputref='LRP001')










