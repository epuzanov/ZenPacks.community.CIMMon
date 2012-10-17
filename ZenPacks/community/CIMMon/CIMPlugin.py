################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMPlugin

CIMPlugin extends SQLPlugin with CIM specific attributes and methods.

$Id: CIMPlugin.py,v 1.7 2012/10/17 18:09:10 egor Exp $"""

__version__ = '$Revision: 1.7 $'[11:-2]

from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin

class CIMPlugin(SQLPlugin):
    """CIMPlugin extends SQLPlugin with CIM specific attributes and methods."""

    deviceProperties = SQLPlugin.deviceProperties + ('snmpSysName',)

    def _getSysnames(self, device, results={}, tableName=""):
        systems = {}
        findCSName = "CIM_SystemComponent" in results
        snmpSysName = (getattr(device, "snmpSysName", ""
                        ) or device.id).strip().lower()
        for comp in (results.get(tableName) or ()):
            compSysName = comp.get("_sysname", "").lower()
            csSysName = snmpSysName
            if findCSName:
                path = (self._getComputerSystemPath(results,
                    comp.get("setPath")) or comp.get("setPath") or "").lower()
                kwargs = {}
                if '.' in path:
                    try:kwargs = eval("(lambda **kwargs:kwargs)(%s)"%path.split(
                                                                    ".", 1)[1])
                    except: pass
                csSysName = kwargs.get("name") or ""
            else:
                csSysName = snmpSysName in compSysName and snmpSysName or ""
            csName = systems.setdefault(csSysName, set())
            if compSysName:
                csName.add(compSysName)
        result = [snmpSysName, ""]
        for sysname, subsystems in systems.iteritems():
            if snmpSysName not in sysname: continue
            result.extend(subsystems)
            if snmpSysName in systems: continue
            if sysname.startswith(result[0]) and sysname > result[0]:
                result[0] = sysname
        if len(result) == 2:
            for sysname, subsystems in systems.iteritems():
                result.extend(subsystems)
        return result

    def _findInstance(self, results, tableName, sProp, sValue):
        if not sValue: return {}
        for inst in results.get(tableName) or ():
            if inst.get(sProp, "").endswith(sValue): return inst
        return {}

    def _getComputerSystemPath(self, results, iPath):
        if not iPath: return ""
        cs = self._findInstance(results, "CIM_SystemComponent", "pc", iPath)
        if not cs:
           cs = self._findInstance(results, "CIM_SystemComponent", "gc", iPath)
           if cs: return iPath
        return self._getComputerSystemPath(results,
                                        cs.get("gc", "")) or cs.get("gc", "")

    def _getCollections(self, results, inst):
        collections = []
        member = inst.get("setPath")
        if member:
            for moc in results.get("CIM_MemberOfCollection") or ():
                if moc.get("member") == member:
                    collections.append(moc.get("collection"))
        return collections

    def _getStatPath(self, results, inst):
        return self._findInstance(results, "CIM_ElementStatisticalData", "me",
            inst.get("setPath")).get("stats") or ""

    def _setCimStatusName(self, inst):
        status = None
        if "status" in inst:
            cimStatusName = "OperationalStatus"
            status = inst.pop("status")
            if isinstance(status, (list, tuple)):
                status = len(status) > 0 and status[0] or 0
                if str(status).replace(".","").isdigit():
                    status = int(float(status))
        if "state" in inst:
            state = inst.pop("state")
            if status in (None, ""):
                cimStatusName = "Status"
                status = {"OK":2, "Error":6, "Degraded":3, "Unknown":0,
                    "Pred Fail":5, "Starting":8, "Stopping":9, "Service":11,
                    "Stressed":4, "NonRecover":7, "No Contact":12,
                    "Lost Comm":13, "good":2}.get(state)
        if status is None:
            status = 0
            cimStatusName = ""
        # inst['status'] = status
        inst["cimStatusName"] = cimStatusName
