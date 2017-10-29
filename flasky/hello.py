from flask import Flask, request, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap

app = Flask(__name__)

manager = Manager(app)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    #user_agent = request.headers.get('User-Agent')
    #return '<h1>Hello World</h1>\n<p>Your browser is %s</p>' % user_agent
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    #return '<h1>Hello, %s!</h1>' % name
    return render_template('user.html', name=name)

if __name__ == '__main__':
    manager.run()