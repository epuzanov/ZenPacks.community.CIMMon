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

$Id: CIMPlugin.py,v 1.1 2012/06/14 20:52:19 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]

from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin

class CIMPlugin(SQLPlugin):
    """CIMPlugin extends SQLPlugin with CIM specific attributes and methods."""

    deviceProperties = SQLPlugin.deviceProperties + ('snmpSysName',)

    def _getSysnames(self, device, results={}, tableName=""):
        systems = {}
        findCSName = "CIM_SystemComponent" in results
        snmpSysName = (getattr(device, "snmpSysName1", ""
                        ) or device.id).strip().lower()
        for comp in (results.get(tableName) or ()):
            compSysName = comp.get("_sysname", "")
            csSysName = snmpSysName
            if findCSName:
                path = (self._getComputerSystemPath(results,
                    comp.get("setPath","")) or comp.get("setPath") or "").lower()
                kwargs = {}
                if '.' in path:
                    try: kwargs = eval("(lambda **kwargs:kwargs)(%s)"%path.split(".",1)[1])
                    except: pass
                csSysName = kwargs.get("name") or ""
            csName = systems.setdefault(csSysName, set())
            if compSysName:
                csName.add(compSysName.lower())
        result = [snmpSysName, ""]
        for sysname, subsystems in systems.iteritems():
            if snmpSysName not in sysname: continue
            result.extend(subsystems)
            if snmpSysName in systems: continue
            if sysname.startswith(result[0]) and sysname > result[0]:
                result[0] = sysname
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

    def _getStatPath(self, results, inst):
        return self._findInstance(results, "CIM_ElementStatisticalData", "me",
            inst.get("setPath")).get("stats") or ""
