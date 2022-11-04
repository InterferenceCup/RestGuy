import socket
import pickle
import sys
import Sprites.JsonReadTest as TileMap

def DinamicSend(sock, senddata):
    Connection = True
    # print("IN SEND")
    while Connection:
        # print("send data")
        sock.send(senddata)
        # print("wait size")
        packet = sock.recv(1024)
        # print("size get")
        if int(str(packet.decode('utf-8'))) == sys.getsizeof(senddata):
            # print("right size")
            sock.send("YES".encode('utf-8'))
            Connection = False
        else:
            # print("bad size")
            sock.send("NO".encode('utf-8'))
    # print("OUT SEND")

def DinamicReciev(sock):
    data = bytearray()
    Connection = True
    # print("IN")
    while Connection:
        # First Get
        # print("wait data")
        packet = sock.recv(1024)
        # print(str(packet.decode('utf-8')))
        data = packet

        # print("data get")

        # Second Get
        # print("send size")
        sock.send(str(sys.getsizeof(data)).encode('utf-8'))
        # print("wait accept")
        packet = sock.recv(1024)
        # print(str(packet.decode('utf-8')))
        # print("get accept")
        if str(packet.decode('utf-8')) == "YES":
            # print("data is ok")
            Connection = False
        # else:
            # print("data is not ok")
    # print("OUT")
    return data

# Client Config
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
RADIUS = 15

Walls = TileMap.ReadJson('Sprites/test_map_1')
for j in range(20):
    for i in range(20):
        if Walls[19 - j][i].center != -1:
            print("#", end = '')
        else:
            print("_", end = '')
    print()

# HOST CONFIG
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5000
print(HOST, PORT)
MOVEMENT_SPEED = 5

'''
# Player Two Config
PlayerTwoPositionX = 50
PlayerTwoPositionY = 50
PlayerTwoColor = "EB5284"
PlayerTwoInformation = {
    'X': PlayerTwoPositionX,
    'Y': PlayerTwoPositionY,
    'COLOR': PlayerTwoColor
}
'''

def get_information(information, number_of_bite, value):
    mask = 1
    mask = mask << number_of_bite
    if value == 1:
        if information & mask:
            return 1
        else:
            return 0
    else:
        if information & mask:
            return 0
        else:
            return 1


def edit_position(information, PlayerInformation):
    if information == 0:
        PlayerInformation['X'] += 0
        PlayerInformation['Y'] += 0
    else:
        PlayerTile = TileMap.GetTile(PlayerInformation['X'], PlayerInformation['Y'])
        if get_information(information, 7, 1):
            if PlayerInformation['X'] - MOVEMENT_SPEED >= RADIUS:
                Wall = Walls[PlayerTile[1]][PlayerTile[0] - 1]
                CenterWall = Wall.center
                if Wall.collision(PlayerInformation['X'] - RADIUS - MOVEMENT_SPEED, PlayerInformation['Y']) == 1:
                    PlayerInformation['X'] += ( Wall.x_right + Wall.x - PlayerInformation['X'] + RADIUS ) / 2
                else:
                    Wall = Walls[PlayerTile[1] + 1][PlayerTile[0] - 1]
                    if Wall.collision(PlayerInformation['X'] - RADIUS - MOVEMENT_SPEED, PlayerInformation['Y'] + RADIUS) == 1:
                        PlayerInformation['X'] += (Wall.x_right + Wall.x - PlayerInformation['X'] + RADIUS) / 2
                        if CenterWall == -1:
                            PlayerInformation['Y'] += (Wall.y_left + Wall.y - PlayerInformation['Y'] - RADIUS - 1) / 2
                    else:
                        Wall = Walls[PlayerTile[1] - 1][PlayerTile[0] - 1]
                        if Wall.collision(PlayerInformation['X'] - RADIUS - MOVEMENT_SPEED, PlayerInformation['Y'] - RADIUS) == 1:
                            PlayerInformation['X'] += (Wall.x_right + Wall.x - PlayerInformation['X'] + RADIUS) / 2
                            if CenterWall == -1:
                                PlayerInformation['Y'] += (Wall.y_right + Wall.y - PlayerInformation['Y'] + RADIUS + 1) / 2
                        else:
                            PlayerInformation['X'] += -MOVEMENT_SPEED
            else:
                PlayerInformation['X'] = RADIUS
        elif get_information(information, 6, 1):
            if PlayerInformation['X'] + MOVEMENT_SPEED <= SCREEN_WIDTH - RADIUS:
                Wall = Walls[PlayerTile[1]][PlayerTile[0] + 1]
                CenterWall = Wall.center
                if Wall.collision(PlayerInformation['X'] + RADIUS + MOVEMENT_SPEED, PlayerInformation['Y']) == 1:
                    PlayerInformation['X'] += (Wall.x_left + Wall.x - PlayerInformation['X'] - RADIUS - 1) / 2
                else:
                    Wall = Walls[PlayerTile[1] + 1][PlayerTile[0] + 1]
                    if Wall.collision(PlayerInformation['X'] + RADIUS + MOVEMENT_SPEED,
                                      PlayerInformation['Y'] + RADIUS) == 1:
                        PlayerInformation['X'] += (Wall.x_left + Wall.x - PlayerInformation['X'] - RADIUS) / 2
                        if CenterWall == -1:
                            PlayerInformation['Y'] += (Wall.y_left + Wall.y - PlayerInformation['Y'] - RADIUS - 1) / 2
                    else:
                        Wall = Walls[PlayerTile[1] - 1][PlayerTile[0] + 1]
                        if Wall.collision(PlayerInformation['X'] + RADIUS + MOVEMENT_SPEED,
                                          PlayerInformation['Y'] - RADIUS) == 1:
                            PlayerInformation['X'] += (Wall.x_left + Wall.x - PlayerInformation['X'] - RADIUS) / 2
                            if CenterWall == -1:
                                PlayerInformation['Y'] += (Wall.y_right + Wall.y - PlayerInformation['Y'] + RADIUS + 1) / 2
                        else:
                            PlayerInformation['X'] += MOVEMENT_SPEED
            else:
                PlayerInformation['X'] = SCREEN_WIDTH - RADIUS
        if get_information(information, 5, 1):
            if PlayerInformation['Y'] + MOVEMENT_SPEED <= SCREEN_HEIGHT - RADIUS:
                Wall = Walls[PlayerTile[1] + 1][PlayerTile[0]]
                CenterWall = Wall.center
                if Wall.collision(PlayerInformation['X'], PlayerInformation['Y'] + RADIUS + MOVEMENT_SPEED) == 1:
                    PlayerInformation['Y'] += (Wall.y_left + Wall.y - PlayerInformation['Y'] - RADIUS) / 2
                else:
                    Wall = Walls[PlayerTile[1] + 1][PlayerTile[0] - 1]
                    if Wall.collision(PlayerInformation['X'] - RADIUS, PlayerInformation['Y'] + RADIUS + MOVEMENT_SPEED) == 1:
                        PlayerInformation['Y'] += (Wall.y_left + Wall.y - PlayerInformation['Y'] - RADIUS) / 2
                        if CenterWall == -1:
                            PlayerInformation['X'] += (Wall.x_right + Wall.x - PlayerInformation['X'] + RADIUS + 1) / 2
                    else:
                        Wall = Walls[PlayerTile[1] + 1][PlayerTile[0] + 1]
                        if Wall.collision(PlayerInformation['X'] + RADIUS, PlayerInformation['Y'] + RADIUS + MOVEMENT_SPEED) == 1:
                            PlayerInformation['Y'] += (Wall.y_left + Wall.y - PlayerInformation['Y'] - RADIUS) / 2
                            if CenterWall == -1:
                                PlayerInformation['X'] += (Wall.x_left + Wall.x - PlayerInformation['X'] - RADIUS - 1) / 2
                        else:
                            PlayerInformation['Y'] += MOVEMENT_SPEED
            else:
                PlayerInformation['Y'] = SCREEN_HEIGHT - RADIUS
        elif get_information(information, 4, 1):
            if PlayerInformation['Y'] - MOVEMENT_SPEED >= RADIUS:
                Wall = Walls[PlayerTile[1] - 1][PlayerTile[0]]
                CenterWall = Wall.center
                if Wall.collision(PlayerInformation['X'], PlayerInformation['Y'] - RADIUS - MOVEMENT_SPEED) == 1:
                    PlayerInformation['Y'] += (Wall.y_right + Wall.y - PlayerInformation['Y'] + RADIUS) / 2
                else:
                    Wall = Walls[PlayerTile[1] - 1][PlayerTile[0] - 1]
                    if Wall.collision(PlayerInformation['X'] - RADIUS,
                                      PlayerInformation['Y'] - RADIUS - MOVEMENT_SPEED) == 1:
                        PlayerInformation['Y'] += (Wall.y_right + Wall.y - PlayerInformation['Y'] + RADIUS) / 2
                        if CenterWall == -1:
                            PlayerInformation['X'] += (Wall.x_right + Wall.x - PlayerInformation['X'] + RADIUS + 1) / 2
                    else:
                        Wall = Walls[PlayerTile[1] - 1][PlayerTile[0] + 1]
                        if Wall.collision(PlayerInformation['X'] + RADIUS,
                                          PlayerInformation['Y'] - RADIUS - MOVEMENT_SPEED) == 1:
                            PlayerInformation['Y'] += (Wall.y_right + Wall.y - PlayerInformation['Y'] + RADIUS) / 2
                            if CenterWall == -1:
                                PlayerInformation['X'] += (Wall.x_left + Wall.x - PlayerInformation['X'] - RADIUS - 1) / 2
                        else:
                            PlayerInformation['Y'] += -MOVEMENT_SPEED
            else:
                PlayerInformation['Y'] = RADIUS
    return PlayerInformation

def main():
    # Socket Config
    ServerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ServerSock.bind((HOST, PORT))
    ServerSock.listen()

    # Clients Config
    Clients = {}

    # Player One Config
    PlayerOnePositionX = 20
    PlayerOnePositionY = 20
    PlayerOneColor = "007CAD"
    PlayerOneInformation = {
        'X': PlayerOnePositionX,
        'Y': PlayerOnePositionY,
        'COLOR': PlayerOneColor
    }

    '''
    # Player Two Config
    PlayerTwoPositionX = 100
    PlayerTwoPositionY = 50
    PlayerTwoColor = "EB5284"

    PlayerTwoInformation = {
        'X': PlayerTwoPositionX,
        'Y': PlayerTwoPositionY,
        'COLOR': PlayerTwoColor
    }
    '''

    # Config
    Players = {
        'Player1': PlayerOneInformation,
        # 'Player2': PlayerTwoInformation
    }

    Client, Address = ServerSock.accept()

    Clients['Player1'] = [Client, Address]
    print("Connected to", {Clients['Player1'][0]})

    # Client, Address = ServerSock.accept()

    # Clients['Player2'] = [Client, Address]
    # print("Connected to", {Clients['Player2'][0]})

    DinamicSend(Clients['Player1'][0], 'Player1'.encode('utf-8'))
    # DinamicSend(Clients['Player1'][0], 'Player2'.encode('utf-8'))

    # DinamicSend(Clients['Player2'][0], 'Player2'.encode('utf-8'))
    # DinamicSend(Clients['Player2'][0], 'Player1'.encode('utf-8'))

    DinamicSend(Clients['Player1'][0], pickle.dumps(Players))
    # DinamicSend(Clients['Player2'][0], pickle.dumps(Players))


    Connection = True
    while Connection:
        try:
            Data = DinamicReciev(Clients['Player1'][0])
        except ConnectionError:
            print("Connection has been resolved")
            Connection = False
            break

        try:
            if int(Data):
                Information = int(Data)
                if Information == 192:
                    Information = 0
                elif Information == 48:
                    Information = 0
                PlayerOneInformation = edit_position(Information, PlayerOneInformation)
        except:
            print("Data has benn broken")

        '''
        try:
            Data = DinamicReciev(Clients['Player2'][0])
        except ConnectionError:
            print("Connection has been resolved")
            Connection = False
            break

        try:
            if int(Data):
                Information = int(Data)
                if Information == 192:
                    Information = 0
                elif Information == 48:
                    Information = 0
                PlayerTwoInformation = edit_position(Information, PlayerTwoInformation)
        except:
            print("Data has benn broken")
        '''

        DinamicSend(Clients['Player1'][0], pickle.dumps(Players))
        # DinamicSend(Clients['Player2'][0], pickle.dumps(Players))


main()
