#!coding:utf-8
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Inspired from: https://github.com/redhat-openstack/khaleesi/blob/master/plugins/callbacks/human_log.py
# Further improved support Ansible 2.0

from __future__ import (absolute_import, division, print_function)
from ansible.plugins.callback import CallbackBase

__metaclass__ = type
import json
import sys,time
reload(sys)
sys.setdefaultencoding('utf-8')

try:
    import simplejson as json
except ImportError:
    import json

# Fields to reformat output for
FIELDS = ['cmd', 'command', 'start', 'end', 'delta', 'msg', 'stdout',
          'stderr', 'results']


FIELD = ['cmd', 'command', 'msg', 'stdout','stderr', 'results','task']
class CallbackModule(CallbackBase):

    """
    Ansible callback plugin for human-readable result logging
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'human_log'
    CALLBACK_NEEDS_WHITELIST = False
    TIME_FORMAT = '%Y/%m/%d %H:%M:%S'
    def human_log(self, data):
        if type(data) == dict:
            for field in FIELDS:
                no_log = data.get('_ansible_no_log')
                if field in data.keys() and data[field] and no_log != True:
                    output = self._format_output(data[field])
                    print("\n{0}: {1}".format(field, output.replace("\\n","\n")))
    def write_log(self,data,res=None):
        now = time.strftime(self.TIME_FORMAT, time.localtime())
        path='/var/log/ansible/test.log'
        with open(path, "a+") as fd:
            if str(data) == 'TASK: setup':
                string = 'TASK: setup'
            #判断文本是否属于task开始
            if str(data).startswith('TASK'):
                string = "{},{}".format(now,data)
            #判断文本是否属于runner_on_ok or runner_on_failed
            if type(data) == dict:
                if data.has_key("cmd"):
                    if data['stderr'] or data['rc'] != 0:
                        string = "Failed.{}\ncommand:{}\n".format(data['stderr'],data['cmd'])
                    else:
                        string = "Task complete success.{}\n".format(data['stdout'].replace("\n","."))
                else:
                    if data.has_key('failed') and data['failed']:
                        string = "Failed.{}\n".format(data['msg'])
                    else:
                        string = "Task,complete success.\n"
            #判断文本是否属于runner_item
            if type(data) == str:
                string = data
            #判断文本是否属于playbook_on_stats
            if res == True:
                hosts = sorted(data.processed.keys())
                for h in hosts:
                    s = data.summarize(h)
                    string = "{}.\tok={},\tchanged={},\tfailures={},\tunreachable={}".format(h,s['ok'],s['changed'],s['failures'],s['unreachable'])
            fd.write("{}\n".format(string))
        print (string)
    def _format_output(self, output):
        # Strip unicode
        if type(output) == unicode:
            output = output.encode(sys.getdefaultencoding(), 'replace')

        # If output is a dict
        if type(output) == dict:
            return json.dumps(output, indent=2)

        # If output is a list of dicts
        if type(output) == list and type(output[0]) == dict:
            # This gets a little complicated because it potentially means
            # nested results, usually because of with_items.
            real_output = list()
            for index, item in enumerate(output):
                copy = item
                if type(item) == dict:
                    for field in FIELDS:
                        if field in item.keys():
                            copy[field] = self._format_output(item[field])
                real_output.append(copy)
            return json.dumps(output, indent=2)

        # If output is a list of strings
        if type(output) == list and type(output[0]) != dict:
            # Strip newline characters
            real_output = list()
            for item in output:
                if "\n" in item:
                    for string in item.split("\n"):
                        real_output.append(string)
                else:
                    real_output.append(item)

            # Reformat lists with line breaks only if the total length is
            # >75 chars
            if len("".join(real_output)) > 75:
                return "\n" + "\n".join(real_output)
            else:
                return " ".join(real_output)

        # Otherwise it's a string, (or an int, float, etc.) just return it
        return str(output)

    def v2_on_any(self, *args, **kwargs):
        pass
    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.write_log(result._result)
    def v2_runner_on_ok(self, result):
        self.write_log(result._result)
    def v2_runner_on_skipped(self, result):
        self.write_log(result._result)
    def v2_runner_item_on_ok(self,result):
        msg = result._result
        res = "Success:[{}],item:{}".format(result._host,msg['item'])
        self.write_log(res)
    def v2_runner_item_on_failed(self,result):
        msg = result._result
        res = "Failed:[{}],item:{},msg:{}".format(result._host,msg['item'],msg['msg'])
        self.write_log(res)
    def v2_runner_item_on_skipped(self,result):
        self.write_log(result._result)
    def v2_playbook_on_stats(self, stats,res=True):
        self.write_log(stats,res)
    def v2_playbook_on_task_start(self, task, is_conditional):
        self.write_log(task)
    def v2_runner_on_unreachable(self, result):
        self.human_log(result._result)

    def v2_runner_on_no_hosts(self, task):
        pass
    def v2_runner_on_async_poll(self, result):
        self.human_log(result._result)

    def v2_runner_on_async_ok(self, host, result):
        self.human_log(result._result)

    def v2_runner_on_async_failed(self, result):
        self.human_log(result._result)
    def v2_playbook_on_start(self, playbook):
        pass

    def v2_playbook_on_notify(self, result, handler):
        pass

    def v2_playbook_on_no_hosts_matched(self):
        pass

    def v2_playbook_on_no_hosts_remaining(self):
        pass

    def v2_playbook_on_vars_prompt(self, varname, private=True, prompt=None,
                                   encrypt=None, confirm=False, salt_size=None,
                                   salt=None, default=None):
        pass

    def v2_playbook_on_setup(self):
        pass

    def v2_playbook_on_import_for_host(self, result, imported_file):
        pass

    def v2_playbook_on_not_import_for_host(self, result, missing_file):
        pass

    def v2_playbook_on_play_start(self, play):
        pass
    def v2_on_file_diff(self, result):
        pass

    def v2_playbook_on_item_ok(self, result):
        pass

    def v2_playbook_on_item_failed(self, result):
        pass

    def v2_playbook_on_item_skipped(self, result):
        pass

    def v2_playbook_on_include(self, included_file):
        pass

    def v2_playbook_item_on_ok(self, result):
        pass

    def v2_playbook_item_on_failed(self, result):
        pass

    def v2_playbook_item_on_skipped(self, result):
        pass
