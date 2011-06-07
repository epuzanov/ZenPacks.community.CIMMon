################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_ManagedSystemElement

CIM_ManagedSystemElement is an abstraction for CIM_ManagedSystemElement class.

$Id: CIMCIM_ManagedSystemElement.py,v 1.0 2011/06/07 20:25:59 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Globals import InitializeClass
from ZenPacks.community.deviceAdvDetail.HWStatus import *
from Products.ZenModel.ZenossSecurity import *

class CIM_ManagedSystemElement(object, HWStatus):

    cimNamespace = 'root/cimv2'
    cimClassName = ''
    cimKeybindings = ''
    cimStatClassName = ''
    cimStatKeybindings = ''
    status = 2

    statusmap ={0: (DOT_GREY, SEV_WARNING, 'Unknown'),
                1: (DOT_GREY, SEV_WARNING, 'Other'),
                2: (DOT_GREEN, SEV_CLEAN, 'OK'),
                3: (DOT_ORANGE, SEV_ERROR, 'Degraded'),
                4: (DOT_YELLOW, SEV_WARNING, 'Stressed'),
                5: (DOT_YELLOW, SEV_WARNING, 'Predictive Failure'),
                6: (DOT_ORANGE, SEV_ERROR, 'Error'),
                7: (DOT_RED, SEV_CRITICAL, 'Non-Recoverable Error'),
                8: (DOT_BLUE, SEV_INFO, 'Starting'),
                9: (DOT_YELLOW, SEV_WARNING, 'Stopping'),
                10: (DOT_ORANGE, SEV_ERROR, 'Stopped'),
                11: (DOT_BLUE, SEV_INFO, 'In Service'),
                12: (DOT_GREY, SEV_WARNING, 'No Contact'),
                13: (DOT_ORANGE, SEV_ERROR, 'Lost Communication'),
                14: (DOT_ORANGE, SEV_ERROR, 'Aborted'),
                15: (DOT_GREY, SEV_WARNING, 'Dormant'),
                16: (DOT_ORANGE, SEV_ERROR, 'Stopping Entity in Error'),
                17: (DOT_GREEN, SEV_CLEAN, 'Completed'),
                18: (DOT_YELLOW, SEV_WARNING, 'Power Mode'),
                }


    _properties = (
                 {'id':'cimNamespace', 'type':'string', 'mode':'w'},
                 {'id':'cimClassName', 'type':'string', 'mode':'w'},
                 {'id':'cimKeybindings', 'type':'string', 'mode':'w'},
                 {'id':'cimStatClassName', 'type':'string', 'mode':'w'},
                 {'id':'cimStatKeybindings', 'type':'string', 'mode':'w'},
                 {'id':'status', 'type':'int', 'mode':'w'},
                )


    def cimInstanceName(self):
        """
        Return the CIM Instance Name
        """
        return '%s WHERE %s' % (self.cimClassName,
                                self.cimKeybindings.replace(',',' AND '))


    def cimStatInstanceName(self):
        """
        Return the CIM_StatisticalData Instance Name
        """
        return '%s WHERE %s' % (self.cimStatClassName,
                                self.cimStatKeybindings.replace(',',' AND '))


    def getRRDTemplates(self):
        """
        Return the RRD Templates list
        """
        templates = [self.__class__.__name__]
        if self.cimClassName and self.cimClassName != self.__class__.__name__:
            templates.append(self.cimClassName)
        for i in range(len(templates)):
            templ = self.getRRDTemplateByName(templates.pop(0))
            if templ: templates.append(templ)
        return templates
