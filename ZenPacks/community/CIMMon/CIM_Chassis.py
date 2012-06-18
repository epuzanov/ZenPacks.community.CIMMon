################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_Chassis

CIM_Chassis is an abstraction of a CIM_Chassis

$Id: CIM_Chassis.py,v 1.1 2012/06/18 23:13:26 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.ZenModel.HWComponent import HWComponent
from Products.ZenRelations.RelSchema import ToOne, ToMany, ToManyCont
from ZenPacks.community.CIMMon.CIM_ManagedSystemElement import *

LINKTMPLT = '<a href="%s" target="_top"><img src="%s" /></a>'
BLANKTMPLT = '<img src="/zport/dmd/disk_%s_%s_blank.png" />'

class CIM_Chassis(HWComponent, CIM_ManagedSystemElement):
    """Chassis object"""

    collectors = ('zenperfsql', 'zencommand', 'zenwinperf')

    portal_type = meta_type = 'CIM_Chassis'

    #layout = 'v1 2 3 4 5 6 7 8 9 10 11 12 13 14'
    #layout = 'h1 3 5 7 9,2 4 6 8 10'
    layout = 'h0 0 0 0,0 0 0 0,0 0 0 0'
    caption = ''

    _properties = HWComponent._properties + (
                 {'id':'layout', 'type':'string', 'mode':'w'},
                 {'id':'caption', 'type':'string', 'mode':'w'},
                ) + CIM_ManagedSystemElement._properties

    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont, "Products.ZenModel.DeviceHW",
                    "chassis")),
        ("harddisks", ToMany(ToOne,
                    "ZenPacks.community.CIMMon.CIM_DiskDrive",
                    "chassis")),
        ) + CIM_ManagedSystemElement._relations

    factory_type_information = (
        {
            'id'             : 'CIM_Chassis',
            'meta_type'      : 'CIM_Chassis',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'Chassis_icon.gif',
            'product'        : 'CIMMon',
            'factory'        : 'manage_addChassis',
            'immediate_view' : 'viewCIMChassis',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewCIMChassis'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'layout'
                , 'name'          : 'Layout'
                , 'action'        : 'viewCIMChassisLayout'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'disks'
                , 'name'          : 'Disks'
                , 'action'        : 'viewCIMChassisDisks'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'events'
                , 'name'          : 'Events'
                , 'action'        : 'viewEvents'
                , 'permissions'   : (ZEN_VIEW, )
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

    def isUserCreated(self):
        """
        Return True if layout not detected
        """
        return self.layout=='h0 0 0 0,0 0 0 0,0 0 0 0' and True or False

    def getLayout(self):
        """
        Build Disk Enclosure layout
        """
        if self.layout == 'h0 0 0 0,0 0 0 0,0 0 0 0': return ''
        bays = {}
        disk = None
        for disk in self.harddisks() or []:
            bays[str(disk.bay)] = LINKTMPLT % ( disk.getPrimaryUrlPath(),
                                                disk.diskImg(self.layout[0]))
        blnk = BLANKTMPLT%(self.layout[0], getattr(disk,'formFactor', 'lff'))
        return '<table border="0">\n<tr>\n<td>%s\n</td>\n</tr>\n</table>\n'%(
            '</td>\n</tr>\n<tr>\n<td>'.join(['</td>\n<td>'.join([bays.get(b,
            blnk) for b in l.split(' ')]) for l in self.layout[1:].split(',')]))

InitializeClass(CIM_Chassis)
