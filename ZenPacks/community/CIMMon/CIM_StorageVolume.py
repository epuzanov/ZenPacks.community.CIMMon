################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_StorageVolume

CIM_StorageVolume is an abstraction of a Logical Disk.

$Id: CIM_StorageVolume.py,v 1.0 2011/06/07 20:27:04 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from ZenPacks.community.deviceAdvDetail.LogicalDisk import LogicalDisk
from ZenPacks.community.CIMMon.CIM_ManagedSystemElement import *

class CIM_StorageVolume(LogicalDisk, CIM_ManagedSystemElement):
    """CIM_StorageVolume object"""

    _properties = LogicalDisk._properties + CIM_ManagedSystemElement._properties

    getRRDTemplates = CIM_ManagedSystemElement.getRRDTemplates

InitializeClass(CIM_StorageVolume)
