import sys
import datetime
import sqlite3
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QItemSelectionModel
from PyQt5.QtWidgets import *



# UI는 QT Designer로 제작할수 있지만 연습을 위해 컴포넌트를 직접 구성함.
# 직접 제작할때는 시그널 - 슬롯 연결이 용이함

# 메인 윈도우 클래스
class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):


        mTabWidget = QTabWidget()

        mWidget = mainWidget()

        mWidget_user = mainWidget_user() # change

        mTabWidget.addTab(mWidget, "대여목록")
        mTabWidget.addTab(mWidget_user, "회원목록")
        # 메인 윈도우에 붙여넣을 위젯 생성 후 Central에 set
        #mWidget = mainWidget()
        #self.setCentralWidget(mWidget)

        self.setCentralWidget(mTabWidget)

        # 종료 액션 생성 및 단축키 설정.
        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+W')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        # 상태바 생성.
        self.statusBar()


        # 메뉴바 생성 후 종료액션 추가함.
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        # 크기 사이즈에 맞게 맞춤.
        self.setGeometry(200, 100, 850, 513)
        self.setWindowTitle('도서대여')
        self.show()



# 메인 위젯 클래스
class mainWidget(QWidget):
    def __init__(self):
        super(mainWidget, self).__init__()
        self.initUI()

    def initUI(self):
        # 변수 선언.
        self.mat_list=[] # 검색 성공시 담아둘 리스트
        self.temp_mat_list= []

        # 테이블 객체 생성
        self.mtable_list = mWid_subTable()

        # 라벨, 버튼, 체크박스 생성
        srchLabel = QLabel("검색어", self)
        srchLabel.setFixedWidth(45)

        # 검색어 입력 칸
        self.srchWord = QLineEdit()
        self.srchWord.setFixedWidth(150)

        # 검색버튼 생성 및 단축키, 기능연결.
        srchBtn = QPushButton("검색", self)
        srchBtn.setFixedWidth(50)
        srchBtn.setShortcut(Qt.Key_Enter)
        srchBtn.clicked.connect(self.btnClickedSearch)

        # 검색 컨트롤 다이얼 설정 및 기능연결.
        self.boxSnum = QSpinBox()
        self.boxSnum.setMinimum(1)
        self.boxSnum.setMaximum(1)
        self.boxSnum.setFixedWidth(55)
        self.boxSnum.valueChanged.connect(self.f_srchIndex)

        # 책대여권수 얼마나 남았는지 체크
        self.srchResult = QLabel()
        if self.mtable_list.returnNum != 0:
            self.returnBook = QLabel("{0}권 대여중".format(self.mtable_list.returnNum))
        else:
            self.returnBook = QLabel("대여중인 책이 없습니다.")

        # 다른곳에서도 원하는 객체의 시그널을 받아와서 해당 클래스의 함수로 연결이 가능하다.
        self.mtable_list.cellChanged.connect(self.f_returnBook)

        # 레이아웃 구성.
        grid = QGridLayout()
        grid.setSpacing(10)
        self.setLayout(grid)

        grid.addWidget(srchLabel, 0, 0)
        grid.addWidget(self.srchWord, 0, 1)
        grid.addWidget(srchBtn, 0, 2)
        grid.addWidget(self.boxSnum, 0, 3)
        grid.addWidget(self.srchResult, 0, 4)
        grid.addWidget(self.returnBook, 0, 10)
        grid.addWidget(self.mtable_list, 1, 0, 1, -1) # -1은 최대

        self.show()


    # 책이 얼마나 남았나 확인하는 함수. (connecting)
    def f_returnBook(self):

        if self.mtable_list.returnNum != 0:
            self.returnBook.setText("{0}권 대여중".format(int(self.mtable_list.returnNum)))
        else:
            self.returnBook.setText("대여중인 책이 없습니다.")


    # 리사이즈 이벤트 함수 오버라이딩함.
    # 레퍼런스에 있는 각각의 클래스함수들을 오버라이딩 하고 일어나는 현상 관찰이 필요할듯.
    def resizeEvent(self, QResizeEvent):

        widSum=0
        for rs in range(5):
            widSum+=self.mtable_list.columnWidth(rs)
        # 비고란의 width를 창 길이 변화마다 조절.
        self.mtable_list.setColumnWidth(5, self.mtable_list.width()-widSum-23)


    # 검색버튼 정의 , 슬롯
    def btnClickedSearch(self):

        self.boxSnum.setValue(1)
        # 이전 검색목록은 흰색으로 변경.
        for mch in self.temp_mat_list:
            mch.setBackground(QColor(255,255,255))

        # 빈칸이면 취소
        if self.srchWord.text() == "":
            self.srchResult.setText("")
            return

        # findItems로 검색 방식 정의, 이후 결과 mat_list에 저장. QTableWidgetItem 형태로 저장됨.
        self.mat_list=self.mtable_list.findItems(self.srchWord.text(), Qt.MatchContains)


        # 검색결과가 한개라도 있다면
        if len(self.mat_list) != 0:

            # 다이얼 값 세팅
            self.boxSnum.setMaximum(len(self.mat_list))
            self.boxSnum.setFocus()
            self.srchResult.setText('''%d개 검색 ("%s")''' % (len(self.mat_list), self.srchWord.text()))

            # 검색결과 색깔 변경.
            self.temp_mat_list=self.mat_list
            for mch in self.mat_list:
                mch.setBackground(QColor(152, 173, 255))

            # 검색 후 첫번째 검색셀로 이동.
            self.mtable_list.setCurrentItem(self.mat_list[0], QItemSelectionModel.SelectCurrent)

        # 검색결과가 없으면
        else:
            QMessageBox.information(self, "검색 실패", "검색 결과가 없습니다.")


    # 다이얼 조절하면 해당 일치하는 Item Index로 이동함.
    def f_srchIndex(self,num):

        try:
            self.mtable_list.setCurrentItem(self.mat_list[num-1], QItemSelectionModel.SelectCurrent)
        except:
            pass


# 테이블 위젯 클래스 (목록을 보여주는 칸들)
class mWid_subTable(QTableWidget):
    def __init__(self):
        super(mWid_subTable, self).__init__()
        self.initUI()

    def initUI(self):
        # 변수 선언.
        self.returnNum = 0 # 책미반납개수
        # DB 이름을 쉽게 가져오기 위해 배열에 저장
        self.dbColName=["no", "date", "name", "bookname", "isreturn", "etc"]

        # DB 연결, table 이름 rentaldata, 없으면 생성.
        self.conn = sqlite3.connect('mscomics.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("create table if not exists rentaldata(no integer primary key autoincrement, date varchar2, name varchar2, bookname varchar2, isreturn varchar2, etc varchar2)")

        # DB에서 데이터 가져와서 self.dbrows에 넣음.
        self.cursor.execute("select * from rentaldata")
        self.dbrows = self.cursor.fetchall()

        # db 데이터가 없으면 한개 넣고 작업실행.
        if len(self.dbrows) == 0:
            self.cursor.execute("insert into rentaldata(date, name, bookname, isreturn, etc) values (?,?,?,?,?)",
                                ("", "", "", 0, ""))
            self.conn.commit()
            self.cursor.execute("select * from rentaldata")
            self.dbrows = self.cursor.fetchall()

        # db데이터 row 수
        lineNum=len(self.dbrows)

        # (row,col)을  (라인 넘버, 6) 으로 set
        self.setRowCount(lineNum)
        self.setColumnCount(6)

        # 정렬 가능하게 만드는 옵션
        self.setSortingEnabled(True)
        # 헤더 설정 및 세로 헤더 안보이게 설정
        self.setHorizontalHeaderLabels(["no","대여날짜","이름","책이름","반납","비고"])
        self.verticalHeader().setVisible(False)

        # 테이블 크기 조절.
        self.setColumnWidth(0, 70)
        self.setColumnWidth(1, 83)
        self.setColumnWidth(2, 67)
        self.setColumnWidth(3, 250)
        self.setColumnWidth(4, 70)

        # DB 정보 가져와서 초기화 작업.
        for no in range(1,lineNum+1):

            # 막줄이면 row 추가하고 작업.
            if no == lineNum:
                self.insertRow(self.rowCount())

            # no를 setData로 int 화 시켜줘야함. str으로 작업하면 정렬에 문제가 생김.
            nItem = QTableWidgetItem()
            nItem.setData(Qt.DisplayRole, no)
            nItem.setTextAlignment(Qt.AlignCenter)
            self.setItem(no, 0, nItem)
            self.item(no, 0).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable) # flag 옵션

            # 데이터 집어넣음.
            self.setItem(no, 1, QTableWidgetItem(self.dbrows[no-1][1]))
            self.setItem(no, 2, QTableWidgetItem(self.dbrows[no-1][2]))
            self.setItem(no, 3, QTableWidgetItem(self.dbrows[no-1][3]))
            self.setItem(no, 5, QTableWidgetItem(self.dbrows[no-1][5]))

            # chackbox 를 집어넣기 위해서는 WidgteItem 생성 이후에 작업해야함, 추가시킬때 매번 세팅 해줘야함.
            self.setItem(no, 4, QTableWidgetItem())
            # db의 내용이 1이면 체크상태, text "\0"인 이유는 정렬기준이 text이기 때문에 "" 다르게 설정.
            if self.dbrows[no-1][4] == "1":
                self.item(no, 4).setCheckState(Qt.Checked)
                self.item(no, 4).setText("\0")

            else:
                self.item(no, 4).setCheckState(Qt.Unchecked)
                self.item(no, 4).setText("")
                self.returnNum += 1 # 반납이 안된게 있다면 책대여 숫자 증가.

            # 체크박스 옵션.
            self.item(no, 4).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)

            for ct in (1, 2):
                self.item(no,ct).setTextAlignment(Qt.AlignCenter)

        # 총 row 수 가져옴.
        self.rowPosition = self.rowCount()

        # 첫줄은 제거, flag설정으로 선택불가능 하게 만들어서 마지막탭에서 처음으로 넘어가지 않게 설정.
        self.setRowHidden(0, True)
        for n in range(6):
            # 임시로 set item 함 이후에는 db에 저장됌
            self.setItem(0, n, QTableWidgetItem("#"))
            self.item(0, n).setFlags(Qt.ItemIsSelectable)

        # 제일 마지막줄 3번째 칸으로 시작.
        self.setCurrentCell(self.rowPosition-1,2)

        # cell은 빈칸까지 포함, item은 말그대로 들어있는 item만 해당
        # 책이름이 입력되는순간 rowPosition을 이용해서 추가함.
        # 셀 데이터 변경, 선택 셀 변경 시그널 연결.
        self.cellChanged.connect(self.f_addRowNum)
        self.currentCellChanged.connect(self.f_addDate)

        self.show()


    # *** 시그널 옆에 있는 파라미터는 함수정의할때 불러와서 사용 가능함 ***
    # 셀 데이터가 변경 되면 일어나는 함수
    # 모든 데이터가 변경 되면 '즉시' db의 데이터를 갱신하여 저장함.
    def f_addRowNum(self, cRow, cCol):

        # self.dbColName=["no", "date", "name", "bookname", "isreturn", "etc"]

        # 변경이 되면 setText도 함께 바뀌니까 2번의 변화가 일어남.
        # 변경되면 해당 위치 내용 db에 저장
        # 체크박스 데이터가 변경되었을때 처리하는 부분
        if cCol == 4:
            #print (self.item(cRow, cCol).checkState())

            # 변경된 데이터가 체크 해제(state: 0) 됐을때 text: ""로 변경하고 DB 데이터도 0 으로 갱신한다.
            if self.item(cRow, cCol).checkState() == 0:
                self.item(cRow, cCol).setText("")
                self.cursor.execute(
                    "update rentaldata set {0} = '{1}' where no = {2}".format
                    (self.dbColName[cCol], "0", cRow))
                self.conn.commit()
                self.returnNum += 0.5 # 변경이 되면 setText도 함께 바뀌니까 2번의 변화가 일어남. 그래서 +0.5
            # 변경된 데이터가 체크(state: 2) 됐을때 text: "\0"로 변경하고 DB 데이터도 1 으로 갱신한다.
            else: # if checkState == 2
                self.item(cRow, cCol).setText("\0")
                self.cursor.execute(
                    "update rentaldata set {0} = '{1}' where no = {2}".format
                    (self.dbColName[cCol], "1", cRow))
                self.conn.commit()
                self.returnNum -= 0.5 # 변경이 되면 setText도 함께 바뀌니까 2번의 변화가 일어남. 그래서 +0.5
                # 수정후 가운데 정렬

        # 나머지 데이터가 변경되면 즉시 DB 데이터를 갱신함.
        else:
            try:
                self.cursor.execute(
                    "update rentaldata set {0} = '{1}' where no = {2}".format
                    (self.dbColName[cCol], self.item(cRow, cCol).text(), cRow))
                self.conn.commit()
            except:
                pass

        # 마지막줄, 책이름 데이터가 변경 되었을때 줄을 추가한다.
        if self.rowPosition - 1 == self.currentRow() and cCol == 3:
            try:
                if self.item(self.rowPosition - 1, 3).text() != "":
                    # print (self.item(self.rowPosition - 1, 2).text())
                    self.insertRow(self.rowPosition)
                    # DB 데이터도 즉시 초기화.
                    self.cursor.execute("insert into rentaldata(date, name, bookname, isreturn, etc) values (?,?,?,?,?)", ("","","","0",""))
                    self.rowPosition = self.rowCount()
                    # Item 도 초기화.
                    # no 초기화
                    nItem = QTableWidgetItem()
                    nItem.setData(Qt.DisplayRole, self.rowPosition - 1)
                    nItem.setTextAlignment(Qt.AlignCenter)
                    self.setItem(self.rowPosition - 1, 0, nItem)
                    self.item(self.rowPosition - 1, 0).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

                    # 1,2,4 초기화.
                    self.setItem(self.rowPosition - 1, 1, QTableWidgetItem())
                    self.setItem(self.rowPosition - 1, 2, QTableWidgetItem())
                    self.setItem(self.rowPosition - 1, 4, QTableWidgetItem())
                    self.item(self.rowPosition - 1, 4).setCheckState(Qt.Unchecked)
                    self.item(self.rowPosition - 1, 4).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)

                    # 필요한부분 가운데 정렬
                    for ct in (1,2):
                        self.item(self.rowPosition - 1, ct).setTextAlignment(Qt.AlignCenter)
            except:
                pass

    # 마지막줄 data 셀로 이동하면 자동으로 오늘의 날짜를 채워준다.
    def f_addDate(self):
        if self.currentColumn() == 1 and self.rowPosition - 1 == self.currentRow():
            self.setItem(self.rowPosition - 1, 1, QTableWidgetItem(str(datetime.date.today())))
            self.item(self.rowPosition - 1, 1).setTextAlignment(Qt.AlignCenter)



# 유저목록 부분, 위와 유사함.
class mainWidget_user(QWidget):
    def __init__(self):
        super(mainWidget_user, self).__init__()
        self.initUI()

    def initUI(self):
        # 변수 선언.
        self.mat_list=[] # 검색 성공시 담아둘 리스트
        self.temp_mat_list= []

        # 테이블 객체 생성
        self.mtable_list = mWid_user_subTable()

        # 라벨, 버튼, 체크박스 생성
        srchLabel = QLabel("검색어", self)
        srchLabel.setFixedWidth(45)

        # 검색어 입력 칸
        self.srchWord = QLineEdit()
        self.srchWord.setFixedWidth(150)

        # 검색버튼 생성 및 단축키, 기능연결.
        srchBtn = QPushButton("검색", self)
        srchBtn.setFixedWidth(50)
        srchBtn.setShortcut(Qt.Key_Enter)
        srchBtn.clicked.connect(self.btnClickedSearch)

        # 검색 컨트롤 다이얼 설정 및 기능연결.
        self.boxSnum = QSpinBox()
        self.boxSnum.setMinimum(1)
        self.boxSnum.setMaximum(1)
        self.boxSnum.setFixedWidth(55)
        self.boxSnum.valueChanged.connect(self.f_srchIndex)

        # 책대여권수 얼마나 남았는지 체크
        self.srchResult = QLabel()

        # 레이아웃 구성.
        grid = QGridLayout()
        grid.setSpacing(10)
        self.setLayout(grid)

        grid.addWidget(srchLabel, 0, 0)
        grid.addWidget(self.srchWord, 0, 1)
        grid.addWidget(srchBtn, 0, 2)
        grid.addWidget(self.boxSnum, 0, 3)
        grid.addWidget(self.srchResult, 0, 4)
        #grid.addWidget(self.returnBook, 0, 10)
        grid.addWidget(self.mtable_list, 1, 0, 1, -1) # -1은 최대

        self.show()


    # 리사이즈 이벤트 함수 오버라이딩함.
    def resizeEvent(self, QResizeEvent):

        widSum=0
        for rs in range(4):
            #print(str(rs),self.mtable_list.columnWidth(rs))
            widSum+=self.mtable_list.columnWidth(rs)
        # 비고란의 width를 창 길이 변화마다 조절.
        self.mtable_list.setColumnWidth(4, self.mtable_list.width()-widSum-23)


    # 검색버튼 정의
    def btnClickedSearch(self):

        self.boxSnum.setValue(1)
        # 이전 검색목록은 흰색으로 변경.
        for mch in self.temp_mat_list:
            mch.setBackground(QColor(255,255,255))

        # 빈칸이면 취소
        if self.srchWord.text() == "":
            self.srchResult.setText("")
            return

        # findItems로 검색 방식 정의, 이후 결과 mat_list에 저장. QTableWidgetItem 형태로 저장됨.
        self.mat_list=self.mtable_list.findItems(self.srchWord.text(), Qt.MatchContains)


        # 검색결과가 한개라도 있다면
        if len(self.mat_list) != 0:

            # 다이얼 값 세팅
            self.boxSnum.setMaximum(len(self.mat_list))
            self.boxSnum.setFocus()
            self.srchResult.setText('''%d개 검색 ("%s")''' % (len(self.mat_list), self.srchWord.text()))

            # 검색결과 색깔 변경.
            self.temp_mat_list=self.mat_list
            for mch in self.mat_list:
                mch.setBackground(QColor(152, 173, 255))

            # 검색 후 첫번째 검색셀로 이동.
            self.mtable_list.setCurrentItem(self.mat_list[0], QItemSelectionModel.SelectCurrent)

        # 검색결과가 없으면
        else:
            QMessageBox.information(self, "검색 실패", "검색 결과가 없습니다.")


    # 다이얼 조절하면 해당 일치하는 Item Index로 이동함.
    def f_srchIndex(self,num):

        try:
            self.mtable_list.setCurrentItem(self.mat_list[num-1], QItemSelectionModel.SelectCurrent)
        except:
            pass


# 유저 테이블 위젯 클래스(위와 유사함)
class mWid_user_subTable(QTableWidget):
    def __init__(self):
        super(mWid_user_subTable, self).__init__()
        self.initUI()

    def initUI(self):
        # 변수 선언.
        self.returnNum = 0 # 책미반납개수
        # DB 이름을 쉽게 가져오기 위해 배열에 저장
        #self.dbColName=["no", "date", "name", "bookname", "isreturn", "etc"]
        self.dbColName = ["no", "name", "addr", "tel", "etc"]

        # DB 연결, table 이름 userdata, 없으면 생성.
        self.conn = sqlite3.connect('mscomics.db')
        self.cursor = self.conn.cursor()
        #self.cursor.execute("drop table userdata")
        self.cursor.execute("create table if not exists userdata(no integer primary key autoincrement, name varchar2, addr varchar2, tel varchar2, etc varchar2)")

        # DB에서 데이터 가져와서 self.dbrows에 넣음.
        self.cursor.execute("select * from userdata")
        self.dbrows = self.cursor.fetchall()

        # db 데이터가 없으면 한개 넣고 작업실행.
        if len(self.dbrows) == 0:
            self.cursor.execute("insert into userdata(name, addr, tel, etc) values (?,?,?,?)", ("", "", "", ""))
            self.conn.commit()
            self.cursor.execute("select * from userdata")
            self.dbrows = self.cursor.fetchall()

        # db데이터 row 수
        lineNum=len(self.dbrows)

        # (row,col)을  (라인 넘버, 5) 으로 set
        self.setRowCount(lineNum)
        self.setColumnCount(5)

        # 정렬 가능하게 만드는 옵션
        self.setSortingEnabled(True)
        # 헤더 설정 및 세로 헤더 안보이게 설정
        self.setHorizontalHeaderLabels(["no","이름","주소","전화번호","비고"])
        self.verticalHeader().setVisible(False)

        # 테이블 크기 조절.
        self.setColumnWidth(0, 43)
        self.setColumnWidth(1, 82)
        self.setColumnWidth(2, 351)
        self.setColumnWidth(3, 107)
        #self.setColumnWidth(4, 1)


        # DB 정보 가져와서 초기화 작업.
        for no in range(1,lineNum+1):

            # 막줄이면 row 추가하고 작업.
            if no == lineNum:
                self.insertRow(self.rowCount())

            # no를 setData로 int 화 시켜줘야함. str으로 작업하면 정렬에 문제가 생김.
            nItem = QTableWidgetItem()
            nItem.setData(Qt.DisplayRole, no)
            nItem.setTextAlignment(Qt.AlignCenter)
            self.setItem(no, 0, nItem)
            self.item(no, 0).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable) # flag 옵션

            # 데이터 집어넣음.
            self.setItem(no, 1, QTableWidgetItem(self.dbrows[no-1][1]))
            self.setItem(no, 2, QTableWidgetItem(self.dbrows[no-1][2]))
            self.setItem(no, 3, QTableWidgetItem(self.dbrows[no-1][3]))
            self.setItem(no, 4, QTableWidgetItem(self.dbrows[no-1][4]))

            for ct in (1, 2):
                self.item(no,ct).setTextAlignment(Qt.AlignCenter)

        # 총 row 수 가져옴.
        self.rowPosition = self.rowCount()

        # 첫줄은 제거, flag설정으로 선택불가능 하게 만들어서 마지막탭에서 처음으로 넘어가지 않게 설정.

        for n in range(5):
            # 임시로 set item 함 이후에는 db에 저장됌
            self.setItem(0, n, QTableWidgetItem("#"))
            self.item(0, n).setFlags(Qt.ItemIsSelectable)
        self.setRowHidden(0, True)

        # 제일 마지막줄 3번째 칸으로 시작.
        self.setCurrentCell(self.rowPosition-1,1)

        # cell은 빈칸까지 포함, item은 말그대로 들어있는 item만 해당
        # 책이름이 입력되는순간 rowPosition을 이용해서 추가함.
        # 셀 데이터 변경, 선택 셀 변경 시그널 연결.
        self.cellChanged.connect(self.f_addRowNum)

        self.show()


    # ***시그널 옆에 있는 파라미터는 함수정의할때 불러와서 사용 가능함***
    # 셀 데이터가 변경 되면 일어나는 함수
    # 모든 데이터가 변경 되면 '즉시' db의 데이터를 갱신하여 저장함.
    def f_addRowNum(self, cRow, cCol):

        # self.dbColName=["no", "date", "name", "bookname", "isreturn", "etc"]

        # 변경이 되면 setText도 함께 바뀌니까 2번의 변화가 일어남.
        # 변경되면 해당 위치 내용 db에 저장
        # 체크박스 데이터가 변경되었을때 처리하는 부분

        try:
            self.cursor.execute(
                "update userdata set {0} = '{1}' where no = {2}".format
                (self.dbColName[cCol], self.item(cRow, cCol).text(), cRow))
            self.conn.commit()
        except Exception as e:
            #("1",e)
            pass

        # 마지막줄, 책이름 데이터가 변경 되었을때 줄을 추가한다.
        if self.rowPosition - 1 == self.currentRow() and cCol == 3:
            try:
                if self.item(self.rowPosition - 1, 3).text() != "":
                    # print (self.item(self.rowPosition - 1, 2).text())
                    self.insertRow(self.rowPosition)
                    # DB 데이터도 즉시 초기화.
                    self.cursor.execute("insert into userdata(name, addr, tel, etc) values (?,?,?,?)", ("","","",""))
                    self.rowPosition = self.rowCount()
                    # Item 도 초기화.
                    # no 초기화
                    nItem = QTableWidgetItem()
                    nItem.setData(Qt.DisplayRole, self.rowPosition - 1)
                    nItem.setTextAlignment(Qt.AlignCenter)
                    self.setItem(self.rowPosition - 1, 0, nItem)
                    self.item(self.rowPosition - 1, 0).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

                    # 1,2,4 초기화.
                    self.setItem(self.rowPosition - 1, 1, QTableWidgetItem())
                    self.setItem(self.rowPosition - 1, 2, QTableWidgetItem())

                    # 필요한부분 가운데 정렬
                    for ct in (1,2):
                        self.item(self.rowPosition - 1, ct).setTextAlignment(Qt.AlignCenter)
            except Exception as e:
                #print("2",e)
                pass


# main, 앱 생성
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(app.exec_())