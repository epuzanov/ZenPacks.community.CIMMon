################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMPowerSupplyMap

CIMPowerSupplyMap maps CIM_PowerSupply CIM class to CIMPowerSupply class.

$Id: CIMPowerSupplyMap.py,v 1.0 2011/06/07 20:35:11 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin

class CIMPowerSupplyMap(SQLPlugin):
    """Map CIM_PowerSupply class to PowerSupply class"""

    maptype = "CIMPowerSupplyMap"
    modname = "ZenPacks.community.CIMMon.CIM_PowerSupply"
    relname = "powersupplies"
    compname = "hw"
    deviceProperties = SQLPlugin.deviceProperties + ('zWinUser',
                                                    'zWinPassword',
                                                    'zCIMConnectionString',
                                                    'zCIMHWNamespace',
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
            args.append("namespace='%s'"%getattr(device, 'zCIMHWNamespace',
                                                'root/cimv2'))
        cs = ','.join(args)
        return {
            "CIM_PowerSupply":
                (
                    "SELECT * FROM CIM_PowerSupply",
                    None,
                    cs,
                    {
                        '__PATH':'_path',
                        '__NAMESPACE':'cimNamespace',
                        'DeviceID':'id',
                        'TotalOutputPower':'watts',
                    },
                ),
            }

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        for instance in results.get("CIM_PowerSupply", []):
            om = self.objectMap(instance)
            om.id = self.prepId(om.id)
            om.cimClassName, om.cimKeybindings = om._path.split('.', 1)
            if om.watts: om.watts = int(om.watts) / 1000
            rm.append(om)
        return rm


