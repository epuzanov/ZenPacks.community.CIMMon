################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_DiskDrive

CIM_DiskDrive is an abstraction of a Hard Disk.

$Id: CIM_DiskDrive.py,v 1.3 2012/06/21 19:31:47 egor Exp $"""

__version__ = "$Revision: 1.3 $"[11:-2]

from Products.ZenModel.HardDisk import HardDisk
from Products.ZenRelations.RelSchema import ToOne, ToMany
from ZenPacks.community.CIMMon.CIM_ManagedSystemElement import *

from Products.ZenUtils.Utils import convToUnits

class CIM_DiskDrive(HardDisk, CIM_ManagedSystemElement):
    """DiskDrive object"""

    collectors = ('zenperfsql', 'zencommand', 'zenwinperf')
    portal_type = meta_type = 'CIM_DiskDrive'

    diskTypes = ("scsi", "ata", "ssd")
    formFactors = {"lff":"lff", "sff":"sff"}
    size = 0
    diskType = ""
    diskTypeImg = ""
    formFactor = ""
    replaceable = True
    bay = -1
    FWRev = ""

    _properties = HardDisk._properties + (
                 {'id':'diskType', 'type':'string', 'mode':'w'},
                 {'id':'diskTypeImg', 'type':'string', 'mode':'w'},
                 {'id':'formFactor', 'type':'string', 'mode':'w'},
                 {'id':'replaceable', 'type':'boolean', 'mode':'w'},
                 {'id':'size', 'type':'int', 'mode':'w'},
                 {'id':'bay', 'type':'int', 'mode':'w'},
                 {'id':'FWRev', 'type':'string', 'mode':'w'},
                ) + CIM_ManagedSystemElement._properties

    _relations = HardDisk._relations + (
        ("chassis", ToOne(ToMany,
                            "ZenPacks.community.CIMMon.CIM_Chassis",
                            "harddisks")),
        ("storagepool", ToOne(ToMany,
                            "ZenPacks.community.CIMMon.CIM_StoragePool",
                            "harddisks")),
        ) + CIM_ManagedSystemElement._relations

    factory_type_information = ( 
        { 
            'id'             : 'CIM_DiskDrive',
            'meta_type'      : 'CIM_DiskDrive',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'HardDisk_icon.gif',
            'product'        : 'CIMMon',
            'factory'        : 'manage_addHardDisk',
            'immediate_view' : 'viewCIMDiskDrive',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewCIMDiskDrive'
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

    security.declareProtected(ZEN_CHANGE_DEVICE, 'setChassis')
    def setChassis(self, chid):
        """
        Set the chassis relationship to the chassis specified by the given id.
        """
        if not chid: return
        for chassis in self.hw().chassis() or []:
            if chassis.getPath() != chid: continue
            self.chassis.addRelation(chassis)
            break

    security.declareProtected(ZEN_VIEW, 'getChassis')
    def getChassis(self):
        """
        Return chassis object
        """
        return self.chassis()

    security.declareProtected(ZEN_CHANGE_DEVICE, 'setStoragePool')
    def setStoragePool(self, spid):
        """
        Set the storagepool relationship to the storage pool specified by the
        given caption.
        """
        if not spid: return
        for sp in getattr(self.device().os, 'storagepools', (lambda:[]))():
            if sp.getPath() != spid: continue
            self.storagepool.addRelation(sp)
            break

    security.declareProtected(ZEN_VIEW, 'getStoragePool')
    def getStoragePool(self):
        """
        Return Disk Group object
        """
        return self.storagepool()

    def getChassisName(self):
        """
        Return Chassis id
        """
        return getattr(self.getChassis(), 'title', 'Unknown')

    def getStoragePoolName(self):
        """
        Return Disk Group name
        """
        return getattr(self.getStoragePool(), 'title', 'Unknown')

    security.declareProtected(ZEN_VIEW, 'getManufacturerLink')
    def getManufacturerLink(self, target=None):
        """
        Return Manufacturer Link
        """
        if self.productClass():
            url = self.productClass().manufacturer.getPrimaryLink()
            if target: url = url.replace(">", " target='%s'>" % target, 1)
            return url
        return ""

    security.declareProtected(ZEN_VIEW, 'getProductLink')
    def getProductLink(self, target=None):
        """
        Return Product Link
        """
        url = self.productClass.getPrimaryLink()
        if target: url = url.replace(">", " target='%s'>" % target, 1)
        return url

    def isUserCreated(self):
        """
        Return True it bay == 0
        """
        return self.bay == -1 and True or False

    def diskImg(self, orientation=''):
        """
        Return disk image filename.
        """
        return '/zport/dmd/disk_%s_%s_%s_%s.png' % (orientation or 'h',
            self.formFactors.get(self.formFactor, 'lff'),
            self.diskTypeImg in self.diskTypes and self.diskTypeImg or 'scsi',
            self.statusDot())

    def bayString(self):
        """
        Return chassis and bay numbers
        """
        return '%s bay %02d'%(self.getChassisName(), int(self.bay))

    def sizeString(self):
        """
        Return the number of total bytes in human readable form ie 10MB
        """
        return convToUnits(self.size, divby=1000)

    def rpmString(self):
        """
        Return the RPM in tradition form ie 7200, 10K
        """
        return 'Unknown'

    def replaceableString(self):
        """
        Return the HotPlug Status
        """
        return self.replaceable and 'Hot Swappable' or 'Non-Hot Swappable'

    def getRRDStatTemplates(self):
        """
        Return the RRD StatisticalData Templates list
        """
        if not self.cimStatClassName: return []
        baseName = self.cimStatClassName.split('_', 1)[-1]
        if baseName == 'DiskDriveStatisticalData': 
            baseName = 'BlockStorageStatisticalData'
        elif baseName == 'DiskDriveMediaAccessStatData': 
            baseName = 'MediaAccessStatData'
        for tname in (self.cimStatClassName, '_'.join(('CIM', baseName))):
            templ = self.getRRDTemplateByName(tname)
            if not templ: continue
            return [templ]
        return []

InitializeClass(CIM_DiskDrive)
