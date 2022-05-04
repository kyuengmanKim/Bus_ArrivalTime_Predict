#제목: Data go KR 인천버스 정보 조회 API 활용하기
# 2022 02 05 edit by HKIM 
 
from DriveData import *
from BusArrivalList import BusArrivalList
from RouteStation import RouteStation ##정류장 목록
from DBControl import DBControl ##DB
from PublicValue import *
#from Holiday import Holiday
import time
from datetime import datetime
from os import path
import sys
import traceback


errorCount = 0
## 노선번호:노선ID

'''
routeList = {
    "1-1": "233000051", "2": "233000013", "2-1": "233000052",
	"7" : "233000058", "8": "233000046", "8-1": "233000057", "8-2": "233000049", 
    "8-3" : "233000047", "9": "233000025", "11": "233000041", "11-2": "233000060", 
    "11-4" : "233000062", "11-5": "233000059", "14": "233000024", "15": "233000022", 
    "16" : "233000034", "17": "233000044", "18": "233000036", "19": "233000026", 
	"5100" : "200000115","1005" : "234000065"
    }
'''
# routeNo : routeID
routeList = {
    "6724": "165000381", "9201": "165000245"
    }

# routeID : BSTOPID
bstopList = ["164000070", "164000346","113000424","113000412"]


##DB
##객체생성
server = "192.168.10.223"
serverPort = 3306
##ori dbc = DBControl(server, "root", "비번", "busarrivaldb", serverPort)
dbc = DBControl(server, "root", "db1234!", "busarrivaldb", serverPort)
#dbc = DBControl("localhost", "root", "비번", "busarrivaldb")


############################################ 조회할 데이터를 만든다
# BUS_EDA_INFO 테이블 만들기

## BUS_Data(분석용 정보 적재 테이블) table 오늘날짜 테이블있는지 확인
if not dbc.isThisTable("BUS_DATA"):
	##없으면 만든다
	dbc.createBusDataTable()	
## BUS_EDA(분석용 버스 정보 적재 테이블) table 오늘날짜 테이블있는지 확인
if not dbc.isThisTable("BUS_EDA_INFO"):
	##없으면 만든다
	dbc.createBusEdainfoTable()
		

try:

	#노선번호와 노선ID로 정류소정보를 생성 하여 BUS_eda_info 테이블을 채운다. 
	for no in routeList.keys():

		print("노선번호 => :", no, routeList[no])
		##조회할 노선의 버스위치 목록
		bb = BusInfo(no)

		if not bb.isConnectInternet():
			print("인터넷 확인하세요!")
			sys.exit()
			
		BList = bb.getBusInfo() #버스정보 획득 RouteID, RouteNo

		if len(BList)>0:
			for bl in BList:					
				print("BList === ROUTEID 리스트", len(BList))

				print (bb.getBusInfo()[0].findtext("ROUTEID"))
				print (bb.getBusInfo()[0].findtext("ROUTENO"))

				#정류장 정보를 조회 해 온다.					
				dd = DriveData(bb.getBusInfo()[0].findtext("ROUTEID"))
				locaList = dd.getBusLocations()

				i=0
				for icbst in locaList:
					#print ("==>",dd.getBusLocations()[i].findtext("BSTOPID"))
					#print ("==>",dd.getBusLocations()[i].findtext("BSTOPNM"))
					#print ("==>",dd.getBusLocations()[i].findtext("BSTOPSEQ"))
					#print ("==>",dd.getBusLocations()[i].findtext("SHORT_BSTOPID"))
					#버스정류장 키와 맞으면 DB 등록
					for ifnd_ky in bstopList:

						if ((bb.getBusInfo()[0].findtext("ROUTEID") == routeList[no]) and ifnd_ky == (dd.getBusLocations()[i].findtext("BSTOPID"))):	
							print("ifnd_ky=======", ifnd_ky)
							data_lst = (dd.getBusLocations()[i].findtext("BSTOPID"),bb.getBusInfo()[0].findtext("ROUTENO"),bb.getBusInfo()[0].findtext("ROUTEID"),dd.getBusLocations()[i].findtext("BSTOPNM"),dd.getBusLocations()[i].findtext("BSTOPSEQ"),dd.getBusLocations()[i].findtext("SHORT_BSTOPID"))
							#정류장 정보 DB 저장 						
							print("data_lst======", data_lst)
							dbc.addDataBusEdainfoTable(data_lst)

					i=i+1

except Exception as e :
	ferr = open("error.txt", 'a')
	print(traceback.format_exc())
	ferr.write(str(datetime.now())+"\n"+str(traceback.format_exc()+"\n"))
	ferr.close()
	errorCount+=1
	if errorCount > 10:
		sys.exit()


#######################################################################################
print("================================roop===========================================================")


while True:## 무한 LOOP

	##하루종일 도는 루프 (날짜 바뀌면 빠짐)
	while True:
		##현재시간 프린트
		now = datetime.now()
		print(now)
		curTime = str(datetime.time(now))
		if  "00:00" in curTime.split('.')[0] :
			time.sleep(60-now.second)
			break
		elif datetime(now.year, now.month, now.day, 1, 0, 0, 0)< now <datetime(now.year, now.month, now.day, 5, 0, 0, 0):
			time.sleep((4-now.hour)*3600 + (60-now.minute)*60) ## 01시부터 05시까지 슬립
			break
		lognum=0

		try:
			##row가져오기
			allRow = dbc.getRowViaTable("BUS_EDA_INFO")
			for rtnVal in allRow:
				#print("rtnVal===",rtnVal)
				print(rtnVal["bstopId"], rtnVal["routeNo"], rtnVal["routeId"], rtnVal["bstopNm"])

				# bstopId 와 routeId  버스도착 정보를 조회 하여  BUS_DATA 테이블을 채운다. 
				cc = BusArrivalList(rtnVal["bstopId"],rtnVal["routeId"])

				BSList = cc.getBuslocationVal()

				#print(BSList)

				if len(BSList)>0:
					print("버스정보 있음 ----------------------------------")
					for busLoca in BSList:		

						#print(busLoca[0])			

						#print (cc.getBuslocationVal()[0].findtext("ARRIVALESTIMATETIME"))
						#print (cc.getBuslocationVal()[0].findtext("BSTOPID"))
						#print (cc.getBuslocationVal()[0].findtext("BUSID"))
						#print (cc.getBuslocationVal()[0].findtext("BUS_NUM_PLATE"))
						#print (cc.getBuslocationVal()[0].findtext("REST_STOP_COUNT"))
						#print (cc.getBuslocationVal()[0].findtext("LATEST_STOP_NAME"))


						thistimenow = datetime.now()
						#print(now)

						bdata_lst = (rtnVal["bstopId"],rtnVal["routeNo"], rtnVal["routeId"], rtnVal["bstopNm"],cc.getBuslocationVal()[0].findtext("BUSID"),cc.getBuslocationVal()[0].findtext("LATEST_STOP_NAME"),cc.getBuslocationVal()[0].findtext("BUS_NUM_PLATE"),cc.getBuslocationVal()[0].findtext("REST_STOP_COUNT"),cc.getBuslocationVal()[0].findtext("ARRIVALESTIMATETIME"), thistimenow)
							
						print(bdata_lst)

						#버스위 정보 BUS_DAT DB 저장 
						dbc.addDataBusdataTable(bdata_lst)
				else:
					print("도착결과 없음")
				
				#1초
				time.sleep(1)

			
		except Exception as e :
			ferr = open("error.txt", 'a')
			print(traceback.format_exc())
			ferr.write(str(datetime.now())+"\n"+str(traceback.format_exc()+"\n"))
			ferr.close()
			errorCount+=1
			if errorCount > 10:
				sys.exit()
		finally:
			print("\n24초 대기....")
			i=0
			for i in range(12):
				print (i*2)
				time.sleep(2)
			print (24)
			#dbc.addDataLogTable(DBControl.dateToTableName(date), (curTime,lognum,"sleep "+str(i)))




	
	

