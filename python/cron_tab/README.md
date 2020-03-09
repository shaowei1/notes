
```
要查看在你的系统上运行的 cron 作业，打开你的终端并键入：

crontab -l
以上命令显示了 crontab 文件中的作业列表。如果要将新的 cron 作业添加到 crontab，请输入：

crontab -e

50 19 * * * python3 hello.py >> a.txt

```

```
*/2 * * * * /path/to/script/to/run.sh
An explanation of the timing is below (add a star and slash before number to run every n timesteps, in this case every 2 minutes)

* * * * * command to be executed
- - - - -
| | | | |
| | | | ----- Day of week (0 - 7) (Sunday=0 or 7)
| | | ------- Month (1 - 12)
| | --------- Day of month (1 - 31)
| ----------- Hour (0 - 23)
------------- Minute (0 - 59)
```

# 方法2
```
<!-- https://pypi.python.org/pypi/python-crontab -->
<!-- pip install python-crontab -->

from crontab import CronTab
#init cron
cron   = CronTab()

#add new cron job
job  = cron.new(command='/usr/bin/echo')

#job settings
job.hour.every(4)
```
