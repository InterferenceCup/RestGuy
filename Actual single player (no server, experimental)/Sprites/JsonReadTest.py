import json
from math import trunc

TILESCALE = 64


class Object:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.center = 0
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
        if self.x_left <= X <= self.x_right:
            return 1
        elif self.y_left <= Y <= self.y_right:
            return 1
        else:
            return 0


def ReadJson(JsonName):
    with open(JsonName + '.json', 'r', encoding='utf-8') as TileMap:
        # Reading .json
        Data = json.load(TileMap)

        # Reading all needed data
        Width = Data["layers"][1]["height"]
        Height = Data["layers"][1]["width"]
        Center = Data["layers"][1]["center"]
        X = Data["layers"][1]["x"]
        Y = Data["layers"][1]["y"]
        XRight = Data["layers"][1]["x_right"]
        XLeft = Data["layers"][1]["x_left"]
        YRight = Data["layers"][1]["y_right"]
        YLeft = Data["layers"][1]["y_left"]
        Matrix = Data["layers"][1]["data"]

        # Make matrix of walls
        Walls = [
            [Object() for _ in range(Width)]
            for _ in range(Height)
        ]

        # Make all tiles
        for j in range(Height):
            for i in range(Width):
                if Matrix[i + j * 20] != 0:
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

        # Print Walls
        for j in range(Height):
            for i in range(Width):
                Walls[j][i].Print()
            print()


def GetTile(X, Y):
    PosX = trunc(X / TILESCALE)
    PosY = trunc(Y / TILESCALE)
    return [PosX, PosY]


ReadJson('test_map_1')
print(GetTile(64, 64))