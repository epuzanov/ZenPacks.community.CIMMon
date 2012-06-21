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

- **zCIMConnectionString** - connection string for OS components (FileSystems,
  Processes, Interfaces, etc)
- **zCIMHWConnectionString** - connection string for Hardware components (Fans,
  HardDisks, Temperature Sensors)

an example for HP ProLiant Server running Windows with HP Management Agent
installed (both OS and HW monitored over WMI):

zCIMConnectionString:

    ::

        'pywmidb',host='${here/manageIp}',user='${here/zWinUser}',password='${here/zWinPassword}',namespace='root/cimv2'

zCIMHWConnectionString:

    ::

        'pywmidb',host='${here/manageIp}',user='${here/zWinUser}',password='${here/zWinPassword}',namespace='root/hpq'

an example for IBM Server (WBEM monitored) running Windows (WinRM2 monitored):

zCIMConnectionString:

    ::

        'pywsmandb',scheme='http',host='${here/manageIp}',port=5985,user='${here/zWinUser}',password='${here/zWinPassword}',namespace='root/cimv2'

zCIMHWConnectionString:

    ::

        'pywbemdb',scheme='https',host='${here/manageIp}',port=5989,user='${here/zWinUser}',password='${here/zWinPassword}',namespace='root/ibmsd'

for HP EVA monitoring set both zCIMConnectionString and zCIMHWConnectionString to:

    ::

        'pywbemdb',scheme='https',host='CommandViewIpAddress',port=5989,user='${here/zWinUser}',password='${here/zWinPassword}',namespace='root/eva'


Modeler Plugins
---------------

- **community.cim.CIMChassisMap** - Chassis modeler plugin, tried to identify
  Model, Vendor and Serial Number information for Device, and Disk Enclosures
- **community.cim.CIMCollectionMap** - Collection modeler plugin, tried to
  identify Redundancy and Replication sets
- **community.cim.CIMComputerSystemMap** - ComputerSystem modeler plugin, tried
  to identify snmpSysName, snmpDescr, snmpContact, Model, Vendor and Serial
  Number information for Device, and also collect subsystems (RAID Controllers,
  FC HBAs, Management Bords) information if pressent
- **community.cim.CIMControllerMap** - PCI cards modeler plugin, tried to
  identify all PCI cards
- **community.cim.CIMDiskDriveMap** - Hard Disks modeler plugin
- **community.cim.CIMFanMap** - Fan (without tachometer) modeler plugin
- **community.cim.CIMFileSystemMap** - File System modeler plugin (do not use it
  with Windows Servers)
- **community.cim.CIMNetworkAdapterMap** - IpInterfaces modeler plugin (based on
  deprecated CIM_NetworkAdapter class, Windows WMI used it...)
- **community.cim.CIMNetworkPortMap** - IpInterfaces modeler plugin wich
  supported FC Ports too
- **community.cim.CIMOperatingSystemMap** - Operating System modeler plugin,
  tried identify OS Version, OS Vendor, Total memory and Swap memory
- **community.cim.CIMPhysicalMemoryMap** - Physical Memory modeler plugin, tried
  to identify memory modules installed in server
- **community.cim.CIMPowerSupplyMap** - Power Supply modeler plugin
- **community.cim.CIMProcessMap** - OS Process modeler plugin
- **community.cim.CIMProcessorMap** - CPU modeler plugin
- **community.cim.CIMStoragePoolMap** - Storage Pool (Disk Group) modeler
  plugin, tried to identify storage pools configured on RAID controller
- **community.cim.CIMStorageVolumeMap** - Storage Volume modeler plugin, tried
  to identify Logical Disks configured on RAID Controller
- **community.cim.CIMTachometerMap** - Fan (with tachometer) modeler plugin
- **community.cim.CIMTemperatureSensorMap** - Temperature Sensor modeler plugin
- **community.cim.CIMUnixProcessMap** - Unix Process modeler plugin (do not use
  it with Windows Servers)
- **community.cim.SNIAChassisMap** - advanced replacement for CIMChassisMap
  plugin which tried to set components dependencies
- **community.cim.SNIAComputerSystemMap** - advanced replacement for
  CIMComputerSystemMap plugin which tried to set components dependencies.
- **community.cim.SNIADiskDriveMap** - advanced replacement for CIMDiskDriveMap
  plugin which tried to set components dependencies, place it in plugins list
  after SNIAStoragePoolMap and SNIAChassisMap plugins
- **community.cim.SNIANetworkPortMap** - advanced replacement for
  CIMNetworkPortMap plugin which tried to set components dependencies
- **community.cim.SNIAStoragePoolMap** - advanced replacement for
  CIMStoragePoolMap plugin which tried to set components dependencies
- **community.cim.SNIAStorageVolumeMap** - advanced replacement for
  CIMStorageVolumeMap plugin which tried to set components dependencies, place
  it in plugins list after SNIAStoragePoolMap plugin
- **community.cim.Win32DiskDriveMap** - Disk Drive modeler plugin for Windows
  Server
- **community.cim.Win32IP4RouteTableMap** - IP Route modeler plugin for Windows
  Server
- **community.cim.Win32LogicalDiskMap** - File System modeler plugin for Windows
  Server (Win32_LogicalDisk based)
- **community.cim.Win32NetworkAdapterMap** - IpInterfaces modeler plugin for
  Windows server
- **community.cim.Win32ProcessMap** - OS Process modeler plugin for Windows
  Server
- **community.cim.Win32ProcessorMap** - CPU modeler plugin for Windows Server
- **community.cim.Win32ServiceMap** - Windows Services modeler plugin
- **community.cim.Win32VolumeMap** - File System modeler plugin for Windows
  Server (Win32_Volume based)


Device Classes
--------------

- Devices/Server/CIM
- Devices/Server/CIM/Linux
- Devices/Server/Windows/CIM
- Devices/Storage/SMI-S


Monitoring Templates
--------------------

- Devices/Server/Windows/CIM/Device
- Devices/Server/Windows/CIM/OSProcess
- Devices/Server/Windows/CIM/Win32_DiskDrive
- Devices/Server/Windows/CIM/Win32_LogicalDisk
- Devices/Server/Windows/CIM/Win32_NetworkAdapter
- Devices/Server/Windows/CIM/Win32_PerfRawData_PerfDisk_LogicalDisk
- Devices/Server/Windows/CIM/Win32_PerfRawData_PerfDisk_PhysicalDisk
- Devices/Server/Windows/CIM/Win32_PerfRawData_Tcpip_NetworkInterface
- Devices/Server/Windows/CIM/Win32_Volume
- Devices/Server/Windows/CIM/WinService
- Devices/CIM_BlockStorageStatisticalData
- Devices/CIM_Collection
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

Reports
-------

- Reports/Device Reports/SMI-S Reports/Hard Disks
- Reports/Device Reports/SMI-S Reports/Controllers
