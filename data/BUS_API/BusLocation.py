from DriveData import DriveData

class BusLocation:
	##조회할 노선 아이디를 받는다.
	def __init__(self, rootTag):
		BusLocation.childTagName = ("routeId", "stationId", "endBus", "plateNo", "stationSeq")
		self.root = rootTag
		self.dataDict = {}
		for t in BusLocation.childTagName:
			self.dataDict[t] = self.root.findtext(t)
		
		
		
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
	def getAll(self):
		return self.dataDict
		
		
##테스트코드
if __name__ == "__main__" :
	dd = DriveData("233000010")
	for bl in dd.getBusLocations():
		cbl = BusLocation(bl)
		print(cbl.getAll())
