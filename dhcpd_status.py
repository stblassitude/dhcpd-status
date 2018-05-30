#!/usr/bin/env python3

import bottle
from bottle import abort, route, run, static_file, view
from collections import namedtuple
from datetime import datetime
from isc_dhcp_leases import Lease, IscDhcpLeases
from isc_dhcpd_conf import IscDhcpdConf
from manuf.manuf import MacParser
from socket import gethostname, inet_aton
import dns.resolver
import dns.reversename
import re
import subprocess

application = bottle.default_app()
macParser = MacParser()
LeaseRow = namedtuple('LeaseRow', 'active age dns end ip mac name start state valid vendor')
ArpRow = namedtuple('ArpRow', 'ip mac')

filters = {
    'all': lambda l: True,
    'active': lambda l: l.active and l.valid,
}


def arpentries():
    entries = []
    arps = subprocess.check_output(["/usr/sbin/arp", "-an"], encoding="UTF-8")
    i = 0
    for line in re.split(r'\n', arps):
        m = re.match(r'\? \((?P<ip>\d+\.\d+\.\d+\.\d+)\) at (?P<mac>.*?) on.*?', line)
        if not m:
            continue
        print("{}: {}, {}".format(i, m.group('ip'), m.group('mac')))
        i = i +1
        entries.append(ArpRow(ip=m.group('ip'), mac=m.group('mac')))
    return entries

def reverse(ip):
    try:
        answer = dns.resolver.query(dns.reversename.from_address(ip), 'PTR')
        return answer[0]
    except dns.resolver.NXDOMAIN:
        return ''


@route('/')
@route('/<filter>')
@view('templates/dhcp-leases')
def dhcpLeases(filter='active'):
    leases = IscDhcpLeases('/var/db/dhcpd/dhcpd.leases')
    entries = {}
    rows = []
    now = datetime.utcnow()
    for l in sorted(leases.get(), key=lambda l: inet_aton(l.ip)):
        age = now - l.start
        age = str(age).split('.')[0]
        state = l.binding_state
        if state == 'active' and l.end and l.end < now:
            state = 'expired'
        name = reverse(l.ip)
        vendor = macParser.get_manuf_long(l.ethernet)
        if filters[filter](l):
            leaserow = LeaseRow(active=l.active, age=age, dns=name, end=l.end, ip=l.ip, mac=l.ethernet,
                    name=l.hostname, start=l.start, state=state, valid=l.valid,
                    vendor=vendor)
            entries[leaserow.mac] = leaserow
            rows.append(leaserow)
    for l in arpentries():
        name = reverse(l.ip)
        vendor = macParser.get_manuf_long(l.mac)
        if l.mac not in entries:
            rows.append(LeaseRow(active=True, age=0, dns=name, end=None, ip=l.ip, mac=l.mac,
                    name='', start=None, state='arp', valid=True, vendor=vendor))
    return dict(extended=False, leases=sorted(rows, key=lambda l: inet_aton(l.ip)))

@route('/static/<filename>')
def static(filename):
    return static_file(filename, root='static')

@route('/favicon.ico')
def favicon():
    abort(404)


if __name__ == "__main__":
    run(host=gethostname(), port=8080, reloader=True)

