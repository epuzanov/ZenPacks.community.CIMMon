
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Acquisition import aq_base
from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenModel.DeviceClass import manage_addDeviceClass
from Products.ZenModel.OperatingSystem import OperatingSystem
from Products.ZenModel.Device import Device
from Products.ZenModel.DeviceHW import DeviceHW
from Products.ZenRelations.RelSchema import *
DeviceHW._relations += (("chassis", ToManyCont(ToOne,
                        "ZenPacks.community.CIMMon.CIM_Chassis", "hw")),
                        ("physicalmemorymodules", ToManyCont(ToOne,
                        "ZenPacks.community.CIMMon.CIM_PhysicalMemory", "hw")),
                        )
OperatingSystem._relations += (("storagepools", ToManyCont(ToOne,
                        "ZenPacks.community.CIMMon.CIM_StoragePool", "os")),
                        ("storagevolumes", ToManyCont(ToOne,
                        "ZenPacks.community.CIMMon.CIM_StorageVolume", "os")),
                        )

def logicalProcessors(self):
    return round(self.device().cacheRRDValue('LoadPercentage_count', 1))

if not hasattr(OperatingSystem, 'logicalProcessors'):
    OperatingSystem.logicalProcessors = logicalProcessors

class ZenPack(ZenPackBase):
    """ CIMMon loader
    """

    packZProperties = [
            ('zCIMConnectionString', "'pywbemdb',scheme='https',host='${here/manageIp}',port=5989,user='${here/zWinUser}',password='${here/zWinPassword}',namespace='root/cimv2'", 'string'),
            ('zCIMHWConnectionString', "'pywbemdb',scheme='https',host='${here/manageIp}',port=5989,user='${here/zWinUser}',password='${here/zWinPassword}',namespace='root/cimv2'", 'string'),
            ]

    dcProperties = {
        '/Server/CIM': {
            'description': ('', 'string'),
            'zCollectorPlugins': (
                (
                'community.cim.CIMComputerSystemMap',
                'community.cim.CIMOperatingSystemMap',
                'community.cim.CIMProcessMap',
                'zenoss.portscan.IpServiceMap',
                ),
                'lines',
            ),
            'zWmiMonitorIgnore': (False, 'boolean'),
        },
        '/Server/CIM/Linux': {
            'description': ('', 'string'),
            'zCollectorPlugins': (
                (
                'community.cim.CIMComputerSystemMap',
                'community.cim.CIMOperatingSystemMap',
                'community.cim.CIMProcessorMap',
                'community.cim.CIMUnixProcessMap',
                'community.cim.CIMFileSystemMap',
                'community.cim.CIMNetworkPortMap',
                'zenoss.portscan.IpServiceMap',
                ),
                'lines',
            ),
            'zWmiMonitorIgnore': (False, 'boolean'),
        },
        '/Server/Windows/CIM': {
            'description': ('', 'string'),
            'zCollectorPlugins': (
                (
                'community.cim.CIMComputerSystemMap',
                'community.cim.CIMOperatingSystemMap',
                'community.cim.CIMChassisMap',
                'community.cim.CIMPhysicalMemoryMap',
                'community.cim.CIMDiskDriveMap',
                'community.cim.Win32ProcessorMap',
                'community.cim.Win32NetworkAdapterMap',
                'community.cim.Win32VolumeMap',
                'community.cim.Win32ProcessMap',
                'community.cim.Win32IP4RouteTableMap',
                'community.cim.Win32ServiceMap',
                'zenoss.portscan.IpServiceMap',
                ),
                'lines',
            ),
            'zCIMConnectionString': ("'pywmidb',host='${here/manageIp}',user='${here/zWinUser}',password='${here/zWinPassword}',namespace='root/cimv2'", 'string'),
            'zCIMHWConnectionString': ("'pywmidb',host='${here/manageIp}',user='${here/zWinUser}',password='${here/zWinPassword}',namespace='root/cimv2'", 'string'),
            'zWmiMonitorIgnore': (False, 'boolean'),
        },
        '/Storage/CIM': {
            'description': ('', 'string'),
            'zCollectorPlugins': (
                (
                'community.cim.SNIAComputerSystemMap',
                'community.cim.SNIAChassisMap',
                'community.cim.SNIAStoragePoolMap',
                'community.cim.SNIAStorageVolumeMap',
                'community.cim.SNIADiskDriveMap',
                'community.cim.SNIANetworkPortMap',
                ),
                'lines',
            ),
            'zWmiMonitorIgnore': (False, 'boolean'),
        },
    }

    def addDeviceClass(self, app, dcp, properties):
        try:
            dc = app.zport.dmd.Devices.getOrganizer(dcp)
            if dc.getOrganizerName() != dcp:
                raise KeyError
        except KeyError:
            dcp, newdcp = dcp.rsplit('/', 1)
            dc = self.addDeviceClass(app, dcp, self.dcProperties.get(dcp, {}))
            manage_addDeviceClass(dc, newdcp)
            dc = app.zport.dmd.Devices.getOrganizer("%s/%s"%(dcp, newdcp))
            dc.description = ''
        for prop, value in properties.iteritems():
            if not hasattr(aq_base(dc), prop):
                dc._setProperty(prop, value[0], type = value[1])
        return dc

    def install(self, app):
        for devClass, properties in self.dcProperties.iteritems():
            self.addDeviceClass(app, devClass, properties)
        ZenPackBase.install(self, app)
        for d in self.dmd.Devices.getSubDevices():
            d.hw.buildRelations()
            d.os.buildRelations()

    def upgrade(self, app):
        for devClass, properties in self.dcProperties.iteritems():
            self.addDeviceClass(app, devClass, properties)
        ZenPackBase.upgrade(self, app)
        for d in self.dmd.Devices.getSubDevices():
            d.hw.buildRelations()
            d.os.buildRelations()

    def remove(self, app, leaveObjects=False):
        for dcp in self.dcProperties.keys():
            try:
                dc = app.zport.dmd.Devices.getOrganizer(dcp)
                dc._delProperty('zCollectorPlugins')
            except: continue
        ZenPackBase.remove(self, app, leaveObjects)
        DeviceHW._relations = tuple([x for x in DeviceHW._relations \
                    if x[0] not in ['chassis', 'physicalmemorymodules']])
        OperatingSystem._relations = tuple([x for x in OperatingSystem._relations \
                    if x[0] not in ['storagepools', 'storagevolumes']])
        for d in self.dmd.Devices.getSubDevices():
            d.hw.buildRelations()
            d.os.buildRelations()
