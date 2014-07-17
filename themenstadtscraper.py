#!/usr/bin/env python3
import requests
import psycopg2

import json

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


def scrape(parallelity=4, postgres_conn_string="dbname=themenstadtplan"):
	XMIN = 5400499.
	XMAX = 5427620.
	YMIN = 5649580.
	YMAX = 5672231.
	BASEURL = "http://stadtplan2.dresden.de/(S(jcksai1ssxvzjbveqyv1aizy))/ajaxpro/ASP.spdd_controls_mapcontainer_ascx,App_Web_o3sebx4k.ashx"
	HEADERS = {"X-AjaxPro-Method": "GetMapTipEx", "Origin": "http://stadtplan2.dresden.de", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "de-DE", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36", "Content-Type": "text/plain; charset=UTF-8", "Accept": "*/*", "Referer": "http://stadtplan2.dresden.de/(S(jcksai1ssxvzjbveqyv1aizy))/spdd.aspx", "Cookie": "cardo3SessionGuid=C3_4ef68a3a-59ca-4a0c-b3cc-722fdabb1c84", "Connection": "keep-alive"}
	BASEREQ = '{"applicationContextType":null,"themeList":"$BaseMap#5#Tiles","gx":%.6f,"gy":%.6f,"srs":31469,"currentMapScale":1500}'

	with psycopg2.connect(postgres_conn_string) as pg_conn:
		pg_conn.autocommit = True
		with pg_conn.cursor() as pg_cursor:
			for query in build_queries(XMIN, XMAX, YMIN, YMAX, basereq=BASEREQ, granularity=10.):
				res = requests.post(BASEURL, data=jsonreq, headers=HEADERS)
				handle_json_response(res.json(), pg_cursor)


if __name__ == "__main__":
	scrape()