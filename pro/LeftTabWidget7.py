#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import csv
import requests
import pymysql
import dbcnn
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class LeftTabWidget(QWidget):
    '''左侧选项栏'''
    def __init__(self):
        super(LeftTabWidget, self).__init__()
        self.labels=self.__dict__
        self.pushButtons=self.__dict__
        self.conn=pymysql.connect(
            host=dbcnn.host,
            port=dbcnn.port,
            user=dbcnn.user,
            passwd=dbcnn.passwd,
            db=dbcnn.db,
            charset=dbcnn.charset,
            )
        self.cur=self.conn.cursor()
        self.aa=b'GIF89a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00\x00\x01\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02L\x01\x00;'

        self.setObjectName('LeftTabWidget')
        self.setWindowTitle('LeftTabWidget')
        with open('QListWidgetQSS.qss', 'r') as f:   #导入QListWidget的qss样式
            self.list_style = f.read()

        self.main_layout = QHBoxLayout(self, spacing=0)     #窗口的整体布局
        self.main_layout.setContentsMargins(0,0,0,0)

        self.left_widget = QListWidget()     #左侧选项列表
        self.left_widget.setStyleSheet(self.list_style)
        self.main_layout.addWidget(self.left_widget)

        self.right_widget = QStackedWidget()
        self.main_layout.addWidget(self.right_widget)
        self._setup_ui(self)

    def _setup_ui(self,LWindow):
        '''加载界面ui'''

        self.left_widget.currentRowChanged.connect(self.right_widget.setCurrentIndex)   #list和右侧窗口的index对应绑定

        self.left_widget.setFrameShape(QListWidget.NoFrame)    #去掉边框

        self.left_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  #隐藏滚动条
        self.left_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 首页
        self.item = QListWidgetItem('首页',self.left_widget)   #左侧选项的添加
        self.item.setSizeHint(QSize(30,60))
        self.item.setTextAlignment(Qt.AlignCenter)
        
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")
        # Grid layout
        self.grid = QGridLayout()
        self.grid.setObjectName("gridLayout")
        self.grid.setSpacing(5)
        # search icon
        self.label = QLabel()
        self.label.setTextFormat(Qt.AutoText)
        self.label.setPixmap(QPixmap("search.ico").scaled(15,15))
        self.label.setObjectName("label")
        self.grid.addWidget(self.label, 2, 1)
        # search box
        self.lineEdit = QLineEdit()
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        #self.lineEdit.setPlaceholderText("用户名")
        self.grid.addWidget(self.lineEdit, 2, 2, 1, 4)
        # search button
        self.pushButton = QPushButton()
        self.pushButton.setObjectName("pushButton")
        #self.pushButton.setIcon(QIcon(QPixmap('login.png').scaled(210,30)))
        #self.pushButton.setStyleSheet("QPushButton{border-image: url(login.png)}")
        self.pushButton.setStyleSheet("border:none;") # no border 
        self.pushButton.clicked.connect(self.book_search)
        self.grid.addWidget(self.pushButton, 2,6)
        # save button
        self.pushButton1 = QPushButton()
        self.pushButton1.setObjectName("pushButton")
        #self.pushButton.setIcon(QIcon(QPixmap('login.png').scaled(210,30)))
        #self.pushButton.setStyleSheet("QPushButton{border-image: url(login.png)}")
        self.pushButton1.setStyleSheet("border:none;") # no border 
        self.pushButton1.clicked.connect(self.search_out)
        self.grid.addWidget(self.pushButton1, 2,7)
        #self.setLayout(self.grid)
        # sub title
        self.labelt = QLabel()
        self.labelt.setText('————今日推荐————')
        #self.labelt.setTextFormat(Qt.AutoText)
        #self.labelt.setPixmap(QPixmap("search.ico").scaled(15,15))
        self.labelt.setObjectName("labelt")
        self.grid.addWidget(self.labelt, 4, 5,1,2)
        # get 8 best book
        self.sqlstring='''select bx_book_ratings.ISBN,
                avg(Book_rating) as rat,Book_title,Book_author,
                Year_of_publication,Publisher,Image_URL_L
            from bx_book_ratings,bx_books 
            where bx_book_ratings.ISBN=bx_books.ISBN and Book_rating>0
            group by bx_book_ratings.ISBN
            order by avg(Book_rating) desc,Year_of_publication desc 
            limit 20'''
        self.cur.execute(self.sqlstring)
        self.conn.commit()
        bb=self.cur.fetchall()
        bbs=[]
        for m in range(20):
            if not self.get_picture(bb[m][-1])==self.aa:
                if len(bbs)<8:
                    bbs.append(bb[m])
        # bookboxs
        self.labels=locals()
        for i in range(8):
            pict=self.get_picture(bbs[i][-1])
            img = QImage.fromData(pict)
            self.labels['label'+str(i)]=QLabel()
            self.labels['label'+str(i)].setVisible(True)
            self.labels['label'+str(i)].setTextFormat(Qt.AutoText)
            #self.labels['label'+str(i)].setPixmap(QPixmap.fromImage(img).scaled(150,200))
            if not pict==self.aa:
                self.labels['label'+str(i)].setPixmap(QPixmap.fromImage(img))
            else:
                self.labels['label'+str(i)].setText('抱歉，没有图片！')
            self.labels['label'+str(i)].setObjectName("label%s"%str(i))
            bi = (bbs[i][2],bbs[i][1],bbs[i][0],bbs[i][3],bbs[i][4],bbs[i][5])
            self.labels['label'+str(i)].setToolTip('书名：%s\n评分：%s\nISBN：%s\n作者：%s出版年：%s\n出版商：%s'%bi)
            #self.pushButtons['psb'+str(i)]= QPushButton()
            #self.pushButtons['psb'+str(i)].setObjectName("psb%s"%i)
            #self.pushButtons['psb'+str(i)].setText("我要评论")
            #self.pushButtons['psb'+str(i)].setStyleSheet("border:none;")
            #self.pushButtons['psb'+str(i)].clicked.connect(self.book_rating)
            self.grid.addWidget(self.labels['label'+str(i)], pow((int(i/4)+2),2)+2,3*(i%4),4,3)
            #self.grid.addWidget(self.pushButtons['psb'+str(i)], pow((int(i/4)+2),2)+5,3*(i%4),1,3)
        self.centralwidget.setWindowFlags(Qt.FramelessWindowHint)#Delete title and frame
        self.centralwidget.setStyleSheet("background-color:white;")
        self.centralwidget.setLayout(self.grid)
        self.right_widget.addWidget(self.centralwidget)
        
        #评论
        self.item = QListWidgetItem('评论',self.left_widget)   #左侧选项的添加
        self.item.setSizeHint(QSize(30,60))
        self.item.setTextAlignment(Qt.AlignCenter)
        self.centralwidget1 = QWidget()
        self.centralwidget1.setObjectName("centralwidget1")
        # Grid layout
        self.grid1 = QGridLayout()
        self.grid1.setObjectName("gridLayout1")
        self.grid1.setSpacing(5)
        # user Icon
        self.label_o = QLabel()
        self.label_o.setTextFormat(Qt.AutoText)
        #self.label_o.setPixmap(QPixmap("book.png").scaled(15,15))
        self.label_o.setPixmap(QPixmap("book.png"))
        self.label_o.setObjectName("label_o")
        self.grid1.addWidget(self.label_o, 2, 1)
        # user input
        self.lineEdit_0 = QLineEdit()
        self.lineEdit_0.setText("")
        self.lineEdit_0.setObjectName("lineEdit_0")
        #self.lineEdit.setPlaceholderText("请输入帐号")
        self.grid1.addWidget(self.lineEdit_0, 2, 2, 1, 4)
        # password Icon
        self.label_2 = QLabel()
        self.label_2.setTextFormat(Qt.AutoText)
        self.label_2.setPixmap(QPixmap("score.png"))
        self.label_2.setObjectName("label_2")
        self.grid1.addWidget(self.label_2, 4, 1)
        # password input 
        self.lineEdit_2 = QLineEdit()
        self.lineEdit_2.setText("")
        #self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        #self.lineEdit_2.setPlaceholderText( "请输入密码")
        self.grid1.addWidget(self.lineEdit_2, 4, 2, 1, 4)
        # login button
        self.pushButton_0 = QPushButton()
        self.pushButton_0.setObjectName("pushButton_0")
        #self.pushButton.setIcon(QIcon(QPixmap('login.png').scaled(210,30)))
        #self.pushButton.setStyleSheet("QPushButton{border-image: url(login.png)}")
        self.pushButton_0.setStyleSheet("border:none;") # no border 
        self.pushButton_0.clicked.connect(self.word_get)
        self.grid1.addWidget(self.pushButton_0, 6,1,1,5)
        self.centralwidget1.setWindowFlags(Qt.FramelessWindowHint)#Delete title and frame
        self.centralwidget1.setStyleSheet("background-color:white;")
        self.centralwidget1.setLayout(self.grid1)
        self.right_widget.addWidget(self.centralwidget1)       
        self.retranslateUi(LWindow)
        QMetaObject.connectSlotsByName(LWindow)
    def retranslateUi(self, LWindow):
        _translate = QCoreApplication.translate
        self.lineEdit.setPlaceholderText(_translate("LWindow", "请输入书名、作者、出版商、出版年或ISBN等"))
        self.pushButton.setText(_translate("LWindow", "立即搜索"))
        self.pushButton1.setText(_translate("LWindow", "保存搜索结果"))

        #self.label_0.setText(_translate("diglog", "用户评价"))
        self.lineEdit_0.setPlaceholderText(_translate("diglog", "请输入书目的ISBN"))
        self.lineEdit_2.setPlaceholderText(_translate("diglog", "请输入评分1-10"))
        self.pushButton_0.setText(_translate("diglog", "提交评分"))
        #self.pushButton_2.setText(_translate("diglog", "注册"))
    def book_search(self):
        self.fo=None
        wo=self.lineEdit.text()

        if wo:
            if wo.isdigit() and len(wo)==4:
                self.sqlstring='''select bx_book_ratings.ISBN,
                        avg(Book_rating),Book_title,Book_author,
                        Year_of_publication,Publisher,Image_URL_L
                    from bx_book_ratings,bx_books 
                    where bx_book_ratings.ISBN=bx_books.ISBN and Book_rating>0
                        and Year_of_publication='%s'
                    group by bx_book_ratings.ISBN
                    order by avg(Book_rating) desc,Year_of_publication desc
                    limit 10000'''%(wo)
                    #"select * from bx_books where Year_of_publication='%d' or ISBN='%d'"%(int(wo),int(wo))
            else:
                self.sqlstring= '''select bx_book_ratings.ISBN,
                        avg(Book_rating) as rat,Book_title,Book_author,
                        Year_of_publication,Publisher,Image_URL_L
                    from bx_book_ratings,bx_books
                    where bx_book_ratings.ISBN=bx_books.ISBN and Book_rating>0
                        and (Book_title like '%s' or Book_author like '%s' 
                        or Year_of_publication like '%s' or bx_books.ISBN like'%s')
                    group by bx_book_ratings.ISBN
                    order by avg(Book_rating) desc,Year_of_publication desc
                    limit 10000'''%(('%'+wo+'%'),('%'+wo+'%'),('%'+wo+'%'),('%'+wo+'%'))
                # "select * from bx_books where Book_title='%s' or Book_author='%s' or Publisher='%s'"%(wo,wo)
            self.cur.execute(self.sqlstring)
            self.conn.commit()
            self.fo=self.cur.fetchall()
            self.labelt.setVisible(False)
            print(self.fo)
            if self.fo:
                if len(self.fo)>=8:
                    for j in range(8):
                        picts=self.get_picture(self.fo[j][-1])
                        nimg = QImage.fromData(picts)
                        #self.labels['label'+str(j)].setPixmap(QPixmap.fromImage(nimg))
                        if not picts==self.aa:
                            self.labels['label'+str(j)].setPixmap(QPixmap.fromImage(nimg))
                        else:
                            self.labels['label'+str(j)].setText('抱歉，没有图片！')
                        bis = (self.fo[j][2],self.fo[j][1],self.fo[j][0],self.fo[j][3],self.fo[j][4],self.fo[j][5])
                        self.labels['label'+str(j)].setToolTip('书名：%s\n评分：%s\nISBN：%s\n作者：%s出版年：%s\n出版商：%s'%bis)
                        print('get book: %s'%bis[0])
                else:
                    for j in range(len(self.fo)):
                        picts=self.get_picture(self.fo[j][-1])
                        nimg = QImage.fromData(picts)
                        self.labels['label'+str(j)].setPixmap(QPixmap.fromImage(nimg))
                        if not picts==self.aa:
                            self.labels['label'+str(j)].setPixmap(QPixmap.fromImage(nimg))
                        else:
                            self.labels['label'+str(j)].setText('抱歉，没有图片！')
                        bis = (self.fo[j][2],self.fo[j][1],self.fo[j][0],self.fo[j][3],self.fo[j][4],self.fo[j][5])
                        self.labels['label'+str(j)].setToolTip('书名：%s\n评分：%s\nISBN：%s\n作者：%s出版年：%s\n出版商：%s'%bis)
                        print('get book: %s'%bis[0])              
                    for k in range(len(self.fo),8):
                        self.labels['label'+str(k)].setVisible(False)
                        #self.pushButtons['psb'+str(k)].setVisible(False)
            else:
                QMessageBox.warning(self,
                     "抱歉",
                     "没有搜索到您要的书",
                     QMessageBox.Yes)
                self.lineEdit.setFocus()
    
    def get_picture(self,url):
        req=requests.get(url)
        if req.content[:3]=='GIF':
            print(req.content)
        return req.content
    def search_out(self):
        filename=QFileDialog.getSaveFileName(self,"保存结果","C:/","CSV Files (*.csv)")
        print(filename)
        if filename[0]:
            with open(filename[0],'a+',newline='',encoding='utf-8-sig') as f:
                headers = ['ISBN', '评分', '书名', '作者', '出版年', '出版商','封面']
                f_csv = csv.writer(f)
                f_csv.writerow(headers)
                f_csv.writerows(self.fo)
    def word_get(self):
        self.ISBN = self.lineEdit_0.text()
        self.rating = self.lineEdit_2.text()
        if self.ISBN and self.rating:
            if self.rating.isdigit() and int(self.rating) in range(1,11):
                self.fsqlstring="select * from bx_books where ISBN='%s';"%self.ISBN
                self.cur.execute(self.fsqlstring)
                self.conn.commit()
                book_exst=self.cur.fetchall()
                if book_exst:
                    import imp
                    imp.reload(dbcnn)
                    if dbcnn.login:
                        print('rating')
                        #result =ratMain.rating_result()
                        self.rsqlstring="select User_id from bx_users where Name='%s'"%dbcnn.login
                        self.cur.execute(self.rsqlstring)
                        self.conn.commit()
                        sqlout=self.cur.fetchall()
                        if sqlout:
                            usqid=int(sqlout[0][0])
                            self.sqlstring="insert into bx_ratings(User_id,ISBN,Book_rating) values('%d','%s','%d');"%(usqid,self.ISBN,int(self.rating))
                            self.cur.execute(self.sqlstring)
                            self.conn.commit()
                            return (self.ISBN,self.rating)
                    else:
                        QMessageBox.warning(self,
                                "警告",
                                "登录之后才能评论！",
                                QMessageBox.Yes)
                else:
                    QMessageBox.warning(self,
                        "警告",
                        "ISBN输入错误！",
                        QMessageBox.Yes)
                    self.lineEdit_0.setFocus()
            else:
                QMessageBox.warning(self,
                    "警告",
                    "请输入正确的评分(1-10)！",
                    QMessageBox.Yes)
                self.lineEdit_2.setFocus()
        else:
            QMessageBox.warning(self,
                    "警告",
                    "请输入ISBN和评分",
                    QMessageBox.Yes)
            self.lineEdit_0.setFocus()
        # def book_rating(self):

def main():
    app = QApplication(sys.argv)
    main_wnd = LeftTabWidget()
    main_wnd.show()
    app.exec()

if __name__ == '__main__':
    main()