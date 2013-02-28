################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012-2013 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIM_Fan

CIM_Fan is an abstraction of a Fan.

$Id: CIM_Fan.py,v 1.3 2013/02/28 21:43:02 egor Exp $"""

__version__ = "$Revision: 1.3 $"[11:-2]

from Products.ZenModel.Fan import Fan
from Products.ZenModel.HWComponent import HWComponent
from ZenPacks.community.CIMMon.CIM_NumericSensor import *

class CIM_Fan(Fan, CIM_NumericSensor):
    """Fan object"""

    collectors = ('zenperfsql', 'zencommand', 'zenwinperf')
    _properties = HWComponent._properties + CIM_NumericSensor._properties

    _relations=Fan._relations + CIM_NumericSensor._relations

    getRRDTemplates = CIM_NumericSensor.getRRDTemplates
    getStatus = CIM_NumericSensor.getStatus
    getStatusImgSrc = CIM_NumericSensor.getStatusImgSrc
    convertStatus = CIM_NumericSensor.convertStatus

    def rpmString(self):
        """
        Return a string representation of the RPM
        """
        if not self.cimStatClassName:
            return self.getStatus() == 2 and 'Normal' or 'Unknown'
        rpm = self.rpm()
        return rpm is None and "unknown" or "%lrpm" % (rpm,)

    def rpm(self, default=None):
        """
        Return a string representation of the RPM
        """
        if not self.cimStatClassName: return None
        rpm = self.cacheRRDValue('CurrentReading', default)
        if rpm is None: return None
        return 10 ** int(self.unitModifier or 0) * rpm

    def getRRDStatTemplates(self):
        """
        Return the RRD StatisticalData Templates list
        """
        if not self.cimStatClassName: return []
        for tname in (self.cimStatClassName, 'CIM_Tachometer'):
            templ = self.getRRDTemplateByName(tname)
            if not templ: continue
            return [templ]
        return []

    def manage_deleteComponent(self, REQUEST=None):
        """
        Delete CIM Component
        """
        self.getPrimaryParent()._delObject(self.id)
        if REQUEST is not None:
            REQUEST['RESPONSE'].redirect(self.device().hw.absolute_url())

InitializeClass(CIM_Fan)
