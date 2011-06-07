################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_Tachometer

CIM_Tachometer is an abstraction of a Fan.

$Id: CIM_Tachometer.py,v 1.0 2011/06/07 20:27:29 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.Fan import Fan
from ZenPacks.community.CIMMon.CIM_ManagedSystemElement import *

class CIM_Tachometer(Fan, CIM_ManagedSystemElement):
    """CIM_Tachometer object"""

    description = ''
    unitModifier = 0
    lowerThresholdCritical = 0
    lowerThresholdFatal = 0
    lowerThresholdNonCritical = 0

    _properties = Fan._properties + (
                 {'id':'description', 'type':'string', 'mode':'w'},
                 {'id':'unitModifier', 'type':'int', 'mode':'w'},
                 {'id':'lowerThresholdCritical', 'type':'int', 'mode':'w'},
                 {'id':'lowerThresholdFatal', 'type':'int', 'mode':'w'},
                 {'id':'lowerThresholdNonCritical', 'type':'int', 'mode':'w'},
                ) + CIM_ManagedSystemElement._properties


    def rpm(self, default=None):
        """
        Return the current RPM
        """
        rpm = self.cacheRRDValue('CurrentReading', default)
        if rpm is None: return None
        return 10 ** int(self.unitModifier or 0) * rpm

    getRRDTemplates = CIM_ManagedSystemElement.getRRDTemplates

InitializeClass(CIM_Tachometer)
