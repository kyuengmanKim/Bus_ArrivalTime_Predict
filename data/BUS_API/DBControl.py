import pymysql
from datetime import datetime


class DBControl:
	def __init__(self, _host, _id, _pw, _dbname, _port=3306):
		#self.con = pymysql.connect(host, port, id, pw, dbname, charset='utf8')
		self.con = pymysql.connect(host=_host, port=_port, user=_id, password=_pw, database=_dbname, charset='utf8')
		self.cur = self.con.cursor(pymysql.cursors.DictCursor)
		self.tableTitle=("id", "stationName","stationID","arrTime","routeNo","routeID", "plateNo" ,  "endBus","weekday","holiday")
		self.tableItemLen = (7, 40, 10, 16, 20, 10, 13, 2,2,2)
		self.cur.execute("set names utf8")
	def __del__(self):
		self.con.close()
		
	##테이블생성
	def createTable(self, tableName):
		sql = "create table " + tableName + " ("
		for i in range(len(self.tableTitle)):
			sql+=(self.tableTitle[i] + " varchar(" + str(self.tableItemLen[i]) + ") not null,")
		sql+="primary key(id) );"
		self.cur.execute(sql)
		self.con.commit()

	def resultSql(self, sql):
		self.cur.execute(sql)
		return list(self.cur.fetchall())
		
	##테이블확인
	def isThisTable(self, tableName):
		self.cur.execute("show tables like '%s'" % tableName)
		printstr =str(self.cur.fetchall())
		#print(printstr)

		return tableName in printstr
		
	##count테이블생성
	def createCountTable(self, tableName):
		self.cur.execute( "create table "+tableName+"count (count char(7) not null);")
		self.cur.execute( "insert into " + tableName + "count (count) values ('%s');" % self.getRowViaSql(tableName))
		self.con.commit()
		
	##row 	
	def getRowViaSql(self, tableName):
		self.cur.execute( "select count(*) from %s;" % tableName)
		answer = self.cur.fetchall()
		return list(answer[0].values())[0]
	def getRowViaTable(self, tableName):
		self.cur.execute("select * from " + tableName)
		answer = self.cur.fetchall()
		#return list(answer[0].values())[0]
		return answer
	def updateRowViaTable(self, tableName):
		curRow = self.getRowViaTable(tableName)
		realRow = self.getRowViaSql(tableName)
		self.cur.execute("update " + tableName + "count set count='%s' where count='%s';" % (realRow, curRow))
	
	def incRowViaTable(self, tableName):
		curRow = int(self.getRowViaTable(tableName))
		sql = "update " + tableName + "count set count='%d' where count='%d';" % (curRow+1, curRow)
		self.cur.execute(sql)
	
	##로그 테이블 생성
	def createLogTable(self, tableName):
		self.cur.execute( "create table "+tableName+ "log (time varchar(16) not null, seq varchar(3) not null, log varchar(128) not null);")
		#self.cur.execute( "insert into " + tableName + "log (time,seq,log) values ('%s','%s','%s');" % self.getRowViaSql(tableName))
		self.con.commit()	
	##로그 테이블 데이터 추가
	def addDataLogTable(self, tableName, data):
		self.cur.execute( "insert into " + tableName + "log (time, seq, log) values ('%s', '%s', '%s');" % data )
		self.con.commit()
		

	## bus eda info 테이블 만들기 
	def createBusEdainfoTable(self):
		exe_query = "CREATE TABLE `Bus_Eda_info` (`bstopId` varchar(45) NOT NULL,`routeNo` char(50) NOT NULL,  `routeId` char(50) DEFAULT NULL, `bstopNm` varchar(45) DEFAULT NULL, `BSTOPSEQ` varchar(45) DEFAULT NULL,  `SHORT_BSTOPID` varchar(45) DEFAULT NULL, PRIMARY KEY (`bstopId`) );"
		self.cur.execute(exe_query)
		#self.cur.execute( "insert into " + tableName + "log (time,seq,log) values ('%s','%s','%s');" % self.getRowViaSql(tableName))
		self.con.commit()	
	## BUS_EDA 테이블 데이터 추가
	def addDataBusEdainfoTable(self, data):

		print(data[0])

		if not self.cur.execute( "select bstopId from BUS_EDA_INFO where bstopId = '%s';" % data[0]):
			self.cur.execute( "insert into BUS_EDA_INFO (bstopId, routeNo, routeId, bstopNm,BSTOPSEQ, SHORT_BSTOPID ) values ('%s', '%s', '%s','%s', '%s', '%s');" % data )
			self.con.commit()


	## bus data 테이블 만들기 
	def createBusDataTable(self):
		exe_query = "CREATE TABLE `BUS_DATA` (`bstopId` varchar(45) NOT NULL, `routeNo` char(50) NOT NULL,  `routeId` char(50) DEFAULT NULL,  `bstopNm` varchar(45) DEFAULT NULL, `busId` varchar(45) DEFAULT NULL, `LATEST_STOP_NAME` varchar(80) DEFAULT NULL, `Bus_Num_Plate` varchar(45) DEFAULT NULL,`Rest_Stop_Count` varchar(45) DEFAULT NULL,`ARRIVALESTIMATETIME` varchar(45) DEFAULT NULL,  `ThisDT` DATETIME DEFAULT NULL );"
		self.cur.execute(exe_query)
		#self.cur.execute( "insert into " + tableName + "log (time,seq,log) values ('%s','%s','%s');" % self.getRowViaSql(tableName))
		self.con.commit()	
	## BUS_EDA 테이블 데이터 추가
	def addDataBusdataTable(self, data):
		self.cur.execute( "insert into Bus_Data (bstopId, routeNo, routeId, bstopNm, busId, LATEST_STOP_NAME, Bus_Num_Plate, Rest_Stop_Count,ARRIVALESTIMATETIME,ThisDT) values ('%s', '%s', '%s','%s', '%s', '%s','%s','%s', '%s', '%s');" % data )
		self.con.commit()		


	##데이터추가
	def addData(self, tableName, data):
		if len(self.tableTitle) != len(data):
			return False
			
		sql = "insert into " + tableName + " ("
		for i in self.tableTitle:
			sql+=(i+",")
			
		sql=sql[:-1] + ") values ("
		#sql+="\b) values ("
		for i in data:
			sql+=("'%s'," % i)
		#sql+="\b) ;"
		sql=sql[:-1] + ") ;"
		self.cur.execute(sql)
		self.con.commit()
		return True
		
	def dateToTableName(date):
		return "data"+date.replace("-", "")
		




##테스트코드
if __name__ == "__main__" :

	now = datetime.now()	
	date = str(datetime.date(now))

	server = "localhost"
	serverPort = 3306
	dbc = DBControl(server, "root", "db1234!", "busarrivaldb", serverPort)



	## BUS_Data(분석용 정보 적재 테이블) table 오늘날짜 테이블있는지 확인
	if not dbc.isThisTable():
		##없으면 만든다
		dbc.createBusDataTable()	
	## BUS_EDA(분석용 버스 정보 적재 테이블) table 오늘날짜 테이블있는지 확인
	if not dbc.isThisTable():
		##없으면 만든다
		dbc.createBusEdainfoTable()
	##오늘날짜 테이블있는지 확인
	if not dbc.isThisTable(DBControl.dateToTableName(date)):
		##없으면 만든다
		dbc.createTable(DBControl.dateToTableName(date))
	##오늘날짜 로그테이블있는지 확인
	if not dbc.isThisTable(DBControl.dateToTableName(date)+"log"):
		##없으면 만든다
		dbc.createLogTable(DBControl.dateToTableName(date))
	##오늘날짜 카운트 있는지 확인	
	if not dbc.isThisTable(DBControl.dateToTableName(date)+"count"):
		##없으면 만든다
		dbc.createCountTable(DBControl.dateToTableName(date))
	else:##있으면 실제 row수와 기록을 맞춘다
		dbc.updateRowViaTable(DBControl.dateToTableName(date))
	##row가져오기
	curCount = int(dbc.getRowViaTable(DBControl.dateToTableName(date)))


