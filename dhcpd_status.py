#!/usr/bin/env python3

import bottle
from bottle import route, static_file, view
from collections import namedtuple
from datetime import datetime
from isc_dhcp_leases import Lease, IscDhcpLeases
from manuf.manuf import MacParser
from socket import inet_aton


application = bottle.default_app()
macParser = MacParser()
LeaseRow = namedtuple('LeaseRow', 'age ip mac name state vendor')

@route('/')
@route('/<filter>')
@view('templates/dhcp-leases')
def dhcpLeases(filter='active'):
    leases = IscDhcpLeases('/var/db/dhcpd/dhcpd.leases')
    rows = []
    for l in sorted(leases.get(), key=lambda l: inet_aton(l.ip)):
        age = datetime.now() - l.start
        age = str(age).split('.')[0]
        vendor = macParser.get_manuf_long(l.ethernet)
        if filter == 'all' or filter == l.binding_state:
            rows.append(LeaseRow(age=age, ip=l.ip, mac=l.ethernet,
                    name=l.hostname, state=l.binding_state, vendor=vendor))
    return dict(leases=rows)

@route('/static/<filename>')
def static(filename):
    return static_file(filename, root='static')
