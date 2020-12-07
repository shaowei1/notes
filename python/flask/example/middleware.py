from werkzeug.wrappers import Request, Response, ResponseStream
from flask import Flask, request


class UserVerifyMiddleware:
    """
    Simple WSGI middleware
    """
    def __init__(self, app):
        """
         a constructor which is required to encapsulate the flask app object
        :param app:
        """
        self.app = app
        self.userName = 'Tony'
        self.password = 'IamIronMan'

    def __call__(self, environ, start_response):
        """
        provide a callable that provides a WSGI application interface
        符合WSGI标准的一个HTTP处理函数

        :param environ: 一个包含所有HTTP请求信息的dict对象；
        :param start_response: 一个发送HTTP响应的函数
        :return: an iterable response after initiating a response with start_response
        """
        request = Request(environ)
        userName = request.authorization['username']
        password = request.authorization['password']

        # these are hardcoded for demonstration
        # verify the username and password from some database or env config variable
        if userName == self.userName and password == self.password:
            environ['user'] = {'name': 'Tony'}
            return self.app(environ, start_response)

        res = Response(u'Authorization failed', mimetype='text/plain', status=401)
        return res(environ, start_response)


app = Flask('DemoApp')

# calling our middleware
app.wsgi_app = UserVerifyMiddleware(app.wsgi_app)

@app.route('/', methods=['GET', 'POST'])
def hello():
    user = request.environ['user']
    return f"Hi {user['name']}"

if __name__ == "__main__":
    app.run('0.0.0.0', '5000', debug=True)

"""
$ curl -u Tony:IamBatMan http://localhost:5000
Authorization failed
$ curl -u Tony:IamIronMan http://localhost:5000
Hi Tony
"""