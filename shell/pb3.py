#!/usr/bin/env python

import os,time
import sys,json
from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from ansible.plugins.callback import default


class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        print json.dumps({host.name: result._result}, indent=4)

def pbexe(sid,war,mode):
  variable_manager = VariableManager()
  loader = DataLoader()

#  inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=[])
  inventory = Inventory(loader=loader, variable_manager=variable_manager)
  playbook_path = '/etc/ansible/yml/'+sid+'.yml'

  if not os.path.exists(playbook_path):
    print playbook_path
    print '[INFO] The playbook does not exist'
    sys.exit()

  Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection','module_path', 'forks', 'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])
  options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh', module_path=None, forks=100, remote_user='root', private_key_file=None, ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True, become_method=None, become_user='root', verbosity=None, check=False)

  variable_manager.extra_vars = {'war': war,'mode': mode} # This can accomodate various other command line arguments.`

  passwords = {}

  #cb = ResultCallback()
#  cb = default.CallbackModule()
  pbex = PlaybookExecutor(playbooks=[playbook_path],  inventory=inventory, variable_manager=variable_manager, loader=loader, options=options, passwords=passwords)
#  pbex._tqm._stdout_callback = cb
  op=sys.stdout

  filename='/var/log/ansible/'+time.strftime('%Y%m%d%H%M%S')+'.log'
  opf=open(filename,'w')
  sys.stdout=opf
  results = pbex.run()
  sys.stdout=op
  opf.close
  print open(filename,'r').read()
  return filename

#pbexe('dcs','dcs_130_138520_130.war','')
