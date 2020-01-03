```
/app/celery_tasks/common.py:9: MonkeyPatchWarning: Monkey-patching ssl after ssl has already been imported may lead to errors, including RecursionError on Python 3.6. It may also silently lead to incorrect behaviour on Python 3.7. Please monkey-patch earlier. See https://github.com/gevent/gevent/issues/1016. Modules that had direct imports (NOT patched): ['urllib3.util.ssl_ (/usr/local/lib/python3.7/site-packages/urllib3/util/ssl_.py)', 'urllib3.util (/usr/local/lib/python3.7/site-packages/urllib3/util/__init__.py)'].
181
12-28 19:37:48
INFO:sqlalchemy.engine.base.Engine:SHOW VARIABLES LIKE 'sql_mode'
182
12-28 19:37:48
monkey.patch_all()
```
