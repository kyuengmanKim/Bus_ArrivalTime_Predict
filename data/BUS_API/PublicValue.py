from DBControl import DBControl ##DB

# INCHEON BUS CUST
BUS_LOCATION_URL = 'http://apis.data.go.kr/6280000/busArrivalService/getBusArrivalList'
ROUTE_STATION_URL = 'http://apis.data.go.kr/6280000/busRouteService/getBusRouteSectionList'
BUS_IDINFO_URL = 'http://apis.data.go.kr/6280000/busRouteService/getBusRouteNo'
service_kry="Mq55fO1HRuLnnWjrxhjZ%2FGx13JLT3zFHFqq7V4kVpxtSMrJa4PpcNhLeIGLQzebHsYtoKVpdoQtucfhaYJV6nw%3D%3D" 
KEY = service_kry



## binary data to utf-8
def binToUtf8(data):
	# 바이너리 데이터를 utf-16으로 디코딩한다
	# 수직 탭을 삭제한다
	return data.decode("utf-8").replace(u"\u000B", u"")

def getRouteList():
	dbc = DBControl("localhost", "root", "db1234!", "joambusdb")
	#dbc = DBControl("localhost", "root", "비번", "busarrivaldb")
	result=dbc.resultSql("select routeName, routeId From routeInfo;")
	routeList={}
	for row in result:
		if '50-1' in str(row):
			continue
		routeList[row['routeName']] = row['routeId']
	return routeList