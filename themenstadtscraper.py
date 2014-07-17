import requests

def scrape():
	XMIN = 5400499
	XMAX = 5427620
	YMIN = 5649580
	YMAX = 5672231

	BASEURL = "http://stadtplan2.dresden.de/(S(jcksai1ssxvzjbveqyv1aizy))/ajaxpro/ASP.spdd_controls_mapcontainer_ascx,App_Web_o3sebx4k.ashx"
	HEADERS = {"X-AjaxPro-Method": "GetMapTipEx", "Origin": "http://stadtplan2.dresden.de", "Accept-Encoding": "gzip,deflate,sdch", "Accept-Language": "de-DE", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36", "Content-Type": "text/plain; charset=UTF-8", "Accept": "*/*", "Referer": "http://stadtplan2.dresden.de/(S(jcksai1ssxvzjbveqyv1aizy))/spdd.aspx", "Cookie": "cardo3SessionGuid=C3_4ef68a3a-59ca-4a0c-b3cc-722fdabb1c84", "Connection": "keep-alive"}

	jsonreq = '{"applicationContextType":null,"themeList":"$BaseMap#5#Tiles","gx":%.6f,"gy":%.6f,"srs":31469,"currentMapScale":128000}' % (XMIN, YMIN)

	res = requests.post(BASEURL, data=jsonreq, headers=HEADERS)
	print(res.text)

if __name__ == "__main__":
	scrape()