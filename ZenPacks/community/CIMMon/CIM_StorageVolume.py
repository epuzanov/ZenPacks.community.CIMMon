################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_StorageVolume

CIM_StorageVolume is an abstraction of a CIM_StorageVolume

$Id: CIM_StorageVolume.py,v 1.5 2012/06/13 20:37:47 egor Exp $"""

__version__ = "$Revision: 1.5 $"[11:-2]

from Products.ZenModel.OSComponent import OSComponent
from Products.ZenRelations.RelSchema import ToOne, ToMany, ToManyCont
from Products.ZenUtils.Utils import convToUnits
from Products.ZenUtils.Utils import prepId
from ZenPacks.community.CIMMon.CIM_ManagedSystemElement import *

import logging
log = logging.getLogger("zen.CIM_StorageVolume")


def manage_addStorageVolume(context, id, userCreated, REQUEST=None):
    """make StorageVolume"""
    svid = prepId(id)
    sv = CIM_StorageVolume(svid)
    context._setObject(svid, sv)
    sv = context._getOb(svid)
    if userCreated: sv.setUserCreatedFlag()
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()+'/manage_main')
    return sv

class CIM_StorageVolume(OSComponent, CIM_ManagedSystemElement):
    """StorageVolume object"""

    collectors = ('zenperfsql', 'zencommand', 'zenwinperf')
    portal_type = meta_type = 'CIM_StorageVolume'

    accessType = ""
    caption = ""
    blockSize = 0
    diskType = ""

    _properties = OSComponent._properties + (
                 {'id':'accessType', 'type':'string', 'mode':'w'},
                 {'id':'caption', 'type':'string', 'mode':'w'},
                 {'id':'blockSize', 'type':'int', 'mode':'w'},
                 {'id':'diskType', 'type':'string', 'mode':'w'},
                ) + CIM_ManagedSystemElement._properties

    _relations = OSComponent._relations + (
        ("os", ToOne(ToManyCont,
            "Products.ZenModel.OperatingSystem",
            "storagevolumes")),
        ("storagepool", ToOne(ToMany,
            "ZenPacks.community.CIMMon.CIM_StoragePool",
            "storagevolumes")),
        )

    factory_type_information = (
        {
            'id'             : 'StorageVolume',
            'meta_type'      : 'StorageVolume',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'StorageVolume_icon.gif',
            'product'        : 'CIMMon',
            'factory'        : 'manage_addStorageVolume',
            'immediate_view' : 'viewCIMStorageVolume',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewCIMStorageVolume'
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

    security = ClassSecurityInfo()

    getRRDTemplates = CIM_ManagedSystemElement.getRRDTemplates
    getStatus = CIM_ManagedSystemElement.getStatus
    getStatusImgSrc = CIM_ManagedSystemElement.getStatusImgSrc
    convertStatus = CIM_ManagedSystemElement.convertStatus

    security.declareProtected(ZEN_CHANGE_DEVICE, 'setStoragePool')
    def setStoragePool(self, spid):
        """
        Set the storagepool relationship to the storage pool specified by the given
        id.
        """
        for sp in self.os().storagepools() or []:
            if sp.getPath() != spid: continue
            self.storagepool.addRelation(sp)
            break

    security.declareProtected(ZEN_VIEW, 'getStoragePool')
    def getStoragePool(self):
        return self.storagepool()

    security.declareProtected(ZEN_VIEW, 'getStoragePoolName')
    def getStoragePoolName(self):
        return getattr(self.getStoragePool(), 'poolId', 'Unknown')

    def totalBytes(self):
        """
        Return the number of total bytes
        """
        return self.cacheRRDValue('NumberOfBlocks', 0) * self.blockSize

    def totalBytesString(self):
        """
        Return the number of total bytes in human readable form ie 10MB
        """
        return convToUnits(self.totalBytes(), divby=1024)

    def getRRDNames(self):
        """
        Return the datapoint name of this StorageVolume
        """
        return ['StorageVolume_NumberOfBlocks']

    def getRRDStatTemplates(self):
        """
        Return the RRD StatisticalData Templates list
        """
        if not self.cimStatClassName: return []
        baseName = self.cimStatClassName.split('_', 1)[-1]
        if baseName == 'VolumeStatisticalData': 
            baseName = 'BlockStorageStatisticalData'
        for tname in (self.cimStatClassName, '_'.join(('CIM', baseName))):
            templ = self.getRRDTemplateByName(tname)
            if not templ: continue
            return [templ]
        return []

InitializeClass(CIM_StorageVolume)
