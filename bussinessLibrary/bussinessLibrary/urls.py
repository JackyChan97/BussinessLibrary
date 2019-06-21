"""bussinessLibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve
from index import views
from bussinessLibrary import settings

urlpatterns = [
    url(r'^index$', views.index, name='index'),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^emails_list/$', views.emails_list, name='emails_list'),
    url(r'^add_emails_page/', views.add_emails_page, name='add_emails_page'),
    url(r'^add_emails$', views.add_emails, name='add_emails'),
    url(r'^delete_emails/(?P<del_address>.*)/$', views.delete_emails, name='delete_emails'),
    url(r'^send_emails', views.send_emails, name='send_emails'),
    url(r'^timing_send_emails', views.timing_send_emails, name='timing_send_emails'),
    url(r'^update_info', views.update_info, name='update_info'),
    url(r'^', views.index, name='index'),
]
