################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_NumericSensor

CIM_NumericSensor is an abstraction of a Power Supply.

$Id: CIM_NumericSensor.py,v 1.0 2012/01/23 23:21:05 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from ZenPacks.community.CIMMon.CIM_ManagedSystemElement import *

class CIM_NumericSensor(CIM_ManagedSystemElement):
    """NumericSensor object"""

    collectors = ('zenperfsql', 'zencommand', 'zenwinperf')
    type = ""
    baseUnits = 2
    unitModifier = 0
    lowerThresholdCritical = 0
    lowerThresholdFatal = 0
    lowerThresholdNonCritical = 0
    upperThresholdCritical = 0
    upperThresholdFatal = 0
    upperThresholdNonCritical = 0

    _properties = CIM_ManagedSystemElement._properties + (
                 {'id':'type', 'type':'string', 'mode':'w'},
                 {'id':'baseUnits', 'type':'int', 'mode':'w'},
                 {'id':'unitModifier', 'type':'int', 'mode':'w'},
                 {'id':'lowerThresholdCritical', 'type':'int', 'mode':'w'},
                 {'id':'lowerThresholdFatal', 'type':'int', 'mode':'w'},
                 {'id':'lowerThresholdNonCritical', 'type':'int', 'mode':'w'},
                 {'id':'upperThresholdCritical', 'type':'int', 'mode':'w'},
                 {'id':'upperThresholdFatal', 'type':'int', 'mode':'w'},
                 {'id':'upperThresholdNonCritical', 'type':'int', 'mode':'w'},
                )

    getRRDTemplates = CIM_ManagedSystemElement.getRRDTemplates
    getStatus = CIM_ManagedSystemElement.getStatus
    getStatusImgSrc = CIM_ManagedSystemElement.getStatusImgSrc
    convertStatus = CIM_ManagedSystemElement.convertStatus

InitializeClass(CIM_NumericSensor)
