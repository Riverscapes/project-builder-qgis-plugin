# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ProjectBuilder
                                 A QGIS plugin
 This plugin will take legacy riverscapes projects and build them into projects complete with project.xml files
                             -------------------
        begin                : 2016-10-26
        copyright            : (C) 2016 by NorthArrowResearch
        email                : info@northarrowresearch.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

######################### REMOTE DEBUG #########################
# To activate remote debugging set DEBUG_PLUGIN=AnalystToolbar as a QGIS
# Environment variable in Preferences -> System -> Environment
import os
if 'DEBUG_PLUGIN' in os.environ and os.environ['DEBUG_PLUGIN'] == "ProjectBuilder":
    import pydevd
    try:
        pydevd.settrace('localhost', port=53100, stdoutToServer=True, stderrToServer=True)
    except:
        print "Move along, nothing to see here"

######################### /REMOTE DEBUG #########################

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ProjectBuilder class from file ProjectBuilder.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .project_builder import ProjectBuilder
    return ProjectBuilder(iface)
