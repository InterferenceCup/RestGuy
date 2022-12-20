import json
import os
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
    with open("Maps/" + JsonName + "/" + JsonName + '_config.json', 'r', encoding='utf-8') as TileMapConfig:
        Data = json.load(TileMapConfig)
        TileScale = Data["tile"] * Data["scale"]
    return TileScale


def GetScale(JsonName):
    with open("Maps/" + JsonName + "/" + JsonName + '_config.json', 'r', encoding='utf-8') as TileMapConfig:
        Scale = json.load(TileMapConfig)["scale"]
    return Scale


def GetBoards(JsonName):
    with open("Maps/" + JsonName + "/" + JsonName + '_config.json', 'r', encoding='utf-8') as TileMapConfig:
        Data = json.load(TileMapConfig)
    return [Data["config"]["map_width"], Data["config"]["map_height"]]


def GetConfigMap(JsonName):
    with open("Maps/" + JsonName + "/" + JsonName + '_config.json', 'r', encoding='utf-8') as TileMapConfig:
        DataConfig = json.load(TileMapConfig)
    return DataConfig


def ReadJson(JsonName):
    with open("Maps/" + JsonName + "/" + JsonName + '_config.json', 'r', encoding='utf-8') as TileMapConfig:
        with open("Maps/" + JsonName + "/" + JsonName + '.json', 'r', encoding='utf-8') as TileMap:
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

            # Reading all needed data
            Matrix = DataMap[1]["data"]
            for h in range(Height):
                for w in range(Width):
                    if Matrix[w + h * Width] != 0:
                        XRight = DataConfig["config"][str(Matrix[w + h * Width] - 1)]["x_right"] * Scale
                        XLeft = DataConfig["config"][str(Matrix[w + h * Width] - 1)]["x_left"] * Scale
                        YTop = DataConfig["config"][str(Matrix[w + h * Width] - 1)]["y_top"] * Scale
                        YDown = DataConfig["config"][str(Matrix[w + h * Width] - 1)]["y_down"] * Scale
                        Center = DataConfig["config"][str(Matrix[w + h * Width] - 1)]["center"] * Scale
                        Walls[Height - 1 - h][w].set_edge(
                            Center,
                            XRight,
                            XLeft,
                            YTop,
                            YDown
                        )
    return Walls


def GetPath(JsonName):
    with open("Maps/" + JsonName + "/" + JsonName + '.json', 'r', encoding='utf-8') as TileMap:
        # Reading .json
        DataMap = json.load(TileMap)["layers"]

        # Matrix value
        Width = DataMap[0]["height"]
        Height = DataMap[0]["width"]
        Path = [[-1 for _ in range(Width)] for _ in range(Height)]
        Matrix = DataMap[1]["data"]
        for h in range(Height):
            for w in range(Width):
                if Matrix[w + h * Width] == 0:
                    Path[Height - h - 1][w] = 1
        Matrix = DataMap[0]["data"]
        for h in range(Height):
            for w in range(Width):
                if Matrix[w + h * Width] == 0:
                    Path[Height - h - 1][w] = -1
    return Path


def GetTile(X, Y, TileScale):
    PosX = trunc(X / TileScale)
    PosY = trunc(Y / TileScale)
    return [PosX, PosY]


def GetConfig(JsonName):
    with open(JsonName + '.json', 'r', encoding='utf-8') as Config:
        Data = json.load(Config)
    return [Data["screen_height"], Data["screen_width"], Data["title"]]


def GetLastIp():
    with open('config.json', 'r', encoding='utf-8') as Config:
        Data = json.load(Config)
    return Data["last_ip"]


def GetLastPort():
    with open('config.json', 'r', encoding='utf-8') as Config:
        Data = json.load(Config)
    return Data["last_port"]


def SetLastIp(Ip):
    with open('config.json', 'r', encoding='utf-8') as Config:
        Data = json.load(Config)
    Data['last_ip'] = Ip
    with open('config.json', 'w') as Config:
        json.dump(Data, Config, indent=4)


def SetLastPort(Port):
    with open('config.json', 'r', encoding='utf-8') as Config:
        Data = json.load(Config)
    Data['last_port'] = Port
    with open('config.json', 'w') as Config:
        json.dump(Data, Config, indent=4)


def GetLastPassword():
    with open('config.json', 'r', encoding='utf-8') as Config:
        Data = json.load(Config)
    return Data["last_password"]


def GetLastUsername():
    with open('config.json', 'r', encoding='utf-8') as Config:
        Data = json.load(Config)
    return Data["last_username"]


def SetLastUsername(Username):
    with open('config.json', 'r', encoding='utf-8') as Config:
        Data = json.load(Config)
    Data['last_username'] = Username
    with open('config.json', 'w') as Config:
        json.dump(Data, Config, indent=4)


def SetLastPassword(Password):
    with open('config.json', 'r', encoding='utf-8') as Config:
        Data = json.load(Config)
    Data['last_password'] = Password
    with open('config.json', 'w') as Config:
        json.dump(Data, Config, indent=4)


def WriteName(Name):
    Data = {
        "name": Name
    }
    with open('Name.json', 'w') as NameFile:
        json.dump(Data, NameFile, indent=4)


def ReadName():
    with open('Name.json', 'r', encoding='utf-8') as NameFile:
        Data = json.load(NameFile)
    os.remove('Name.json')
    return Data["name"]


def ReadPlayer():
    with open('config.json', 'r', encoding='utf-8') as Config:
        Data = json.load(Config)
    return Data["player"]

def GetObjects(Map):
    with open("Maps/" + Map + "/" + Map + '_config.json', 'r', encoding='utf-8') as Config:
        Data = json.load(Config)
    return Data["objects"]

def GetTables(Map):
    with open("Maps/" + Map + "/" + Map + '_config.json', 'r', encoding='utf-8') as Config:
        Data = json.load(Config)
    return Data["tables"]
