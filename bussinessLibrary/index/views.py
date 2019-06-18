from django.shortcuts import render
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import time
from index.models import Project
import templates

# Create your views here.


def SendEmail(request):
    with open("pw.txt",'r') as f:
        text = f.read()
        text = text.split("abc123")
    from_add = text[0]
    password = text[1]
    add_list = []
    content = "test"
    port = 465
    mail_server = "smtp.qq.com"
    message = MIMEText(content,"plain","utf-8")
    message['From'] = Header("BLSYS","utf-8")
    message['To'] = Header("Customer","utf-8")
    message['Subject'] = Header(time.strftime("%Y-%m-%d")+"商机","utf-8")

    try:
        mail = smtplib.SMTP_SSL(mail_server,port)
        status = mail.login(from_add,password)
        print(status)
        mail.sendmail(from_add,add_list,message.as_string())
        print("邮件发送成功")
        mail.quit()
    except:
        print("发送失败")


def index(request):
    data = {'hello', 'test'}
    return render(request, "index.html", {'data': data} )

