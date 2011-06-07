################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_Fan

CIM_Fan is an abstraction of a Fan.

$Id: CIM_Fan.py,v 1.0 2011/06/07 20:24:48 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.Fan import Fan
from ZenPacks.community.CIMMon.CIM_ManagedSystemElement import *

class CIM_Fan(Fan, CIM_ManagedSystemElement):
    """CIM_Fan object"""

    _properties = Fan._properties + CIM_ManagedSystemElement._properties

    def rpmString(self, default=None):
        """
        Return a string representation of the RPM
        """
        return self.getStatus() == 0 and 'Normal' or 'unknown'

    getRRDTemplates = CIM_ManagedSystemElement.getRRDTemplates

InitializeClass(CIM_Fan)
