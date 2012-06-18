################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_TemperatureSensor

CIM_TemperatureSensor is an abstraction of a temperature sensor or probe.

$Id: CIM_TemperatureSensor.py,v 1.2 2012/06/18 23:21:17 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Products.ZenModel.TemperatureSensor import TemperatureSensor
from Products.ZenModel.HWComponent import HWComponent
from ZenPacks.community.CIMMon.CIM_NumericSensor import *

class CIM_TemperatureSensor(TemperatureSensor, CIM_NumericSensor):
    """TemperatureSensor object"""

    collectors = ('zenperfsql', 'zencommand', 'zenwinperf')
    _properties = HWComponent._properties + CIM_NumericSensor._properties

    _relations=TemperatureSensor._relations + CIM_NumericSensor._relations

    getRRDTemplates = CIM_NumericSensor.getRRDTemplates
    getStatus = CIM_NumericSensor.getStatus
    getStatusImgSrc = CIM_NumericSensor.getStatusImgSrc
    convertStatus = CIM_NumericSensor.convertStatus

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

InitializeClass(CIM_TemperatureSensor)
