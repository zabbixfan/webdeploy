#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
import time
import pb3

# Create your views here.

def shell(request):
  sid = request.GET.get('sid','')
  war = request.GET.get('war','')
  mode = request.GET.get('mode','0')

  if (war==''):
    re='请选择更新包'
  if (sid<>'' and war<>''):
    f = pb3.pbexe(sid,war,mode)
    re = open(f,'r')

  return HttpResponse(re)
def deploy(request):
    host = request.GET['host']
    group = request.GET['group']
    path = request.GET['path']
    url = request.GET['url']
    if (url==''):
        re='请选择更新包'
    if (host<>'' and group<>'' and url<>'' and path<>''):
        f = pbtest.pbexe(host,group,path,url)
        re = open(f,'r')
    return HttpResponse(re)
    #return HttpResponse('%s,%s,%s,%s'%(host,group,files,path))

