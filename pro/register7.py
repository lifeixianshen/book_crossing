# -*- coding:utf-8 -*-
import time
import re
import pymysql
from xpinyin import Pinyin
from PyQt5.QtGui import QIcon,QPixmap,QPalette
from PyQt5.QtWidgets import QWidget,QDialog,QGridLayout,QMessageBox,QComboBox
from PyQt5.QtWidgets import QLabel,QPushButton,QLineEdit,QMainWindow
from PyQt5.QtCore import Qt,QCoreApplication,QMetaObject,QVariant,QSize
from area import dictPorovince, dictCity
import dbcnn

class signMainForm(QDialog):

    def __init__(self, parent=None):
        super(signMainForm, self).__init__(parent)
        self.havelogin=False
        self.conn=pymysql.connect(
            host=dbcnn.host,
            port=dbcnn.port,
            user=dbcnn.user,
            passwd=dbcnn.passwd,
            db=dbcnn.db,
            charset=dbcnn.charset,
        )
        self.py=Pinyin()
        self.sign_user=None
        self.pe = QPalette()
        self.pe.setColor(QPalette.WindowText,Qt.red)
        self.setupUi(self)
        self.retranslateUi(self)
        self.add_ress()

    def setupUi(self,signlog):
        self.setWindowTitle("DataDialog")
        self.resize(300,300)
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
        #self.label0.setText("用户注册")
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
        #self.grid.addWidget(self.buttonClose, 1,11)
        self.grid.addWidget(self.buttonClose, 1,8)
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
        #self.lineEdit.setPlaceholderText("用户名")
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
        #self.lineEdit_2.setPlaceholderText( "密码")
        self.grid.addWidget(self.lineEdit_2, 4, 2, 1, 4)
        #E-mail Icon
        self.label3 = QLabel()
        self.label3.setTextFormat(Qt.AutoText)
        self.label3.setPixmap(QPixmap("email.ico").scaled(15,15))
        self.label3.setObjectName("label3")
        self.grid.addWidget(self.label3, 7, 1)
        #E-mail
        self.lineEdit_3 = QLineEdit()
        self.lineEdit_3.setText("")
        #self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.lineEdit_3.setObjectName("lineEdit_3")
        #self.lineEdit_3.setPlaceholderText( "E-mail")
        self.grid.addWidget(self.lineEdit_3, 7, 2, 1, 4)
        #Adress Icon
        self.label4 = QLabel()
        self.label4.setTextFormat(Qt.AutoText)
        self.label4.setPixmap(QPixmap("adress.ico").scaled(15,15))
        self.label4.setObjectName("label4")
        self.grid.addWidget(self.label4, 5, 1)
        #Adress
        self.label_province = QLabel()
        self.label_province.setObjectName("label_province")
        self.grid.addWidget(self.label_province,5,2)
        self.comboBox_province = QComboBox()
        self.comboBox_province.setMinimumSize(QSize(120, 0))
        self.comboBox_province.setObjectName("comboBox_province")
        self.comboBox_province.addItem("")
        #self.grid.addWidget(self.comboBox_province,5,3,1,2)
        self.grid.addWidget(self.comboBox_province,5,3)
        self.label_city = QLabel()
        self.label_city.setObjectName("label_city")
        #self.grid.addWidget(self.label_city,5,5)
        self.grid.addWidget(self.label_city,5,4)
        self.comboBox_city = QComboBox()
        self.comboBox_city.setMinimumSize(QSize(120, 0))
        self.comboBox_city.setObjectName("comboBox_city")
        self.comboBox_city.addItem("")
        #self.grid.addWidget(self.comboBox_city,5,6,1,2)
        self.grid.addWidget(self.comboBox_city,5,5)
        self.labelp = QLabel()
        self.labelp.setTextFormat(Qt.AutoText)
        self.labelp.setPalette(self.pe)
        #self.labelp.setPixmap(QPixmap("age.ico").scaled(15,15))
        self.labelp.setObjectName("labelp")
        #self.grid.addWidget(self.labelp, 5, 8,1,2)
        self.grid.addWidget(self.labelp, 5, 6)
        #Age Icon
        self.label5 = QLabel()
        self.label5.setTextFormat(Qt.AutoText)
        self.label5.setPixmap(QPixmap("age.ico").scaled(15,15))
        self.label5.setObjectName("label5")
        self.grid.addWidget(self.label5, 6, 1)
        #Age
        self.lineEdit_5 = QLineEdit()
        self.lineEdit_5.setText("")
        #self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.lineEdit_5.setObjectName("lineEdit_4")
        #self.lineEdit_3.setPlaceholderText( "E-mail")
        self.grid.addWidget(self.lineEdit_5, 6, 2, 1, 4)
        # send 
        self.pushButton0 = QPushButton()
        self.pushButton0.setObjectName("pushButton0")
        #self.pushButton.setIcon(QIcon(QPixmap('login.png').scaled(210,30)))
        #self.pushButton.setStyleSheet("QPushButton{border-image: url(login.png)}")
        self.pushButton0.setStyleSheet("border:none;") # no border 
        self.pushButton0.clicked.connect(self.click_send)
        self.grid.addWidget(self.pushButton0, 7,7,1,2)
        # Code Icon
        self.label6 = QLabel()
        self.label6.setTextFormat(Qt.AutoText)
        self.label6.setPixmap(QPixmap("code.ico").scaled(15,15))
        self.label6.setObjectName("label6")
        self.grid.addWidget(self.label6, 8, 1)        
        # Code
        self.lineEdit_6 = QLineEdit()
        self.lineEdit_6.setText("")
        #self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.lineEdit_6.setObjectName("lineEdit_6")
        #self.lineEdit_3.setPlaceholderText( "E-mail")
        self.grid.addWidget(self.lineEdit_6, 8, 2, 1, 4)
        # login button
        self.pushButton = QPushButton()
        self.pushButton.setObjectName("pushButton")
        #self.pushButton.setIcon(QIcon(QPixmap('login.png').scaled(210,30)))
        #self.pushButton.setStyleSheet("QPushButton{border-image: url(login.png)}")
        self.pushButton.setStyleSheet("border:none;") # no border 
        self.pushButton.clicked.connect(self.check_code)
        self.grid.addWidget(self.pushButton, 9,1,1,5)
        # require user
        self.label1 = QLabel()
        #self.label1.setText("")
        self.label1.setTextFormat(Qt.AutoText)
        self.label1.setPalette(self.pe)
        #self.label.setPixmap(QPixmap("user.ico").scaled(15,15))
        self.label1.setObjectName("label")
        self.grid.addWidget(self.label1, 3, 6)
        self.label7 = QLabel()
        #self.label1.setText("")
        self.label7.setTextFormat(Qt.AutoText)
        self.label7.setPalette(self.pe)
        #self.label.setPixmap(QPixmap("user.ico").scaled(15,15))
        self.label7.setObjectName("labe7")
        self.grid.addWidget(self.label7, 4, 6)
        self.label8 = QLabel()
        #self.label1.setText("")
        self.label8.setTextFormat(Qt.AutoText)
        self.label8.setPalette(self.pe)
        #self.label.setPixmap(QPixmap("user.ico").scaled(15,15))
        self.label8.setObjectName("labe8")
        #self.grid.addWidget(self.label8, 5, 10)
        self.grid.addWidget(self.label8, 5, 7)
        self.label9 = QLabel()
        #self.label1.setText("")
        self.label9.setTextFormat(Qt.AutoText)
        self.label9.setPalette(self.pe)
        #self.label.setPixmap(QPixmap("user.ico").scaled(15,15))
        self.label9.setObjectName("labe9")
        self.grid.addWidget(self.label9, 7, 6)
        self.labelo = QLabel()
        #self.label1.setText("")
        self.labelo.setTextFormat(Qt.AutoText)
        self.labelo.setPalette(self.pe)
        #self.label.setPixmap(QPixmap("user.ico").scaled(15,15))
        self.labelo.setObjectName("labeo")
        self.grid.addWidget(self.labelo, 8, 6)
        '''
        # signup button
        self.pushButton_2 = QPushButton()
        self.pushButton_2.setObjectName("pushButton_2")
        #self.pushButton_2.setText('注册')
        self.pushButton_2.setStyleSheet("border:none;") # no border 
        self.grid.addWidget(self.pushButton_2,9,4,1,2)
        '''
        self.retranslateUi(signlog)
        QMetaObject.connectSlotsByName(signlog)
    def retranslateUi(self, signlog):
        _translate = QCoreApplication.translate
        self.label0.setText(_translate("signlog", "用户注册"))
        self.lineEdit.setPlaceholderText(_translate("signlog", "请输入用户名"))
        self.lineEdit_2.setPlaceholderText(_translate("signlog", "请输入密码"))
        self.lineEdit_3.setPlaceholderText(_translate("signlog","请输入邮箱"))
        #self.lineEdit_4.setPlaceholderText(_translate("signlog","您所在城市"))
        self.lineEdit_5.setPlaceholderText(_translate("signlog","您的年龄"))
        self.lineEdit_6.setPlaceholderText(_translate("signlog","请输入验证码"))
        self.pushButton0.setText(_translate("signlog", "发送验证码"))
        self.pushButton.setText(_translate("signlog", "立即注册"))
        self.label1.setText(_translate("signlog", "*"))
        self.label7.setText(_translate("signlog", "*"))
        self.label8.setText(_translate("signlog", "*"))
        self.label9.setText(_translate("signlog", "*"))
        self.labelo.setText(_translate("signlog", "*"))
        #self.pushButton_2.setText(_translate("signlog", "注册"))
        self.label_province.setText(_translate("signlog", "省份："))
        self.comboBox_province.setItemText(0, _translate("signlog", "请选择"))
        self.label_city.setText(_translate("signlog", "城市："))
        self.comboBox_city.setItemText(0, _translate("signlog", "请选择"))
        self.labelp.setText(_translate("signlog", "地址"))
    def add_ress(self):
        self.comboBox_province.clear()
        self.comboBox_province.addItem('请选择')
        for key, value in dictPorovince.items():
            self.comboBox_province.addItem(value, QVariant(key))
        self.comboBox_province.activated.connect(self.add_city)
        self.comboBox_city.activated.connect(self.just_btn_enable)
    # 当省份按钮被选择后添加对应的城市数据
    def add_city(self, index):
        pro_code = self.comboBox_province.itemData(index)
        self.city = dictCity.get(pro_code, dict())
        self.comboBox_city.clear()
        self.comboBox_city.addItem('请选择')
        #self.comboBox_town.clear()
        #self.comboBox_town.addItem('请选择')
        if self.comboBox_province.currentText() != '请选择':
            for key, value in self.city.items():
                self.comboBox_city.addItem(value, QVariant(key))  
    def just_btn_enable(self):
        #if self.comboBox_town.currentText() != '请选择':
        if self.comboBox_city.currentText() != '请选择':
            return True
        else:
            QMessageBox.warning(self,
                    "注意",
                    "请选择所在城市",
                    QMessageBox.Yes)
            self.lineEdit.setFocus()
            return False
    def check_age(self,sign_age):
        age_vaild=False
        if sign_age:
            try:
                age1=int(sign_age)
                if age1<=150 and age1>=0:
                    age_vaild=True
                else:
                    QMessageBox.warning(self,
                        "警告",
                        "看您的年龄不是地球人啊！",
                        QMessageBox.Yes)
                    self.lineEdit_5.setFocus()
            except ValueError:
                QMessageBox.warning(self,
                    "警告",
                    "年龄只接受正整数！",
                    QMessageBox.Yes)
                self.lineEdit_5.setFocus()
        return age_vaild
    def chk_usr_pwd(self, sign_user,sign_password,sign_mail):
        style_pass=False
        if sign_user and sign_password and sign_mail and self.just_btn_enable():
            pwd_num = sign_password.isalpha() # all alpha ?
            pwd_digit = sign_password.isdigit() # all digit ?
            pwd_num = sign_password.isalpha() # all alpha ?
            pwd_digit = sign_password.isdigit() # all digit ?
            #only alpha or digit ?
            usr_numalp=sign_user.isalnum() 
            pwd_numalp=sign_password.isalnum() 
            pwd_low = sign_password.islower() #all lower cases ?
            # 6-20 characters ?
            usr_len= len(sign_user)>=6 and (len(sign_user)<=20 )
            pwd_len= len(sign_password)>=6 and (len(sign_password)<=20 )
            usr_head= sign_user[0].isalpha() # head is an alpha
            if not (sign_user and usr_head and usr_numalp and usr_len):
                QMessageBox.warning(self,
                    "警告",
                    "用户名必须满足：\n1.以字母开头\n2.长度为6-20个字字符\n3.只含有英文字母或数字",
                    QMessageBox.Yes)
                self.lineEdit.setFocus()
            elif (not sign_password) or (not pwd_len) or (not pwd_numalp) or pwd_num or pwd_low or pwd_digit:
                QMessageBox.warning(self,
                    "警告",
                    "密码必须满足：\n长度为6-20个字符\n包含大小写字母和数字\n不包含特殊字符",
                    QMessageBox.Yes)
                self.lineEdit_2.setFocus()
            elif not re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", sign_mail):
                QMessageBox.warning(self,
                    "警告",
                    "请检查邮箱格式",
                    QMessageBox.Yes)
                self.lineEdit_3.setFocus()
            else:
                self.cur=self.conn.cursor()        
                self.sqlstring="select * from bx_users where Name='"+sign_user+"'"
                self.cur.execute(self.sqlstring)
                usr_exst=self.cur.fetchall()
                self.conn.commit()
                if usr_exst:
                    QMessageBox.warning(self,
                    "注意",
                    "用户名已存在\n请修改用户名！",
                    QMessageBox.Yes)
                    self.lineEdit.setFocus()
                else:
                    self.asqlstring="select * from bx_users where Email='"+sign_mail.lower()+"'"
                    self.cur.execute(self.asqlstring)
                    self.conn.commit()
                    mail_exst=self.cur.fetchall()
                    if mail_exst:
                        QMessageBox.warning(self,
                            "注意",
                            "邮箱已存在\n请更换邮箱！",
                        QMessageBox.Yes)
                        self.lineEdit_3.setFocus()
                    else:
                        self.tsqlstring="select * from bx_tmpusers where Name='%s';"%sign_user
                        self.cur.execute(self.tsqlstring)
                        self.conn.commit()
                        usr_exst_t=self.cur.fetchall()
                        self.msqlstring="select * from bx_tmpusers where Email='%s';"%sign_mail.lower()
                        self.cur.execute(self.msqlstring)
                        self.conn.commit()
                        mail_exst_t=self.cur.fetchall()
                        if usr_exst_t and mail_exst_t:
                            QMessageBox.warning(self,
                                "注意",
                                "验证码早已发过，\n 请查询邮箱！",
                                QMessageBox.Yes)
                            self.lineEdit_6.setFocus()
                        elif usr_exst_t :
                            QMessageBox.warning(self,
                                "注意",
                                "用户名已存在\n请修改用户名！",
                                QMessageBox.Yes)
                            self.lineEdit.setFocus()
                        elif mail_exst_t:
                            QMessageBox.warning(self,
                                "注意",
                                "邮箱已存在\n请更换邮箱！",
                                QMessageBox.Yes)
                            self.lineEdit_3.setFocus()
                        else:
                            style_pass=True
        else:
            QMessageBox.warning(self,
                                "注意",
                                "有*标志的是必填内容！",
                                QMessageBox.Yes)
            self.lineEdit_3.setFocus()
        #self.cur.close()
        return style_pass
    def click_send(self):
        self.sign_user = self.lineEdit.text()
        self.sign_password = self.lineEdit_2.text()
        self.usr_mail=self.lineEdit_3.text()
        self.usr_pwd_vali=self.chk_usr_pwd(self.sign_user,self.sign_password,self.usr_mail)
        #self.mail_vali= self.check_mail(self.usr_mail) 
        #adress_vail=self.just_btn_enable()
        #if self.usr_pwd_vali and self.mail_vali and adress_vail:
        self.age=self.lineEdit_5.text()
        if not self.age:
            self.usr_age_vail=True
        else:
           self.usr_age_vail=self.check_age(self.age)
        if self.usr_pwd_vali and self.usr_age_vail:
            self.wcur=self.conn.cursor()
            self.wsqlstring="insert into bx_tmpusers(Name,Email) values('%s','%s');"%(self.sign_user,self.usr_mail.lower())
            self.wcur.execute(self.wsqlstring)
            self.conn.commit()
            #time.sleep(3)
            QMessageBox.warning(self,
                    "恭喜",
                    "验证码已发送，\n请检查邮箱",
                    QMessageBox.Yes)
            self.lineEdit_6.setFocus()
    
    
    def check_code(self):
        self.cod = self.lineEdit_6.text()
        self.ct=self.py.get_pinyin(self.comboBox_city.currentText(), '')
        self.pv=self.py.get_pinyin(self.comboBox_province.currentText(), '')
        self.adress=self.ct +', '+ self.pv + ', china'
        self.rcur=self.conn.cursor()
        if self.sign_user:
            self.rsqlstring="select Code from bx_tmpusers where Name='%s'"%self.sign_user
            while True:
                c=self.rcur.execute(self.rsqlstring)
                self.conn.commit()
                if c:
                    d=self.rcur.fetchone()[0]
                    break
        if self.cod and d==self.cod:
            QMessageBox.warning(self,
                    "恭喜",
                    "注册成功，请登录",
                    QMessageBox.Yes)
            self.ocur=self.conn.cursor()
            if self.age:
                te=(self.adress,int(self.age),self.sign_password,self.sign_user)
                self.osqlstring="update bx_tmpusers set Location='%s',Age='%d',Pass_word='%s' where Name='%s';"%te
            else:
                te=(self.adress,self.sign_password,self.sign_user)
                self.osqlstring="update bx_tmpusers set Location='%s',Pass_word='%s' where Name='%s';"%te
            self.ocur.execute(self.osqlstring)
            self.conn.commit()                                                                                                              
            self.close()
        else:
            QMessageBox.warning(self,
                    "注意",
                    "验证码错误！",
                    QMessageBox.Yes)
            self.ocur=self.conn.cursor()
        
