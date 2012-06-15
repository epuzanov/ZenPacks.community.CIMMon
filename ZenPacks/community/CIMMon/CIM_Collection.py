################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_Collection

CIM_Collection is an abstraction of a CIM_Collection

$Id: CIM_Collection.py,v 1.0 2012/06/15 23:07:16 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.OSComponent import OSComponent
from Products.ZenRelations.RelSchema import ToOne, ToManyCont
from ZenPacks.community.CIMMon.CIM_ManagedSystemElement import *

class CIM_Collection(OSComponent, CIM_ManagedSystemElement):
    """Collection object"""

    collectors = ('zenperfsql', 'zencommand', 'zenwinperf')
    portal_type = meta_type = 'CIM_Collection'

    _properties = OSComponent._properties+CIM_ManagedSystemElement._properties

    _relations = OSComponent._relations + (
        ("os", ToOne(
            ToManyCont,
            "Products.ZenModel.OperatingSystem",
            "collections")),
        )

    factory_type_information = ( 
        {
            'id'             : 'CIM_Collection',
            'meta_type'      : 'CIM_Collection',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'Collection_icon.gif',
            'product'        : 'CIMMon',
            'factory'        : 'manage_addCollection',
            'immediate_view' : 'viewCIMCollection',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewCIMCollection'
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

InitializeClass(CIM_Collection)
