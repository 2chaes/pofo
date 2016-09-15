import sys
import _thread
import time
import re
import sqlite3

import encodings.idna # 쓰레드할때 필요함.
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
import webbrowser


# 뉴스 파싱 프로그램
# 숫자 하나당 15개씩 최근 기사를 가져온다.
class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

        
    def initUI(self):
        # 변수 선언.
        self.searchword=""
        self.th_num=1
        self.th_done=0
        self.name_temp_addr=[[],[]]
        self.name_addr=[[],[]]
        self.lasttempnum=0
        self.conn = sqlite3.connect('news.db')
        self.cursor = self.conn.cursor()

        # 라벨, 버튼, 체크박스 생성
        titleLabel = QLabel("검색어", self)
        searchbtn = QPushButton("검색", self)
        contentLabel = QLabel("내용", self)
        self.resetcb = QCheckBox('초기화', self)

        # 버튼 기능 정의
        searchbtn.setShortcut(Qt.Key_Enter)
        searchbtn.clicked.connect(self.btnClickedSearch)


        # stat bar 생성
        self.stat = QStatusBar()
        self.stat.showMessage('Ready')

        
        self.titleEdit = QLineEdit() # 검색어 입력 칸
        self.search_list = QListWidget() # 리스트 출력 위젯
        self.search_list.itemDoubleClicked.connect(self.listClicked) # 리스트 더블클릭 기능 정의.

        # 검색 수 선택 박스.
        self.boxSnum = QSpinBox()
        self.boxSnum.setMinimum(1)
        self.boxSnum.setMaximum(267)

        # 레이아웃 구성.
        grid = QGridLayout()
        grid.setSpacing(10)
        self.setLayout(grid)
        grid.addWidget(titleLabel, 0, 0)
        grid.addWidget(self.titleEdit, 0, 1)
        grid.addWidget(self.resetcb, 0, 2)
        grid.addWidget(self.boxSnum, 0, 3)
        grid.addWidget(searchbtn, 0, 4)
        
        grid.addWidget(contentLabel, 1, 0)
        grid.addWidget(self.search_list, 1, 1, 1, 4)
        grid.addWidget(self.stat, 3, 0, -1, -1)
        
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle('News Parse')

        self.show()


    def btnClickedSearch(self):
        
        self.stat.showMessage('Searching...')
        self.searchword=""                
        self.searchword=urllib.request.pathname2url(self.titleEdit.text()) # 검색어 인코딩

        # 빈칸 체크
        if len(self.searchword) == 0:
            self.stat.showMessage('Empty')
            return


        self.search_list.clear() # 리스트 초기화

        # 초기화 체크 되어있으면 drop table
        if self.resetcb.isChecked():
            try:
                self.cursor.execute("drop table {0}".format(self.titleEdit.text().strip().replace(" ", "_")))
            except:
                QMessageBox.information(self, "검색기록 없음", "초기화 할 수 없는 검색어 입니다.")

        # 검색어 테이블이 있으면 이용 없으면 만듬.
        self.cursor.execute("create table if not exists {0}(num integer primary key autoincrement, title varchar2, newsaddr varchar2)".format(self.titleEdit.text().strip().replace(" ","_")))
        

        # 배열 초기화
        self.name_addr=[[],[]]
        
        # 데이터 가져와서 역순으로 배열에 넣음.
        self.cursor.execute("select num, title, newsaddr from {0}".format(self.titleEdit.text().strip().replace(" ","_")))
        self.rows = self.cursor.fetchall()
        
        for row in reversed(self.rows):
            self.name_addr[0].append(row[1])
            self.search_list.addItem(row[1])
            self.name_addr[1].append(row[2])

        # 쓰레드 처리 영역.
        self.th_num=1
        self.th_done=0
        for num in range(1,self.boxSnum.value()+1):
            _thread.start_new_thread(self.th_urllib, (num,))
            #time.sleep(0.5)
        
        # if thread 처리가 끝나면 넘어감.
        while self.th_done < 1: pass

        # 새로 갱신된다면 이전 리스트들은 다시 흰색
        #for setcol in range(self.lasttempnum):
        for setcol in range(len(self.name_addr[0])):
            self.search_list.item(setcol).setBackground(QColor(255,255,255))    

        # db에 검색결과를 역순으로 추가한다
        # db에 저장되는순서는 1. 이전날짜 ... 끝. 최신날짜
        # 리스트에 저장되고 출력되는 순서는 1. 최신날짜 ... 끝. 이전날짜
        for dbnum in reversed(range(len(self.name_temp_addr[0]))):
            self.cursor.execute("insert into {0}(title, newsaddr) values (?, ?)".format(self.titleEdit.text().strip().replace(" ","_")), (self.name_temp_addr[0][dbnum], self.name_temp_addr[1][dbnum]))
        
        self.conn.commit() # 커밋 한다

        # 이게 있어야 클릭 순서가 맞춰짐
        # 더블클릭 함수쪽에서 db숫자로 접근하면 문제 해결 가능함
        self.name_addr[0]=self.name_temp_addr[0]+self.name_addr[0]
        self.name_addr[1]=self.name_temp_addr[1]+self.name_addr[1]

        # 리스트에 name_temp_addr을 추가
        self.search_list.insertItems(0, self.name_temp_addr[0])

        # 추가된 개수만큼 리스트의 컬러를 변경        
        for setcol in range(len(self.name_temp_addr[0])):
            self.search_list.item(setcol).setBackground(QColor(152,173,255))

        # 이전에 얼마나 검색됐나 확인하는 변수
        self.lasttempnum=len(self.name_temp_addr[0])

        if self.th_done==2: # self.th_done이 1이면 검색완료, 2면 검색결과가 없음. (th1번에서 0개 검색)
            QMessageBox.information(self, "검색결과 없음", "없엉ㅋ")


        # 다시 토글시켜줌
        if self.resetcb.isChecked(): self.resetcb.toggle()
        
        self.stat.showMessage('Done. adds {0}'.format(len(self.name_temp_addr[0])))
        self.name_temp_addr=[[],[]] # temp 초기화

        
    def listClicked(self, item):
        webbrowser.open(self.name_addr[1][self.search_list.currentRow()])

    # 쓰레드 영역으로 처리하는 함수
    # 숫자 10을 입력했다면 10개의 페이지에서 15개씩, 총 150개를 가져와야 하므로
    # 각각의 페이지를 쓰레드를 활용해서 한꺼번에 연다음 순서에 맞게 정리한다.
    def th_urllib(self, num):

        # 검색어로 검색.
        calhtml = urlopen('https://m.search.naver.com/search.naver?where=m_news&query='+self.searchword+'&sort=1&start='+str((num-1)*15+1))
        #soup = BeautifulSoup(calhtml, 'lxml')
        soup = BeautifulSoup(calhtml.read(), "html.parser")
        soupnews = soup.find(class_='lst_news').find_all(class_='api_bx')

        # 검색어가 없다면 th_done=2 하고 반환
        if len(soupnews) == 0:
            if num == 1:
                self.th_done = 2
            return
        
        # 이전단계가 끝나면 시행함.
        while self.th_num != num:
            if self.th_done == 1 : return

        check=0
        for newsn in soupnews:
            # 같은 주소가 리스트에 존재하면 탈출
            if newsn.a.get('href') in self.name_addr[1]:
                check=1
                break
            # 검색 결과를 배열에 넣음
            self.name_temp_addr[0].append(newsn.find(class_='tit_headline').get_text())
            self.name_temp_addr[1].append(newsn.a.get('href'))

        # 검색체크 개수에 쓰레드를 다 시행하거나, 같은 주소가 있거나, 검색 개수가 15개 미만이면 쓰레드 종료를 알려준다
        if self.th_num == self.boxSnum.value() or check==1 or len(self.name_temp_addr[0]) < 15:
            self.th_done = 1
            time.sleep(1)
        
        # 단계가 끝났다고 변수에 +1함
        self.th_num+=1
    

def main():
    app = QApplication(sys.argv)
    ex = Example()
    #app.exec_()
        
    sys.exit(app.exec_())

 
if __name__ == '__main__':
    main()
