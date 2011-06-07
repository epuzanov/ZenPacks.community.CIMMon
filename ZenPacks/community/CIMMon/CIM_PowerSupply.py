################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_PowerSupply

CIM_PowerSupply is an abstraction of a Power Supply.

$Id: CIM_PowerSupply.py,v 1.0 2011/06/07 20:26:35 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.PowerSupply import PowerSupply
from ZenPacks.community.CIMMon.CIM_ManagedSystemElement import *

class CIM_PowerSupply(PowerSupply, CIM_ManagedSystemElement):
    """PowerSupply object"""

    _properties = PowerSupply._properties + CIM_ManagedSystemElement._properties

    getRRDTemplates = CIM_ManagedSystemElement.getRRDTemplates

InitializeClass(CIM_PowerSupply)
