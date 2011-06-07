################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_TemperatureSensor

CIM_TemperatureSensor is an abstraction of a temperature sensor or probe.

$Id: CIM_TemperatureSensor.py,v 1.0 2011/06/07 20:28:38 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.TemperatureSensor import TemperatureSensor
from ZenPacks.community.CIMMon.CIM_ManagedSystemElement import *

class CIM_TemperatureSensor(TemperatureSensor, CIM_ManagedSystemElement):
    """CIM_TemperatureSensor object"""

    baseUnits = 2
    type = 'Unknown'
    unitModifier = 0
    upperThresholdCritical = 0
    upperThresholdFatal = 0
    upperThresholdNonCritical = 0

    _properties = TemperatureSensor._properties + (
                 {'id':'baseUnits', 'type':'int', 'mode':'w'},
                 {'id':'type', 'type':'string', 'mode':'w'},
                 {'id':'unitModifier', 'type':'int', 'mode':'w'},
                 {'id':'upperThresholdCritical', 'type':'int', 'mode':'w'},
                 {'id':'upperThresholdFatal', 'type':'int', 'mode':'w'},
                 {'id':'upperThresholdNonCritical', 'type':'int', 'mode':'w'},
                ) + CIM_ManagedSystemElement._properties

    def temperatureCelsius(self, default=None):
        """
        Return the current temperature in degrees celsius
        """
        temp = self.cacheRRDValue('CurrentReading', default)
        if temp is None: return None
        temp = 10 ** int(self.unitModifier or 0) * temp
        if self.baseUnits == 2: return long(temp)
        if self.baseUnits == 3: return long((temp - 32) / 9 * 5)
        if self.baseUnits == 4: return long(temp - 273.15)
        return long(temp)
    temperature = temperatureCelsius

    getRRDTemplates = CIM_ManagedSystemElement.getRRDTemplates

InitializeClass(CIM_TemperatureSensor)
