################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""info.py

Representation of CIM components.

$Id: info.py,v 1.3 2012/06/25 21:10:56 egor Exp $"""

__version__ = "$Revision: 1.3 $"[11:-2]

from zope.interface import implements
from ZenPacks.community.CIMMon import interfaces
from ZenPacks.community.CIMMon.infos import *

class CIM_PhysicalMemoryInfo(PhysicalMemoryInfo):
    implements(interfaces.IPhysicalMemoryInfo)

class CIM_DiskDriveInfo(DiskDriveInfo):
    implements(interfaces.IDiskDriveInfo)

class CIM_ChassisInfo(ChassisInfo):
    implements(interfaces.IChassisInfo)

class CIM_StoragePoolInfo(StoragePoolInfo):
    implements(interfaces.IStoragePoolInfo)

class CIM_StorageVolumeInfo(StorageVolumeInfo):
    implements(interfaces.IStorageVolumeInfo)

class CIM_FanInfo(FanInfo):
    implements(interfaces.IFanInfo)

class CIM_PowerSupplyInfo(PowerSupplyInfo):
    implements(interfaces.IPowerSupplyInfo)

class CIM_TemperatureSensorInfo(TemperatureSensorInfo):
    implements(interfaces.ITemperatureSensorInfo)

class CIM_ComputerSystemInfo(ComputerSystemInfo):
    implements(interfaces.IComputerSystemInfo)

class CIM_NetworkPortInfo(NetworkPortInfo):
    implements(interfaces.INetworkPortInfo)

class CIM_RedundancySetInfo(RedundancySetInfo):
    implements(interfaces.IRedundancySetInfo)

class CIM_ReplicationGroupInfo(ReplicationGroupInfo):
    implements(interfaces.IReplicationGroupInfo)
