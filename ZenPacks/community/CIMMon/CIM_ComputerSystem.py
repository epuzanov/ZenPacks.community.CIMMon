################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_ComputerSystem

CIM_ComputerSystem is an abstraction of a Expansion Card.

$Id: CIM_ComputerSystem.py,v 1.3 2012/06/21 19:34:10 egor Exp $"""

__version__ = "$Revision: 1.3 $"[11:-2]

from Products.ZenModel.ExpansionCard import ExpansionCard
from Products.ZenRelations.RelSchema import ToOne, ToMany
from ZenPacks.community.CIMMon.CIM_ManagedSystemElement import *

class CIM_ComputerSystem(ExpansionCard, CIM_ManagedSystemElement):
    """Expansion Card object"""

    collectors = ('zenperfsql', 'zencommand', 'zenwinperf')
    portal_type = meta_type = 'CIM_ComputerSystem'

    FWRev = ''
    monitor = True

    _properties = ExpansionCard._properties + (
                {'id':'FWRev', 'type':'string', 'mode':'w'},
                ) + CIM_ManagedSystemElement._properties

    _relations = ExpansionCard._relations + (
        ("interfaces", ToMany(ToOne,
                            "ZenPacks.community.CIMMon.CIM_NetworkPort",
                            "controller")),
        ) + CIM_ManagedSystemElement._relations

    factory_type_information = (
        {
            'id'             : 'CIMComputerSystem',
            'meta_type'      : 'CIMComputerSystem',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'CIMMon',
            'factory'        : 'manage_addExpansionCard',
            'immediate_view' : 'viewCIMComputerSystem',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewCIMComputerSystem'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'events'
                , 'name'          : 'Events'
                , 'action'        : 'viewEvents'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'ports'
                , 'name'          : 'Ports'
                , 'action'        : 'viewCIMComputerSystemPorts'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_DEVICE, )
                },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
          },
        )

    getRRDTemplates = CIM_ManagedSystemElement.getRRDTemplates
    getStatus = CIM_ManagedSystemElement.getStatus
    getStatusImgSrc = CIM_ManagedSystemElement.getStatusImgSrc
    convertStatus = CIM_ManagedSystemElement.convertStatus

    def sysUpTime(self):
        """
        Return the controllers UpTime
        """
        cpuUpTime = round(self.cacheRRDValue('sysUpTime', -1))
        if cpuUpTime == -1: return -1
        return cpuUpTime / 10

    def uptimeString(self):
        """
        Return the controllers uptime string

        @rtype: string
        @permission: ZEN_VIEW
        """
        ut = self.sysUpTime()
        if ut < 0:
            return "Unknown"
        elif ut == 0:
            return "0d:0h:0m:0s"
        ut = float(ut)/100.
        days = ut/86400
        hour = (ut%86400)/3600
        mins = (ut%3600)/60
        secs = ut%60
        return "%02dd:%02dh:%02dm:%02ds" % (
            days, hour, mins, secs)

    def getRRDNames(self):
        """
        Return the datapoint name of this StorageProcessorCard
        """
        return ['sysUpTime']

InitializeClass(CIM_ComputerSystem)
