################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_DiskDrive

CIM_DiskDrive is an abstraction of a Hard Disk.

$Id: CIM_DiskDrive.py,v 1.0 2011/06/07 20:23:10 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenUtils.Utils import convToUnits
from Products.ZenModel.HardDisk import HardDisk
from ZenPacks.community.CIMMon.CIM_ManagedSystemElement import *

class CIM_DiskDrive(HardDisk, CIM_ManagedSystemElement):
    """CIM_DiskDrive object"""

    rpm = 0
    size = 0
    diskType = ""
    hotPlug = 0
    bay = 0
    FWRev = ""


    _properties = HardDisk._properties + (
                 {'id':'rpm', 'type':'int', 'mode':'w'},
                 {'id':'diskType', 'type':'string', 'mode':'w'},
                 {'id':'size', 'type':'int', 'mode':'w'},
                 {'id':'bay', 'type':'int', 'mode':'w'},
                 {'id':'FWRev', 'type':'string', 'mode':'w'},
                ) + CIM_ManagedSystemElement._properties

    factory_type_information = (
        {
            'id'             : 'HardDisk',
            'meta_type'      : 'HardDisk',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'HardDisk_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addHardDisk',
            'immediate_view' : 'viewCIMDiskDrive',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewCIMDiskDrive'
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


    def sizeString(self):
        """
        Return the number of total bytes in human readable form ie 10MB
        """
        return convToUnits(self.size, divby=1000)


    def rpmString(self):
        """
        Return the RPM in tradition form ie 7200, 10K
        """
        if int(self.rpm) == 1:
            return 'Unknown'
        if int(self.rpm) < 10000:
            return int(self.rpm)
        else:
            return "%sK" %(int(self.rpm) / 1000)

    getRRDTemplates = CIM_ManagedSystemElement.getRRDTemplates

InitializeClass(CIM_DiskDrive)
