from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from game import GameState
import json


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

game_state = GameState()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_joined(data):
    nickname = data['nickname']
    game_state.add_player(nickname)

@socketio.on('update_position')
def handle_update_position(data):
    game_state.update_player_position(data['nickname'], data['position'])


@socketio.on('shoot')
def handle_shoot(data):
    nickname = data['nickname']
    game_state.toggle_player_is_shooting(nickname)

@app.route("/map")
def mapview():
    # creating a map in the view
    movingmap = Map(
        identifier="movingmap",
        varname="movingmap",
        lat=60.185509859,
        lng=24.824594148,
        markers=[
            {
             'icon': 'https://users.aalto.fi/~villev1/junc2019/img/base_small.svg',
             'lat': 60.186709, 
             'lng': 24.833501,
             'infobox': "<b>Prong 1</b>"
          },
          {
             'icon': 'https://users.aalto.fi/~villev1/junc2019/img/sweat_small.svg',
             'lat': 60.186182, 
             'lng': 24.826143,
             'infobox': "<b>Prong 2</b>"
          },
          {
             'icon': 'https://users.aalto.fi/~villev1/junc2019/img/spiral_small.svg',
             'lat': 60.189557,
             'lng': 24.829249,
             'infobox': "<b>Pellet</b>"
          },
          {
             'icon': 'https://users.aalto.fi/~villev1/junc2019/img/angerroo_small.svg',
             'lat': 60.176536,
             'lng': 24.834275,
             'infobox': "<b>Target</b>"
          }
        ],
    )
    return render_template('map.html', movingmap=movingmap)


# # Function to make MongoDBAPI object
# def makeObject(link=link, dbName = "LocalDB", dbCollection="LocalCollection"):
#     mdbobject = MongoDBDriver.MongoDBAPI(link)
#     mdbobject.defineDB(dbName)
#     mdbobject.defineCollection(dbCollection)
#     return mdbobject


class Thread(object):
    def __init__(self):
        self.thread = None

    def start_server(self):
        socketio.run(app, debug=True, port=80, use_reloader=False)

    def start(self):
        self.thread = socketio.start_background_task(self.start_server)

    def wait(self):
        self.thread.join()


if __name__ == '__main__':
    t = Thread()
    t.start()


    while True:
        socketio.sleep(1)
        game_state.update()
        socketio.emit('state_update', game_state.get_json(), scope='/map')
        print('Sent updated state')

    socketio.wait()
