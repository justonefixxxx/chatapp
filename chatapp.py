from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile('config.py')
ws = SocketIO(app)

last_messages = []


@app.route('/')
def hello_world():
    return render_template('index.html')


@ws.on('connect', namespace='/chat')
def connect():
    for x in last_messages:
        emit('message', x)


@ws.on('joined_message', namespace='/chat')
def joined_chat(data):
    emit('message', {'username': data['username'],
                     'dateTime': datetime.utcnow().isoformat() + 'Z',
                     'type': 'joined_message'},
         namespace='/chat', broadcast=True)


@ws.on('send_message', namespace='/chat')
def handle_message(data):
    res = {
        'message': data['message'],
        'username': data['username'],
        'dateTime': datetime.utcnow().isoformat() + 'Z',
        'type': 'message'
    }
    emit('message', res, namespace='/chat', broadcast=True)
    if len(res) > 100:
        last_messages.pop(0)
    last_messages.append(res)


if __name__ == '__main__':
    ws.run(app, host='0.0.0.0', port=3001)
