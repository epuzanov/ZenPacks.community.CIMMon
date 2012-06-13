################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMProcessMap

CIMProcessMap finds various processes running on a device.

$Id: CIMProcessMap.py,v 1.2 2012/06/13 20:47:15 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]

from ZenPacks.community.CIMMon.CIMPlugin import CIMPlugin

class CIMProcessMap(CIMPlugin):
    """Map CIM_Process class to OSProcess class"""

    maptype = "OSProcessMap"
    compname = "os"
    relname = "processes"
    modname = "Products.ZenModel.OSProcess"
    classname = "createFromObjectMap"
    deviceProperties = CIMPlugin.deviceProperties + ('zCIMConnectionString',)

    def queries(self, device):
        connectionString = getattr(device, 'zCIMConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_Process":
                (
                    "SELECT Name FROM CIM_Process",
                    None,
                    cs,
                    {
                        "procName":"Name",
                    }
                ),
            }


    def process(self, device, results, log):
        """collect SQL information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        instances = results.get("CIM_Process")
        if not instances: return rm
        for inst in instances:
            try:
                om = self.objectMap(inst)
                if not getattr(om, 'procName', False): 
                    log.warning("Skipping process with no name")
                    continue
                om.parameters = getattr(om, 'parameters', '') or ''
                if isinstance(om.parameters, (list, tuple)):
                    om.parameters = ' '.join(om.parameters)
                rm.append(om)
            except AttributeError:
                continue
        return rm
