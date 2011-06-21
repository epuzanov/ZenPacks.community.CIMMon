################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMProcessorMap

CIMProcessorMap maps the CIM_Processor class to cpus objects

$Id: CIMProcessorMap.py,v 1.1 2011/06/21 21:26:34 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]

from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

import re
CACHELEVEL = re.compile(r'.*(\d).*(\d).*(\d).*')

def getManufacturerAndModel(key):
    """
    Attempts to parse accurate manufacturer and model information of a CPU from
    the single product string passed in.

    @param key: A product key. Hopefully containing manufacturer and model name.
    @type key: string
    @return: A MultiArgs object containing the model and manufacturer.
    @rtype: Products.DataDollector.plugins.DataMaps.MultiArgs
    """
    cpuDict = {
        'Intel': '(Intel|Pentium|Xeon)',
        'AMD': '(AMD|Opteron|Athlon|Sempron|Phenom|Turion)',
        }

    for manufacturer, regex in cpuDict.items():
        if re.search(regex, key):
            return MultiArgs(key, manufacturer)

    # Revert to default behavior if no specific match is found.
    return MultiArgs(key, "Unknown")


class CIMProcessorMap(SQLPlugin):

    maptype = "CPUMap"
    modname = "Products.ZenModel.CPU"
    compname = "hw"
    relname = "cpus"
    deviceProperties = SQLPlugin.deviceProperties + ('zWinUser',
                                                    'zWinPassword',
                                                    'zCIMConnectionString',
                                                    'zCIMHWNamespace',
                                                    )

    Families = {1:"Other",
                2:"Unknown",
                3:"Intel 8086",
                4:"Intel 80286",
                5:"Intel 80386",
                6:"Intel 80486",
                7:"Intel 8087",
                8:"Intel 80287",
                9:"Intel 80387",
                10:"Intel 80487",
                11:"Intel Pentium(R) brand",
                12:"Intel Pentium(R) Pro",
                13:"Intel Pentium(R) II",
                14:"Intel Pentium(R) processor with MMX(TM) technology",
                15:"Intel Celeron(TM)",
                16:"Intel Pentium(R) II Xeon(TM)",
                17:"Intel Pentium(R) III",
                18:"Cyrix M1 Family",
                19:"Cyrix M2 Family",
                24:"AMD K5 Family",
                25:"AMD K6 Family",
                26:"AMD K6-2",
                27:"AMD K6-3",
                28:"AMD Athlon(TM) Processor Family",
                29:"AMD Duron(TM) Processor",
                30:"AMD AMD29000 Family",
                31:"AMD K6-2+",
                32:"IBM Power PC Family",
                33:"IBM Power PC 601",
                34:"IBM Power PC 603",
                35:"IBM Power PC 603+",
                36:"IBM Power PC 604",
                37:"IBM Power PC 620",
                38:"IBM Power PC X704",
                39:"IBM Power PC 750",
                48:"DEC Alpha Family",
                49:"DEC Alpha 21064",
                50:"DEC Alpha 21066",
                51:"DEC Alpha 21164",
                52:"DEC Alpha 21164PC",
                53:"DEC Alpha 21164a",
                54:"DEC Alpha 21264",
                55:"DEC Alpha 21364",
                64:"MIPS Family",
                65:"MIPS R4000",
                66:"MIPS R4200",
                67:"MIPS R4400",
                68:"MIPS R4600",
                69:"MIPS R10000",
                80:"Sun SPARC Family",
                81:"Sun SuperSPARC",
                82:"Sun microSPARC II",
                83:"Sun microSPARC IIep",
                84:"Sun UltraSPARC",
                85:"Sun UltraSPARC II",
                86:"Sun UltraSPARC IIi",
                87:"Sun UltraSPARC III",
                88:"Sun UltraSPARC IIIi",
                96:"Motorola 68040",
                97:"Motorola 68xxx Family",
                98:"Motorola 68000",
                99:"Motorola 68010",
                100:"Motorola 68020",
                101:"Motorola 68030",
                112:"AT&T Hobbit Family",
                120:"Transmeta Crusoe(TM) TM5000 Family",
                121:"Transmeta Crusoe(TM) TM3000 Family",
                122:"Transmeta Efficeon(TM) TM8000 Family",
                128:"Weitek",
                130:"Intel Itanium(TM) Processor",
                131:"AMD Athlon(TM) 64 Processor Family",
                132:"AMD Opteron(TM) Processor Family",
                133:"AMD Sempron(TM) Processor Family",
                134:"AMD Turion(TM) 64 Mobile Technology",
                135:"AMD Opteron(TM) Dual-Core Processor Family",
                136:"AMD Athlon(TM) 64 X2 Dual-Core Processor Family",
                137:"AMD Turion(TM) 64 X2 Mobile Technology",
                144:"HP PA-RISC Family",
                145:"HP PA-RISC 8500",
                146:"HP PA-RISC 8000",
                147:"HP PA-RISC 7300LC",
                148:"HP PA-RISC 7200",
                149:"HP PA-RISC 7100LC",
                150:"HP PA-RISC 7100",
                160:"NEC V30 Family",
                176:"Intel Pentium(R) III Xeon(TM)",
                177:"Intel Pentium(R) III Processor with Intel(R) SpeedStep(TM) Technology",
                178:"Intel Pentium(R) 4",
                179:"Intel(R) Xeon(TM)",
                180:"IBM AS400 Family",
                181:"Intel(R) Xeon(TM) processor MP",
                182:"AMD Athlon(TM) XP Family",
                183:"AMD Athlon(TM) MP Family",
                184:"Intel(R) Itanium(R) 2",
                185:"Intel(R) Pentium(R) M processor",
                186:"Intel(R) Celeron(R) D processor",
                187:"Intel(R) Pentium(R) D processor",
                188:"Intel(R) Pentium(R) Processor Extreme Edition",
                189:"Intel(R) Core(TM) Solo Processor",
                190:"AMD K7",
                191:"Intel(R) Core(TM)2 Duo Processor",
                200:"IBM S/390 and zSeries Family",
                201:"IBM ESA/390 G4",
                202:"IBM ESA/390 G5",
                203:"IBM ESA/390 G6",
                204:"IBM z/Architectur base",
                210:"VIA C7(TM)-M Processor Family",
                211:"VIA C7(TM)-D Processor Family",
                212:"VIA C7(TM) Processor Family",
                213:"VIA Eden(TM) Processor Family",
                250:"Intell i860",
                251:"Intell i960",
                254:"Reserved (SMBIOS Extension)",
                255:"Reserved (Un-initialized Flash Content - Lo)",
                260:"Hitachi SH-3",
                261:"Hitachi SH-4",
                280:"ARM",
                281:"ARM StrongARM",
                300:"Cyrix 6x86",
                301:"Cyrix MediaGX",
                302:"Cyrix MII",
                320:"WinChip",
                350:"DSP",
                500:"Video Processor",
                }


    def queries(self, device):
        args = [getattr(device, 'zCIMConnectionString',
                                        "'pywbemdb',scheme='https',port=5989")]
        kwargs = eval('(lambda *argsl,**kwargs:kwargs)(%s)'%args[0])
        if 'host' not in kwargs:
            args.append("host='%s'"%device.manageIp)
        if 'user' not in kwargs:
            args.append("user='%s'"%getattr(device, 'zWinUser', ''))
        if 'password' not in kwargs:
            args.append("password='%s'"%getattr(device, 'zWinPassword', ''))
        if 'namespace' not in kwargs:
            args.append("namespace='%s'"%getattr(device, 'zCIMHWNamespace',
                                                                'root/cimv2'))
        cs = ','.join(args)
        return {
            "CIM_Processor":
                (
                    "SELECT CPUStatus,DeviceID,Family,MaxClockSpeed FROM CIM_Processor",
                    None,
                    cs,
                    {
                        'CPUStatus':'_status',
                        'DeviceID':'id',
                        'Family':'_name',
                        'MaxClockSpeed':'clockspeed',
                    }
                ),
            }


    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        socket = 1
        instances = results.get("CIM_Processor", [])
        for socket, instance in enumerate(results.get("CIM_Processor", [])):
            om = self.objectMap(instance)
            if om._status == 0: continue
            try:
                om.id = self.prepId(om.id)
                om.socket = socket
                om.setProductKey = getManufacturerAndModel(
                                        self.Families.get(om._name, om._name))
            except AttributeError:
                continue
            rm.append(om)
        return rm
