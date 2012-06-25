################################################################################
#
# This program is part of the Win32Mon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""Win32ProductMap

Win32ProductMap maps Win32_Product class to Product class.

$Id: Win32ProductMap.py,v 1.0 2012/06/13 20:43:13 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMProductMap \
    import CIMProductMap
import re
DATEPAT = re.compile(r"(\d4)(\d2)(\d2)")

class Win32ProductMap(CIMProductMap):
    """Map Win32_Product class to Product class"""

    def queries(self, device):
        connectionString = getattr(device, 'zCIMConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_Product":
                (
                    "SELECT * FROM Win32_Product",
                    None,
                    cs,
                    {
                        "setProductKey":"Name",
                        "_manuf":"Vendor",
                        "_setInstallDate":"InstallDate",
                        "setInstallDate":"InstallDate2",
                    },
                ),
            }

    def _getInstallDate(self, inst):
        instDate = inst.get("setInstallDate")
        if not instDate:
            r = DATEPAT.match(str(inst.get("_setInstallDate")))
            if r:
                instDate = "%s/%s/%s 00:00:00" % r.groups()
        return instDate or "1968/01/08 00:00:00"
