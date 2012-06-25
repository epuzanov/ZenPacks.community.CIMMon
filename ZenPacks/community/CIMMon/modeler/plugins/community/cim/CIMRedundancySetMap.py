################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMRedundancySetMap

CIMRedundancySetMap maps CIM_RedundancySet class to RedundancySet class.

$Id: CIMRedundancySetMap.py,v 1.0 2012/06/13 20:43:13 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from ZenPacks.community.CIMMon.CIMPlugin import CIMPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs


class CIMRedundancySetMap(CIMPlugin):
    """Map CIM_RedundancySet class to RedundancySet class"""

    maptype = "RedundancySetMap"
    modname = "ZenPacks.community.CIMMon.CIM_RedundancySet"
    relname = "redundancysets"
    compname = "os"
    deviceProperties = CIMPlugin.deviceProperties + ('zCIMConnectionString',)

    def queries(self, device):
        connectionString = getattr(device, 'zCIMConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_RedundancySet":
                (
                    "SELECT * FROM CIM_RedundancySet",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "id":"InstanceID",
                        "title":"ElementName",
                        "loadBalanceAlgorithm":"LoadBalanceAlgorithm",
                        "_loadBalanceAlgorithm":"OtherLoadBalanceAlgorithm",
                        "minNumberNeeded":"MinNumberNeeded",
                        "_typeOfSet":"OtherTypeOfSet",
                        "typeOfSet":"TypeOfSet",
                        "_sysname":"InstanceID",
                    },
                ),
            }

    def _getSysnames(self, device, results={}, tableName=""):
        sysnames = []
        snmpSysName = (getattr(device, "snmpSysName", ""
                        ) or device.id).strip().lower()
        for inst in results.get("CIM_RedundancySet") or ():
            instid = str(inst.get("id") or "").lower()
            if snmpSysName not in instid: continue
            sysnames.append(instid)
        return sysnames

    def _getLoadBalanceAlgorithm(self, inst):
        LBALGS = ("Unknown", "Other", "No Load Balancing", "Round Robin",
                "Least Blocks","Least IO","Address Region","Product Specific")
        lbalg = inst.get("loadBalanceAlgorithm")
        try:
            return lbalg>1 and LBALGS[lbalg] or inst.get("_loadBalanceAlgorithm"
                                                                ) or "Unknown"
        except:
            return "Unknown"

    def _getTypeOfSet(self, inst):
        SETTYPES = ("Unknown", "Other", "N+1", "Load Balanced", "Sparing",
                    "Limited Sparing")
        results = []
        sTypes = inst.get("typeOfSet") or ()
        if isinstance(sTypes, (str, unicode)):
            sTypes = sTypes.split()
        oTypes = inst.get("_typeOfSet") or ()
        if isinstance(oTypes, (str, unicode)):
            oTypes = oTypes.split()
        for idx, rsType in enumerate(sTypes):
            try:results.append(rsType != 1 and SETTYPES[rsType] or oTypes[idx])
            except IndexError: pass
        return " ".join(results)

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        instances = results.get("CIM_RedundancySet")
        if not instances: return rm
        sysnames = self._getSysnames(device, results, "CIM_RedundancySet")
        for inst in instances:
            if (inst.get("_sysname") or "").lower() not in sysnames: continue
            try:
                om = self.objectMap(inst)
                om.id = self.prepId(om.id)
                if "typeOfSet" in inst:
                    om.typeOfSet = self._getTypeOfSet(inst)
                if "loadBalanceAlgorithm" in inst:
                    om.loadBalanceAlgorithm=self._getLoadBalanceAlgorithm(inst)
            except AttributeError:
                continue
            rm.append(om)
        return rm
