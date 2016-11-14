# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ProjectBuilderDialog
                                 A QGIS plugin
 This plugin will take legacy riverscapes projects and build them into projects complete with project.xml files
                             -------------------
        begin                : 2016-10-26
        git sha              : $Format:%H$
        copyright            : (C) 2016 by NorthArrowResearch
        email                : info@northarrowresearch.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

#from projectxml import ProjectXML
from vbet import VBETproject
from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'project_builder_dialog_base.ui'))


class ProjectBuilderDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(ProjectBuilderDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # Here we bind the browse buttons to some actions. We should probably namespace
        # This since we're going to have a lot of them. Maybe even write a generic function
        # for Browse -> Text control handling since this is a pretty common thing.
        self.btnBrowseDEM.clicked.connect(lambda: self.file_browser(self.txtDEM))
        self.btnBrowseNetwork.clicked.connect(lambda: self.file_browser(self.txtNetwork))
        self.btnBrowseEOut.clicked.connect(lambda: self.file_browser(self.txtEOut))
        self.btnBrowseFA.clicked.connect(lambda: self.file_browser(self.txtFA))
        self.btnBrowseSlope.clicked.connect(lambda: self.file_browser(self.txtSlope))
        self.btnBrowseUOut.clicked.connect(lambda: self.file_browser(self.txtUOut))

        self.btnBrowseOutputFolder.clicked.connect(lambda: self.folder_browser(self.txtOutputFolder))

        # Handle what happens when we click OK
        self.btnBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.copyVBET)
        self.btnBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.close)

        print "GUI loaded and linked"

    def file_browser(self, txtControl):
        filename = QtGui.QFileDialog.getOpenFileName(self, "Open file", "", "All files (*)")
        txtControl.setText(filename)
        self.recalc_state()

    def folder_browser(self, txtControl):
        foldername = QtGui.QFileDialog.getExistingDirectory(self, "Select Folder")
        txtControl.setText(foldername)
        self.recalc_state()

    def copyVBET(self):
        VBETproject(self.txtOutputFolder.text(), self.txtDEM.text(), self.txtNetwork.text(), self.txtEOut.text(),
                    huc_id=self.txtHUCID.text(), huc_name=self.txtHUCName.text(), smbuf=self.txtSmBuf.text(),
                    medbuf=self.txtMedBuf.text(), lgbuf=self.txtLgBuf.text(), lowda=self.txtLowDA.text(),
                    highda=self.txtHighDA.text(), lgslope=self.txtLgSlope.text(), medslope=self.txtMedSlope.text(),
                    smslope=self.txtSmSlope.text())

    #def btnBoxClick(self):
    #    projectxml = ProjectXML('/Users/matt/Desktop/myxml.xml', 'VBET', 'My VBET Project')
    #    projectxml.addMeta("metaName", "metaValue", projectxml.project)
    #    projectxml.addMeta("metaName2", 7234, projectxml.project)

    #    projectxml.addVBETRealization("My first realization", 123234)
    #    projectxml.write()


    def recalc_state(self):
        print "recalc state"