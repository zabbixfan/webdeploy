#coding:utf-8
from django.shortcuts import render
from auto_install.models import appgroup ,apphost,auth,tasklog
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage  
import urllib2,re,json
import playbooktask
import logging
import random,requests
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
logger=logging.getLogger('auto')
# Create your views here1.
def my_login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
		logger.info('{} has been login.'.format(user))
                login(request,user)
                return HttpResponseRedirect('/')
            else:
                print "login error"
    return render(request,'login.html')

def my_logout(request):
   logger.info('{} has been logout.'.format(request.user))
   logout(request)
   return HttpResponseRedirect('/login')

@login_required(login_url="/login")
def deploy(request):
    return render(request,'deploy.html')

@login_required(login_url="/login")
def index(request):
    user = request.user
    return render(request,'idx.html',{'user':user})

@login_required(login_url="/login")
def module_list(request):
    tmplist = []
    moddict= {}
    authobj = auth.objects.filter(user_id=request.user.id)
    for e in authobj:
        if e.appgroup.appgroup not in tmplist:
            tmplist.append(e.appgroup.appgroup)
    for i in tmplist:
        modobj = appgroup.objects.filter(appgroup=i)
        modlist=[]
        for j in modobj:
            dict = {
                "id": j.id,
                "modname": j.appname
                }     
            modlist.append(dict)
        moddict[i]=modlist               
    return HttpResponse(json.dumps(moddict,indent=4),content_type='application/json')
@login_required(login_url="/login")
def app_list(request):
    mid = request.GET['id']
    if mid is not None:
        moduleobj = appgroup.objects.filter(id=mid)
        #nprint(moduleobj)
        if moduleobj is None:
            return None
        url = moduleobj[0].warpath
        appname = moduleobj[0].appname
        warpath = []
        if moduleobj[0].deploytype == 'nexus':
            string = r'\"(.*/maven-metadata\.xml)?\"'
            method = "search"
            metadata = urlhadle(url,string,method)
            r = requests.get(metadata[0])
            with open('temp.xml','wb') as f:
                f.write(r.content)
            f = get_tagname()
            for i in f:
                wardict = {}
                realurl = str(url) + i +"/"
                string = r'>(%s.*\.war?)(?=\<\/a\>)'%(appname)
                wars = urlhadle(realurl, string)
                if wars is not None:
                    wardict = {
                        'url': realurl,
                        'wars': wars
                    }
                    warpath.append(wardict)
                    warpath=sorted(warpath,key=lambda x:x['wars'],reverse=True)
        else:
            string = r'"(%s.*?\.war)".*?'%(appname)
            wars = urlhadle(url,string)
            if wars is not None:
                wardict ={
                    'url': url,
                    'wars': wars
                    }
                warpath.append(wardict)
        return HttpResponse(json.dumps({'warpath':warpath},indent=4,),content_type='application/json')
def urlhadle(hurl,reg,fmethod="findall"):
    try:
        data = urllib2.urlopen(hurl).read()
        if fmethod == "findall":
            res = sorted(re.findall(reg,data),reverse=True)
        else:
            res = re.search(reg, data)
            if res is not None:
                res = res.groups()
        return res
    except Exception, e:
        logger.info('url {} can\'t access,{}'.format(hurl,e))
def get_tagname():
    from xml.dom.minidom import parse
    doc = parse("temp.xml")
    root= doc.getElementsByTagName("version")
    version = [dat.firstChild.data for dat in root]
    return version

#@login_required(login_url="/login")
def server_list(request):
    sid = request.GET['sid']
    serverobj = apphost.objects.filter(appgroup_id=sid)
    serverlist=[]
    for e in serverobj:
        appname = appgroup.objects.filter(id=e.appgroup_id)[0].appname
        serverdict = {
            "addr": e.hostaddr,
            "appname": appname,
            "work_dir": e.path,
            "user":e.username,
            "sid": e.id
            }
        serverlist.append(serverdict)
    return HttpResponse(json.dumps({'serverlist':serverlist},indent=4,),content_type='application/json')

@login_required(login_url="/login")
def commit(request):
    sid = request.GET.getlist('sid')
    war = request.GET['war']
    info = ''
    authobj = auth.objects.filter(user_id=request.user.id)
    authgroup = [item.appgroup.id for item in authobj]
    if (war == ''):
        info = '请选择更新包'
    if (sid == []):
        info = '请选择正确的服务器'
    if (len(sid) and war <> ''):
	sn = random.randint(1,1000)
        for i in sid:
            ids = i.encode("utf-8")
            for j in authgroup:
                hostobj = apphost.objects.filter(appgroup_id=j)
                if ids in [str(item.id) for item in hostobj]:
                    break
            else:
                info = '无访问权限，请联系管理员'
                return HttpResponse(info)
            ret_obj = apphost.objects.filter(id=ids)
            appname = [item.appgroup.appname for item in ret_obj][0].encode("utf-8")
            hostaddr = [item.hostaddr for item in ret_obj][0].encode("utf-8")
            workdir = [item.path for item in ret_obj][0].encode("utf-8")
            yml = 'yml/tomcatdeploy.yml'
	    logger.info('{} commit a deploy with arguments: {} {} {} {} {} {}.'.format(request.user,sn,hostaddr,appname,workdir,yml,war))
            f = playbooktask.ExecuteTask(request.user.id,sn,hostaddr,appname,workdir,yml,"deploy",war)
        info = open(f,'r')
    return HttpResponse(info)

@login_required(login_url="/login")
def rollback(request):
    sid = request.GET.getlist('sid')
    info = ''
    authobj = auth.objects.filter(user_id=request.user.id)
    authgroup = [item.appgroup.id for item in authobj]
    sn = random.randint(1,1000)
    if len(sid):
        for i in sid:
            ids = i.encode("utf-8")
            for j in authgroup:
                hostobj = apphost.objects.filter(appgroup_id=j)
                if ids in [str(item.id) for item in hostobj]:
                    break
            else:
                info = '无访问权限，请联系管理员'
                return HttpResponse(info)
            ids = i.encode("utf-8")
            ret_obj = apphost.objects.filter(id=ids)
            appname = [item.appgroup.appname for item in ret_obj][0].encode("utf-8")
            hostaddr = [item.hostaddr for item in ret_obj][0].encode("utf-8")
            workdir = [item.path for item in ret_obj][0].encode("utf-8")
            yml = 'yml/tomcatrollback.yml'  
    	    logger.info('{} commit a deploy with arguments:{} {} {} {} {}.'.format(request.user,sn,hostaddr,appname,workdir,yml))
            f = playbooktask.ExecuteTask(request.user.id,sn,hostaddr,appname,workdir,yml,'rollback')
        info = open(f,'r')
    else:
        info = '请选择正确的服务器'
    return HttpResponse(info)
def zcgl(request):
    return render(request,'zcgl.html')

@login_required(login_url="/login")
def log(request):
    user=request.user
    loglist=[]
    logobj = tasklog.objects.filter(excute_user_id=request.user.id)
    for log in logobj:
        res = "执行成功" if log.result == 0 else "执行失败"
        logdict = {
            "appgroup": log.appgroup.appname,
            "host": log.task_host,
            "logtype": log.log_type,
            "btime": log.begin_time,
            "etime": log.end_time,
            "res": res,
            "id": log.id
            }
        loglist.append(logdict)
    loglist = sorted(loglist,key=lambda b:b["btime"],reverse=True)
    after_range_num=5
    before_range_num=4
    try:
        page = int(request.GET.get("page",1))
        
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    paginator = Paginator(loglist,8)
    try:
        log_list = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
        log_list = paginator.page(paginator.num_pages)
    pagerange=list(paginator.page_range)
    if page >= after_range_num:
        page_range = pagerange[page-after_range_num:page+before_range_num]
    else:
        page_range=pagerange[0:page+before_range_num]
    return  render(request,'logs.html',{'loglist':log_list,'page_range':page_range})

@login_required(login_url="/login")
def ldetail(request):
    if "id" not in request.GET.keys():
        return HttpResponse("请输入正确ID")
    lid = request.GET['id']
    logobj = tasklog.objects.filter(id=lid)
    if len(logobj) == 0:
        return HttpResponse("参数错误")
    else:
        serial = logobj[0].task_serial
        filename = "/var/log/ansible/{}.log".format(serial)
        try:
            with open(filename,'r') as info:
                return HttpResponse(info.read())
        except Exception,e:
            logger.info(e)
            return HttpResponse("日志不存在") 
