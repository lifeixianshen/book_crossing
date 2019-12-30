# -*- coding:utf-8 -*-
import time
import pymysql
import random
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
class mail_register():
    def __init__(self,time_out):
        self.conn=pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='root',
            db='book_crossing',
            charset='utf8',
        )
        self.mail_list=set([])
        self.time_out=time_out
        c=self.register(self.time_out)
        
        self.conn.close()
        
    def get_account(self):
        self.acc_cur=self.conn.cursor()
        self.acc_string="select Name from bx_users where Name is not null;"
        self.acc_cur.execute(self.acc_string)
        self.conn.commit()
        usr_list=set([i[0] for i in self.acc_cur.fetchall()])
        #self.ask_cur.execute("truncate table bx_tmpusers;")
        #self.conn.commit()
        self.acc_cur.close()
        #self.conn.close()
        return usr_list
    def get_send(self):
        #self.mail_list=self.mail_list | get_account()
        self.ask_cur=self.conn.cursor()
        self.mail_string="select Name,Email,Code from bx_tmpusers;"
        self.ask_cur.execute(self.mail_string)
        self.conn.commit()
        namil=self.ask_cur.fetchall()
        usr_list=[i[0] for i in namil]
        mails=[i[1] for i in namil]
        codes=[i[2] for i in namil]
        #self.ask_cur.execute("truncate table bx_tmpusers;")
        #self.conn.commit()
        #self.cur.close()
        for i in range(0,len(usr_list)):
            if usr_list[i] not in self.mail_list:
                if codes[i]:
                    self.mail_list.add(usr_list[i])
                    print('给%s的邮件已经发送过了'%usr_list[i])
                else:
                    Code=str(random.randint(10000,99999))
                    my_sender='2569130079@qq.com'    # 发件人邮箱账号
                    my_pass = 'lzrsrzamwwgodijh'     # 发件人邮箱密码
                    my_user=mails[i]      # 收件人邮箱账号 
                    try:
                        msg=MIMEText('您的验证码是%s'%Code,'plain','utf-8')
                        msg['From']=formataddr(["瀚海书屋",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
                        msg['To']=formataddr(["user",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
                        msg['Subject']="瀚海书屋注册验证码"                # 邮件的主题，也可以说是标题
                        server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
                        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
                        server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
                        server.quit()  # 关闭连接
                        self.mail_list.add(i)
                        ret=True
                        print('给%s的邮件发送成功'%usr_list[i])
                    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
                        print('给%s的邮件发送失败'%usr_list[i])
                        ret=False
                    self.find_i = "UPDATE bx_tmpusers SET Code='%s' WHERE Name='%s'"%(Code,usr_list[i])
                    #self.ask_cur.execute(self.find_i,[Code,usr_list[i]])
                    self.ask_cur.execute(self.find_i)
                    self.conn.commit()
            #else:
            #    print('给%s的邮件已经发送过了'%usr_list[i])
        self.ask_cur.close()
        #self.conn.close()
    def get_maxid(self):
        self.id_cur=self.conn.cursor()
        self.id_string="select max(User_id) from bx_users;"
        self.id_cur.execute(self.id_string)
        self.conn.commit()
        max_ids=self.id_cur.fetchall()
        if max_ids:
            max_id=max_ids[0][0]
        else:
            max_id=0
        return max_id
    def write_t(self):
        self.w_cur=self.conn.cursor()
        self.n_string="select Location,Age,Name,Email,Pass_word from bx_tmpusers where Pass_word is not null;"
        self.w_cur.execute(self.n_string)
        self.conn.commit()
        new_acc=self.w_cur.fetchall()
        for i in range(0,len(new_acc)):
            accs=self.get_account()
            if new_acc[i][2] not in accs and new_acc[i][3]:
                maxid=self.get_maxid()
                if new_acc[i][1]:
                    self.write_string= """INSERT INTO bx_users(User_id,
                    Location, Age, Name,Email,Pass_word)
                    VALUES ('%d', '%s', '%d', '%s', '%s', '%s')"""%(maxid+1,new_acc[i][0],int(new_acc[i][1]),new_acc[i][2],new_acc[i][3],new_acc[i][4])
                else:
                    self.write_string= """INSERT INTO bx_users(User_id,
                    Location, Age, Name,Email,Pass_word)
                    VALUES ('%d', '%s', NULL, '%s', '%s','%s')"""%(maxid+1,new_acc[i][0],new_acc[i][2],new_acc[i][3],new_acc[i][4])
                print(self.write_string)
                self.w_cur.execute(self.write_string)
                self.conn.commit()
        return
    def register(self,time_o):
        while True:
            users = self.get_account()
            self.mail_list=self.mail_list | users
            a=self.get_send()
            users2 = self.get_account()
            self.mail_list=self.mail_list | users2
            b=self.write_t()
            print(1)
            time.sleep(time_o)
            
    def check_rating(self):
        self.rat_cur=self.conn.cursor()
        self.ratsql="select * from bx_ratings"
        self.rat_cur.execute(self.ratsql)
        self.conn.commit()
        self.ratouts=self.rat_cur.fetchall()
        if self.ratout:
            for i in self.ratout:
                self.ratsqls="select * from bx_book_ratings where User_id='%d' and ISBN='%s'"%(i[0],i[1])
                self.rat_cur.execute(self.ratsqls)
                self.conn.commit()
                self.ratout=self.rat_cur.fetchall()
                if self.ratout:
                    if int(self.ratout)!=int(i[2]):
                        self.xsqls="UPDATE bx_book_ratings SET Book_rating='%d' WHERE User_id='%d' and ISBN='%s'"%(i[2],i[0],i[1])
                        self.rat_cur.execute(self.xsqls)
                        self.conn.commit()
                else:
                    self.isqls="""INSERT INTO bx_book_ratings
                        VALUES ('%d', '%s', '%d')"""%(i[0],i[1],i[2])
                    self.rat_cur.execute(self.isqls)
                    self.conn.commit() 
    def rating(self):
        while True:
             e=self.check_rating()
             time.sleep(time_o)
        return e
if __name__=='__main__':
    d=mail_register(5)