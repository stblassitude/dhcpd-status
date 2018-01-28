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
LeaseRow = namedtuple('LeaseRow', 'age ip mac name state valid vendor')

filters = {
    'all': lambda l: True,
    'active': lambda l: l.active and l.valid,
}

@route('/')
@route('/<filter>')
@view('templates/dhcp-leases')
def dhcpLeases(filter='active'):
    leases = IscDhcpLeases('/var/db/dhcpd/dhcpd.leases')
    rows = []
    now = datetime.utcnow()
    for l in sorted(leases.get(), key=lambda l: inet_aton(l.ip)):
        age = now - l.start
        age = str(age).split('.')[0]
        state = l.binding_state
        if state == 'active' and l.end and l.end < now:
            state = 'expired'
        vendor = macParser.get_manuf_long(l.ethernet)
        if filters[filter](l):
            rows.append(LeaseRow(age=age, ip=l.ip, mac=l.ethernet,
                    name=l.hostname, state=state, valid=l.valid,
                    vendor=vendor))
    return dict(leases=rows)

@route('/static/<filename>')
def static(filename):
    return static_file(filename, root='static')
