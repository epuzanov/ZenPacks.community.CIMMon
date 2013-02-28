################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012-2013 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_ManagedSystemElement

CIM_ManagedSystemElement is an abstraction for CIM_ManagedSystemElement class.

$Id: CIM_ManagedSystemElement.py,v 1.8 2013/02/28 21:30:59 egor Exp $"""

__version__ = "$Revision: 1.7 $"[11:-2]

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.ZenModel.ZenossSecurity import *
from Products.ZenRelations.RelSchema import ToMany

class CIM_ManagedSystemElement:
    """ManagedSystemElement object"""

    collectors = ('zenperfsql', 'zencommand', 'zenwinperf')
    status = 2
    title = ''
    cimClassName = ''
    cimKeybindings = ''
    cimStatClassName = ''
    cimStatKeybindings = ''
    cimStatusName = ''

    _properties=(
                {'id':'status', 'type':'int', 'mode':'w'},
                {'id':'title', 'type':'string', 'mode':'w'},
                {'id':'cimClassName', 'type':'string', 'mode':'w'},
                {'id':'cimKeybindings', 'type':'string', 'mode':'w'},
                {'id':'cimStatClassName', 'type':'string', 'mode':'w'},
                {'id':'cimStatKeybindings', 'type':'string', 'mode':'w'},
                {'id':'cimStatusName', 'type':'string', 'mode':'w'},
                )

    _relations = (
        ("redundancysets", ToMany(ToMany,
            "ZenPacks.community.CIMMon.CIM_RedundancySet",
            "members")),
        )

    statusmap ={0: ('grey', 3, 'Unknown'),
                1: ('yellow', 3, 'Other'),
                2: ('green', 0, 'OK'),
                3: ('yellow', 3, 'Degraded'),
                4: ('yellow', 3, 'Stressed'),
                5: ('yellow', 3, 'Predictive Failure'),
                6: ('orange', 4, 'Error'),
                7: ('red', 5, 'Non-Recoverable Error'),
                8: ('blue', 2, 'Starting'),
                9: ('yellow', 3, 'Stopping'),
                10: ('orange', 4, 'Stopped'),
                11: ('blue', 2, 'In Service'),
                12: ('grey', 3, 'No Contact'),
                13: ('orange', 4, 'Lost Communication'),
                14: ('orange', 4, 'Aborted'),
                15: ('grey', 3, 'Dormant'),
                16: ('orange', 4, 'Stopping Entity in Error'),
                17: ('green', 0, 'Completed'),
                18: ('yellow', 3, 'Power Mode'),
                }

    security = ClassSecurityInfo()

    security.declareProtected(ZEN_CHANGE_DEVICE, 'setPath')
    def setPath(self, path):
        """
        Set cimClassName and cimKeybindings string
        """
        self.cimClassName, self.cimKeybindings = path.split('.', 1)

    security.declareProtected(ZEN_VIEW, 'getPath')
    def getPath(self):
        """
        Return instance path string of CIM class
        """
        if not self.cimKeybindings: return self.cimClassName
        return '%s.%s'%(self.cimClassName, self.cimKeybindings)

    security.declareProtected(ZEN_CHANGE_DEVICE, 'setStatPath')
    def setStatPath(self, path):
        """
        Set cimStatClassName and cimStatKeybindings string
        """
        if not path: path = '.'
        self.cimStatClassName, self.cimStatKeybindings = path.split('.', 1)

    security.declareProtected(ZEN_VIEW, 'getStatPath')
    def getStatPath(self):
        """
        Return instance path string of statistical data CIM class
        """
        if not self.cimStatKeybindings: return self.cimStatClassName
        return '%s.%s'%(self.cimStatClassName, self.cimStatKeybindings)

    def whereString(self):
        """
        Return the WHERE string for use in WQL query.
        """
        return self.cimKeybindings.replace(',', ' AND ')

    def statWhereString(self):
        """
        Return the WHERE string for use in WQL query.
        """
        return self.cimStatKeybindings.replace(',', ' AND ')

    security.declareProtected(ZEN_CHANGE_DEVICE, 'setCollections')
    def setCollections(self, colids):
        """
        Set the collection relationship to the collection set specified by the
        given id.
        """
        for colid in colids or ():
            if not colid: continue
            for col in getattr(self.device().os,'redundancysets',(lambda:[]))():
                if col.getPath() != colid: continue
                self.redundancysets.addRelation(col)
                break

    security.declareProtected(ZEN_VIEW, 'getCollections')
    def getCollections(self):
        """
        Return Collection object
        """
        return getattr(self, 'redundancysets', lambda:None)()

    security.declareProtected(ZEN_CHANGE_DEVICE, 'convertStatus')
    def convertStatus(self, status):
        """
        Convert status to the status string
        """
        return self.statusmap.get(status, ('grey', 3, 'Other'))[2]

    security.declareProtected(ZEN_CHANGE_DEVICE, 'getStatus')
    def getStatus(self, statClass=None):
        """
        Return the status number for this component of class statClass.
        """
        if not self.monitored() \
            or not self.device() \
            or not self.device().monitorDevice(): return 0
        return self.status

    def getStatusImgSrc(self, status=None):
        """
        Return the img source for a status number
        """
        if status is None: status = self.getStatus()
        src = self.statusmap.get(status, ('grey', 3, 'Other'))[0]
        return '/zport/dmd/img/%s_dot.png' % src

    def statusDot(self, status=None):
        """
        Return the img source for a status number
        Return the Dot Color based on maximal severity
        """
        if status is None: status = self.getStatus()
        return self.statusmap.get(status, ('grey', 3, 'Other'))[0]

    def statusString(self, status=None):
        """
        Return the status string
        """
        if status is None: status = self.getStatus()
        return self.getStatusString(status)

    def getRRDStatTemplates(self):
        """
        Return the RRD StatisticalData Templates list
        """
        templates = []
        if self.cimStatClassName:
            templ = self.getRRDTemplateByName(self.cimStatClassName)
            if templ:
                templates.append(templ)
        return templates

    def getRRDTemplates(self):
        """
        Return the RRD Templates list
        """
        templates = self.getRRDStatTemplates()
        if self.cimStatClassName == self.cimClassName: return templates
        tnames = [self.cimClassName, self.__class__.__name__, self.meta_type]
        if self.cimStatusName:
            tnames.append('CIM_ManagedSystemElement')
        for tname in tnames:
            templ = self.getRRDTemplateByName(tname)
            if not templ: continue
            templates.append(templ)
            break
        return templates

InitializeClass(CIM_ManagedSystemElement)