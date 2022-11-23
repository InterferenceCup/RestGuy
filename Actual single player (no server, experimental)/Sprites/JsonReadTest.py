import json
from math import trunc

<<<<<<< HEAD
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
=======

# Class for Walls named Object
class Object:
    def __init__(self):
        self.x = 0  # Create x
        self.y = 0  # Create y
        self.center = -1  # Create center (existing of wall)
        self.x_right = 0  # X right board
        self.x_left = 0  # X left board
        self.y_top = 0  # Y top board
        self.y_down = 0  # Y down board
>>>>>>> origin/Pavel-was-here

    def set_coordinates(self, X, Y):
        self.x = X
        self.y = Y

<<<<<<< HEAD
    def set_edge(self, Center, XRight, XLeft, YRight, YLeft):
        self.center = Center
        self.x_right = XRight
        self.x_left = XLeft
        self.y_right = YRight
        self.y_left = YLeft
=======
    def set_edge(self, Center, XRight, XLeft, YTop, YDown):
        self.center = Center
        self.x_right = XRight
        self.x_left = XLeft
        self.y_top = YTop
        self.y_down = YDown
>>>>>>> origin/Pavel-was-here

    def Print(self):
        print("{", self.x, self.y, "}", end='')

    def collision(self, X, Y):
        if self.center == 0:
            if self.x_left + self.x <= X <= self.x_right + self.x:
<<<<<<< HEAD
                if self.y_left + self.y <= Y <= self.y_right + self.y:
=======
                if self.y_down + self.y <= Y <= self.y_top + self.y:
>>>>>>> origin/Pavel-was-here
                    return 1
                else:
                    return 0
            else:
                return 0
        else:
            return 0


<<<<<<< HEAD
def ReadJson(JsonName):
    with open('test_map_1' + '_config.json', 'r', encoding='utf-8') as TileMapConfig:
=======
def GetTileScale(JsonName):
    with open(JsonName + '_config.json', 'r', encoding='utf-8') as TileMapConfig:
        Data = json.load(TileMapConfig)
        TileScale = Data["tile"] * Data["scale"]
    return TileScale


def GetScale(JsonName):
    with open(JsonName + '_config.json', 'r', encoding='utf-8') as TileMapConfig:
        Scale = json.load(TileMapConfig)["scale"]
    return Scale


def GetBoards(JsonName):
    with open('Sprites/' + JsonName + '_config.json', 'r', encoding='utf-8') as TileMapConfig:
        Data = json.load(TileMapConfig)
    return [Data["config"]["map_width"], Data["config"]["map_height"]]


def ReadJson(JsonName):
    with open(JsonName + '_config.json', 'r', encoding='utf-8') as TileMapConfig:
>>>>>>> origin/Pavel-was-here
        with open(JsonName + '.json', 'r', encoding='utf-8') as TileMap:
            # Reading .json
            DataConfig = json.load(TileMapConfig)
            DataMap = json.load(TileMap)["layers"]

<<<<<<< HEAD
=======
            # Matrix value
            Width = DataMap[0]["height"]
            Height = DataMap[0]["width"]
            Scale = DataConfig["scale"]
            TileScale = DataConfig["tile"] * Scale

            # Make matrix of walls
            Walls = [
                [Object() for _ in range(Width)]
                for _ in range(Height)
            ]
            for j in range(Height):
                for i in range(Width):
                    Walls[j][i].set_coordinates(
                        TileScale / 2 + i * TileScale,
                        TileScale / 2 + j * TileScale
                    )

            # Make matrix for path
            Path = [
                [-1 for _ in range(Width)]
                for _ in range(Height)
            ]

>>>>>>> origin/Pavel-was-here
            # Reading all needed data
            for layers in DataConfig["layers"]:
                for datamap in DataMap:
                    if datamap["name"] == layers:
<<<<<<< HEAD
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

=======
                        Matrix = datamap["data"]
                        XRight = DataConfig["config"][layers]["x_right"] * Scale
                        XLeft = DataConfig["config"][layers]["x_left"] * Scale
                        YTop = DataConfig["config"][layers]["y_top"] * Scale
                        YDown = DataConfig["config"][layers]["y_down"] * Scale
                        Center = DataConfig["config"][layers]["center"] * Scale

                        # Make all tiles
                        for j in range(Height):
                            for i in range(Width):
                                if Matrix[i + j * Height] != 0:
                                    Walls[Width - 1 - j][i].set_edge(
                                        Center,
                                        XRight,
                                        XLeft,
                                        YTop,
                                        YDown
                                    )
                                else:
                                    Path[i][Height - j - 1] = 1
    return Walls, Path


def GetTile(X, Y, TileScale):
    PosX = trunc(X / TileScale)
    PosY = trunc(Y / TileScale)
    return [PosX, PosY]


def GetConfig(JsonName):
    with open(JsonName + '.json', 'r', encoding='utf-8') as Config:
        Data = json.load(Config)
    return [Data["screen_height"], Data["screen_width"], Data["title"]]
>>>>>>> origin/Pavel-was-here
