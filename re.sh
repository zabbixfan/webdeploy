kill -9 `cat /geelyapp/opsdev/web/logs/uwsgi.pid`
sleep 2
uwsgi --ini 9000.ini -w main --touch-reload /geelyapp/opsdev/web/shell/reload.set 
