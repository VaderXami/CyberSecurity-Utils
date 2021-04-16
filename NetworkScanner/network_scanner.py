import scapy.all as scapy
import optparse


def getArgs():
    parser = optparse.OptionParser()
    parser.add_option("-p", "--internet-protocol", dest="_ip")
    (options, arguments) = parser.parse_args()
    if not options._ip:
        parser.error("[-] Please specify an IP")
    return options

def scan(ip):
    _arpRequest = scapy.ARP(pdst=ip)
    _broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    _arpRequestBroadcast = _broadcast/_arpRequest
    _answeredList = scapy.srp(_arpRequestBroadcast, timeout=1, verbose=False)[0]

    _clientsList = []
    for _answares in _answeredList:
        _clientDict = {"ip": _answares[1].psrc, "mac": _answares[1].hwsrc}
        _clientsList.append(_clientDict)
    return _clientsList


def printFunction(_resultsList):
    print("IP\t\t\tMAC Address\n------------------------------------------")
    for _client in _resultsList:
        print(_client["ip"] + "\t\t" + _client["mac"])

def engine():
    options = getArgs()
    _clientList = scan(options._ip)
    printFunction(_clientList)

engine()
