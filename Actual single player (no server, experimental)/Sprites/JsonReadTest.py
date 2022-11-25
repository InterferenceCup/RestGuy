import json
from math import trunc


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

    def set_coordinates(self, X, Y):
        self.x = X
        self.y = Y

    def set_edge(self, Center, XRight, XLeft, YTop, YDown):
        self.center = Center
        self.x_right = XRight
        self.x_left = XLeft
        self.y_top = YTop
        self.y_down = YDown

    def Print(self):
        print("{", self.x, self.y, "}", end='')

    def collision(self, X, Y):
        if self.center == 0:
            if self.x_left + self.x <= X <= self.x_right + self.x:
                if self.y_down + self.y <= Y <= self.y_top + self.y:
                    return 1
                else:
                    return 0
            else:
                return 0
        else:
            return 0


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
        with open(JsonName + '.json', 'r', encoding='utf-8') as TileMap:
            # Reading .json
            DataConfig = json.load(TileMapConfig)
            DataMap = json.load(TileMap)["layers"]

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

            # Reading all needed data
            for layers in DataConfig["layers"]:
                for datamap in DataMap:
                    if datamap["name"] == layers:
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