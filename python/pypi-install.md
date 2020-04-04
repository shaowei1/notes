### Environment

```bash
# setuotools 和 wheel 用来构建你的项目
python3 -m pip install --user --upgrade setuptools wheel
# twine 用来上传你的包到 PyPi 
python3 -m pip install --user --upgrade twine

```

### 目录

```
packaging_tutorial/
  example_pkg/
    __init__.py
  tests/
  setup.py
  LICENSE
  README.md

```

#### Setup.py

`setup.py` 是setuptools的构建脚本。它告诉setuptools你的包（例如名称和版本）以及要包含的代码文件

name 是包名。发布之前请上 PyPi 搜索一下有没有同名的包，防止冲突。
version 是版本号，更新的时候会寻找比当前版本更高的版本号，所以不要乱写。
description是短描述，一般是一句话。
long_description是长描述，详细的介绍。我直接读入了 README.md.
url是你项目的地址。一般会填 github 地址。
packages 是包列表。setuptools.find_packages() 可以自动找到目录下所有的包，在这个例子中是 “mxgames”, 只有一个包。
install_requires是这个包的所需的依赖。
classifiers 是分类。根据 PyPi Classifiers 填写，至少要包含所用的 Python 版本。

```python
"""
Flask-Log-Request-Id
====================

|CircleCI|

**Flask-Log-Request-Id** is an extension for `Flask`_ that can parse and handle
the request-id sent by request processors like `Amazon ELB`_, `Heroku Request-ID`_
or any multi-tier infrastructure as the one used at microservices. A common
usage scenario is to inject the request\\_id in the logging system so that all
log records, even those emitted by third party libraries, have attached the
request\\_id that initiated their call. This can greatly improve tracing and debugging of problems.


Features
--------

Flask-Log-Request-Id provides the ``current_request_id()`` function which can be used
at any time to get the request id of the initiated execution chain. It also comes with
log filter to inject this information on log events as also an extension to forward
the current request id into Celery's workers.


Example: Parse request id and send it to to logging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the following example, we will use the ``RequestIDLogFilter`` to inject
the request id on all log events, and a custom formatter to print this
information. If all these sounds unfamiliar please take a look at `python logging system`_

.. code:: python

    import logging
    import logging.config
    from random import randint
    from flask import Flask
    from flask_log_request_id import RequestID, RequestIDLogFilter

    def generic_add(a, b):
        \"""Simple function to add two numbers that is not aware of the request id\"""
        logging.debug('Called generic_add({}, {})'.format(a, b))
        return a + b

    app = Flask(__name__)
    RequestID(app)

    # Setup logging
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - level=%(levelname)s - request_id=%(request_id)s - %(message)s"))
    handler.addFilter(RequestIDLogFilter())  # << Add request id contextual filter
    logging.getLogger().addHandler(handler)


    @app.route('/')
    def index():
        a, b = randint(1, 15), randint(1, 15)
        logging.info('Adding two random numbers {} {}'.format(a, b))
        return str(generic_add(a, b))


Installation
------------
The easiest way to install it is using ``pip`` from PyPI

.. code:: bash

    pip install flask-log-request-id


License
-------

See the `LICENSE`_ file for license rights and limitations (MIT).


.. _Flask: http://flask.pocoo.org/
.. _Amazon ELB: http://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-request-tracing.html
.. _Heroku Request-ID: https://devcenter.heroku.com/articles/http-request-id
.. _python logging system: https://docs.python.org/3/library/logging.html
.. _LICENSE: https://github.com/Workable/flask-log-request-id/blob/master/LICENSE.md
.. |CircleCI| image:: https://img.shields.io/circleci/project/github/Workable/flask-log-request-id.svg
   :target: https://circleci.com/gh/Workable/flask-log-request-id

"""
import re
import ast
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('flask_log_request_id/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

test_requirements = [
    'nose',
    'flake8',
    'mock==2.0.0',
    'coverage~=4.5.4',
    'celery~=4.3.0'
]

setup(
    name='Flask-Log-Request-ID',
    version=version,
    url='http://github.com/Workable/flask-log-request-id',
    license='MIT',
    author='Konstantinos Paliouras, Ioannis Foukarakis',
    author_email='squarious@gmail.com, ioannis.foukarakis@gmail.com',
    description='Flask extension that can parse and handle multiple types of request-id '
                'sent by request processors like Amazon ELB, Heroku or any multi-tier '
                'infrastructure as the one used for microservices.',
    long_description=__doc__,
    maintainer="Konstantinos Paliouras",
    maintainer_email="squarious@gmail.com",
    packages=[
        'flask_log_request_id',
        'flask_log_request_id.extras'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.8',
    ],
    tests_require=test_requirements,
    setup_requires=[
        "flake8",
        "nose"
    ],
    extras_require={
        'test': test_requirements
    },
    test_suite='nose.collector',
    classifiers=[
        'Environment :: Web Environment', 'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent', 'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ])

```

#### LICENSE

[chooselicense]: https://choosealicense.com/licenses/mit/

> LICENSE.md
>


```markdown
MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### 构建项目

```bash
python setup.py check
python setup.py sdist bdist_wheel
# will generate directory named by dist

```

### 上传

```bash
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
# use username and password from PyPi
```

> 配置用户名密码
>
> ~/.pypric
>
> ```bash
> [distutils]
> index-servers=pypi
> 
> [pypi]
> repository = https://upload.pypi.org/legacy/
> username: [username]
> password: [password]
> ```
>
> ```bash
> twine upload dist/*
> 
> ```



[reference]: https://packaging.python.org/tutorials/packaging-projects/

