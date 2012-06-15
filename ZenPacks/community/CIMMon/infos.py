################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""infos.py

Representation of CIM components.

$Id: infos.py,v 1.2 2012/06/15 23:47:35 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.infos.component.ipinterface import IpInterfaceInfo
from Products.Zuul.decorators import info
from Products.ZenUtils.Utils import convToUnits

class DiskDriveInfo(ComponentInfo):

    serialNumber = ProxyProperty("serialNumber")
    diskType = ProxyProperty("diskType")
    FWRev = ProxyProperty("FWRev")
    bay = ProxyProperty("bay")

    @property
    def size(self):
        return convToUnits(self._object.size, divby=1000)

    @property
    @info
    def manufacturer(self):
        pc = self._object.productClass()
        if (pc):
            return pc.manufacturer()

    @property
    @info
    def product(self):
        return self._object.productClass()

    @property
    @info
    def chassis(self):
        return self._object.getChassis()

    @property
    @info
    def storagePool(self):
        return self._object.getStoragePool()

class PhysicalMemoryInfo(ComponentInfo):

    slot = ProxyProperty("slot")

    @property
    def size(self):
        return convToUnits(self._object.size)

    @property
    @info
    def manufacturer(self):
        pc = self._object.productClass()
        if (pc):
            return pc.manufacturer()

    @property
    @info
    def product(self):
        return self._object.productClass()

class ChassisInfo(ComponentInfo):

    serialNumber = ProxyProperty("serialNumber")
    layout = ProxyProperty("layout")

    @property
    @info
    def manufacturer(self):
        pc = self._object.productClass()
        if (pc):
            return pc.manufacturer()

    @property
    @info
    def product(self):
        return self._object.productClass()

class StoragePoolInfo(ComponentInfo):

    @property
    def totalDisks(self):
        return self._object.totalDisks()

    @property
    def totalBytesString(self):
        return self._object.totalBytesString()

    @property
    def usedBytesString(self):
        return self._object.usedBytesString()

    @property
    def availBytesString(self):
        return self._object.availBytesString()

    @property
    def capacity(self):
        capacity = self._object.capacity()
        if str(capacity).isdigit():
            capacity = '%s%%'%capacity
        return capacity

class StorageVolumeInfo(ComponentInfo):

    accessType = ProxyProperty("accessType")
    diskType = ProxyProperty("diskType")

    @property
    def totalBytesString(self):
        return self._object.totalBytesString()

    @property
    @info
    def storagePool(self):
        return self._object.getStoragePool()

class FanInfo(ComponentInfo):

    type = ProxyProperty('type')

    @property
    def state(self):
        return self._object.getStatusString()

    @property
    def rpm(self):
        return self._object.rpmString()

class PowerSupplyInfo(ComponentInfo):

    watts = ProxyProperty('watts')
    type = ProxyProperty('type')

    @property
    def state(self):
        return self._object.getStatusString()

    @property
    def millivolts(self):
        return self._object.millivolts()

class TemperatureSensorInfo(ComponentInfo):

    @property
    def state(self):
        return self._object.getStatusString()

    @property
    def temperature(self):
        return self._object.temperatureFahrenheit()

class ComputerSystemInfo(ComponentInfo):

    slot = ProxyProperty('slot')
    serialNumber = ProxyProperty('serialNumber')
    FWRev = ProxyProperty('FWRev')

    @property
    @info
    def manufacturer(self):
        pc = self._object.productClass()
        if (pc):
            return pc.manufacturer()

    @property
    @info
    def product(self):
        return self._object.productClass()

    @property
    def uptime(self):
        return self._object.uptimeString()

    @property
    def monitored(self):
        return ""

    @property
    def state(self):
        return self._object.getStatusString()

class NetworkPortInfo(IpInterfaceInfo):

    @property
    @info
    def controller(self):
        return self._object.getController()

    @property
    def state(self):
        return self._object.getStatusString()

class CollectionInfo(ComponentInfo):

    @property
    def state(self):
        return self._object.getStatusString()

