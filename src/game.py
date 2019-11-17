import json

class GameState:
    def __init__(self):
        self.players = {}
        self.target = None
        self.pelletExists = False
        self.dingos = [
            "https://users.aalto.fi/~villev1/junc2019/img/base_dingus.svg",
        "https://users.aalto.fi/~villev1/junc2019/img/sweat_dingus.svg",
        "https://users.aalto.fi/~villev1/junc2019/img/spiral_dingus.svg"
        ]
        self.playerCount = 0

    def add_player(self, nickname):
        print ("PRINTING NICKNAME IN GAME.PY", nickname)
        if self.playerCount >= 2:
            return "Already have 3 players"

        #self.players[nickname] = Player(nickname)

        if not self.pelletExists:
            self.players[nickname] = Player(nickname,"pellet", self.dingos[self.playerCount])
            #self.players[nickname].role = "pellet"
            self.pelletExists = True
        else:
            self.players[nickname] = Player(nickname,"prong", self.dingos[self.playerCount])
            #self.players[nickname].role = "prong"
        return "Added player " + self.players[nickname].nickname + " with role " + self.players[nickname].role

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
    def __init__(self, nickname, role, dingo, latitude=0., longitude=0.):
        self.nickname = nickname
        self.latitude = latitude
        self.longitude = longitude
        #self.is_shooting = False
        self.role = role
        self.dingo = dingo


class Target:
    def __init__(self, lat, lon):
        self.latitude = lat
        self.longitude = lon
