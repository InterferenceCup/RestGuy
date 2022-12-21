import random
from os import listdir
from threading import Thread
import socket
import pickle

import requests

import JsonReadTest as TileMap
import ServerFunctions as server


class Ingredient:
    def __init__(self, coordinates, delta, texture):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.delta_x = delta[0]
        self.delta_y = delta[1]
        self.texture = texture

    def coordinates(self):
        return [self.x, self.y]

    def target(self):
        return [self.x + self.delta_x, self.y + self.delta_y]


class Recept:
    def __init__(self, ingredients, texture):
        self.ingredients = []
        for ingredient in ingredients:
            self.ingredients.append(ingredient)
        self.texture = texture
        self.stage = 0

    def get_ingredient(self):
        return self.ingredients[self.stage]

    def up_stage(self):
        self.stage += 1

    def down_stage(self):
        self.stage -= 1

    def null_stage(self):
        self.stage = 0

    def is_it_ready(self):
        if self.stage == len(self.ingredients):
            return True
        else:
            return False


class Order:
    def __init__(self, coordinates, delta, recept, table):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.delta_x = delta[0]
        self.delta_y = delta[1]
        self.recept = recept
        self.stage = "getting"
        self.table = table
        self.texture = "recept"

    def coordinates(self):
        return [self.x, self.y]

    def target(self):
        return [self.x + self.delta_x, self.y + self.delta_y]


# Get information
def GetInformation(Information, NumberOfBit, Value):
    Mask = 1  # Creating of mask
    Mask = Mask << NumberOfBit  # Prepare mask for processing

    # If we must process by 1
    if Value == 1:
        # If we have one on our bit
        if Information & Mask:
            return 1
        # Else
        else:
            return 0
    # If we must process by 0
    else:
        if Information & Mask:
            return 0
        else:
            return 1


# Edit position
def EditPosition(information, PlayerInformation, Walls, TileScale):
    # Client Config
    RadiusUp = 10
    RadiusDown = 32
    RadiusLeft = 20
    RadiusRight = 20
    MovementSpeed = 5

    if information == 0:
        PlayerInformation['X'] += 0
        PlayerInformation['Y'] += 0
        PlayerInformation['ACTION'] = 'Static'
    else:
        PlayerTile = TileMap.GetTile(PlayerInformation['X'], PlayerInformation['Y'], TileScale)
        if GetInformation(information, 7, 1):
            PlayerInformation['SPRITE'] = 'Left'
            PlayerInformation['ACTION'] = ''
            Wall = Walls[PlayerTile[1]][PlayerTile[0] - 1]
            CenterWall = Wall.center
            if Wall.collision(PlayerInformation['X'] - RadiusLeft - MovementSpeed,
                              PlayerInformation['Y']) == 1:
                PlayerInformation['X'] += (Wall.x_right + Wall.x - PlayerInformation['X'] + RadiusLeft) / 2
                PlayerInformation['SPRITE'] = 'Left'
                PlayerInformation['ACTION'] = 'Static'
            else:
                Wall = Walls[PlayerTile[1] + 1][PlayerTile[0] - 1]
                if Wall.collision(PlayerInformation['X'] - RadiusLeft - MovementSpeed,
                                  PlayerInformation['Y'] + RadiusUp) == 1:
                    PlayerInformation['X'] += (Wall.x_right + Wall.x - PlayerInformation['X'] + RadiusLeft) / 2
                    if CenterWall == -1:
                        PlayerInformation['Y'] += (Wall.y_down + Wall.y - PlayerInformation['Y'] - RadiusUp - 1) / 4
                        PlayerInformation['X'] += -MovementSpeed / 2
                    else:
                        PlayerInformation['SPRITE'] = 'Left'
                        PlayerInformation['ACTION'] = 'Static'
                else:
                    Wall = Walls[PlayerTile[1] - 1][PlayerTile[0] - 1]
                    if Wall.collision(PlayerInformation['X'] - RadiusLeft - MovementSpeed,
                                      PlayerInformation['Y'] - RadiusDown) == 1:
                        PlayerInformation['X'] += (Wall.x_right + Wall.x - PlayerInformation['X'] + RadiusLeft) / 2
                        if CenterWall == -1:
                            PlayerInformation['Y'] += (Wall.y_top + Wall.y - PlayerInformation[
                                'Y'] + RadiusDown + 1) / 4
                            PlayerInformation['X'] += -MovementSpeed / 2
                        else:
                            PlayerInformation['SPRITE'] = 'Left'
                            PlayerInformation['ACTION'] = 'Static'
                    else:
                        PlayerInformation['X'] += -MovementSpeed
        elif GetInformation(information, 6, 1):
            PlayerInformation['SPRITE'] = 'Right'
            PlayerInformation['ACTION'] = ''
            Wall = Walls[PlayerTile[1]][PlayerTile[0] + 1]
            CenterWall = Wall.center
            if Wall.collision(PlayerInformation['X'] + RadiusRight + MovementSpeed,
                              PlayerInformation['Y']) == 1:
                PlayerInformation['X'] += (Wall.x_left + Wall.x - PlayerInformation['X'] - RadiusRight) / 2
                PlayerInformation['SPRITE'] = 'Right'
                PlayerInformation['ACTION'] = 'Static'
            else:
                Wall = Walls[PlayerTile[1] + 1][PlayerTile[0] + 1]
                if Wall.collision(PlayerInformation['X'] + RadiusRight + MovementSpeed,
                                  PlayerInformation['Y'] + RadiusUp) == 1:
                    PlayerInformation['X'] += (Wall.x_left + Wall.x - PlayerInformation['X'] - RadiusRight) / 2
                    if CenterWall == -1:
                        PlayerInformation['Y'] += (Wall.y_down + Wall.y - PlayerInformation['Y'] - RadiusUp - 1) / 2
                        PlayerInformation['X'] += MovementSpeed
                    else:
                        PlayerInformation['SPRITE'] = 'Right'
                        PlayerInformation['ACTION'] = 'Static'
                else:
                    Wall = Walls[PlayerTile[1] - 1][PlayerTile[0] + 1]
                    if Wall.collision(PlayerInformation['X'] + RadiusRight + MovementSpeed,
                                      PlayerInformation['Y'] - RadiusDown) == 1:
                        PlayerInformation['X'] += (Wall.x_left + Wall.x - PlayerInformation['X'] - RadiusRight) / 2
                        if CenterWall == -1:
                            PlayerInformation['Y'] += (Wall.y_top + Wall.y - PlayerInformation[
                                'Y'] + RadiusDown + 1) / 2
                            PlayerInformation['X'] += MovementSpeed
                        else:
                            PlayerInformation['SPRITE'] = 'Right'
                            PlayerInformation['ACTION'] = 'Static'
                    else:
                        PlayerInformation['X'] += MovementSpeed
        if GetInformation(information, 5, 1):
            PlayerInformation['SPRITE'] = 'Up'
            PlayerInformation['ACTION'] = ''
            Wall = Walls[PlayerTile[1] + 1][PlayerTile[0]]
            CenterWall = Wall.center
            if Wall.collision(PlayerInformation['X'],
                              PlayerInformation['Y'] + RadiusUp + MovementSpeed) == 1:
                PlayerInformation['Y'] += (Wall.y_down + Wall.y - PlayerInformation['Y'] - RadiusUp) / 2
                PlayerInformation['SPRITE'] = 'Up'
                PlayerInformation['ACTION'] = 'Static'
            else:
                Wall = Walls[PlayerTile[1] + 1][PlayerTile[0] - 1]
                if Wall.collision(PlayerInformation['X'] - RadiusLeft,
                                  PlayerInformation['Y'] + RadiusUp + MovementSpeed) == 1:
                    PlayerInformation['Y'] += (Wall.y_down + Wall.y - PlayerInformation['Y'] - RadiusRight) / 2
                    if CenterWall == -1:
                        PlayerInformation['X'] += (Wall.x_right + Wall.x - PlayerInformation['X'] + RadiusLeft + 1) / 2
                        PlayerInformation['Y'] += MovementSpeed
                    else:
                        PlayerInformation['SPRITE'] = 'Up'
                        PlayerInformation['ACTION'] = 'Static'
                else:
                    Wall = Walls[PlayerTile[1] + 1][PlayerTile[0] + 1]
                    if Wall.collision(PlayerInformation['X'] + RadiusRight,
                                      PlayerInformation['Y'] + RadiusUp + MovementSpeed) == 1:
                        PlayerInformation['Y'] += (Wall.y_down + Wall.y - PlayerInformation['Y'] - RadiusDown) / 2
                        if CenterWall == -1:
                            PlayerInformation['X'] += (Wall.x_left + Wall.x - PlayerInformation[
                                'X'] - RadiusRight - 1) / 2
                            PlayerInformation['Y'] += MovementSpeed
                        else:
                            PlayerInformation['SPRITE'] = 'Up'
                            PlayerInformation['ACTION'] = 'Static'
                    else:
                        PlayerInformation['Y'] += MovementSpeed
        elif GetInformation(information, 4, 1):
            PlayerInformation['SPRITE'] = 'Down'
            PlayerInformation['ACTION'] = ''
            Wall = Walls[PlayerTile[1] - 1][PlayerTile[0]]
            CenterWall = Wall.center
            if Wall.collision(PlayerInformation['X'],
                              PlayerInformation['Y'] - RadiusDown - MovementSpeed) == 1:
                PlayerInformation['Y'] += (Wall.y_top + Wall.y - PlayerInformation['Y'] + RadiusDown) / 2
                PlayerInformation['SPRITE'] = 'Down'
                PlayerInformation['ACTION'] = 'Static'
            else:
                Wall = Walls[PlayerTile[1] - 1][PlayerTile[0] - 1]
                if Wall.collision(PlayerInformation['X'] - RadiusLeft,
                                  PlayerInformation['Y'] - RadiusDown - MovementSpeed) == 1:
                    PlayerInformation['Y'] += (Wall.y_top + Wall.y - PlayerInformation['Y'] + RadiusDown) / 2
                    if CenterWall == -1:
                        PlayerInformation['X'] += (Wall.x_right + Wall.x - PlayerInformation['X'] + RadiusRight + 1) / 2
                        PlayerInformation['Y'] += -MovementSpeed
                    else:
                        PlayerInformation['SPRITE'] = 'Down'
                        PlayerInformation['ACTION'] = 'Static'
                else:
                    Wall = Walls[PlayerTile[1] - 1][PlayerTile[0] + 1]
                    if Wall.collision(PlayerInformation['X'] + RadiusRight,
                                      PlayerInformation['Y'] - RadiusDown - MovementSpeed) == 1:
                        PlayerInformation['Y'] += (Wall.y_top + Wall.y - PlayerInformation['Y'] + RadiusDown) / 2
                        if CenterWall == -1:
                            PlayerInformation['X'] += (Wall.x_left + Wall.x - PlayerInformation[
                                'X'] - RadiusLeft - 1) / 2
                            PlayerInformation['Y'] += -MovementSpeed
                        else:
                            PlayerInformation['SPRITE'] = 'Down'
                            PlayerInformation['ACTION'] = 'Static'
                    else:
                        PlayerInformation['Y'] += -MovementSpeed
    return PlayerInformation


class Sock:

    def __init__(self, sock, host, port):
        self.sock = sock
        self.host = str(host)
        self.port = str(port)
        self.client = None
        self.adress = None
        self.using = False
        self.information = 0

    def listen(self):
        self.sock.listen()

    def accept(self):
        client, adress = self.sock.accept()
        return client, adress


class Server:

    def __init__(self):
        # Map config
        self.map = random.choice([f for f in listdir("Maps/")])
        self.walls = TileMap.ReadJson(self.map)
        self.tile_scale = TileMap.GetTileScale(self.map)
        self.tables = TileMap.GetTables(self.map)
        self.ingredients = self.Ingredients()
        self.bowls = self.TablesForFood()
        self.order = {}
        self.food = [
            "pizza",
            "burger",
            "chicken",
            "ramen",
            "omlet",
            "friedegg",
            "curry",
            "bacon",
            "spaghetti"
        ]

        self.lobby_host = socket.gethostbyname(socket.gethostname())
        self.lobby_port = random.randrange(1000, 10000)
        while True:
            try:
                self.lobby_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creation if socket
                self.lobby_server.bind((self.lobby_host, self.lobby_port))  # Bind of socket
                break
            except:
                self.lobby_port = random.randrange(1000, 10000)

        print("Host: " + str(self.lobby_host))
        print("Port: " + str(self.lobby_port))
        TileMap.SetLastPort(str(self.lobby_port))

        # Init players
        self.players = {}
        self.player_list = []
        for i in range(TileMap.ReadPlayer()):
            self.player_list.append("Player" + str(i + 1))
            self.players["Player" + str(i + 1)] = self.create_players(352, 928)

        for player in self.player_list:
            self.order[player] = self.create_pizza(player)

        for player in self.player_list:
            self.players[player]['target'] = self.order[player].target()
            self.players[player]['order'] = self.order[player].target()

        # Init server
        self.clients = {}
        self.servers = {}
        self.threads = {}

        print("Map: " + self.map)
        print("Waiting players: ")
        for players in self.player_list:
            print("\t - " + players)

        self.end = False

    def create_players(self, X, Y):
        PlayerInformation = {
            'X': X,
            'Y': Y,
            'SPRITE': 'Down',
            'ACTION': 'Static',
            'SCORE': 0,
            'name': 'Unknown',
            'target': None,
            'item': None,
            'order': None
        }
        return PlayerInformation

    def connecting(self):
        self.lobby_server.listen()  # Open socket
        for player in self.player_list:
            client, address = self.lobby_server.accept()  # Accept connection
            self.clients[player] = [client, address]  # Accept data of Client
            print("Connected to", {self.clients[player][1]})  # Printing for me
            self.servers[player] = self.creating_own_server()
            print("\t - Socket created")
            while True:
                if server.DynamicSend(self.clients[player][0], self.servers[player].port.encode('utf-8')) != 0:
                    print("\t - Reconnecting")
                    continue
                self.servers[player].listen()
                self.servers[player].client, self.servers[player].adress = self.servers[player].accept()
                self.servers[player].sock.settimeout(0.5)
                print("\t - Accepted Connection")
                if server.DynamicSend(self.servers[player].client, player.encode('utf-8')) != 0:  # Send name of Client
                    print("\t - Reconnecting")
                    continue
                if server.DynamicSend(self.servers[player].client, pickle.dumps(self.players)) != 0:  # Send X and Y
                    print("\t - Reconnecting")
                    continue
                if server.DynamicSend(self.servers[player].client, self.map.encode('utf-8')) != 0:  # Send map
                    print("\t - Reconnecting")
                    continue
                name = server.DynamicRecv(self.servers[player].client)
                if name != None:
                    self.players[player]["name"] = name.decode('utf-8')
                self.servers[player].using = True
                print("\t - Data was send")
                break

    def creating_own_server(self):
        host = socket.gethostbyname(socket.gethostname())
        port = random.randrange(1000, 10000)
        while True:
            try:
                client_server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creation if socket
                client_server_sock.bind((host, port))  # Bind of socket
                break
            except:
                port = random.randrange(1000, 10000)
        client_server = Sock(client_server_sock, host, port)
        return client_server

    def working(self, server_client, player):
        print("Start " + player + "'s server")
        while True:
            data = {}  # Creation of data list
            server_client.sock.settimeout(0.02)
            # Trying to recv PlayerOne action
            try:
                data = server.DynamicRecv(server_client.client)  # Recv
            except ConnectionError:
                self.servers[player].using = False
                print("Connection Error")  # Say of Error

            # Trying to read action
            try:
                # If we have action
                if data == None:
                    data = str(self.servers[player].information)
                else:
                    self.servers[player].using = True
                    # If action is normal

                    information = int(data)  # Read action
                    if GetInformation(information, 0, 1):
                        tile = TileMap.GetTile(self.players[player]['X'], self.players[player]['Y'], 64)
                        target = self.players[player]['target']
                        if tile[0] == target[0] and tile[1] == target[1]:
                            if self.order[player].stage == "getting":
                                self.order[player].stage = "cooking"
                                self.players[player]["target"] = self.order[player].recept.get_ingredient().target()
                                self.players[player]["item"] = self.order[player].texture
                                self.players[player]["order"] = None
                            elif self.order[player].stage == "cooking":
                                self.players[player]["item"] = self.order[player].recept.get_ingredient().texture
                                self.order[player].recept.up_stage()
                                self.players[player]["target"] = self.order[player].table.target()
                                self.order[player].stage = "bowl"
                            elif self.order[player].stage == "bowl":
                                if not self.order[player].recept.is_it_ready():
                                    self.players[player]["item"] = None
                                    self.players[player]["target"] = self.order[player].recept.get_ingredient().target()
                                    self.order[player].stage = "cooking"
                                else:
                                    self.players[player]["item"] = self.order[player].recept.texture
                                    self.order[player].stage = "giving"
                                    self.players[player]["target"] = self.order[player].target()
                            elif self.order[player].stage == "giving":
                                self.players[player]['SCORE'] += 1
                                self.order[player] = self.create_pizza(player)
                                self.players[player]["target"] = self.order[player].target()
                                self.players[player]["item"] = None
                                self.players[player]["order"] = self.order[player].target()
                        information -= 1
                        # If action is not right
                    if information == 192:
                        information = 0
                    elif information == 48:
                        information = 0
                    self.servers[player].information = information
                    self.players[player] = EditPosition(information,
                                                        self.players[player],
                                                        self.walls,
                                                        self.tile_scale)  # Making new position
                    if self.IsItOnOneTile(player):
                        if self.order[player].stage == "bowl":
                            self.order[player].recept.down_stage()
                            self.players[player]['item'] = "effect"
                            self.players[player]["target"] = self.order[player].recept.get_ingredient().target()
                            self.order[player].stage = "cooking"
                        elif self.order[player].stage == "giving":
                            self.order[player].recept.null_stage()
                            self.players[player]['item'] = "effect"
                            self.players[player]["target"] = self.order[player].recept.get_ingredient().target()
                            self.order[player].stage = "cooking"

            except:
                print("Data has benn broken")

            # If we can send without problem
            if server.DynamicSend(server_client.client, pickle.dumps(self.players)) != 0:
                try:
                    self.servers[player].using = False
                    self.servers[player].client, self.servers[player].adress = server.Accept(server_client.sock,
                                                                                             self.players,
                                                                                             player,
                                                                                             self.map)  # Try to create new connection
                except:
                    # print("Bad")
                    print('', end='')
            else:
                self.servers[player].using = True

            self.IsItEnd()
            if self.end:
                return 0

    def start(self):
        for player in self.player_list:
            self.threads[player] = Thread(target=self.working, args=(self.servers[player], player))
        self.threads['reconnect'] = Thread(target=self.reconnect)
        print(self.threads)
        for thread in self.threads:
            self.threads[thread].start()
        for thread in self.threads:
            self.threads[thread].join()
        print("All sockets has stopped")

    def reconnect(self):
        print("Reconnect active")
        self.lobby_server.settimeout(1)
        while True and not self.end:
            try:
                client, adress = self.lobby_server.accept()
                for servers in self.servers:
                    if not self.servers[servers].using:
                        print("Server Found")
                        server.DynamicSend(client, self.servers[servers].port.encode('utf-8'))
                        break
                    else:
                        print("Server is blocked")
            except:
                client = None

    def create_pizza(self, player_number):
        ingredients = [random.choice(list(self.ingredients.values())),
                       random.choice(list(self.ingredients.values())),
                       random.choice(list(self.ingredients.values()))]
        recept = Recept(ingredients, random.choice(self.food))
        config = random.choice(self.tables)
        table = self.bowls[player_number]
        order = Order([config['x'], config['y']], [config['delta_x'], config['delta_y']], recept, table)
        return order

    def Ingredients(self):
        objects = TileMap.GetObjects(self.map)
        fridge = TileMap.GetFridge(self.map)
        ingredients = {}
        for obj in objects:
            ingredients[obj["name"]] = Ingredient(
                [obj['x'], obj['y']],
                [obj['delta_x'], obj['delta_y']],
                obj["name"]
            )
        for obj in fridge:
            ingredients[obj["name"]] = Ingredient(
                [obj['x'], obj['y']],
                [obj['delta_x'], obj['delta_y']],
                obj["name"]
            )
        return ingredients

    def TablesForFood(self):
        tables = {}
        tables_without_food = TileMap.GetBowls(self.map)
        i = 0
        for obj in tables_without_food:
            tables["Player" + str(i + 1)] = Ingredient(
                [obj['x'], obj['y']],
                [obj['delta_x'], obj['delta_y']],
                'bowl'
            )
            i += 1
        return tables

    def IsItOnOneTile(self, player):
        MyTile = TileMap.GetTile(self.players[player]['X'], self.players[player]['Y'], 64)
        for players in self.players:
            if players != player:
                HisTile = TileMap.GetTile(self.players[players]['X'], self.players[players]['Y'], 64)
                if MyTile[0] == HisTile[0] and MyTile[1] == HisTile[1]:
                    return True
        return False

    def IsItEnd(self):
        for players in self.players:
            if self.players[players]["SCORE"] == 1:
                self.end = True
                break

    def SendAllData(self):
        for players in self.players:
            if self.players[players]["name"] != "Unknown":
                try:
                    with requests.Session() as s:
                        steps = 0
                        orders = 0
                        result = s.get('http://localhost:8080/users').text
                        result = result.split(sep='|')
                        for i in range(len(result) - 1):
                            result[i] = result[i].split(sep='-')
                        print(result)
                        for res in result:
                            if res[0].strip() == self.players[players]["name"]:
                                steps = int(res[2].strip())
                                orders = int(res[3].strip())
                        payload = {
                            'username': self.players[players]["name"],
                            'steps': int(self.players[players]["SCORE"] * 10.5) + steps,
                            'orders': self.players[players]["SCORE"] + orders
                        }
                        s.post('http://localhost:8080/update', data=payload)
                except:
                    print("No connection to server")


def main():
    ThreadingServer = Server()
    ThreadingServer.connecting()
    ThreadingServer.start()
    ThreadingServer.SendAllData()
    print("Your server has stopped")


main()
