from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit
from flask_googlemaps import GoogleMaps

# initialize Flask
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')
GoogleMaps(
    app,
    key="AIzaSyBmm32aJXraStLKXAG0J3rpyWIDOSM0w2E"
)

socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('joined')
def handle_joined(message):
    join_room('main_room')
    emit('update', {'msg': 'Somebody joined'}, room='main_room')


@socketio.on('update_position')
def handle_text(position):
    emit('update', {'msg': f"Position of {position['name']} is {position['position']}"}, room='main_room')



if __name__ == '__main__':
    socketio.run(app, debug=True)