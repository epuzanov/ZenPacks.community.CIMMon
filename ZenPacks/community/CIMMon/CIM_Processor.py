################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_Processor

CIM_Processor is an abstraction of a CPU.

$Id: CIM_Processor.py,v 1.0 2011/06/07 20:26:49 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Globals import InitializeClass
from Products.ZenModel.CPU import CPU

class CIM_Processor(CPU):
    """CIM_Processor object"""

    core = 1
    socket = 0
    clockspeed = 0
    extspeed = 0
    voltage = 0
    cacheSizeL1 = 0
    cacheSizeL2 = 0

    _properties = (
         {'id':'core', 'type':'int', 'mode':'w'},
         {'id':'socket', 'type':'int', 'mode':'w'},
         {'id':'clockspeed', 'type':'int', 'mode':'w'},     #MHz
         {'id':'extspeed', 'type':'int', 'mode':'w'},       #MHz
         {'id':'voltage', 'type':'int', 'mode':'w'},        #Millivolts
         {'id':'cacheSizeL1', 'type':'int', 'mode':'w'},    #KBytes
         {'id':'cacheSizeL2', 'type':'int', 'mode':'w'},    #KBytes
    )

InitializeClass(CIM_Processor)
