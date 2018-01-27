#!/usr/bin/env python3

import bottle
from bottle import route, static_file, view
from isc_dhcp_leases import Lease, IscDhcpLeases

application = bottle.default_app()

@route('/')
@view('templates/dhcp-leases')
def dhcpLeases():
    leases = IscDhcpLeases('/var/db/dhcpd/dhcpd.leases')
    rows = []
    for k, l in leases.get_current().items():
        rows.append(l)
    return dict(leases=rows)

@route('/static/<filename>')
def static(filename):
    return static_file(filename, root='static')
