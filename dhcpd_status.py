#!/usr/bin/env python3

import bottle
from bottle import route, static_file, view
from isc_dhcp_leases import Lease, IscDhcpLeases
from manuf.manuf import MacParser

application = bottle.default_app()
macParser = MacParser()

@route('/')
@view('templates/dhcp-leases')
def dhcpLeases():
    leases = IscDhcpLeases('/var/db/dhcpd/dhcpd.leases')
    rows = []
    for k, l in leases.get_current().items():
        rows.append(l)
    return dict(leases=rows, macs=macParser)

@route('/static/<filename>')
def static(filename):
    return static_file(filename, root='static')
