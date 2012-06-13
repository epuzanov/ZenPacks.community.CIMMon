================================
ZenPacks.community.CIMMon
================================

About
=====

This ZenPack provides basic infrastructure (components classes and modeler
plugins) for CIM based monitoring.

Requirements
============

Zenoss
------

You must first have, or install, Zenoss 2.5.2 or later. This ZenPack was tested
against Zenoss 2.5.2 and Zenoss 3.2. You can download the free Core version of
Zenoss from http://community.zenoss.org/community/download.

ZenPacks
--------

You must first install:

- `SQLDataSource ZenPack <http://community.zenoss.org/docs/DOC-5913>`_.
- `Advanced Device Details ZenPack <http://community.zenoss.org/docs/DOC-3452>`_ 
  (Zenoss 2.5.x only)


Installation
============

Normal Installation (packaged egg)
----------------------------------

Download the `CIMMon ZenPack <http://community.zenoss.org/docs/DOC-0000>`_.
Copy this file to your Zenoss server and run the following commands as the zenoss
user.

    ::

        zenpack --install ZenPacks.community.CIMMon-1.0.egg
        zenoss restart

Developer Installation (link mode)
----------------------------------

If you wish to further develop and possibly contribute back to the CIMMon
ZenPack you should clone the git `repository <https://github.com/epuzanov/ZenPacks.community.CIMMon>`_,
then install the ZenPack in developer mode using the following commands.

    ::

        git clone git://github.com/epuzanov/ZenPacks.community.CIMMon.git
        zenpack --link --install ZenPacks.community.CIMMon
        zenoss restart


Usage
=====

Installing the ZenPack will add the following items to your Zenoss system.


zProperties
-----------

- zCIMConnectionString
- zCIMHWConnectionString


Modeler Plugins
---------------

- community.cim.CIMChassisMap.py
- community.cim.CIMComputerSystemMap.py
- community.cim.CIMControllerMap.py
- community.cim.CIMDiskDriveMap.py
- community.cim.CIMFanMap.py
- community.cim.CIMFileSystemMap.py
- community.cim.CIMNetworkAdapterMap.py
- community.cim.CIMNetworkPortMap.py
- community.cim.CIMOperatingSystemMap.py
- community.cim.CIMPhysicalMemoryMap.py
- community.cim.CIMPowerSupplyMap.py
- community.cim.CIMProcessMap.py
- community.cim.CIMProcessorMap.py
- community.cim.CIMStoragePoolMap.py
- community.cim.CIMStorageVolumeMap.py
- community.cim.CIMTachometerMap.py
- community.cim.CIMTemperatureSensorMap.py
- community.cim.CIMUnixProcessMap.py
- community.cim.SNIAChassisMap.py
- community.cim.SNIAComputerSystemMap.py
- community.cim.SNIADiskDriveMap.py
- community.cim.SNIANetworkPortMap.py
- community.cim.SNIAStoragePoolMap.py
- community.cim.SNIAStorageVolumeMap.py
- community.cim.Win32IP4RouteTableMap.py
- community.cim.Win32LogicalDiskMap.py
- community.cim.Win32NetworkAdapterMap.py
- community.cim.Win32ProcessMap.py
- community.cim.Win32ProcessorMap.py
- community.cim.Win32ServiceMap.py
- community.cim.Win32VolumeMap.py


Monitoring Templates
--------------------

- Devices/Server/Windows/CIM/Device
- Devices/Server/Windows/CIM/OSProcess
- Devices/Server/Windows/CIM/Win32_LogicalDisk
- Devices/Server/Windows/CIM/Win32_NetworkAdapter
- Devices/Server/Windows/CIM/Win32_PerfRawData_PerfDisk_LogicalDisk
- Devices/Server/Windows/CIM/Win32_PerfRawData_PerfDisk_PhysicalDisk
- Devices/Server/Windows/CIM/Win32_PerfRawData_Tcpip_NetworkInterface
- Devices/Server/Windows/CIM/Win32_Volume
- Devices/Server/Windows/CIM/WinService
- Devices/CIM_BlockStorageStatisticalData
- Devices/CIM_Device
- Devices/CIM_FileSystem
- Devices/CIM_ManagedSystemElement
- Devices/CIM_MediaAccessStatData
- Devices/CIM_NetworkAdapter
- Devices/CIM_NetworkPort
- Devices/CIM_Processor
- Devices/CIM_StorageVolume
- Devices/CIM_Tachometer
- Devices/CIM_TemperatureSensor
