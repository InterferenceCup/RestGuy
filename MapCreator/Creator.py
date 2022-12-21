import json
import os
import random
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


def PrintFile(JsonName, File):
    with open("Maps/" + JsonName + "/" + JsonName + '.json', 'w') as TileMap:
        # File["layers"] = Layers
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
    NewLayers.append(Layers[2])

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


def CreateConfig(JsonName, Layers, Tables, Objects, Fridge, Bowls, Spawn):
    Config = {
        "layers": [],
        "scale": 1,
        "tile": 64,
        "config": {
            "map_width": Layers[0]["width"] * 64,
            "map_height": Layers[0]["height"] * 64
        },
        "tables": Tables,
        "objects": Objects,
        "fridge": Fridge,
        "bowls": Bowls,
        "spawn": Spawn
    }

    Matrix = Layers[1]["data"]
    Height = Layers[1]["height"]
    Width = Layers[1]["width"]
    for h in range(Height):
        for w in range(Width):
            if Matrix[w + h * Width] != 0 and not Matrix[w + h * Width] - 1 in Config["layers"]:
                Config["layers"].append(Matrix[w + h * Width] - 1)
                Config["config"][str(Matrix[w + h * Width] - 1)] = {
                    "y_top": 32,
                    "y_down": -32,
                    "x_right": 32,
                    "x_left": -32,
                    "center": 0
                }

    PrintFileConfig(JsonName, Config)


def CreateTables(Layers):
    Layer = None
    for layer in Layers:
        if layer["name"] == "Tables":
            Layer = layer
    Tables = []
    Matrix = Layer["data"]
    Height = Layer["height"]
    Width = Layer["width"]
    for h in range(Height):
        for w in range(Width):
            if Matrix[w + h * Width] != 0:
                Tables.append({
                    'x': w,
                    'y': Width - 1 - h,
                    'delta_x': 0,
                    'delta_y': 0
                })

    return Tables

def CreateSpawn(Layers):
    Layer = None
    for layer in Layers:
        if layer["name"] == "Spawn":
            Layer = layer
    Spawn = []
    Matrix = Layer["data"]
    Height = Layer["height"]
    Width = Layer["width"]
    for h in range(Height):
        for w in range(Width):
            if Matrix[w + h * Width] != 0:
                Spawn.append({
                    'x': w,
                    'y': Width - 1 - h
                })

    return Spawn

def CreateBowls(Layers):
    for layer in Layers:
        if layer["name"] == "Bowls":
            Layer = layer
    Bowls = []
    Matrix = Layer["data"]
    Height = Layer["height"]
    Width = Layer["width"]
    for h in range(Height):
        for w in range(Width):
            if Matrix[w + h * Width] != 0:
                Bowls.append({
                    'x': w,
                    'y': Width - 1 - h,
                    'delta_x': 0,
                    'delta_y': 0
                })

    for layer in Layers:
        if layer["name"] == "Bowls_X_Y":
            Layer = layer
    Matrix = Layer["data"]
    Height = Layer["height"]
    Width = Layer["width"]
    i = 0
    for h in range(Height):
        for w in range(Width):
            if Matrix[w + h * Width] != 0:
                Bowls[i]["delta_x"] = w - Bowls[i]["x"]
                Bowls[i]["delta_y"] = Width - 1 - h - Bowls[i]["y"]
                i += 1

    return Bowls


def CreateProducts(Layers):
    Layer = None
    for layer in Layers:
        if layer["name"] == "Products":
            Layer = layer
    Objects = []
    Matrix = Layer["data"]
    Height = Layer["height"]
    Width = Layer["width"]
    Products = [
        "cheese",
        "ketchup",
        "meat",
        "bread",
        "egg",
        "fish",
        "potato",
        "apple",
        "milk",
        "mushroom"
    ]
    for h in range(Height):
        for w in range(Width):
            if Matrix[w + h * Width] != 0:
                i = random.randrange(0, len(Products))
                Objects.append({
                    'name': Products[i],
                    'x': w,
                    'y': Width - 1 - h,
                    'delta_x': 0,
                    'delta_y': 0
                })
                Products.pop(i)

    for layer in Layers:
        if layer["name"] == "Products_X_Y":
            Layer = layer
    Matrix = Layer["data"]
    Height = Layer["height"]
    Width = Layer["width"]
    j = 0
    for h in range(Height):
        for w in range(Width):
            if Matrix[w + h * Width] != 0:
                Objects[j]["delta_x"] = w - Objects[j]["x"]
                Objects[j]["delta_y"] = Width - 1 - h - Objects[j]["y"]
                j += 1

    for layer in Layers:
        if layer["name"] == "Fridge":
            Layer = layer
    Fridge = []
    Matrix = Layer["data"]
    Height = Layer["height"]
    Width = Layer["width"]
    for h in range(Height):
        for w in range(Width):
            if Matrix[w + h * Width] != 0:
                for i in range(len(Products)):
                    Fridge.append({
                        'name': Products[i],
                        'x': w,
                        'y': Width - 1 - h,
                        'delta_x': 0,
                        'delta_y': 0
                    })

    for layer in Layers:
        if layer["name"] == "Fridge_X_Y":
            Layer = layer
    Matrix = Layer["data"]
    Height = Layer["height"]
    Width = Layer["width"]
    for h in range(Height):
        for w in range(Width):
            if Matrix[w + h * Width] != 0:
                for i in range(len(Products)):
                    Fridge[i]["delta_x"] = w - Fridge[i]["x"]
                    Fridge[i]["delta_y"] = Width - 1 - h - Fridge[i]["y"]

    return Objects, Fridge


def main():
    # INPUT
    print("EnterMapName: ", end="")
    JsonName = input()

    # FIRST CREATION
    CopyAll(JsonName)
    Layers = ReadLayers(JsonName)
    Tables = CreateTables(Layers)
    for i in range(len(Layers)):
        if Layers[i]["name"] == "Tables":
            Layers.pop(i)
            break
    Objects, Fridge = CreateProducts(Layers)
    try:
        for i in range(len(Layers)):
            if Layers[i]["name"] == "Products" or Layers[i]["name"] == "Products_X_Y" or Layers[i]["name"] == "Fridge" or Layers[i]["name"] == "Fridge_X_Y":
                Layers.pop(i)
                i -= 1
    except:
        i = 0
    Bowls = CreateBowls(Layers)
    for i in range(len(Layers)):
        if Layers[i]["name"] == "Bowls":
            Layers.pop(i)
            break
    Spawn = CreateSpawn(Layers)
    for i in range(len(Layers)):
        if Layers[i]["name"] == "Spawn":
            Layers.pop(i)
            break
    # NewLayers = Splitting(JsonName, Layers)
    File = ReadAllFile(JsonName)
    PrintFile(JsonName, File)
    EditConfig(JsonName)
    # Crop("Maps/" + JsonName + "/Sprite", JsonName, 64, 64)

    # SECOND CREATION
    CreateConfig(JsonName, Layers, Tables, Objects, Fridge, Bowls, Spawn)


main()
