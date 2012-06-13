################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""Win32ProcessorMap

Win32ProcessorMap maps the Win32_Processor class to CPU objects

$Id: Win32ProcessorMap.py,v 1.0 2012/06/13 20:54:19 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMProcessorMap \
    import CIMProcessorMap

class Win32ProcessorMap(CIMProcessorMap):
    """Map Win32_Processor class to CPU class"""

    deviceProperties=CIMProcessorMap.deviceProperties+('zCIMConnectionString',)

    def queries(self, device):
        connectionString = getattr(device, 'zCIMConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_Processor":
                (
                    "SELECT * FROM Win32_Processor",
                    None,
                    cs,
                    {
                        "snmpindex":"__path",
                        "_status":"CpuStatus",
                        "id":"DeviceID",
                        "_name":"Name",
                        "voltage":"CurrentVoltage",
                        "clockspeed":"MaxClockSpeed",
                        "_extspeed":"ExternalBusClockSpeed",
                        "extspeed":"ExtClock",
                        "core":"NumberOfCores",
                        "socket":"SocketDesignation",
                        "_voltage":"VoltageCaps",
                    }
                ),
            "CIM_CacheMemory":
                (
                    "SELECT * FROM Win32_CacheMemory",
                    None,
                    cs,
                    {
                        "BlockSize":"BlockSize",
                        "level":"Level",
                        "Blocks":"NumberOfBlocks",
                    }
                ),
            }

    def _getSocketNumber(self, instance):
        """return cpu socket number"""
        return int(instance.get("id", "CPU0")[3:] or 0)

    def _getExtspeed(self, instance):
        """return external bus clock speed"""
        return int(instance.get("extspeed",0) or instance.get("_extspeed",0) or 0)

    def _getVoltage(self, instance):
        """return cpu voltage"""
        voltage = {"1":50, "2":33, "4":29}.get(str(instance["_voltage"]), 0)
        if not voltage:
            voltage = int(instance.get("voltage", None) or 0)
        return voltage * 100

    def _getCacheMemory(self, results, instance):
        """processing CacheMemory table"""
        cache = {1:0, 2:0, 3:0}
        cpus = len([i for i in results.get("CIM_Processor") if i.get("_status",
                                                                    1)>0]) or 1
        caches = 0
        for inst in results.get("CIM_CacheMemory", ()):
            try:
                level = int(inst.get("level", 0) or 0) - 2
                if level == 2: caches = caches + 1
                cache[level] = int(inst.get("BlockSize", 0) or 0) * int(
                            inst.get("Blocks", 0) or 0) / 1024 + cache[level]
            except: continue
        if caches < cpus: return cache
        for level in (1, 2, 3):
            cache[level] = cache[level] / cpus
        return cache
