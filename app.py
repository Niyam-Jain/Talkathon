from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, send

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('join_room_view'))  # Correct endpoint name
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle registration logic here
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/join_room', methods=['GET', 'POST'])
def join_room_view():
    if request.method == 'POST':
        session['room'] = request.form['room']
        return redirect(url_for('chat'))
    return render_template('join_room.html')

@app.route('/chat')
def chat():
    if 'username' not in session or 'room' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', username=session['username'], room=session['room'])

@socketio.on('join')
def handle_join(data):
    room = data['room']
    username = data['username']
    join_room(room)
    send({'msg': f"{username} has joined the room."}, to=room)

@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    username = data['username']
    leave_room(room)
    send({'msg': f"{username} has left the room."}, to=room)


@socketio.on('message')
def handle_message(data):
    room = data['room']
    send({'msg': data['msg'], 'username': data['username']}, to=room)

if __name__ == '__main__':
    socketio.run(app)
