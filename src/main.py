from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

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

@socketio.on('join')
def handle_joined(data):
    join_room('main_room')
    emit('update', {'msg': 'Somebody joined'}, room='main_room')

@socketio.on('update_position')
def handle_update_position(position):
    emit('update', {'msg': f"Position of {position['name']} is {position['position']}"}, room='main_room')

@app.route("/map")
def mapview():
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=60.185509859,
        lng=24.824594148,
        markers=[(60.185509859, 24.824594148)]
    )
    sndmap = Map(
        identifier="sndmap",
        lat=60.185509859,
        lng=24.824594148,
        markers=[
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png',
             'lat': 60.186709, 
             'lng': 24.833501,
             'infobox': "<b>Prong 1</b>"
          },
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png',
             'lat': 60.186182, 
             'lng': 24.826143,
             'infobox': "<b>Prong 2</b>"
          },
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
             'lat': 60.189557,
             'lng': 24.829249,
             'infobox': "<b>Pellet</b>"
          },
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
             'lat': 60.176536,
             'lng': 24.834275,
             'infobox': "<b>Target</b>"
          }
        ]
    )
    movingmap = Map(
        identifier="movingmap",
        varname="movingmap",
        lat=60.185509859,
        lng=24.824594148,
        markers=[
            {
                'lat': 60.186709,
                'lng': 24.833501
            }
        ],
        zoom=12
    )

    movingmarkers = [
        {
            'lat': 60.186709, 
            'lng': 24.833501
        },
        {
            'lat': 60.186182,
            'lng': 24.826143
        },
        {
            'lat': 60.189557,
            'lng': 24.829249
        },
        {
            'lat': 60.176536,
            'lng': 24.834275
        }
    ]
    return render_template('map.html', mymap=mymap, sndmap=sndmap, movingmap=movingmap, movingmarkers=movingmarkers)


# # Function to make MongoDBAPI object
# def makeObject(link=link, dbName = "LocalDB", dbCollection="ChariotCloudTable"):
#     mdbobject = MongoDBDriver.MongoDBAPI(link, user, password, authdb)
#     mdbobject.defineDB(dbName)
#     mdbobject.defineCollection(dbCollection)
#     return mdbobject


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=True)