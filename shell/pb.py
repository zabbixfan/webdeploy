import sys
import ansible.playbook
from ansible import callbacks
from ansible import utils

stats = callbacks.AggregateStats()
playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)
def execute(play,params):
  pb = ansible.playbook.PlayBook(
    playbook=play,
    stats=stats,
    callbacks=playbook_cb,
    runner_callbacks=runner_cb,
    check=False,
    extra_vars=eval(params)
  )
  print pb
  return  pb.run()
if __name__=='__main__':
  res=execute(sys.argv[1],sys.argv[2])
  print res
