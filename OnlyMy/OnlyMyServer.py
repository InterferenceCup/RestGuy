import socket
import pickle
import Sprites.JsonReadTest as TileMap
import ServerFunctions as Server


# Get information
def GetInformation(Information, NumberOfBit, Value):
    Mask = 1    # Creating of mask
    Mask = Mask << NumberOfBit   # Prepare mask for processing

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
    Config = TileMap.GetConfig("Config")
    ScreenWidth = Config[1]
    ScreenHeight = Config[0]
    Radius = 15
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
            if PlayerInformation['X'] - MovementSpeed >= Radius:
                Wall = Walls[PlayerTile[1]][PlayerTile[0] - 1]
                CenterWall = Wall.center
                if Wall.collision(PlayerInformation['X'] - Radius - MovementSpeed,
                                  PlayerInformation['Y']) == 1:
                    PlayerInformation['X'] += (Wall.x_right + Wall.x - PlayerInformation['X'] + Radius) / 2
                else:
                    Wall = Walls[PlayerTile[1] + 1][PlayerTile[0] - 1]
                    if Wall.collision(PlayerInformation['X'] - Radius - MovementSpeed,
                                      PlayerInformation['Y'] + Radius) == 1:
                        PlayerInformation['X'] += (Wall.x_right + Wall.x - PlayerInformation['X'] + Radius) / 2
                        if CenterWall == -1:
                            PlayerInformation['Y'] += (Wall.y_down + Wall.y - PlayerInformation['Y'] - Radius - 1) / 2
                            PlayerInformation['X'] += -MovementSpeed
                    else:
                        Wall = Walls[PlayerTile[1] - 1][PlayerTile[0] - 1]
                        if Wall.collision(PlayerInformation['X'] - Radius - MovementSpeed,
                                          PlayerInformation['Y'] - Radius) == 1:
                            PlayerInformation['X'] += (Wall.x_right + Wall.x - PlayerInformation['X'] + Radius) / 2
                            if CenterWall == -1:
                                PlayerInformation['Y'] += (Wall.y_top + Wall.y - PlayerInformation['Y'] + Radius + 1) / 2
                                PlayerInformation['X'] += -MovementSpeed
                        else:
                            PlayerInformation['X'] += -MovementSpeed
            else:
                PlayerInformation['X'] = Radius
        elif GetInformation(information, 6, 1):
            PlayerInformation['SPRITE'] = 'Right'
            PlayerInformation['ACTION'] = ''
            if PlayerInformation['X'] + MovementSpeed <= ScreenWidth - Radius:
                Wall = Walls[PlayerTile[1]][PlayerTile[0] + 1]
                CenterWall = Wall.center
                if Wall.collision(PlayerInformation['X'] + Radius + MovementSpeed,
                                  PlayerInformation['Y']) == 1:
                    PlayerInformation['X'] += (Wall.x_left + Wall.x - PlayerInformation['X'] - Radius - 1) / 2
                else:
                    Wall = Walls[PlayerTile[1] + 1][PlayerTile[0] + 1]
                    if Wall.collision(PlayerInformation['X'] + Radius + MovementSpeed,
                                      PlayerInformation['Y'] + Radius) == 1:
                        PlayerInformation['X'] += (Wall.x_left + Wall.x - PlayerInformation['X'] - Radius) / 2
                        if CenterWall == -1:
                            PlayerInformation['Y'] += (Wall.y_down + Wall.y - PlayerInformation['Y'] - Radius - 1) / 2
                            PlayerInformation['X'] += MovementSpeed
                    else:
                        Wall = Walls[PlayerTile[1] - 1][PlayerTile[0] + 1]
                        if Wall.collision(PlayerInformation['X'] + Radius + MovementSpeed,
                                          PlayerInformation['Y'] - Radius) == 1:
                            PlayerInformation['X'] += (Wall.x_left + Wall.x - PlayerInformation['X'] - Radius) / 2
                            if CenterWall == -1:
                                PlayerInformation['Y'] += (Wall.y_top + Wall.y - PlayerInformation['Y'] + Radius + 1) / 2
                                PlayerInformation['X'] += MovementSpeed
                        else:
                            PlayerInformation['X'] += MovementSpeed
            else:
                PlayerInformation['X'] = ScreenWidth - Radius
        if GetInformation(information, 5, 1):
            PlayerInformation['SPRITE'] = 'Up'
            PlayerInformation['ACTION'] = ''
            if PlayerInformation['Y'] + MovementSpeed <= ScreenHeight - Radius:
                Wall = Walls[PlayerTile[1] + 1][PlayerTile[0]]
                CenterWall = Wall.center
                if Wall.collision(PlayerInformation['X'],
                                  PlayerInformation['Y'] + Radius + MovementSpeed) == 1:
                    PlayerInformation['Y'] += (Wall.y_down + Wall.y - PlayerInformation['Y'] - Radius) / 2
                else:
                    Wall = Walls[PlayerTile[1] + 1][PlayerTile[0] - 1]
                    if Wall.collision(PlayerInformation['X'] - Radius,
                                      PlayerInformation['Y'] + Radius + MovementSpeed) == 1:
                        PlayerInformation['Y'] += (Wall.y_down + Wall.y - PlayerInformation['Y'] - Radius) / 2
                        if CenterWall == -1:
                            PlayerInformation['X'] += (Wall.x_right + Wall.x - PlayerInformation['X'] + Radius + 1) / 2
                            PlayerInformation['Y'] += MovementSpeed
                    else:
                        Wall = Walls[PlayerTile[1] + 1][PlayerTile[0] + 1]
                        if Wall.collision(PlayerInformation['X'] + Radius,
                                          PlayerInformation['Y'] + Radius + MovementSpeed) == 1:
                            PlayerInformation['Y'] += (Wall.y_down + Wall.y - PlayerInformation['Y'] - Radius) / 2
                            if CenterWall == -1:
                                PlayerInformation['X'] += (Wall.x_left + Wall.x - PlayerInformation['X'] - Radius - 1) / 2
                                PlayerInformation['Y'] += MovementSpeed
                        else:
                            PlayerInformation['Y'] += MovementSpeed
            else:
                PlayerInformation['Y'] = ScreenHeight - Radius
        elif GetInformation(information, 4, 1):
            PlayerInformation['SPRITE'] = 'Down'
            PlayerInformation['ACTION'] = ''
            if PlayerInformation['Y'] - MovementSpeed >= Radius:
                Wall = Walls[PlayerTile[1] - 1][PlayerTile[0]]
                CenterWall = Wall.center
                if Wall.collision(PlayerInformation['X'],
                                  PlayerInformation['Y'] - Radius - MovementSpeed) == 1:
                    PlayerInformation['Y'] += (Wall.y_top + Wall.y - PlayerInformation['Y'] + Radius) / 2
                else:
                    Wall = Walls[PlayerTile[1] - 1][PlayerTile[0] - 1]
                    if Wall.collision(PlayerInformation['X'] - Radius,
                                      PlayerInformation['Y'] - Radius - MovementSpeed) == 1:
                        PlayerInformation['Y'] += (Wall.y_top + Wall.y - PlayerInformation['Y'] + Radius) / 2
                        if CenterWall == -1:
                            PlayerInformation['X'] += (Wall.x_right + Wall.x - PlayerInformation['X'] + Radius + 1) / 2
                            PlayerInformation['Y'] += -MovementSpeed
                    else:
                        Wall = Walls[PlayerTile[1] - 1][PlayerTile[0] + 1]
                        if Wall.collision(PlayerInformation['X'] + Radius,
                                          PlayerInformation['Y'] - Radius - MovementSpeed) == 1:
                            PlayerInformation['Y'] += (Wall.y_top + Wall.y - PlayerInformation['Y'] + Radius) / 2
                            if CenterWall == -1:
                                PlayerInformation['X'] += (Wall.x_left + Wall.x - PlayerInformation['X'] - Radius - 1) / 2
                                PlayerInformation['Y'] += -MovementSpeed
                        else:
                            PlayerInformation['Y'] += -MovementSpeed
            else:
                PlayerInformation['Y'] = Radius
    return PlayerInformation


def main():
    # Map config
    Walls = TileMap.ReadJson('Sprites/test_map_1')
    TileScale = TileMap.GetTileScale('Sprites/test_map_1')

    # HOST CONFIG
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 5000
    print(HOST, PORT)

    # Socket Config
    ServerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creation if socket
    ServerSock.bind((HOST, PORT))  # Bind of socket
    ServerSock.listen()  # Open socket

    # Clients Config
    Clients = {}  # Create List

    # PlayerOne Config
    #   Create PlayerOne X, Y, Color config
    PlayerOnePositionX = 20  # PlayerOne X Position
    PlayerOnePositionY = 20  # PlayerOne Y Position
    PlayerOneColor = "007CAD"  # PlayerOne Sprite
    #   Create PlayerOne List
    PlayerOneInformation = {
        'X': PlayerOnePositionX,
        'Y': PlayerOnePositionY,
        'SPRITE': 'Down',
        'ACTION': 'Static'
    }

    # All Player Config
    Players = {
        'Player1': PlayerOneInformation,
    }

    # Connection to Client
    #    First Client
    Client, Address = ServerSock.accept()  # Accept connection
    Clients['Player1'] = [Client, Address]  # Accept data of Client
    print("Connected to", {Clients['Player1'][0]})  # Printing for me
    Server.DynamicSend(Clients['Player1'][0], 'Player1'.encode('utf-8'))  # Send name of Client
    Server.DynamicSend(Clients['Player1'][0], pickle.dumps(Players))  # Send X and Y
    Server.DynamicSend(Clients['Player1'][0], 'Sprites/test_map_1'.encode('utf-8'))

    # Start working
    while True:
        Data = {}  # Creation of data list
        PlayerOneInformation['ACTION'] = 'Static'
        # Trying to recv PlayerOne action
        try:
            Data = Server.DynamicRecv(Clients['Player1'][0])  # Recv
        except ConnectionError:
            print("Connection Error")  # Say of Error

        # Trying to read action
        try:
            # If we have action
            if Data != None:
                # If action is normal
                if int(Data):
                    Information = int(Data)  # Read action
                    # If action is not right
                    if Information == 192:
                        Information = 0
                    elif Information == 48:
                        Information = 0
                    PlayerOneInformation = EditPosition(Information,
                                                        PlayerOneInformation,
                                                        Walls,
                                                        TileScale)  # Making new position
        except:
            print("Data has benn broken")

        # If we can send without problem
        if Server.DynamicSend(Clients['Player1'][0], pickle.dumps(Players)) != 0:
            try:
                Clients['Player1'] = Server.Accept(ServerSock,
                                                   Players,
                                                   'Player1',
                                                   'Sprites/test_map_1')  # Try to create new connection
            except:
                print("Bad")


main()
