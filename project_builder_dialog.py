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

from projectxml import ProjectXML
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
        self.btnBrowseFile1.clicked.connect(lambda: self.file_browser(self.txtFile1))
        self.btnBrowseFile2.clicked.connect(lambda: self.file_browser(self.txtFile2))
        self.btnBrowseFile3.clicked.connect(lambda: self.file_browser(self.txtFile3))
        self.btnBrowseOutputFolder.clicked.connect(lambda: self.file_browser(self.txt))

        # Handle what happens when we click OK
        self.btnBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.btnBoxClick)
        self.btnBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.close)

        print "GUI loaded and linked"

    def file_browser(self, txtControl):
        filename = QtGui.QFileDialog.getOpenFileName(self, "Open XML file", "",
                                                     "XML File (*.xml);;GCD File (*.gcd);;All files (*)")
        txtControl.setText(filename)
        self.recalc_state()

    def btnBoxClick(self):
        projectxml = ProjectXML('/Users/matt/Desktop/myxml.xml', 'VBET', 'My VBET Project')
        projectxml.addMeta("metaName", "metaValue", projectxml.project)
        projectxml.addMeta("metaName2", 7234, projectxml.project)

        projectxml.addVBETRealization("My first realization", 123234)
        projectxml.write()


    def recalc_state(self):
        print "recalc state"