################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_Processor

CIM_Processor is an abstraction of a CPU.

$Id: CIM_Processor.py,v 1.2 2012/10/14 16:32:28 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Globals import InitializeClass
from Products.ZenModel.CPU import CPU

class CIM_Processor(CPU):
    """Processor object"""

    core = 1
    cacheSizeL3 = 0

    _properties = CPU._properties + (
         {'id':'core', 'type':'int', 'mode':'w'},
         {'id':'cacheSizeL3', 'type':'int', 'mode':'w'},    #KBytes
    )

InitializeClass(CIM_Processor)
