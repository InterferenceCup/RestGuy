import json
import os
from shutil import copyfile as Copy

'''def Crop(Path, Input, Height, Width):
    if not os.path.isdir(Path):
        os.mkdir(Path)
    Im = Image.open("Skeleton/" + str(ReadName(Input, k)))
    ImWidth, ImHeight = Im.size
    k = 1
    area = (0, 0, 64, 64)
    for i in range(0, ImHeight, Height):
        for j in range(0, ImWidth, Width):
            Tile = (j, i, j + ImWidth, i + ImHeight)
            NewImage = Im.crop(Tile)
            NewImage = NewImage.crop(area)
            NewImage.save(Path + "/" + str(ReadName(Input, k)) + ".png", "PNG")
            k += 1'''


def CreateLayerPrototype():
    Layer = {
        "data": [],
        "height": 0,
        "id": 1,
        "name": "layer",
        "opacity": 1,
        "type": "tilelayer",
        "visible": True,
        "width": 0,
        "x": 0,
        "y": 0,
    }
    return Layer


def ReadLayers(JsonName):
    with open("Skeleton/" + JsonName + '.json', 'r', encoding='utf-8') as TileMap:
        Layers = json.load(TileMap)["layers"]
    return Layers


def ReadAllFile(JsonName):
    with open("Skeleton/" + JsonName + '.json', 'r', encoding='utf-8') as TileMap:
        File = json.load(TileMap)
    return File


def PrintFile(JsonName, File, Layers):
    with open("Maps/" + JsonName + "/" + JsonName + '.json', 'w') as TileMap:
        File["layers"] = Layers
        File["tilesets"][0]["source"] = JsonName + "_tiles.json"
        json.dump(File, TileMap, indent=4)


def EditConfig(JsonName):
    with open("Maps/" + JsonName + "/" + JsonName + '_tiles.json', 'r', encoding='utf-8') as TileConfig:
        File = json.load(TileConfig)
    with open("Maps/" + JsonName + "/" + JsonName + '_tiles.json', 'w') as TileConfig:
        File["image"] = JsonName + ".png"
        json.dump(File, TileConfig, indent=4)


def PrintFileConfig(JsonName, File):
    with open("Maps/" + JsonName + "/" + JsonName + '_config.json', 'w') as TileMap:
        json.dump(File, TileMap, indent=4)


def ReadName(JsonName, ID):
    with open("Skeleton/" + JsonName, 'r', encoding='utf-8') as Tiles:
        Tile = json.load(Tiles)["tiles"]
        for tile in Tile:
            if tile["id"] == ID - 1:
                return tile["id"]


def GetTileSet(JsonName):
    with open("Skeleton/" + JsonName + '.json', 'r', encoding='utf-8') as TileMap:
        Set = json.load(TileMap)["tilesets"][0]["source"]
    return Set


def GetImage(JsonName):
    with open("Skeleton/" + JsonName, 'r', encoding='utf-8') as TileConfig:
        Im = json.load(TileConfig)["image"]
    return Im


def CopyAll(JsonName):
    if not os.path.isdir("Maps/" + JsonName + "/"):
        os.mkdir("Maps/" + JsonName + "/")
    Copy("Skeleton/" + GetTileSet(JsonName), "Maps/" + JsonName + "/" + JsonName + "_tiles.json")
    Copy("Skeleton/" + GetImage(GetTileSet(JsonName)), "Maps/" + JsonName + "/" + JsonName + ".png")


def Splitting(JsonName, Layers):
    Numbers = []
    NewLayers = []
    Data = Layers[1]["data"]
    Height = Layers[1]["height"]
    Width = Layers[1]["width"]
    NewLayers.append(Layers[0])

    for tile in Data:
        if tile not in Numbers:
            Numbers.append(tile)

    for number in Numbers:
        if number != 0:
            Matrix = [0 for _ in range(Width * Height)]
            for j in range(Height):
                for i in range(Width):
                    if Data[i + j * Height] == number:
                        Matrix[i + j * Height] = number
                    else:
                        Matrix[i + j * Height] = 0
            NewLayers.append(CreateLayerPrototype())
            NewLayers[-1]["data"] = Matrix
            NewLayers[-1]["name"] = ReadName(GetTileSet(JsonName), number)
            NewLayers[-1]["width"] = Width
            NewLayers[-1]["height"] = Height

    return NewLayers


def ReadNewLayers(JsonName):
    with open("Maps/" + JsonName + "/" + JsonName + '.json', 'r', encoding='utf-8') as TileMap:
        Layers = json.load(TileMap)["layers"]
    return Layers


def CreateConfig(JsonName, Layers):
    Config = {
        "layers": [],
        "scale": 1,
        "tile": 64,
        "config": {
            "map_width": Layers[0]["width"] * 64,
            "map_height": Layers[0]["height"] * 64
        }
    }

    for layers in Layers:
        if layers["name"] != "Base":
            Config["layers"].append(layers["name"])
            Config["config"][layers["name"]] = {
                "y_top": 32,
                "y_down": -32,
                "x_right": 32,
                "x_left": -32,
                "center": 0
            }

    PrintFileConfig(JsonName, Config)


def main():
    # INPUT
    print("EnterMapName: ", end="")
    JsonName = input()

    # FIRST CREATION
    CopyAll(JsonName)
    Layers = ReadLayers(JsonName)
    NewLayers = Splitting(JsonName, Layers)
    File = ReadAllFile(JsonName)
    PrintFile(JsonName, File, NewLayers)
    EditConfig(JsonName)
    # Crop("Maps/" + JsonName + "/Sprite", JsonName, 64, 64)

    # SECOND CREATION
    CreateConfig(JsonName, ReadNewLayers(JsonName))


main()
