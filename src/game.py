import json

class GameState:
    def __init__(self):
        self.players = {}
        self.target = None

    def add_player(self, nickname):
        self.players[nickname] = Player(nickname)

    def toggle_player_is_shooting(self, nickname):
        if nickname in self.players:
            self.players[nickname].is_shooting = not self.players[nickname].is_shooting

    def remove_player(self, nickname):
        del self.players[nickname]

    def update_player_position(self, nickname, position):
        if nickname in self.players:
            self.players[nickname].latitude = float(position[0])
            self.players[nickname].longitude = float(position[1])

    def update(self):
        pass

    def get_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class Player:
    def __init__(self, nickname, latitude=0., longitude=0.):
        self.nick = nickname
        self.latitude = latitude
        self.longitude = longitude
        self.is_shooting = False


class Target:
    def __init__(self, lat, lon):
        self.latitude = lat
        self.longitude = lon
