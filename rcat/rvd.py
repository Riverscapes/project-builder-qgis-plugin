import os
from osgeo import gdal
from osgeo import ogr
import datetime
import shutil
import uuid
from projectxml import ProjectXML

class RVDproject:
    """class to create and populate a project structure for RVD projects"""

    def __init__(self, projectName, projPath, ex_veg, hist_veg, network, valleybottom, rvd, conversion="", lrp="",
                 thiessen="", hucid="", hucname=""):

        self.ProjectName = projectName
        self.ToolName = "RVD"
        self.ToolVersion = "0.1"

        self.hucid = hucid
        self.hucname = hucname
        self.time = datetime.datetime.now()

        self.projPath = projPath
        self.ex_veg = ex_veg
        self.hist_veg = hist_veg
        self.network = network
        self.valleybottom = valleybottom
        self.rvd = rvd
        self.conversion = conversion
        self.lrp = lrp
        self.thiessen = thiessen

        self.xmlpath = self.projPath + "/project.rs.xml"

        newxml = ProjectXML(self.xmlpath, self.ToolName, self.ProjectName)

        if not self.hucid == "":
            newxml.addMeta("HUCID", self.hucid, newxml.project)
        idlist = [int(x) for x in str(self.hucid)]
        if idlist[0] == 1 and idlist[1] == 7:
            newxml.addMeta("Region", "CRB", newxml.project)
        if not self.hucname == "":
            newxml.addMeta("Watershed", self.hucname, newxml.project)

        newxml.addRVDRealization("RVD Realization 1", rid="RZ1", dateCreated=self.time.strftime("%Y-%m-%d %H:%M:%S"),
                                 productVersion=self.ToolVersion, guid=self.getUUID())

        self.set_structure(projPath)
        self.copy_datasets(projPath, ex_veg, hist_veg, network, valleybottom, rvd, conversion, lrp, thiessen, newxml)

        newxml.write()

    def set_structure(self, projPath):
        """Sets up the folder structure for an RVD project"""

        if not os.path.exists(projPath):
            os.mkdir(projPath)

        if os.getcwd() is not projPath:
            os.chdir(projPath)

        os.mkdir("01_Inputs")
        os.mkdir("02_Analyses")
        os.chdir("01_Inputs")
        os.mkdir("01_Ex_Veg")
        os.mkdir("02_Hist_Veg")
        os.mkdir("03_Network")
        os.mkdir("04_Valley")
        os.mkdir("05_LRP")
        os.chdir("01_Ex_Veg")
        os.mkdir("Ex_Veg_1")
        os.chdir("Ex_Veg_1")
        os.mkdir("Ex_Rasters")
        os.chdir(projPath + "/01_Inputs/02_Hist_Veg")
        os.mkdir("Hist_Veg_1")
        os.chdir("Hist_Veg_1")
        os.mkdir("Hist_Rasters")
        os.chdir(projPath + "/01_Inputs/03_Network")
        os.mkdir("Network_1")
        os.chdir("Network_1")
        os.mkdir("Thiessen")
        os.chdir(projPath + "/01_Inputs/04_Valley")
        os.mkdir("Valley_1")
        os.chdir(projPath + "/01_Inputs/05_LRP")
        os.mkdir("LRP_1")
        os.chdir(projPath + "/02_Analyses")
        os.mkdir("Output_1")
        os.chdir(projPath)

    def copy_datasets(self, projPath, ex_veg, hist_veg, network, valleybottom, rvd, conversion, lrp, thiessen, newxml):
        """Copies the existing data sets used to run RVD into the RVD project structure"""

        if os.getcwd() is not projPath:
            os.chdir(projPath)

        shutil.copytree(ex_veg, "01_Inputs/01_Ex_Veg/Ex_Veg_1/" + os.path.basename(ex_veg))

        exvegpath = "01_Inputs/01_Ex_Veg/Ex_Veg_1/" + os.path.basename(ex_veg)
        newxml.addProjectInput("Raster", "Existing Vegetation", str(exvegpath), iid="EXVEG1", guid=self.getUUID())
        newxml.addRVDInput(newxml.RVDrealizations[0], "Existing Vegetation", ref="EXVEG1")

        shutil.copytree(hist_veg, "01_Inputs/02_Hist_Veg/Hist_Veg_1/" + os.path.basename(hist_veg))

        histvegpath = "01_Inputs/02_Hist_Veg/Hist_Veg_1/" + os.path.basename(hist_veg)
        newxml.addProjectInput("Raster", "Historic Vegetation", str(histvegpath), iid="HISTVEG1", guid=self.getUUID())
        newxml.addRVDInput(newxml.RVDrealizations[0], "Historic Vegetation", ref="HISTVEG1")

        network_copy = "01_Inputs/03_Network/Network_1/" + os.path.basename(network)
        inNetwork = ogr.GetDriverByName("ESRI Shapefile").Open(network)
        ogr.GetDriverByName("ESRI Shapefile").CopyDataSource(inNetwork, network_copy)

        newxml.addProjectInput("Vector", "Network", network_copy, iid="DN01", guid=self.getUUID())
        newxml.addRVDInput(newxml.RVDrealizations[0], "Network", ref="DN01")

        valleybottom_copy = "01_Inputs/04_Valley/Valley_1/" + os.path.basename(valleybottom)
        inValleybottom = ogr.GetDriverByName("ESRI Shapefile").Open(valleybottom)
        ogr.GetDriverByName("ESRI Shapefile").CopyDataSource(inValleybottom, valleybottom_copy)

        newxml.addProjectInput("Vector", "Valley Bottom", valleybottom_copy, iid="VALLEY1", guid=self.getUUID())
        newxml.addRVDInput(newxml.RVDrealizations[0], "Valley", ref="VALLEY1")

        rvd_copy = "02_Analyses/Output_1/" + os.path.basename(rvd)
        inRvd = ogr.GetDriverByName("ESRI Shapefile").Open(rvd)
        ogr.GetDriverByName("ESRI Shapefile").CopyDataSource(inRvd, rvd_copy)

        newxml.addOutput("Analysis 1", "Vector", "RVD 1", rvd_copy, newxml.RVDrealizations[0], guid=self.getUUID())

        if not conversion == "":
            conversion_copy = "02_Analyses/Output_1/" + os.path.basename(conversion)
            inConversion = gdal.Open(conversion)
            driver = gdal.GetDriverByName("GTiff")
            driver.CreateCopy(conversion_copy, inConversion)

            newxml.addOutput("Analysis 1", "Raster", "Conversion 1", conversion_copy, newxml.RVDrealizations[0],
                             guid=self.getUUID())

        if not lrp == "":
            lrp_copy = "01_Inputs/05_LRP/LRP_1/" + os.path.basename(lrp)
            inLrp = ogr.GetDriverByName("ESRI Shapefile").Open(lrp)
            ogr.GetDriverByName("ESRI Shapefile").CopyDataSource(inLrp, lrp_copy)

            newxml.addProjectInput("Vector", "Large River Polygon", lrp_copy, iid="LRP1", guid=self.getUUID())
            newxml.addRVDInput(newxml.RVDrealizations[0], "LRP", ref="LRP1")

        if not thiessen == "":
            thiessen_copy = "01_Inputs/03_Network/Network_1/Thiessen/" + os.path.basename(thiessen)
            inThiessen = ogr.GetDriverByName("ESRI Shapefile").Open(thiessen)
            ogr.GetDriverByName("ESRI Shapefile").CopyDataSource(inThiessen, thiessen_copy)

            newxml.addRVDInput(newxml.RVDrealizations[0], "Thiessen Polygons", name="Thiessen Polygons",
                               path=thiessen_copy, guid=self.getUUID())

    def getUUID(self):
        return str(uuid.uuid4()).upper()










