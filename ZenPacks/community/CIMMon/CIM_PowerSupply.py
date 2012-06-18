################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_PowerSupply

CIM_PowerSupply is an abstraction of a Power Supply.

$Id: CIM_PowerSupply.py,v 1.2 2012/06/18 23:19:53 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Products.ZenModel.PowerSupply import PowerSupply
from Products.ZenModel.HWComponent import HWComponent
from ZenPacks.community.CIMMon.CIM_NumericSensor import *

class CIM_PowerSupply(PowerSupply, CIM_NumericSensor):
    """PowerSupply object"""

    collectors = ('zenperfsql', 'zencommand', 'zenwinperf')

    _properties = HWComponent._properties + (
                 {'id':'watts', 'type':'string', 'mode':'w'},
    ) + CIM_NumericSensor._properties

    _relations=PowerSupply._relations + CIM_NumericSensor._relations

    getRRDTemplates = CIM_NumericSensor.getRRDTemplates
    getStatus = CIM_NumericSensor.getStatus
    getStatusImgSrc = CIM_NumericSensor.getStatusImgSrc
    convertStatus = CIM_NumericSensor.convertStatus

InitializeClass(CIM_PowerSupply)
