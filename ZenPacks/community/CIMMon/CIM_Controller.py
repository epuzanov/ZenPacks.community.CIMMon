################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_Controller

CIM_Controller is an abstraction of a Expansion Card.

$Id: CIM_Controller.py,v 1.0 2012/02/23 19:35:23 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.ExpansionCard import ExpansionCard
from ZenPacks.community.CIMMon.CIM_ManagedSystemElement import *

class CIM_Controller(ExpansionCard, CIM_ManagedSystemElement):
    """Expansion Card object"""

    collectors = ('zenperfsql', 'zencommand', 'zenwinperf')

    _properties=ExpansionCard._properties + CIM_ManagedSystemElement._properties


    getRRDTemplates = CIM_ManagedSystemElement.getRRDTemplates
    getStatus = CIM_ManagedSystemElement.getStatus
    getStatusImgSrc = CIM_ManagedSystemElement.getStatusImgSrc
    convertStatus = CIM_ManagedSystemElement.convertStatus

InitializeClass(CIM_Controller)
