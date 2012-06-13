################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_NetworkAdapter

CIM_NetworkAdapter is an abstraction of a Network Adapter.

$Id: CIM_NetworkAdapter.py,v 1.0 2012/02/20 22:07:37 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.IpInterface import IpInterface
from ZenPacks.community.CIMMon.CIM_ManagedSystemElement import *

class CIM_NetworkAdapter(IpInterface, CIM_ManagedSystemElement):
    """NetworkAdapter object"""

    collectors = ('zenperfsql', 'zencommand', 'zenwinperf')

    _properties=IpInterface._properties + CIM_ManagedSystemElement._properties

    getRRDTemplates = CIM_ManagedSystemElement.getRRDTemplates
    getStatus = CIM_ManagedSystemElement.getStatus
    getStatusImgSrc = CIM_ManagedSystemElement.getStatusImgSrc
    convertStatus = CIM_ManagedSystemElement.convertStatus

InitializeClass(CIM_NetworkAdapter)
