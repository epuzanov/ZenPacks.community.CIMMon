################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_NetworkPort

CIM_NetworkPort is an abstraction of a Network Port.

$Id: CIM_NetworkPort.py,v 1.0 2012/02/20 22:07:37 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.IpInterface import IpInterface
from Products.ZenRelations.RelSchema import ToOne, ToMany
from ZenPacks.community.CIMMon.CIM_ManagedSystemElement import *

class CIM_NetworkPort(IpInterface, CIM_ManagedSystemElement):
    """NetworkPort object"""

    collectors = ('zenperfsql', 'zencommand', 'zenwinperf')

    _properties=IpInterface._properties + CIM_ManagedSystemElement._properties

    _relations = IpInterface._relations + (
        ("controller", ToOne(ToMany,
                            "ZenPacks.community.CIMMon.CIM_ComputerSystem",
                            "interfaces")),
        )

    security = ClassSecurityInfo()

    getRRDTemplates = CIM_ManagedSystemElement.getRRDTemplates
    getStatus = CIM_ManagedSystemElement.getStatus
    getStatusImgSrc = CIM_ManagedSystemElement.getStatusImgSrc
    convertStatus = CIM_ManagedSystemElement.convertStatus

    security.declareProtected(ZEN_CHANGE_DEVICE, 'setController')
    def setController(self, cid):
        """
        Set the controller relationship to the controller specified by the
        given id.
        """
        if not cid: return
        for card in getattr(self.device().hw, 'cards', (lambda:[]))():
            if getattr(card, 'getPath', lambda:'')() != cid: continue
            self.controller.addRelation(card)
            break

    security.declareProtected(ZEN_VIEW, 'getController')
    def getController(self):
        """
        Return chassis object
        """
        return self.controller()


InitializeClass(CIM_NetworkPort)
