import random
from threading import Thread
import socket
import pickle
import JsonReadTest as TileMap
import ServerFunctions as server


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
        self.map = 'Dungeon_map_1'
        self.walls = TileMap.ReadJson(self.map)
        self.tile_scale = TileMap.GetTileScale(self.map)

        # Lobby Config
        self.lobby_host = socket.gethostbyname(socket.gethostname())
        self.lobby_port = 5000
        print("Host: " + str(self.lobby_host))
        print("Port: " + str(self.lobby_port))

        # Lobby socket Config
        self.lobby_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creation if socket
        self.lobby_server.bind((self.lobby_host, self.lobby_port))  # Bind of socket

        # Init players
        self.players = {
            'Player1': self.create_players(352, 928),
            'Player2': self.create_players(352, 928)
        }
        self.player_list = [
            'Player1',
            'Player2'
        ]

        # Init server
        self.clients = {}
        self.servers = {}
        self.threads = {}

        print("Map: " + self.map)
        print("Waiting players: ")
        for players in self.player_list:
            print("\t - " + players)

    def create_players(self, X, Y):
        PlayerInformation = {
            'X': X,
            'Y': Y,
            'SPRITE': 'Down',
            'ACTION': 'Static',
            'SCORE': 0
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
                        self.players[player]['SCORE'] += 1
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

    def start(self):
        for player in self.player_list:
            self.threads[player] = Thread(target=self.working, args=(self.servers[player], player))
        self.threads['reconnect'] = Thread(target=self.reconnect)
        print(self.threads)
        for thread in self.threads:
            self.threads[thread].start()
        for thread in self.threads:
            self.threads[thread].join()

    def reconnect(self):
        print("Reconnect active")
        while True:
            client, adress = self.lobby_server.accept()
            for servers in self.servers:
                if not self.servers[servers].using:
                    print("Server Found")
                    server.DynamicSend(client, self.servers[servers].port.encode('utf-8'))
                    break
                else:
                    print("Server is blocked")


def main():
    ThreadingServer = Server()
    ThreadingServer.connecting()
    ThreadingServer.start()
    print("That's all")


main()
