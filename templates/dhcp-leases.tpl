<html>
<head>
	<title>DHCP Leases</title>
	<link rel="stylesheet" href="static/main.css">
</head>
<body>
<h1>DHCP Leases</h1>
<table>
<tr>
	<th>IP</th>
	<th>MAC</th>
	<th>Vendor</th>
	<th>Name</th>
	<th>Age</th>
</tr>
% for l in leases:
<tr>
	<td>{{l.ip}}</td>
	<td>{{l.ethernet}}</td>
	<td>{{macs.get_manuf(l.ethernet)}}</td>
	<td>{{l.hostname}}</td>
	<td>{{l.start}}</td>
</tr>
% end
</table>
</body>
</html>
