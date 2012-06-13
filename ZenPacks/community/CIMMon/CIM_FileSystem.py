################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_FileSystem

CIM_FileSystem is an abstraction of a File System.

$Id: CIM_FileSystem.py,v 1.1 2012/06/13 20:33:43 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.ZenModel.FileSystem import FileSystem
from ZenPacks.community.CIMMon.CIM_ManagedSystemElement import *

class CIM_FileSystem(FileSystem, CIM_ManagedSystemElement):
    """FileSystem object"""

    collectors = ('zenperfsql', 'zencommand', 'zenwinperf')
    _properties = FileSystem._properties + CIM_ManagedSystemElement._properties

    getRRDTemplates = CIM_ManagedSystemElement.getRRDTemplates
    getStatus = CIM_ManagedSystemElement.getStatus
    getStatusImgSrc = CIM_ManagedSystemElement.getStatusImgSrc
    convertStatus = CIM_ManagedSystemElement.convertStatus

InitializeClass(CIM_FileSystem)
