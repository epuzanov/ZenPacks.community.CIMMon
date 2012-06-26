################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_RedundancySet

CIM_RedundancySet is an abstraction of a CIM_RedundancySet

$Id: CIM_RedundancySet.py,v 1.2 2012/06/26 19:43:09 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Products.ZenModel.OSComponent import OSComponent
from Products.ZenRelations.RelSchema import ToOne, ToMany, ToManyCont
from ZenPacks.community.CIMMon.CIM_ManagedSystemElement import *
from Products.ZenUtils.Utils import prepId

def manage_addRedundancySet(context, id, userCreated, REQUEST=None):
    """make RedundancySet"""
    colid = prepId(id)
    col = CIM_RedundancySet(colid)
    context._setObject(colid, col)
    col = context._getOb(colid)
    if userCreated: col.setUserCreatedFlag()
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()+'/manage_main')
    return col

class CIM_RedundancySet(OSComponent, CIM_ManagedSystemElement):
    """RedundancySet object"""

    collectors = ('zenperfsql', 'zencommand', 'zenwinperf')
    portal_type = meta_type = 'CIM_RedundancySet'

    loadBalanceAlgorithm = ""
    minNumberNeeded = 0
    typeOfSet = ""

    statusmap ={0: ('grey', 3, 'Unknown'),
                1: ('yellow', 3, 'Other'),
                2: ('green', 0, 'Fully Redundant'),
                3: ('yellow', 3, 'Degraded'),
                4: ('yellow', 4, 'Redundancy Lost'),
                5: ('yellow', 5, 'Overall Failure'),
                }

    _properties = OSComponent._properties + (
                {'id':'loadBalanceAlgorithm', 'type':'string', 'mode':'w'},
                {'id':'minNumberNeeded', 'type':'int', 'mode':'w'},
                {'id':'typeOfSet', 'type':'string', 'mode':'w'},
                ) + CIM_ManagedSystemElement._properties

    _relations = OSComponent._relations + (
        ("os", ToOne(
            ToManyCont,
            "Products.ZenModel.OperatingSystem",
            "redundancysets")),
        ("members", ToMany(
            ToMany,
            "ZenPacks.community.CIMMon.CIM_ManagedSystemElement",
            "redundancysets")),
        )

    factory_type_information = ( 
        {
            'id'             : 'CIM_RedundancySet',
            'meta_type'      : 'CIM_RedundancySet',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'RedundancySet_icon.gif',
            'product'        : 'CIMMon',
            'factory'        : 'manage_addRedundancySet',
            'immediate_view' : 'viewCIMRedundancySet',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewCIMRedundancySet'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'members'
                , 'name'          : 'Members'
                , 'action'        : 'viewCIMRedundancySetMembers'
                , 'permissions'   : (ZEN_VIEW, )
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

InitializeClass(CIM_RedundancySet)
