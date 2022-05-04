from DriveData import DriveData
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
from xml.etree.ElementTree import fromstring
from PublicValue import *


class BusArrivalList:
	##조회할 노선 아이디를 받는다.
	def __init__(self, bstopId, routeId):

		print("self, routeId== bstopId ===========================>", self, routeId, bstopId)
		
		## xml url
		BusArrivalList.url = BUS_LOCATION_URL
		## 인증키
		BusArrivalList.key = KEY
			
		self.routeId = routeId
		self.bstopId = bstopId
		self.xmlStr = "" ##xml문자열 담을 변수
		self.root = None ##최상위 항목 담을 변수
		self.isOnInternet = True ## 인터넷연결여부 
		

		##xml요청 주소에 넘길 인자 세팅 option = "&numOfRows=100&pageNo=1&routeId="
		queryParams = '?' + urlencode({quote_plus('serviceKey') : "KEYKEY", quote_plus('numOfRows') : "100", quote_plus('pageNo') : "1",quote_plus('routeId') : self.routeId, quote_plus('bstopId') : self.bstopId })
		queryParams = queryParams.replace("KEYKEY", BusArrivalList.key)

		### del 
		print(self.url + queryParams)
		
		
		##xml문서 받아와 str으로 xmlStr에 담는다.
		request = Request(self.url + queryParams)
		request.get_method = lambda: 'GET'
		try:
			self.xmlStr = binToUtf8(urlopen(request).read())
			self.root = fromstring(self.xmlStr)
		except:
			self.isOnInternet = False


		#print(self.xmlStr)


	def isConnectInternet(self):
		return self.isOnInternet
		
	## 본 정보의 루트태그 msgBody의 유무 체크
	def isSuccess(self):
		if not self.isOnInternet:
			return False
	
		return self.root.find("msgBody")!=None
		
	## xml문서의 루트태그 리턴
	def getRoot(self):
		if not self.isOnInternet:
			return None
		return self.root
		
	## xml문서에서 본 정보(버스위치)리스트 리턴
	def getBuslocationVal(self):
		if not self.isSuccess():
			return []
			
		aList = list(self.root.find("msgBody"))
		
		##정류장 순서 기준을 정렬
		#sorted(aList, key = lambda x: int(x.findtext("routeId")))

		return aList




		
	def getRouteId(self):
		return self.dataDict[BusLocation.childTagName[0]]
	def getStationId(self):
		return self.dataDict[BusLocation.childTagName[1]]
	def getEndBus(self):
		return self.dataDict[BusLocation.childTagName[2]]
	def getPlateNo(self):
		return self.dataDict[BusLocation.childTagName[3]]
	def getStationSeq(self):
		return self.dataDict[BusLocation.childTagName[4]]
	def getStationSeq(self):
		return self.dataDict[BusLocation.childTagName[5]]
	def getAll(self):
		return self.dataDict
		
		
##테스트코드
if __name__ == "__main__" :
	dd = DriveData("165000381")
	for bl in dd.getBusLocations():
		cbl = BusLocation(bl)
		print(cbl.getAll())


