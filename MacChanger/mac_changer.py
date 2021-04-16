#!/usr/bin/env python

import subprocess
import optparse
import re

def getArgs():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="_interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="_newMacAddress", help="New Mac address")
    (options, arguments) = parser.parse_args()
    if not options._interface:
        parser.error("[-] Please specify an interface.")
    elif not options._newMacAddress:
        parser.error("[-] Please sepecify a MAC Address")
    return options

def changeMac(_interface, _newMacAddress):
    # print("[+] Changing MAC address for " + _interface + " to " + _newMacAddress + "\n")
    subprocess.call(["ifconfig", _interface, "down"])
    subprocess.call(["ifconfig", _interface, "hw", "ether", _newMacAddress])
    subprocess.call(["ifconfig", _interface, "up"])

def getCurrentMac(_interface):
    _ifconfigResult = subprocess.check_output(["ifconfig", _interface])
    _macAddressSearchResult = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(_ifconfigResult))
    if _macAddressSearchResult:
        return _macAddressSearchResult.group(0)
    else:
        print("[-] Could not retrieve the MAC Address")

def engine():
    options = getArgs()
    _currentMac = getCurrentMac(options._interface)
    print("Current MAC Address: " + str(_currentMac))
    changeMac(options._interface, options._newMacAddress)
    _currentMac = getCurrentMac(options._interface)
    if _currentMac == options._newMacAddress:
        print("[+] New MAC Address: " + str(_currentMac))
    else:
        print("[-] MAC Address did not get changed.")

engine()
