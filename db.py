#!/usr/bin/env python
#coding:utf-8
#just test 
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
import django
django.setup()
from app1.models import * 
from app1.zabbix import *

z=zabbix()
groups=z.group_get()
for group in groups: 
  print group["groupid"],group["name"]
  hostgroup.objects.get_or_create(name=group["name"],zid=group["groupid"],defaults={'status':1})

print "host..............."
groups=hostgroup.objects.filter(status=1).values('id','zid')
for group in groups:
  hosts=z.hostgroup_get(group["zid"])
  for h in hosts:
    print group["zid"],h["name"]
    host.objects.get_or_create(name=h["name"],host=h["host"],hostgroup_id=group["id"],zid=h["hostid"],defaults={'status':1})

print "graph.............."
hosts=host.objects.filter(status=1).values('host','id')
for h in hosts:
  graphs=z.hostgraph_get(h['host'])
  for g in graphs:
    print h["host"],g["name"]
    graph.objects.get_or_create(name=g["name"],type=g["graphtype"],zid=g["graphid"],host_id=h["id"],defaults={'status':0})
