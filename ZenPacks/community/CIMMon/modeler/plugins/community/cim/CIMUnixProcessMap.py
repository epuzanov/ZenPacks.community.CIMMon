################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMUnixProcessMap

CIMUnixProcessMap finds various processes running on a device.

$Id: CIMUnixProcessMap.py,v 1.3 2012/06/13 20:49:38 egor Exp $"""

__version__ = '$Revision: 1.3 $'[11:-2]

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMProcessMap \
    import CIMProcessMap

class CIMUnixProcessMap(CIMProcessMap):
    """Map CIM_UnixProcess class to OSProcess class"""

    def queries(self, device):
        connectionString = getattr(device, "zCIMConnectionString", "")
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_Process":
                (
                    "SELECT Name,Parameters FROM CIM_UnixProcess",
                    None,
                    cs,
                    {
                        "parameters":"Parameters",
                        "procName":"Name",
                    }
                ),
            }
