#!/usr/bin/env python3
import requests
import psycopg2

import json

from progressbar import AnimatedProgressBar

def write_to_db(postgres_cursor, record, lat, lon):
	"""
		postgres_cursor: psycopg2._psycopg.cursor
		record: string (json)
		lat: float
		lon: float
	"""
	jsonstring = json.dumps(record, ensure_ascii=False, sort_keys=True)

	# Prüfen, ob element bereits in der Datenbank vorhanden ist.
	postgres_cursor.execute("""SELECT 1 FROM elemente WHERE properties::text = %s""", (jsonstring,))
	# Falls nicht, rein damit.
	if postgres_cursor.fetchone() is None:
		postgres_cursor.execute("""INSERT INTO elemente (properties, location) VALUES (%s, ST_GeomFromText('POINT(%s %s)', 4326));""", (jsonstring, lat, lon))


def handle_json_response(response_data, postgres_cursor):
	""" 
		response_data: dict
		postgres_cursor: psycopg2._psycopg.cursor
	"""

	lat = response_data["value"]["PointInWgs"]["Y"]
	lon = response_data["value"]["PointInWgs"]["X"]

	for record in response_data["value"]["Records"]:
		write_to_db(postgres_cursor, record, lat, lon)


def build_queries(xmin, xmax, ymin, ymax, basereq, granularity=10.):
	g = 1/granularity
	xstart = int(xmin*g)
	xend = int((xmax+1)*g)
	ystart = int(ymin*g)
	yend = int((ymax+1)*g)

	for x_g in range(xstart, xend):
		for y_g in range(ystart, yend):
			x = x_g*granularity
			y = y_g*granularity
			yield(basereq % (x, y))


def number_of_queries(xmin, xmax, ymin, ymax, granularity):
	g = 1/granularity
	xstart, xend, ystart, yend = int(xmin*g), int((xmax+1)*g), int(ymin*g), int((ymax+1)*g)
	return (xend-xstart)*(yend-ystart)


def scrape(parallelity=4, postgres_conn_string="dbname=themenstadtplan"):
	GRANULARITY = 10.

	XMIN = 5400499.
	XMAX = 5427620.
	YMIN = 5649580.
	YMAX = 5672231.

	# kleinerer Testausschnitt
	# XMIN = 5412133.
	# XMAX = 5415148.
	# YMIN = 5656993.
	# YMAX = 5657370.

	BASEURL = "http://stadtplan2.dresden.de/(S(jcksai1ssxvzjbveqyv1aizy))/ajaxpro/ASP.spdd_controls_mapcontainer_ascx,App_Web_o3sebx4k.ashx"
	HEADERS = {"X-AjaxPro-Method": "GetMapTipEx", "Origin": "http://stadtplan2.dresden.de", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "de-DE", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36", "Content-Type": "text/plain; charset=UTF-8", "Accept": "*/*", "Referer": "http://stadtplan2.dresden.de/(S(jcksai1ssxvzjbveqyv1aizy))/spdd.aspx", "Cookie": "cardo3SessionGuid=C3_4ef68a3a-59ca-4a0c-b3cc-722fdabb1c84", "Connection": "keep-alive"}
	BASEREQ = '{"applicationContextType":null,"themeList":"6.1121|278.1397_6.2/278.1397|318.105_6.2/318.105|320.1580_6.2/320.1580|6.1286|6.1388|6.1478|6.640|6.1444|6.1006|6.641|6.613|6.642|6.1194|6.1257|6.343|6.854|6.22|6.130|6.103|6.128|6.377|6.379|6.565|6.105|6.108|6.109|6.117|6.106|6.107|6.177|6.178|6.994|6.118|6.119|6.1580|6.1582|6.376|6.431|6.432|6.1325|6.1321|6.1322|6.1323|6.777|6.783|6.778|6.779|6.775|6.782|6.784|6.785|6.769|6.770|6.771|6.773|6.772|6.774|6.780|6.781|6.910|6.776|6.768|6.363|6.429|6.498|6.426|6.1011|6.1523|6.511|6.542|6.144|6.183|6.187|6.189|6.360|6.357|6.592|6.359|6.358|6.356|6.444|6.477|6.483|6.470|6.471|6.478|6.472|6.479|6.473|6.480|6.474|6.481|6.484|6.475|6.476|6.482|6.1483|6.1048|6.147|6.146|6.1214|6.196|6.967|6.1407|6.1403|6.1418|6.1318|6.142|6.437|6.441|6.442|6.434|6.435|6.443|6.436|6.539|6.529|6.531|6.532|6.533|6.534|6.535|6.536|6.537|6.622|6.1414|6.1413|6.1195|6.597|6.594|6.596|6.599|6.595|6.598|6.1310|6.1320|6.1324|6.447|6.445|6.1294|6.1295|6.191|6.192|6.446|6.1293|6.193|6.194|6.450|6.451|6.452|6.448|6.449|6.430|6.993|6.566|6.197|6.831|6.807|6.578|6.638|6.1436|6.1440|6.614|6.1359|6.1445|6.1449|6.954|6.1080|6.839|6.1408|6.1395|6.1312|6.127|6.1524|6.1552|6.1049|6.1326|279.159_6.2/279.159|6.992|6.524|6.525|6.123|6.121|6.122|6.1046|6.1397|6.1554|6.1555|6.1047|6.795|6.796|6.767|6.871|6.870|6.935|6.701|6.341|6.152|6.1369|6.153|6.148|6.1562|6.42|6.1505|6.975|6.1461|6.1460|6.1459|6.1489|6.1482|6.846|6.886|6.887|6.888|6.889|6.885|6.902|6.900|6.901|6.949|6.950|6.951|6.286|6.289|6.295|6.296|6.1231|6.1232|6.1368|6.1547|6.590|6.805|6.1251|6.1075|6.1073|6.586|6.1591|6.1217|6.1216|6.1225|6.422|6.407|6.408|6.200|6.203|6.204|6.409|6.410|6.411|6.205|6.206|6.207|6.208|6.209|6.210|6.316|6.847|6.1307|6.486|6.601|6.463|6.233|6.236|6.234|6.237|6.235|6.159|6.232|6.283|6.47|6.1129|6.861|6.1192|6.545|6.325|6.1556|6.372|6.371|6.1052|6.369|6.370|6.983|6.1317|6.1338|6.1468|6.427|6.648|6.647|6.649|6.653|6.654|6.652|6.651|6.876|6.877|6.176|6.125|$BaseMap#5#Tiles","gx":%.6f,"gy":%.6f,"srs":31469,"currentMapScale":1000}'

	progressbar = AnimatedProgressBar(end=number_of_queries(XMIN, XMAX, YMIN, YMAX, GRANULARITY), width=80)

	with psycopg2.connect(postgres_conn_string) as pg_conn:
		pg_conn.autocommit = True
		with pg_conn.cursor() as pg_cursor:
			for query in build_queries(XMIN, XMAX, YMIN, YMAX, basereq=BASEREQ, granularity=GRANULARITY):
				res = requests.post(BASEURL, data=query, headers=HEADERS)
				handle_json_response(res.json(), pg_cursor)
				progressbar + 1
				progressbar.show_progress()


if __name__ == "__main__":
	scrape()