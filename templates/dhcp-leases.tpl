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
	<th>State</th>
</tr>
% for l in leases:
<tr class="{{l.state}}">
	<td>{{l.ip}}</td>
	<td class="mac">{{l.mac}}</td>
	<td>{{l.vendor}}</td>
	<td>{{l.name}}</td>
	<td class="age">{{l.age}}</td>
	<td>{{l.state}}</td>
</tr>
% end
</table>
</body>
</html>
