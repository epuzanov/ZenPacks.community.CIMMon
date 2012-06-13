################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""interfaces

describes the form field to the user interface.

$Id: interfaces.py,v 1.1 2012/06/13 20:39:49 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.Zuul.interfaces import IComponentInfo,\
                                    IIpInterfaceInfo,\
                                    IExpansionCardInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class IPhysicalMemoryInfo(IComponentInfo):
    """
    Info adapter for Physical Memory Module components.
    """
    manufacturer = schema.Entity(title=u"Manufacturer", readonly=True,
                                group='Details')
    product = schema.Entity(title=u"Model", readonly=True, group='Details')
    slot = schema.Int(title=u"Slot", readonly=False,group='Details')
    size = schema.Text(title=u"Size", readonly=True, group='Details')

class IDiskDriveInfo(IComponentInfo):
    """
    Info adapter for Disk Drive components.
    """
    manufacturer = schema.Entity(title=u"Manufacturer", readonly=True,
                                                                group='Details')
    product = schema.Entity(title=u"Model", readonly=True, group='Details')
    serialNumber = schema.Text(title=u"Serial #", readonly=True,group='Details')
    FWRev = schema.Text(title=u"Firmware", readonly=True, group='Details')
    size = schema.Text(title=u"Size", readonly=True, group='Details')
    diskType = schema.Text(title=u"Type", readonly=True, group='Details')
    chassis = schema.Entity(title=u"Chassis", readonly=True,group='Details')
    storagePool = schema.Entity(title=u"Disk Group", readonly=True,
                                                                group='Details')
    bay = schema.Int(title=u"Bay", readonly=False, group='Details')

class IChassisInfo(IComponentInfo):
    """
    Info adapter for Chassis components.
    """
    manufacturer = schema.Entity(title=u"Manufacturer", readonly=True,
                                                                group='Details')
    product = schema.Entity(title=u"Model", readonly=True, group='Details')
    serialNumber = schema.Text(title=u"Serial #", readonly=True,group='Details')
    layout = schema.Text(title=u"Layout String", readonly=False,group='Details')

class IStoragePoolInfo(IComponentInfo):
    """
    Info adapter for Storage Pool components.
    """
    totalDisks = schema.Int(title=u"Total Disk", readonly=True, group="Details")
    totalBytesString = schema.Text(title=u"Total Bytes", readonly=True,
                                                                group="Details")
    usedBytesString = schema.Text(title=u"Used Bytes", readonly=True,
                                                                group="Details")
    availBytesString = schema.Text(title=u"Available Bytes", readonly=True,
                                                                group="Details")
    capacity = schema.Text(title=u"Utilization", readonly=True, group="Details")

class IStorageVolumeInfo(IComponentInfo):
    """
    Info adapter for Storage Volume components.
    """
    storagePool = schema.Entity(title=u"Disk Group", readonly=True,
                                                                group='Details')
    accessType = schema.Text(title=u"Access Type", readonly=True,
                                                                group='Details')
    diskType = schema.Text(title=u"Disk Type", readonly=True, group='Details')
    totalBytesString = schema.Text(title=u"Total Bytes", readonly=True,
                                                                group="Details")
class IPowerSupplyInfo(IComponentInfo):
    """
    Info adapter for PowerSupply components.
    """
    watts = schema.Int(title=u'Watts', group='Overview', readonly=True)
    type = schema.Text(title=u'Type', group='Overview', readonly=True)
    millivolts = schema.Int(
        title=u'Millivolts', group='Overview', readonly=True)

class ITemperatureSensorInfo(IComponentInfo):
    """
    Info adapter for TemperatureSensor components.
    """
    temperature = schema.Int(
        title=u'Temperature (Fahrenheit)', group='Overview', readonly=True)

class IFanInfo(IComponentInfo):
    """
    Info adapter for Fan components.
    """
    type = schema.Text(title=u'Type', group='Overview', readonly=True)
    rpm = schema.Text(title=u'RPM', group='Overview', readonly=True)

class IComputerSystemInfo(IExpansionCardInfo):
    """
    Info adapter for Controller components.
    """
    FWRev = schema.Text(title=u"Firmware", readonly=True, group='Details')
    uptime = schema.Text(title=u"Uptime", readonly=True, group='Details')

class INetworkPortInfo(IIpInterfaceInfo):
    """
    Info adapter for Controller components.
    """
    controller =schema.Entity(title=u"Controller",readonly=True,group='Details')
