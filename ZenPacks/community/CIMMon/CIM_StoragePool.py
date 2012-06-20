################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_StoragePool

CIM_StoragePool is an abstraction of a CIM_StoragePool

$Id: CIM_StoragePool.py,v 1.3 2012/06/20 20:37:48 egor Exp $"""

__version__ = "$Revision: 1.3 $"[11:-2]

from Products.ZenModel.OSComponent import OSComponent
from Products.ZenRelations.RelSchema import ToOne, ToMany, ToManyCont
from ZenPacks.community.CIMMon.CIM_ManagedSystemElement import *

from Products.ZenUtils.Utils import prepId
from Products.ZenUtils.Utils import convToUnits

def manage_addStoragePool(context, id, userCreated, REQUEST=None):
    """make StoragePool"""
    spid = prepId(id)
    sp = CIM_StoragePool(spid)
    context._setObject(spid, sp)
    sp = context._getOb(spid)
    if userCreated: sp.setUserCreatedFlag()
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()+'/manage_main')
    return sp

class CIM_StoragePool(OSComponent, CIM_ManagedSystemElement):
    """StoragePool object"""

    collectors = ('zenperfsql', 'zencommand', 'zenwinperf')
    portal_type = meta_type = 'CIM_StoragePool'

    totalManagedSpace = 0
    poolId = "0"
    usage = "Unrestricted"

    _properties = OSComponent._properties + (
                 {'id':'totalManagedSpace', 'type':'int', 'mode':'w'},
                 {'id':'poolId', 'type':'string', 'mode':'w'},
                 {'id':'usage', 'type':'string', 'mode':'w'},
                ) + CIM_ManagedSystemElement._properties

    _relations = OSComponent._relations + (
        ("os", ToOne(
            ToManyCont,
            "Products.ZenModel.OperatingSystem",
            "storagepools")),
        ("harddisks", ToMany(
            ToOne,
            "ZenPacks.community.CIMMon.CIM_DiskDrive",
            "storagepool")),
        ("storagevolumes", ToMany(
            ToOne,
            "ZenPacks.community.CIMMon.CIM_StorageVolume",
            "storagepool")),
        ) + CIM_ManagedSystemElement._relations

    factory_type_information = ( 
        {
            'id'             : 'CIM_StoragePool',
            'meta_type'      : 'CIM_StoragePool',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'StoragePool_icon.gif',
            'product'        : 'CIMMon',
            'factory'        : 'manage_addStoragePool',
            'immediate_view' : 'viewCIMStoragePool',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewCIMStoragePool'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'disks'
                , 'name'          : 'Disks'
                , 'action'        : 'viewCIMStoragePoolDisks'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'volumes'
                , 'name'          : 'Volumes'
                , 'action'        : 'viewCIMStoragePoolVolumes'
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

    def totalBytes(self):
        return self.totalManagedSpace or 0

    def usedBytes(self):
        return self.totalBytes() - self.cacheRRDValue('RemainingManagedSpace',0)

    def totalBytesString(self):
        return convToUnits(self.totalBytes(), divby=1024)

    def usedBytesString(self):
        return convToUnits(self.usedBytes(), divby=1024)

    def availBytesString(self):
        return convToUnits((self.totalBytes() - self.usedBytes()), divby=1024)

    def capacity(self):
        """
        Return the percentage capacity of a filesystems using its rrd file
        """
        __pychecker__='no-returnvalues'
        if self.totalBytes() is not 0:
            return int(100.0 * self.usedBytes() / self.totalBytes())
        return 'unknown'

    def totalDisks(self):
        """
        Return total disks number
        """
        return len(self.harddisks())

    def getRRDNames(self):
        """
        Return the datapoint name of this StoragePool
        """
        return ['StoragePool_RemainingManagedSpace']

InitializeClass(CIM_StoragePool)
