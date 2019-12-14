# 关于cookie的同源策略及绕过(跨域)
说明：大致的域名/目录结构：
molibird.com -- molibird.com/index.php
a.molibird.com -- a.molibird.com/index.php
b.molibird.com -- b.molibird.com/index.php

## cookie的"同源策略"和一般的同源策略 区别：
一般的同源策略：需要满足：协议 域名 端口
cookie的"同源策略"：仅仅关注 域名

## cookie的domain属性：
domain决定了 访问页面的时候 哪些cookie是需要发送/可以保存
domain默认值为当前域名

表格：横向是domain的属性值，纵向是请求的网页/域名

域\cookie.domain	          molibird.com	.molibird.com	a.molibird.com	b.molibird.com
molibird.com/index.php	   可以	           可以	         X	            X
a.molibird.com/index.php	 X	            可以	         可以	           X
b.molibird.com/index.php	 X	            可以	         X	            可以

## 绕过限制：
即 设置cookie时 指定具体需要的domain(不用默认值)：

设置domain的要求：
(1)父域名
(2)"子"域名：所有子域名 包括 自己
注意：
无法修改到.com这类顶级域名
无法修改到 具体的子域名 比如 molibird.com 修改到 a.molibird.com
无法修改到"同级域名" 比如 a.molibird.com 修改到 b.molibird.com 是不行的

## example

```python
from flask import Flask
from flask import render_template, request, g, redirect

LOGIN_ADDRESS = 'https://a.molibird.com/index.php'
account_access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X2lkIjoxMDAxNiwiYWNjb3VudF9zdGF0dXMiOiJlbmFibGVkIiwicm9sZXMiOlsicm9vdCIsImFkbWluIl0sInBlcm1zIjpbXSwidXNlcl9pZCI6MTAwMDAwMiwidXNlcl9zdGF0dXMiOiJlbmFibGVkIiwiYWNjb3VudHMiOlsxMDAxNiwxMDAwMDAzLDEwMDAwMDQsMTAwMDAwNSwxMDAwMDA2LDEwMDAwMDcsMTAwMDAwOSwxMDAwMDEwLDEwMDAwMTEsMTAwMDAxNSwxMDAwMDE3LDEwMDAwMjEsMTAwMDAyNSwxMDAwMDI3LDEwMDAwNDRdLCJpc3MiOiJZZXNSMGtjZWZ0R0RTOXNGZjdmbVVhYVRkcm9sUUljRyIsImlhdCI6MTU3NTYyMTM3MiwiZXhwIjoxNTc1NzA3NzcyfQ.btAnJMEVQmZiK7alcPfeWlySLd9OfdQOgDKzypUFlzg'
app = Flask(__name__)


@app.route('/')
def hello():
    response = redirect(LOGIN_ADDRESS, 302)
    response.headers["Access-Control-Allow-Credentials"] = "true"

    response.set_cookie(
        "--MSECPro--",
        account_access_token,
        domain=".molibird.com",
        path='/'
    )

    return response


if __name__ == '__main__':
    app.run()
    # app.run(host='0.0.0.0', port='55100')
```
