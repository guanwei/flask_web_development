## 第3章： 模板

### 3.1 Jinja2模板引擎

形式最简单的Jinja2模板就是一个包含响应文本的文件

templates/index.html
```
<h1>Hello World!</h1>
```

包含一个使用变量表示的动态部分

templates/user.html
```
<h1>Hello, {{ name }}!</h1>
```

#### 3.1.1 渲染模板

默认情况下，Flask在程序文件夹中的templates子文件夹中寻找模板

Flask提供的render_template函数把Jinja2模板引擎集成到程序中

hello.py
```
from flask import Flask, render_template

# ...

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
```

#### 3.1.2 变量

Jinja2能识别所有类型的变量
```
<p>A value from a directroy: {{ mydict['key'] }}.</p>
<p>A value from a list: {{ mylist[3] }}.</p>
<p>A value from a list, with a variale index: {{ mylist[myintvar] }}.</p>
<p>A value from an object's method: {{ myobj.somemethod() }}.</p>
```

可以使用过滤器修改变量
```
Hello, {{ name|capitalize }}
```

Jinja2变量过滤器

过滤器名 | 说明
---|---
safe | 渲染值时不转义
capitalize | 把值的首字母转换成大写，其他字母转换成小写
lower | 把值转换成小写形式
upper | 把值转换成大写形式
title | 把值中的每个单词的首字母都转换成大写
trim | 把值的首尾空格去掉
striptags | 渲染之前把值中所有的HTML标签都删除掉

#### 3.1.3 控制结构

Jinja2提供了多种控制结构，可用来改变模板的渲染流程

条件控制语句
```
{% if user %}
    Hello, {{ user }}
{% else %}
    Hello, stranger!
{% endif %}
```

使用for循环
```
<ul>
    {% for comment in comments %}
        <li>{{ comment }}</li>
    {% endfor %}
</ul>
```

Jinja2还支持宏
```
{% macro render_comment(comment) %}
    <li>{{ comment }}</li>
{% endmacro %}

<ul>
    {% for comment in comments %}
        {{ render_comment(comment) }}
    {% endfor %}
</ul>
```

可以将宏保存在单独的文件中，在需要使用的模板中导入
```
{% import 'macros.html' as macros %}
<ul>
    {% for comment in comments %}
        {{ macros.render_comment(comment) }}
    {% endfor %}
</ul>
```

可以将模板代码片段写入单独的文件中，再包含在所有模板中
```
{% include 'common.html' %}
```

另一种重复使用代码的强大方式是模板继承

首先，创建一个名为base.html的基模板
```
<html>
    <head>
        {% block head %}
        <title>{% block title%}{% endblock %} - My Application</title>
        <% endblock %>
    </head>
    <body>
        <% block body %>
        <% endblock %>
    </body>
</html>
```

下面代码是基模板的衍生模板
```
{% extends "base.html" %}
{% block title %}Index{% endblock %}
{% block head %}
    {{ super() }}
    <style>
    </style>
{% endblock %}
<% block body %>
<h1>Hello World!</h1>
<% endblock %>
```

`extends`指令声明这个模板衍生自base.html，使用`super()`获得原来的内容

### 3.2 使用Flask-Bootstrap集成Twitter Bootstrap

Bootstrap (http://getbootstrap.com/)是Twitter开发的一个开源框架，提供用户界面组件可用于创建整洁且具有吸引力的网页

安装Flask-Bootstrap的Flask扩展
```
(venv) $ pip install flask-bootstrap
```

hello.py: 初始化Flask-Bootstrap
```
from flask_bootstrap import Bootstrap
# ...
bootstrap = Bootstrap(app)
```

templates/user.html: 使用Flask-Bootstrap的模板
```
{% extends "bootstrap/base.html" %}

{% block title %}Flasky{% endblock %}

{% block navbar %}
<div class="navbar navbar-inverse" role="navigation">
    <div class="container">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="/">Flasky</a>
        </div>
        <div class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
                <li><a href="/">Home</a></li>
            </ul>
        </div>
    </div>
</div>
{% endblock %}

{% block content %}
<div class="container">
    <div class="page-header">
        <h1>Hello, {{ name }}!</h1>
    </div>
</div>
{% endblock %}
```

如果要在衍生模板中添加新的JavaScript文件，需要这么定义scripts块
```
{% block scripts %}
{{ super() }}
<script type="text/javascript" src="my-script.js"></script>
{% endblock %}
```

### 3.3 自定义错误页面

