################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMPhysicalMemoryMap

CIMPhysicalMemoryMap maps the CIM_PhysicalMemory to CIMPhysicalMemory objects

$Id: CIMPhysicalMemoryMap.py,v 1.0 2011/06/07 20:34:28 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.ZenUtils.Utils import convToUnits
from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin

import re
MODULENAME = re.compile(r'.*(\d).*(\d).*')

class CIMPhysicalMemoryMap(SQLPlugin):
    """Map CIM_PhysicalMemoryMap class to CIMPhysicalMemory class"""

    maptype = "CIMPhysicalMemoryMap"
    modname = "ZenPacks.community.CIMMon.CIM_PhysicalMemory"
    relname = "memorymodules"
    compname = "hw"
    deviceProperties = SQLPlugin.deviceProperties + ('zWinUser',
                                                    'zWinPassword',
                                                    'zCIMConnectionString',
                                                    'zCIMHWNamespace',
                                                    )

    slottypes  =  { 0: 'Slot',
                    1: 'Slot',
                    2: 'SIP',
                    3: 'DIP',
                    4: 'ZIP',
                    5: 'SOJ',
                    6: 'Proprietary',
                    7: 'SIMM',
                    8: 'DIMM',
                    9: 'TSOP',
                    10:'PGA',
                    11:'RIMM',
                    12:'SO-DIMM',
                    13:'SRIMM',
                    14:'SMD',
                    15:'SSMP',
                    16:'QFP',
                    17:'TQFP',
                    18:'SOIC',
                    19:'LCC',
                    20:'PLCC',
                    21:'BGA',
                    22:'FPBGA',
                    23:'LGA',
                    }

    technologies = {0: 'Unknown',
                    1: 'Other',
                    2: 'DRAM',
                    3: 'Synchronous DRAM',
                    4: 'Cache DRAM',
                    5: 'EDO',
                    6: 'EDRAM',
                    7: 'VRAM',
                    8: 'SRAM',
                    9: 'RAM',
                    10:'ROM',
                    11:'Flash',
                    12:'EEPROM',
                    13:'FEPROM',
                    14:'EPROM',
                    15:'CDRAM',
                    16:'3DRAM',
                    17:'SDRAM',
                    18:'SGRAM',
                    19:'RDRAM',
                    20:'DDR',
                    21:'DDR2',
                    22:'BRAM',
                    23:'FB-DIMM',
                    24:'DDR3',
                    25:'FBD2',
                    }

    def queries(self, device):
        args = [getattr(device, 'zCIMConnectionString',
                                        "'pywbemdb',scheme='https',port=5989")]
        kwargs = eval('(lambda *argsl,**kwargs:kwargs)(%s)'%args[0])
        if 'host' not in kwargs:
            args.append("host='%s'"%device.manageIp)
        if 'user' not in kwargs:
            args.append("user='%s'"%getattr(device, 'zWinUser', ''))
        if 'password' not in kwargs:
            args.append("password='%s'"%getattr(device, 'zWinPassword', ''))
        if 'namespace' not in kwargs:
            args.append("namespace='%s'"%getattr(device, 'zCIMHWNamespace',
                                                'root/cimv2'))
        cs = ','.join(args)
        return {
            "CIM_PhysicalMemory":
                (
                    "SELECT __PATH,__NAMESPACE,Capacity,FormFactor,Manufacturer,MemoryType,Name,SerialNumber,Speed FROM CIM_PhysicalMemory",
                    None,
                    cs,
                    {
                        '__PATH':'_path',
                        '__NAMESPACE':'cimNamespace',
                        'Capacity':'size',
                        'FormFactor':'_slottype',
                        'Manufacturer':'_manufacturer',
                        'MemoryType':'_technology',
                        'Name':'slot',
                        'SerialNumber':'serialNumber',
                        'Speed':'_speed',
                    },
                ),
            }


    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        for instance in results.get("CIM_PhysicalMemory", []):
            om = self.objectMap(instance)
            try:
                om.slot, board = MODULENAME.search(om.slot).groups()
                om.id = self.prepId("Board%s %s %s" % (board,
                                        self.slottypes.get(om._slottype,'Slot'),
                                        om.slot))
                om.cimClassName, om.cimKeybindings = om._path.split('.', 1)
                if om.size > 0:
                    model = []
                    if not om._manufacturer: om._manufacturer = ''
                    model.append(getattr(om, '_manufacturer', ''))
                    if self.technologies.get(om._technology, '') != '':
                        model.append(self.technologies.get(om._technology, ''))
                    if self.slottypes.get(om._slottype, '') != '' and om._slottype > 1:
                        model.append(self.slottypes.get(om._slottype, ''))
                    model.append(convToUnits(om.size))
                    if getattr(om, '_frequency', 0) > 0:
                        model.append("%sMHz" % getattr(om, '_frequency', 0))
                    if getattr(om, '_speed', 0) > 0:
                        model.append("%sns" % getattr(om, '_speed', 0))
                    om.setProductKey = "%s" % " ".join(model)
            except AttributeError:
                continue
            rm.append(om)
        return rm
