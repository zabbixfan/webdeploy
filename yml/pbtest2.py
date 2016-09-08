#!/usr/bin/env python

import os,time
import sys,json
import random
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from ansible.plugins.callback import default


def pbexe(serial,host,module,apppath,yaml,url=None):
    variable_manager = VariableManager()
    loader = DataLoader()
    hostfile = '/ansible/hosts'
#  inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=[])
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

  #cb = ResultCallback()
#  cb = default.CallbackModule()
    pbex = PlaybookExecutor( playbooks=[playbook_path],  inventory=inventory, variable_manager=variable_manager, loader=loader, options=options, passwords=passwords)
#  pbex._tqm._stdout_callback = cb
    op=sys.stdout
  #pbex.run()
    filename='/var/log/ansible/'+time.strftime('%Y-%m-%d-%H')+module+str(serial)+'.log'
    opf=open(filename,'a+')
    sys.stdout=opf
    results = pbex.run()
    sys.stdout=op
    opf.close
  print open(filename,'r').read()
    return filename
if __name__ == '__main__':
    sn=random.randint(1,1000)
    pbexe(sn,'10.86.87.10','ansible','/geelyapp/tomcat-ansible','/geelyapp/opsdev/web/yml/test2.yml','http://10.86.87.253:8088/Beta/VSD/Openapi/openapi.war')
