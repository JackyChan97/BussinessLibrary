from django.shortcuts import render
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import time
from index.models import Email
from index.models import Project
import templates
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.core.mail import send_mass_mail
import os
# Create your views here.


def send_emails(request):
    # pa = os.getcwd()+"\\index\\pw.txt"
    # with open(pa,'r') as f:
    #     text = f.read()
    #     text = text.split("abc123")
    # from_add = text[0]
    # password = text[1]
    # el = Email.objects.all()
    # add_list = []
    # for i in el:
    #     add_list = [add_list, i.address]
    # cl = Project.objects.all()
    # content = ""
    # for i in cl:
    #     content = content+"项目名: "+i.name+" url: "+i.url+'\n'
    #
    # subject = time.strftime("%Y-%m-%d")+"商机"
    #
    # send_mail(subject,content,from_add,add_list,fail_silently=False)
    # port = 465
    # mail_server = "smtp.qq.com"
    # message = MIMEText(content,"plain","utf-8")
    # message['From'] = Header("BLSYS","utf-8")
    # message['To'] = Header("Customer","utf-8")
    # message['Subject'] = Header(time.strftime("%Y-%m-%d")+"商机","utf-8","utf-8")

    # try:
    #     mail = smtplib.SMTP_SSL(mail_server,port)
    #     status = mail.login(from_add,password)
    #     print(status)
    #     mail.sendmail(from_add,add_list,message.as_string())
    #     print("邮件发送成功")
    #     mail.quit()
    # except:
    #     print("发送失败")

    return render(request, "index.html")

def index(request):
    global timing_send_emails_tag
    projects = Project.objects.all()
    return render(request, "index.html", {'projects': projects, 'timing_send_emails_tag':timing_send_emails_tag})


def emails_list(request):
    ret = Email.objects.all()
    return render(request, "emails.html", {"Emails": ret})


def delete_emails(request, del_address):
    if del_address:
        del_obj = Email.objects.get(address=del_address)  # 继承models中的数据库类
        del_obj.delete()  # 删除操作
        return redirect("/emails_list/")
    else:
        return HttpResponse("ERROR,check the data and try again")  # 若不存在数据或其他错误


def add_emails(request):#第一次请求页面的时候，返回一个页面，页面有两个填写框
    error_msg = ""
    if request.method == "POST":
        new_address = request.POST.get("address", None)# print(new_name)
        new_annotation = request.POST.get("annotation", None)
        try:
            validate_email(new_address)
            print("你添加的email address为：{0}".format(new_address))
            Email.objects.create(address=new_address, annotation=new_annotation)#数据库中新创建一条数据行
            return redirect("/emails_list/") # redirect返回方法 HttpResponse返回字符串
        except:
            error_msg = "Address is not right, please try again!"
            return render(request, "add_emails.html", {"error": error_msg})  # render完成HTML界面替换

    else:
        error_msg = "Address is not right, please try again!"
        return render(request, "add_emails.html", {"error": error_msg})#render完成HTML界面替换


def add_emails_page(request):
    return render(request, 'add_emails.html')


timing_send_emails_tag = 0


def timing_send_emails(request):
    global timing_send_emails_tag
    if timing_send_emails_tag:
        timing_send_emails_tag = 0
    else:
        timing_send_emails_tag = 1

    projects = Project.objects.all()
    return render(request, "index.html", {'projects': projects, 'timing_send_emails_tag': timing_send_emails_tag})


