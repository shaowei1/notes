# code style setting

```
Editor --> Code Style --> Hard Wrap at: 79
Tools  --> Python Integrated Tools --> Docstrings --> Docstring format: Google

init-hook=''
pylink --rcfile=pylint.conf app/
```



# shortcuts
https://blog.csdn.net/qq_18863573/article/details/74910975

## celey
script path: /Users/root1/.virtualenvs/flask-env/bin/celery
pamameters: worker -l debug -A c-egg-origin.celery
working directory: /Users/root1/Github/loguru/example


celery -A engine.runserver.celery worker -l debug -Q MERCHANT:CELERY:publish_tmall_product,queue_name1
/Users/root1/Github/ecpro-merchant/app
