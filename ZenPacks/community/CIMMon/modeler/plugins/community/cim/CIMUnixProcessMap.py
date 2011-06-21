################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMUnixProcessMap

CIMUnixProcessMap finds various software packages installed on a device.

$Id: CIMUnixProcessMap.py,v 1.2 2011/06/21 21:28:58 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]

from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin

class CIMUnixProcessMap(SQLPlugin):

    maptype = "OSProcessMap"
    compname = "os"
    relname = "processes"
    modname = "Products.ZenModel.OSProcess"
    classname = 'createFromObjectMap'
    deviceProperties = SQLPlugin.deviceProperties + ('zWinUser',
                                                    'zWinPassword',
                                                    'zCIMConnectionString',
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
        if 'namespace' not in kwargs:
            args.append("namespace='root/cimv2'")
        cs = ','.join(args)
        return {
            "CIM_UnixProcess":
                (
                    "SELECT Name,Parameters FROM CIM_UnixProcess",
                    None,
                    cs,
                    {
                        'Parameters':'parameters',
                        'Name':'procName',
                    }
                ),
            }


    def process(self, device, results, log):
        """collect SQL information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        for instance in results.get("CIM_UnixProcess", []):
            try:
                om = self.objectMap(instance)
                if not getattr(om, 'procName', False): 
                    log.warning("Skipping process with no name")
                    continue
                om.procName = str(om.procName)
                om.parameters = ' '.join(getattr(om, 'parameters', []))
                rm.append(om)
            except AttributeError:
                continue
        return rm
