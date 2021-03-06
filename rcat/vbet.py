import os
from osgeo import gdal
from osgeo import ogr
import datetime
import uuid
from projectxml import ProjectXML


class VBETproject:
    """class to create and populate a project structure for V-BET projects"""

    def __init__(self, projectName, projPath, dem, network, output_edited, flow="", slope="", output_unedited="",
                 huc_id="", huc_name="", smbuf="", medbuf="", lgbuf="", lowda="", highda="",
                 lgslope="", medslope="", smslope=""):

        self.ProjectName = projectName
        self.ToolName = "VBET"
        self.ToolVersion = "0.1"

        self.huc_id = huc_id
        self.huc_name = huc_name

        self.proj_path = projPath
        self.dem_path = dem
        self.network_path = network
        self.output_edited_path = output_edited
        self.flow_path = flow
        self.slope_path = slope
        self.output_unedited_path = output_unedited
        self.huc_id = huc_id
        self.huc_name = huc_name
        self.time = datetime.datetime.now()
        self.smbuf = smbuf
        self.medbuf = medbuf
        self.lgbuf = lgbuf
        self.lowda = lowda
        self.highda = highda
        self.lgslope = lgslope
        self.medslope = medslope
        self.smslope = smslope

        self.xmlpath = self.proj_path + "/project.rs.xml"

        # check that project doesn't already exist/folder structure isn't already created
        if os.path.exists(self.proj_path + "/01_Inputs"):
            raise Exception("This project may already exist.  If you wish to re-run, delete existing project folder.")

        newxml = ProjectXML(self.xmlpath, self.ToolName, self.ProjectName)

        if not self.huc_id == "":
            newxml.addMeta("HUCID", self.huc_id, newxml.project)
        idlist = [int(x) for x in str(self.huc_id)]
        if idlist[0] == 1 and idlist[1] == 7:
            newxml.addMeta("Region", "CRB", newxml.project)
        if not self.huc_name == "":
            newxml.addMeta("Watershed", self.huc_name, newxml.project)

        newxml.addVBETRealization("VBET Realization 1", rid="RZ1", dateCreated=self.time.strftime("%Y-%m-%d %H:%M:%S"),
                                  productVersion=self.ToolVersion, guid=self.getUUID())

        if not self.smbuf == "":
            newxml.addParameter("sm_buf", self.smbuf, newxml.VBETrealizations[0])
        if not self.medbuf == "":
            newxml.addParameter("med_buf", self.medbuf, newxml.VBETrealizations[0])
        if not self.lgbuf == "":
            newxml.addParameter("lg_buf", self.lgbuf, newxml.VBETrealizations[0])
        if not self.lowda == "":
            newxml.addParameter("low_da", self.lowda, newxml.VBETrealizations[0])
        if not self.highda == "":
            newxml.addParameter("high_da", self.highda, newxml.VBETrealizations[0])
        if not self.lgslope == "":
            newxml.addParameter("lg_slope", self.lgslope, newxml.VBETrealizations[0])
        if not self.medslope == "":
            newxml.addParameter("med_slope", self.medslope, newxml.VBETrealizations[0])
        if not self.smslope == "":
            newxml.addParameter("sm_slope", self.smslope, newxml.VBETrealizations[0])

        self.set_structure(projPath)
        self.copy_datasets(projPath, dem, network, output_edited, flow, slope, output_unedited, newxml)

        newxml.write()

    def set_structure(self, proj_path):
        """Sets up the folder structure for a V-BET project"""

        if not os.path.exists(proj_path):
            os.mkdir(proj_path)

        if os.getcwd() is not proj_path:
            os.chdir(proj_path)

        os.mkdir("01_Inputs")
        os.mkdir("02_Analyses")
        os.chdir("01_Inputs")
        os.mkdir("01_Topo")
        os.mkdir("02_Network")
        os.chdir("01_Topo")
        os.mkdir("DEM_1")
        os.chdir("DEM_1")
        os.mkdir("Slope")
        os.mkdir("Flow")
        os.chdir(proj_path + "/01_Inputs/02_Network/")
        os.mkdir("Network_1")
        os.chdir("Network_1")
        os.mkdir("Buffers")
        os.chdir(proj_path + "/02_Analyses/")
        os.mkdir("Output_1")
        os.chdir(proj_path)

    def copy_datasets(self, proj_path, dem_path, network_path, output_edited_path, flow_path, slope_path,
                      output_unedited_path, newxml):
        """Copies the existing data sets used to run V-BET into the V-BET project structure"""

        if os.getcwd() is not proj_path:
            os.chdir(proj_path)

        fname, fext = os.path.splitext(dem_path)
        dem_copy = "01_Inputs/01_Topo/DEM_1/" + os.path.basename(dem_path)
        inDEM = gdal.Open(dem_path)
        if fext == ".tif":
            driver = gdal.GetDriverByName("GTiff")
            driver.CreateCopy(dem_copy, inDEM)
        elif fext == ".img":
            driver = gdal.GetDriverByName("HFA")
            driver.CreateCopy(dem_copy, inDEM)
        else:
            raise Exception("input DEM is not type .tif or .img")
        del fname, fext

        newxml.addProjectInput("DEM", "DEM", dem_copy, iid="DEM1", guid=self.getUUID())
        newxml.addVBETInput(newxml.VBETrealizations[0], "DEM", ref="DEM1")

        network_copy = "01_Inputs/02_Network/Network_1/" + os.path.basename(network_path)
        inNetwork = ogr.GetDriverByName("ESRI Shapefile").Open(network_path)
        ogr.GetDriverByName("ESRI Shapefile").CopyDataSource(inNetwork, network_copy)

        newxml.addProjectInput("Vector", "Drainage Network", network_copy, iid="DN1", guid=self.getUUID())
        newxml.addVBETInput(newxml.VBETrealizations[0], "Network", ref="DN1")

        output_edited_copy = "02_Analyses/Output_1/" + os.path.basename(output_edited_path)
        inOutput_edited = ogr.GetDriverByName("ESRI Shapefile").Open(output_edited_path)
        ogr.GetDriverByName("ESRI Shapefile").CopyDataSource(inOutput_edited, output_edited_copy)

        newxml.addOutput("Analysis 1", "Vector", "Edited Valley Bottom", output_edited_copy, newxml.VBETrealizations[0],
                         guid=self.getUUID())

        if not flow_path == "":
            fname, fext = os.path.splitext(flow_path)
            flow_copy = "01_Inputs/01_Topo/DEM_1/Flow/" + os.path.basename(flow_path)
            inFlow = gdal.Open(flow_path)
            if fext == ".tif":
                driver = gdal.GetDriverByName("GTiff")
                driver.CreateCopy(flow_copy, inFlow)
            elif fext == ".img":
                driver = gdal.GetDriverByName("HFA")
                driver.CreateCopy(flow_copy, inFlow)
            else:
                raise Exception("drainage area raster is not type .tif or .img")
            del fname, fext

            newxml.addVBETInput(newxml.VBETrealizations[0], "Flow", name="Drainage Area", path=flow_copy,
                                guid=self.getUUID())

        if not slope_path == "":
            fname, fext = os.path.splitext(slope_path)
            slope_copy = "01_Inputs/01_Topo/DEM_1/Slope/" + os.path.basename(slope_path)
            inSlope = gdal.Open(slope_path)
            if fext == ".tif":
                driver = gdal.GetDriverByName("GTiff")
                driver.CreateCopy(slope_copy, inSlope)
            elif fext == ".img":
                driver = gdal.GetDriverByName("HFA")
                driver.CreateCopy(slope_copy, inSlope)
            else:
                raise Exception("slope raster is not type .tif or .img")

            newxml.addVBETInput(newxml.VBETrealizations[0], "Slope", name="Slope", path=slope_copy, guid=self.getUUID())

        if not output_unedited_path == "":
            output_unedited_copy = "02_Analyses/Output_1/" + os.path.basename(output_unedited_path)
            inOutput_unedited = ogr.GetDriverByName("ESRI Shapefile").Open(output_unedited_path)
            ogr.GetDriverByName("ESRI Shapefile").CopyDataSource(inOutput_unedited, output_unedited_copy)

            newxml.addOutput("Analysis1", "Vector", "Unedited Valley Bottom", output_unedited_copy,
                             newxml.VBETrealizations[0], guid=self.getUUID())

    def getUUID(self):
        return str(uuid.uuid4()).upper()