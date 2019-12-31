# -*- coding:utf-8 -*-
import pymysql
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtWidgets import QWidget,QDialog,QGridLayout,QMessageBox
from PyQt5.QtWidgets import QLabel,QPushButton,QLineEdit,QMainWindow
from PyQt5.QtCore import Qt,QCoreApplication,QMetaObject
from register7 import *
import dbcnn

class MainForm(QDialog):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.havelogin=False
        self.login_user='False'
        self.setupUi(self)
        self.retranslateUi(self)
        

    def setupUi(self,diglog):
        self.setWindowTitle("DataDialog")
        self.resize(300,200)
        #self.centralWidget = QWidget(self)
        #self.centralWidget.setObjectName("centralWidget")
        #self.centralWidget.resize(700, 900)
        # glide layout
        #self.grid = QGridLayout(self.centralWidget)
        #self.resize(700, 900)
        #self.setObjectName("centralWidget")
        self.grid = QGridLayout()
        self.grid.setObjectName("gridLayout")
        self.grid.setSpacing(5)
        self.setLayout(self.grid)
        #Delete title and frame
        self.setWindowFlags(Qt.FramelessWindowHint)
        #self.setStyleSheet("background-color:white;")        
        # title
        self.label0 = QLabel()
        self.label0.setObjectName("label0")
        #self.label0.setText("用户登录")
        self.label0.setTextFormat(Qt.AutoText)
        self.label0.setStyleSheet("border:none;") # no border   
        self.grid.addWidget(self.label0, 1, 0, 1, 2)
        # close button
        self.buttonClose = QPushButton('×')
        #self.buttonClose.setIcon(QIcon(QPixmap('close.ico')))
        #self.buttonClose.setIconSize(20, 20)
        self.buttonClose.setObjectName('buttonClose')
        #self.buttonClose.setStyleSheet("border:none;") # no border
        self.buttonClose.clicked.connect(self.close)
        self.grid.addWidget(self.buttonClose, 1,6)
        # user Icon
        self.label = QLabel()
        self.label.setTextFormat(Qt.AutoText)
        self.label.setPixmap(QPixmap("user.ico").scaled(15,15))
        self.label.setObjectName("label")
        self.grid.addWidget(self.label, 3, 1)
        # user input
        self.lineEdit = QLineEdit()
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        #self.lineEdit.setPlaceholderText("请输入帐号")
        self.grid.addWidget(self.lineEdit, 3, 2, 1, 4)
        # password Icon
        self.label2 = QLabel()
        self.label2.setTextFormat(Qt.AutoText)
        self.label2.setPixmap(QPixmap("password.ico").scaled(15,15))
        self.label2.setObjectName("label2")
        self.grid.addWidget(self.label2, 4, 1)
        # password input 
        self.lineEdit_2 = QLineEdit()
        self.lineEdit_2.setText("")
        #self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        #self.lineEdit_2.setPlaceholderText( "请输入密码")
        self.grid.addWidget(self.lineEdit_2, 4, 2, 1, 4)
        # login button
        self.pushButton = QPushButton()
        self.pushButton.setObjectName("pushButton")
        #self.pushButton.setIcon(QIcon(QPixmap('login.png').scaled(210,30)))
        #self.pushButton.setStyleSheet("QPushButton{border-image: url(login.png)}")
        self.pushButton.setStyleSheet("border:none;") # no border 
        self.pushButton.clicked.connect(self.word_get)
        self.grid.addWidget(self.pushButton, 7,1,1,5)       
        # signup button
        self.pushButton_2 = QPushButton()
        self.pushButton_2.setObjectName("pushButton_2")
        #self.pushButton_2.setText('注册')
        self.pushButton_2.setStyleSheet("border:none;") # no border 
        self.pushButton_2.clicked.connect(self.signclick)
        self.grid.addWidget(self.pushButton_2,9,4,1,2)
        
        self.retranslateUi(diglog)
        QMetaObject.connectSlotsByName(diglog)
    def retranslateUi(self, diglog):
        _translate = QCoreApplication.translate
        self.label0.setText(_translate("diglog", "用户登录"))
        self.lineEdit.setPlaceholderText(_translate("diglog", "请输入用户名或邮箱"))
        self.lineEdit_2.setPlaceholderText(_translate("diglog", "请输入密码"))
        self.pushButton.setText(_translate("diglog", "立即登录"))
        self.pushButton_2.setText(_translate("diglog", "注册"))
    
    def word_get(self):
        self.login_user = self.lineEdit.text()
        self.login_password = self.lineEdit_2.text()
        self.conn=pymysql.connect(
            host=dbcnn.host,
            port=dbcnn.port,
            user=dbcnn.user,
            passwd=dbcnn.passwd,
            db=dbcnn.db,
            charset=dbcnn.charset,
        )
        self.cur=self.conn.cursor()
        tu = (self.login_password,self.login_user,self.login_user)
        self.sqlstring="select Name from bx_users where Pass_word='%s' and (Name='%s' or Email='%s');"%tu
        self.cur.execute(self.sqlstring)
        self.conn.commit()
        usr_exst=self.cur.fetchall()
        print(usr_exst)
        #if login_user == 'admin' and login_password == '123456':
        if usr_exst:
            self.login_user=usr_exst[0][0]
            self.havelogin=True
            self.write_login(s=self.login_user)
            self.close()
        else:
            self.havelogin=False
            QMessageBox.warning(self,
                    "警告",
                    "用户名或密码错误！",
                    QMessageBox.Yes)
            self.lineEdit.setFocus()
        self.conn.close()
    @staticmethod
    def logresult():
        dialog = MainForm()
        runlog = dialog.exec()
        #runlog = dialog.show()
        result = dialog.havelogin
        u=dialog.login_user
        return (result,u)
    def signclick(self):
        signdialog = signMainForm()
        runlog = signdialog.exec()
    def write_login(self,s='False'):
        with open('dbcnn.py','r') as f:
            dbb = f.readlines()
            dblines=(dbb[:6])+["login='"+s+"'"]
            print(dbb[:6])
        with open('dbcnn.py','w') as fw:           
            fw.writelines(dblines)
        return
            