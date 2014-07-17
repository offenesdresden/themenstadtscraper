from ..themenstadtscraper import handle_json_response

import json
import psycopg2

def test_handlejsonresponse():
	jsonstring = """{"value":{"Records":[{"Heading":"Ortsamt/Ortschaft","ThemeId":"5.3","IsContentTheme":false,"DetailOpensInNewWindow":false,"CustomDetailLinkText":null,"Hits":[{"Text":"Pieschen","HasDetailUrl":false,"ThemeId":"5.3","LayerName":"L483","Id":"Pieschen"}],"TotalHitCount":1,"IdColumnDataType":64,"RenderAsTable":false,"PkValueAvailable":true,"PkFieldName":"NAME","TableProps":null},{"Heading":"Stadtteil","ThemeId":"5.3","IsContentTheme":false,"DetailOpensInNewWindow":false,"CustomDetailLinkText":null,"Hits":[{"Text":"Pieschen-Süd","HasDetailUrl":false,"ThemeId":"5.3","LayerName":"L484","Id":"21"}],"TotalHitCount":1,"IdColumnDataType":64,"RenderAsTable":false,"PkValueAvailable":true,"PkFieldName":"NUMMER","TableProps":null}],"OriginPoint":{"X":5410700.00000001,"Y":5660240,"EpsgCode":31469,"XStr":"5410700","YStr":"5660240","IsLatLon":false,"RenderAsTable":false},"PointInSystemEpsg":{"X":5410700.00000001,"Y":5660240,"EpsgCode":31469,"XStr":"5410700","YStr":"5660240","IsLatLon":false,"RenderAsTable":false},"PointInAdditionalEpsgs":null,"PointInWgs":{"X":13.7239723121753,"Y":51.0703402850307,"EpsgCode":4326,"XStr":"13° 43' 26''","YStr":"51° 4' 13''","IsLatLon":true,"RenderAsTable":false},"ZValueQueried":true,"ZValue":{"ZValue":105.4499,"Source":{"Driver":14,"SourceId":1063,"Base":2}},"ZValueText":"105,4 Meter / NHN"}}"""
	j = json.loads(jsonstring)

	with psycopg2.connect("dbname=themenstadtplan") as pg_conn:
		pg_conn.autocommit = True
		with pg_conn.cursor() as pg_cursor:
			handle_json_response(j, pg_cursor)