import json
from math import trunc

TILESCALE = 40


class Object:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.center = -1
        self.x_right = 0
        self.x_left = 0
        self.y_right = 0
        self.y_left = 0

    def set_coordinates(self, X, Y):
        self.x = X
        self.y = Y

    def set_edge(self, Center, XRight, XLeft, YRight, YLeft):
        self.center = Center
        self.x_right = XRight
        self.x_left = XLeft
        self.y_right = YRight
        self.y_left = YLeft

    def Print(self):
        print("{", self.x, self.y, "}", end='')

    def collision(self, X, Y):
        if self.center == 0:
            if self.x_left + self.x <= X <= self.x_right + self.x:
                if self.y_left + self.y <= Y <= self.y_right + self.y:
                    return 1
                else:
                    return 0
            else:
                return 0
        else:
            return 0


def ReadJson(JsonName):
    with open('test_map_1' + '_config.json', 'r', encoding='utf-8') as TileMapConfig:
        with open(JsonName + '.json', 'r', encoding='utf-8') as TileMap:
            # Reading .json
            DataConfig = json.load(TileMapConfig)
            DataMap = json.load(TileMap)["layers"]

            # Reading all needed data
            for layers in DataConfig["layers"]:
                for datamap in DataMap:
                    if datamap["name"] == layers:
                        Width = datamap["height"]
                        Height = datamap["width"]
                        X = datamap["x"]
                        Y = datamap["y"]
                        Matrix = datamap["data"]
                        XRight = DataConfig["config"][layers]["x_right"]
                        XLeft = DataConfig["config"][layers]["x_left"]
                        YRight = DataConfig["config"][layers]["y_right"]
                        YLeft = DataConfig["config"][layers]["y_left"]
                        Center = DataConfig["config"][layers]["center"]

                # Make matrix of walls
                Walls = [
                    [Object() for _ in range(Width)]
                    for _ in range(Height)
                ]

                # Make all tiles
                for j in range(Height):
                    for i in range(Width):
                        if Matrix[i + j * 20] != 0:
                            norm = j
                            j = 19 - j
                            Walls[j][i].set_edge(
                                Center,
                                XRight,
                                XLeft,
                                YRight,
                                YLeft
                            )
                            Walls[j][i].set_coordinates(
                                X + TILESCALE / 2 + i * TILESCALE,
                                Y + TILESCALE / 2 + j * TILESCALE
                            )
                            j = norm
                        else:
                            norm = j
                            j = 19 - j
                            Walls[j][i].set_edge(
                                -1,
                                0,
                                0,
                                0,
                                0
                            )
                            Walls[j][i].set_coordinates(
                                X + TILESCALE / 2 + i * TILESCALE,
                                Y + TILESCALE / 2 + j * TILESCALE
                            )
                            j = norm

    return Walls


def GetTile(X, Y):
    PosX = trunc(X / TILESCALE)
    PosY = trunc(Y / TILESCALE)
    return [PosX, PosY]


with open('test_map_1' + '_config.json', 'r', encoding='utf-8') as TileMapConfig:
    Data = json.load(TileMapConfig)
    print(Data)

print(ReadJson('test_map_1'))

