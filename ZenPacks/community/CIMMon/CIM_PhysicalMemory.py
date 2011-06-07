################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_PhysicalMemory

CIM_PhysicalMemory is an abstraction of a Memory module.

$Id: CIM_PhysicalMemory.py,v 1.0 2011/06/07 20:26:14 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from ZenPacks.community.deviceAdvDetail.MemoryModule import MemoryModule
from ZenPacks.community.CIMMon.CIM_ManagedSystemElement import *

class CIM_PhysicalMemory(MemoryModule, CIM_ManagedSystemElement):
    """CIM_PhysicalMemory object"""

    _properties = MemoryModule._properties+CIM_ManagedSystemElement._properties

    getRRDTemplates = CIM_ManagedSystemElement.getRRDTemplates

InitializeClass(CIM_PhysicalMemory)
