from common.msploitdb import MetasploitXML
from common.MaltegoTransform import *
import sys

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

def dotransform(args):
    excludes = ["Nessus Scan Information"]
    # entitytags = ["hostid", "info", "name","vulnattemptcount"]
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    fn = mt.getVar("fromfile")
    ip = mt.getVar("address")
    host = MetasploitXML(fn).gethost(ip)

    vulncount = int(mt.getVar("vulncount"))
    if vulncount > 0:
        for vuln in host.vulns:
            vulnent = mt.addEntity("maltego.Vulnerability", vuln.name)
            vulnent.setValue("{}/{}".format(vuln.name,host.address))
            vulnent.addAdditionalFields("refs", "References", False, ",".join([x.ref for x in vuln.refs]))
            vulnent.addAdditionalFields("ipaddress", "IP Address", False, host.address)
            vulnent.addAdditionalFields("hostid", "Host ID", False, host.id)
            vulnent.addAdditionalFields("os", "OS Name", False, host.osname)

            for tag,val in vuln:
                if isinstance(val,str):
                    vulnent.addAdditionalFields(tag, tag.capitalize() , False, val)

    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['enumvulns.py',
#  '10.10.10.63',
#  'ipv4-address=10.10.10.63#ipaddress.internal=false#notecount=25#address=10.10.10.63#purpose=client#osfamily=Windows#servicecount=16#name=JEEVES#state=alive#vulncount=39#fromfile=/root/data/scan/hthebox/msplotdb20180522.xml#osname=Windows 10#osflavor=Pro']
# dotransform(args)
