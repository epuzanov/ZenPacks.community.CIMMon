################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_ReplicationGroup

CIM_ReplicationGroup is an abstraction of a CIM_ReplicationGroup

$Id: CIM_ReplicationGroup.py,v 1.2 2012/06/27 19:43:21 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Products.ZenModel.OSComponent import OSComponent
from Products.ZenRelations.RelSchema import ToOne, ToMany, ToManyCont
from ZenPacks.community.CIMMon.CIM_ManagedSystemElement import *
from Products.ZenUtils.Utils import prepId

def manage_addReplicationGroup(context, id, userCreated, REQUEST=None):
    """make ReplicationGroup"""
    colid = prepId(id)
    col = CIM_ReplicationGroup(colid)
    context._setObject(colid, col)
    col = context._getOb(colid)
    if userCreated: col.setUserCreatedFlag()
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()+'/manage_main')
    return col

class CIM_ReplicationGroup(OSComponent, CIM_ManagedSystemElement):
    """ReplicationGroup object"""

    collectors = ('zenperfsql', 'zencommand', 'zenwinperf')
    portal_type = meta_type = 'CIM_ReplicationGroup'

    _properties = OSComponent._properties+CIM_ManagedSystemElement._properties

    _relations = OSComponent._relations + (
        ("os", ToOne(
            ToManyCont,
            "Products.ZenModel.OperatingSystem",
            "replicationgroups")),
        ("members", ToMany(
            ToMany,
            "ZenPacks.community.CIMMon.CIM_StorageVolume",
            "replicationgroups")),
        )

    factory_type_information = ( 
        {
            'id'             : 'CIM_ReplicationGroup',
            'meta_type'      : 'CIM_ReplicationGroup',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ReplicationGroup_icon.gif',
            'product'        : 'CIMMon',
            'factory'        : 'manage_addReplicationGroup',
            'immediate_view' : 'viewCIMReplicationGroup',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewCIMReplicationGroup'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'volumes'
                , 'name'          : 'Volumes'
                , 'action'        : 'viewCIMReplicationGroupMembers'
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

InitializeClass(CIM_ReplicationGroup)
