
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

def logicalProcessors(self):
    return round(self.device().cacheRRDValue('LoadPercentage_count', 1))

if not hasattr(OperatingSystem, 'logicalProcessors'):
    OperatingSystem.logicalProcessors = logicalProcessors

class ZenPack(ZenPackBase):
    """ CIMMon loader
    """

    packZProperties = [
            ('zCIMConnectionString', "'pywbemdb',scheme='https',port=5989", 'string'),
            ('zCIMHWNamespace', "root/cimv2", 'string'),
            ]

    dcProperties = {
        '/CIM': {
            'description': ('', 'string'),
            'zCollectorPlugins': (
                (
                'community.cim.CIMDeviceMap',
                'community.cim.CIMProcessorMap',
                'community.cim.CIMFanMap',
                'community.cim.CIMTachometerMap',
                'community.cim.CIMTemperatureSensorMap',
                'community.cim.CIMProcessMap',
                'zenoss.portscan.IpServiceMap',
                ),
                'lines',
            ),
            'zWmiMonitorIgnore': (False, 'boolean'),
        },
    }

    def addDeviceClass(self, app, dcp, properties):
        try:
            dc = app.zport.dmd.Devices.getOrganizer(dcp)
        except:
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

    def upgrade(self, app):
        for devClass, properties in self.dcProperties.iteritems():
            self.addDeviceClass(app, devClass, properties)
        ZenPackBase.upgrade(self, app)

    def remove(self, app, leaveObjects=False):
        for dcp in self.dcProperties.keys():
            try:
                dc = app.zport.dmd.Devices.getOrganizer(dcp)
                dc._delProperty('zCollectorPlugins')
            except: continue
        ZenPackBase.remove(self, app, leaveObjects)
