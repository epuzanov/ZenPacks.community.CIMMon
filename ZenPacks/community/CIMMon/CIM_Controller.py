################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012-2013 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_Controller

CIM_Controller is an abstraction of a Expansion Card.

$Id: CIM_Controller.py,v 1.2 2013/02/28 21:41:50 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Products.ZenModel.ExpansionCard import ExpansionCard
from ZenPacks.community.CIMMon.CIM_ManagedSystemElement import *

class CIM_Controller(ExpansionCard, CIM_ManagedSystemElement):
    """Expansion Card object"""

    collectors = ('zenperfsql', 'zencommand', 'zenwinperf')

    _properties=ExpansionCard._properties + CIM_ManagedSystemElement._properties

    _relations=ExpansionCard._relations + CIM_ManagedSystemElement._relations

    getRRDTemplates = CIM_ManagedSystemElement.getRRDTemplates
    getStatus = CIM_ManagedSystemElement.getStatus
    getStatusImgSrc = CIM_ManagedSystemElement.getStatusImgSrc
    convertStatus = CIM_ManagedSystemElement.convertStatus

    def manage_deleteComponent(self, REQUEST=None):
        """
        Delete CIM Component
        """
        self.getPrimaryParent()._delObject(self.id)
        if REQUEST is not None:
            REQUEST['RESPONSE'].redirect(self.device().hw.absolute_url())

InitializeClass(CIM_Controller)
