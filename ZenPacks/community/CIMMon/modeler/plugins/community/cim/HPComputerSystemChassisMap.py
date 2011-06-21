################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPComputerSystemChassisMap

HPComputerSystemChassisMap maps HP_ComputerSystemChassis class hw product.

$Id: HPComputerSystemChassisMap.py,v 1.0 2011/06/21 21:29:18 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

class HPComputerSystemChassisMap(SQLPlugin):
    """HPComputerSystemChassisMap maps HP_ComputerSystemChassis class to hw
    products.
    """

    maptype = "DeviceMap"
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
        if 'namespace' not in kwargs: args.append("namespace='root/HPQ'")
        cs = ','.join(args)
        return {
            "CIM_ComputerSystem":
                (
                    "SELECT Manufacturer,Model,ProductID,SerialNumber FROM HP_ComputerSystemChassis",
                    None,
                    cs,
                    {
                        'Manufacturer': '_manuf',
                        'Model': 'setHWProductKey',
                        'ProductID': 'setHWTag',
                        'SerialNumber': 'setHWSerialNumber',
                    },
                ),
            }


    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        try:
            cs = results.get('CIM_ComputerSystem', [{}])[0]
            if not cs: return
            om = self.objectMap(cs)
            if not om._manuf: om._manuf = 'Unknown'
            om.setHWProductKey = MultiArgs(om.setHWProductKey, om._manuf)
        except:
            log.warning('processing error')
            return
        return [om]

