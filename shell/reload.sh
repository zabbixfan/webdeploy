#!/bin/bash
objectdir="/geelyapp/opsdev/web"
/usr/local/inotify/bin/inotifywait -mrq --exclude "(static|log|shell|\.swp|\.swx|\.pyc|\.py\~)" --timefmt '%d%m%y %H:%M' --format '%T %w%f' --event modify,delete,move,create,attrib ${objectdir} | while read files
do
/bin/touch /geelyapp/opsdev/web/shell/reload.set
continue
done &
