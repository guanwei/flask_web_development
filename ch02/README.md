## 第二章：程序的基本结构

### 2.1 初始化

使用下面代码创建Flask类的对象
```
from flask import Flask
app = Flask(__name__)
```

### 2.2 路由和视图函数

处理URL和函数之间关系的程序成为路由

使用程序实例提供的app.route修饰器，把修饰的函数注册为路由，像index()这样的函数称为视图函数（view function）
```
@app.route('/')
def index():
    return '<h1>Hello World!</h1>'
```

route修饰器使用特殊的句法支持动态部分，尖括号中的内容就是动态部分
```
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name
```

### 2.3 启动服务器

程序实例用run方法启动Flask集成的开发Web服务器
```
if __name__ == '__main__':
    app.run(debug=True)
```

### 2.4 一个完整的程序

hello.py: 一个完整的Flask程序
```
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

if __name__ == '__main__':
    app.run(debug=True)
```

使用下面命令启动程序
```
(venv) $ python hello.py
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 849-979-998
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

hello.py: 包含动态路由的Flask程序
```
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello %s!</h1>' % name

if __name__ == '__main__':
    app.run(debug=True)
```

### 2.5 请求-响应循环

#### 2.5.1 程序和请求上下文

Flask使用上下文临时把某些对象变为全局访问
```
from flask import request

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent
```

Flask使用上下文让特定的变量在一个线程中全局可访问，与此同时却不会干扰其他线程

在Flask中有两种上下文：程序上下文和请求上下文

变量名 | 上下文 | 说明
---|---|---
current_app | 程序上下文 | 当前激活程序的程序实例
g | 程序上下文 | 处理请求时用作临时存储的对象。每次请求都会重设这个变量
request | 请求上下文 | 请求对象，封装了客户端发出的HTTP请求中的内容
session | 请求上下文 | 用户会话，用于存储请求之间要“记住”的值的字典

Python shell会话演示程序上下文的使用方法
```
(venv) $ python
>>> from hello import app
>>> from flask import current_app
>>> current_app.name
Traceback (most recent call last):
...
RuntimeError: working outside of application context
>>> app_ctx = app.app_context()
>>> app_ctx.push()
>>> current_app.name
'hello'
>>> app_ctx.pop()
```

#### 2.5.2 请求调度

在Python shell中检查为hello.py生成的映射
```
(venv) $ python
>>> from hello import app
>>> app.url_map
Map([<Rule '/' (HEAD, OPTIONS, GET) -> index>,
  <Rule '/static/<filename>' (HED, OPTIONS, GET) -> static>,
  <Rule '/user/<name>' (HEAD, OPTIONS, GET) -> user>])
```

`/static/<filename>`路由是Flask添加的特殊路由

#### 2.5.3 请求钩子

请求钩子使用修饰器来实现。Flask支持以下4种钩子
- before_first_request: 注册一个函数，在处理第一个请求之前运行
- before_request: 注册一个函数，在每次请求之前运行
- after_request: 注册一个函数，如果没有未处理的异常抛出，在每次请求之后运行
- teardown_request: 注册一个函数，即使有未处理的异常抛出，也在每次请求之后运行

在请求钩子和视图函数之间共享数据一般使用上下文全局变量`g`

#### 2.5.4 响应

如果视图函数返回的响应需要使用不同的状态码，那么可以把数字代码作为第二个返回值，添加到响应文本之后
```
@app.route('/')
def index():
    return '<h1>Bad Request</h1>', 400
```

Flask视图函数还可以返回Request对象。下面代码创建一个响应对象，然后设置了cookie
```
from flask import make_response

@app.route('/')
def index():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response
```

Flask提供了redirect()辅助函数，用于生成重定向响应
```
from flask import Flask

@app.route('/')
def index():
    return redirect('http://www.example.com')
```

还有一种特殊的响应由abort函数生成，用于处理错误
```
from flask import abort

@app.route('/user/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return '<h1>Hello, %s</h1>' % user.name
```

abort抛出异常把控制权交给Web服务器

### 2.6 Flask扩展

Flask-Script是一个Flask扩展，为Flask程序添加一个命令行解析器

安装Flask-Script扩展
```
(venv) $ pip install flask-script
```

hello.py: 使用Flask-Script
```
from flask_script import Manager
manager = Manager(app)

# ...

if __name__ == '__main__':
    manager.run()
```

运行hello.py，会显示用法帮助
```
(venv) $ python hello.py
usage: hello.py [-?] {shell,runserver} ...

positional arguments:
  {shell,runserver}
    shell            Runs a Python shell inside Flask application context.
    runserver        Runs the Flask development server i.e. app.run()

optional arguments:
  -?, --help         show this help message and exit
```

下面命令让Web服务器监听公共网络接口上的连接
```
(venv) $ python hello.py runserver --host 0.0.0.0
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```