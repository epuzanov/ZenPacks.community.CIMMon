################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMReplicationGroupMap

CIMReplicationGroupMap maps CIM_ReplicationGroup class to ReplicationGroup class.

$Id: CIMReplicationGroupMap.py,v 1.0 2012/06/13 20:43:13 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from ZenPacks.community.CIMMon.CIMPlugin import CIMPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

class CIMReplicationGroupMap(CIMPlugin):
    """Map CIM_ReplicationGroup class to ReplicationGroup class"""

    maptype = "ReplicationGroupMap"
    modname = "ZenPacks.community.CIMMon.CIM_ReplicationGroup"
    relname = "replicationgroups"
    compname = "os"
    deviceProperties = CIMPlugin.deviceProperties + ('zCIMConnectionString',)

    def queries(self, device):
        connectionString = getattr(device, 'zCIMConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_ReplicationGroup":
                (
                    "SELECT * FROM CIM_ReplicationGroup",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "id":"InstanceID",
                        "title":"ElementName",
                        "_sysname":"InstanceID",
                    },
                ),
            }

    def _getSysnames(self, device, results={}, tableName=""):
        sysnames = []
        snmpSysName = (getattr(device, "snmpSysName", ""
                        ) or device.id).strip().lower()
        for inst in results.get("CIM_ReplicationGroup") or ():
            instid = str(inst.get("id") or "").lower()
            if snmpSysName not in instid: continue
            sysnames.append(instid)
        return sysnames

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        instances = results.get("CIM_ReplicationGroup")
        if not instances: return rm
        sysnames = self._getSysnames(device, results, "CIM_ReplicationGroup")
        for inst in instances:
            if (inst.get("_sysname") or "").lower() not in sysnames: continue
            try:
                om = self.objectMap(inst)
                om.id = self.prepId(om.id)
            except AttributeError:
                continue
            rm.append(om)
        return rm
