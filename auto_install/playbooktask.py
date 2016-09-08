#!/usr/bin/env python

import os,time
import sys,json
import random
import django
from django.utils import timezone
sys.path.append('/geelyapp/opsdev/web')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
django.setup()
from django.contrib.auth.models import User
from auto_install.models import appgroup ,apphost,auth,tasklog
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from ansible.plugins.callback import default
from writelog import CallbackModule
class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    def __init__(self,sn):
        self.sn = sn
    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        print ("good",sn)
    def v2_playbook_on_stats(self,stats):
        print(self.sn)
def ExecuteTask(userid,serial,host,module,apppath,yaml,type,url=None):
    starttime = timezone.now()
    sn = "%s%s%s"%(time.strftime('%Y%m%d%H'),str(serial),module)
    res = pbexe(userid,sn,host,module,apppath,yaml,url)
    endtime = timezone.now()
    appobj = apphost.objects.filter(hostaddr=host)
    groupid = appobj[0].appgroup_id
    u1 = User.objects.get(id=userid)
    g1 = appgroup.objects.get(id=groupid)
    T1 = tasklog(task_serial=sn,task_host=host,begin_time=starttime,end_time=endtime,result=res,excute_user=u1,appgroup=g1,log_type=type)
    T1.save()
    filename='/var/log/ansible/'+sn+'.log'
    return filename
def pbexe(userid,serial,host,module,apppath,yaml,url=None):
    variable_manager = VariableManager()
    loader = DataLoader()
    hostfile = '/ansible/hosts'
    inventory = Inventory(loader=loader, variable_manager=variable_manager,host_list='/ansible/hosts')
    playbook_path = yaml

    if not os.path.exists(playbook_path):
        print playbook_path
        print '[INFO] The playbook does not exist'
        sys.exit()

    Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection','module_path', 'forks', 'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])
    options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh', module_path=None, forks=100, remote_user='root', private_key_file=None, ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True, become_method=None, become_user='root', verbosity=None, check=False)

    variable_manager.extra_vars = {
            'host': host,
            'module': module,
            'tomcat_root': apppath,
            'url': url
} # This can accomodate various other command line arguments.`
    passwords = {}
    cb = CallbackModule(serial)
#  cb = default.CallbackModule()
    pbex = PlaybookExecutor( playbooks=[playbook_path],  inventory=inventory, variable_manager=variable_manager, loader=loader, options=options, passwords=passwords)
    pbex._tqm._stdout_callback = cb
    results = pbex.run()
    return results
if __name__ == '__main__':
    sn=random.randint(1,1000)
    ExecuteTask(1,sn,'10.86.87.49','ansible','/geelyapp/tomcat-ansible','/geelyapp/opsdev/web/yml/test3.yml','http://10.86.87.253:8088/Beta/VSD/Openapi/openapi.war')    
