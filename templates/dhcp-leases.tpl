<html>
<head>
	<title>DHCP Leases</title>
	<link rel="stylesheet" href="static/main.css">
</head>
<body>
<h1>DHCP Leases</h1>
<table>
	<th>IP<br />DNS</th>
	<th>MAC</th>
	<th>Vendor</th>
	<th>Name</th>
	<th>Age</th>
	<th>State</th>
% if extended:
	<th>active<br />valid</th>
	<th>start<br />end</th>
% end
</tr>
% for l in leases:
<tr class="state-{{l.state}} ip-{{l.color}}">
	<td>{{l.ip}}<br/>{{l.dns}}</td>
	<td class="mac">{{l.mac}}</td>
	<td>{{l.vendor}}</td>
	<td>{{l.name}}</td>
	<td class="age">{{l.age}}</td>
	<td class="state">{{l.state}}</td>
% if extended:
	<td>{{l.active}}<br />{{l.valid}}</td>
	<td>{{l.start}}<br />{{l.end}}</td>
% end
</tr>
% end
</table>
</body>
</html>
