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

$Id: CIM_Collection.py,v 1.1 2012/06/18 23:13:46 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.ZenModel.OSComponent import OSComponent
from Products.ZenRelations.RelSchema import ToOne, ToMany, ToManyCont
from ZenPacks.community.CIMMon.CIM_ManagedSystemElement import *
from Products.ZenUtils.Utils import prepId

def manage_addCollection(context, id, userCreated, REQUEST=None):
    """make ConsistencySet"""
    colid = prepId(id)
    col = CIM_Collection(colid)
    context._setObject(colid, col)
    col = context._getOb(colid)
    if userCreated: col.setUserCreatedFlag()
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()+'/manage_main')
    return col

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
        ("members", ToMany(
            ToOne,
            "ZenPacks.community.CIMMon.CIM_ManagedSystemElement",
            "collection")),
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
                { 'id'            : 'members'
                , 'name'          : 'Members'
                , 'action'        : 'viewCIMCollectionMembers'
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

InitializeClass(CIM_Collection)
