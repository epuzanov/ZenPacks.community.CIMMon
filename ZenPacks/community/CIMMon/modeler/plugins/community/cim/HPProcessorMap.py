################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPProcessorMap

HPProcessorMap maps the HP_Processor class to cpus objects

$Id: HPProcessorMap.py,v 1.0 2011/06/21 21:29:32 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

import re
CACHELEVEL = re.compile(r'.*(\d).*(\d).*(\d).*')

def getManufacturerAndModel(key):
    """
    Attempts to parse accurate manufacturer and model information of a CPU from
    the single product string passed in.

    @param key: A product key. Hopefully containing manufacturer and model name.
    @type key: string
    @return: A MultiArgs object containing the model and manufacturer.
    @rtype: Products.DataDollector.plugins.DataMaps.MultiArgs
    """
    cpuDict = {
        'Intel': '(Intel|Pentium|Xeon)',
        'AMD': '(AMD|Opteron|Athlon|Sempron|Phenom|Turion)',
        'VIA': '(VIA)',
        'ARM': '(ARM)',
        'IBM': '(IBM)',
        'HP': '(HP)',
        'NEC': '(NEC)',
        'Cyrix': '(Cyrix)',
        'DEC': '(DEC)',
        'MIPS': '(MIPS)',
        'Sun': '(Sun)',
        'Motorola': '(Motorola)',
        'Transmeta': '(Transmeta)',
        }

    for manufacturer, regex in cpuDict.items():
        if re.search(regex, key):
            return MultiArgs(key, manufacturer)

    # Revert to default behavior if no specific match is found.
    return MultiArgs(key, "Unknown")


class HPProcessorMap(SQLPlugin):

    maptype = "CPUMap"
    modname = "ZenPacks.community.CIMMon.CIM_Processor"
    compname = "hw"
    relname = "cpus"
    deviceProperties = SQLPlugin.deviceProperties + ('zWinUser',
                                                    'zWinPassword',
                                                    'zCIMHWConnectionString',
                                                    )

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
        if 'namespace' not in kwargs: args.append("namespace='root/HPQ'")
        cs = ','.join(args)
        return {
            "CIM_Processor":
                (
                    "SELECT CPUStatus,CurrentClockSpeed,DeviceID,ExternalBusClockSpeed,Description,NumberOfEnabledCores FROM HP_Processor",
                    None,
                    cs,
                    {
                        'CPUStatus':'_status',
                        'CurrentClockSpeed':'clockspeed',
                        'DeviceID':'id',
                        'ExternalBusClockSpeed':'extspeed',
                        'Description':'_name',
                        'NumberOfEnabledCores':'core',
                    }
                ),
            "CIM_CacheMemory":
                (
                    "SELECT BlockSize,DeviceID,NumberOfBlocks FROM HP_ProcessorCacheMemory",
                    None,
                    cs,
                    {
                        'BlockSize':'BlockSize',
                        'DeviceID':'DeviceID',
                        'NumberOfBlocks':'NumberOfBlocks',
                    }
                ),
            }

    def processCacheMemory(self, instances):
        """processing CacheMemory table"""
        cache = {1:0, 2:0, 3:0}
        firstcpu = None
        for inst in instances:
            try:
                cpu, core, level = CACHELEVEL.search(inst['DeviceID']).groups()
                if firstcpu is None: firstcpu = cpu
                if firstcpu != cpu: continue
                cache[int(level)] = inst['BlockSize'] * inst['NumberOfBlocks'] \
                                                / 1024 + int(cache[int(level)])
            except: continue
        return cache


    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        cache = self.processCacheMemory(results.get("CIM_CacheMemory", []))
        for instance in results.get("CIM_Processor", []):
            om = self.objectMap(instance)
            if om._status == 0: continue
            try:
                om.socket = om.id.split()[-1]
                om.id = self.prepId(om.id)
                if not om.extspeed: om.extspeed = 0
                om.cacheSizeL1 = cache.get(1, 0)
                om.cacheSizeL2 = cache.get(2, 0)
#                om.cacheSizeL3 = cache.get(3, 0)
                om.setProductKey = getManufacturerAndModel(om._name)
            except AttributeError:
                continue
            rm.append(om)
        return rm
