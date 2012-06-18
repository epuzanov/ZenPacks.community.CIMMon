################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_PhysicalMemory

CIM_PhysicalMemory is an abstraction of a Memory module.

$Id: CIM_PhysicalMemory.py,v 1.2 2012/06/18 23:19:32 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Globals import DTMLFile

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.HWComponent import HWComponent
from Products.ZenUtils.Utils import convToUnits
from ZenPacks.community.CIMMon.CIM_ManagedSystemElement import *

class CIM_PhysicalMemory(HWComponent, CIM_ManagedSystemElement):
    """PhysicalMemory object"""

    collectors = ('zenperfsql', 'zencommand', 'zenwinperf')
    portal_type = meta_type = 'CIM_PhysicalMemory'

    slot = 0
    size = 0

    _properties = HWComponent._properties + (
        {'id':'slot', 'type':'int', 'mode':'w'},
        {'id':'size', 'type':'int', 'mode':'w'},
    ) + CIM_ManagedSystemElement._properties

    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont, "Products.ZenModel.DeviceHW",
                                                    "physicalmemorymodules")),
        ) + CIM_ManagedSystemElement._relations

    factory_type_information = (
        {
            'id'             : 'MemoryModule',
            'meta_type'      : 'MemoryModule',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'MemoryModule_icon.gif',
            'product'        : 'CIMMon',
            'factory'        : 'manage_addMemoryModule',
            'immediate_view' : 'viewMemoryModule',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewMemoryModule'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_DEVICE, )
                },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
          },
        )

    getRRDTemplates = CIM_ManagedSystemElement.getRRDTemplates
    getStatus = CIM_ManagedSystemElement.getStatus
    getStatusImgSrc = CIM_ManagedSystemElement.getStatusImgSrc
    convertStatus = CIM_ManagedSystemElement.convertStatus

    def sizeString(self):
        """
        Return the number of total bytes in human readable form ie 10MB
        """
        return self.size > 0 and convToUnits(self.size) or ''

InitializeClass(CIM_PhysicalMemory)
