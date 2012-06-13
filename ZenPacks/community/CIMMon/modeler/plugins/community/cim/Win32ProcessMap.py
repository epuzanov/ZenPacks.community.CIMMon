################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""Win32ProcessMap

Win32ProcessMap finds various processes running on a device.

$Id: Win32ProcessMap.py,v 1.0 2012/06/13 20:53:45 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMProcessMap \
    import CIMProcessMap

class Win32ProcessMap(CIMProcessMap):
    """Map Win32_Process class to OSProcess class"""

    def queries(self, device):
        connectionString = getattr(device, 'zCIMConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_Process":
                (
                    "SELECT Name,CommandLine FROM Win32_Process",
                    None,
                    cs,
                    {
                        "parameters":"CommandLine",
                        "procName":"Name",
                    }
                ),
            }
