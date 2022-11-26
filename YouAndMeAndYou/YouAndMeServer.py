import socket
import pickle
import JsonReadTest as TileMap
import ServerFunctions as Server


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
                            PlayerInformation['Y'] += (Wall.y_top + Wall.y - PlayerInformation['Y'] + RadiusDown + 1) / 4
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
                            PlayerInformation['Y'] += (Wall.y_top + Wall.y - PlayerInformation['Y'] + RadiusDown + 1) / 2
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
                            PlayerInformation['X'] += (Wall.x_left + Wall.x - PlayerInformation['X'] - RadiusRight - 1) / 2
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
                            PlayerInformation['X'] += (Wall.x_left + Wall.x - PlayerInformation['X'] - RadiusLeft - 1) / 2
                            PlayerInformation['Y'] += -MovementSpeed
                        else:
                            PlayerInformation['SPRITE'] = 'Down'
                            PlayerInformation['ACTION'] = 'Static'
                    else:
                        PlayerInformation['Y'] += -MovementSpeed
    return PlayerInformation


def main():
    # Map config
    Map = 'Dungeon_map_1'
    Walls = TileMap.ReadJson(Map)
    TileScale = TileMap.GetTileScale(Map)

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
    PlayerOnePositionX = 352  # PlayerOne X Position
    PlayerOnePositionY = 928  # PlayerOne Y Position
    #   Create PlayerOne List
    PlayerOneInformation = {
        'X': PlayerOnePositionX,
        'Y': PlayerOnePositionY,
        'SPRITE': 'Down',
        'ACTION': 'Static',
        'SCORE': 0
    }

    # PlayerTwo Config
    #   Create PlayerTwo X, Y, Color config
    PlayerTwoPositionX = 352  # PlayerTwo X Position
    PlayerTwoPositionY = 928  # PlayerTwo Y Position
    #   Create PlayerTwo List
    PlayerTwoInformation = {
        'X': PlayerTwoPositionX,
        'Y': PlayerTwoPositionY,
        'SPRITE': 'Down',
        'ACTION': 'Static',
        'SCORE': 0
    }

    # PlayerThree Config
    #   Create PlayerTwo X, Y, Color config
    PlayerThreePositionX = 352  # PlayerTwo X Position
    PlayerThreePositionY = 928  # PlayerTwo Y Position
    #   Create PlayerTwo List
    PlayerThreeInformation = {
        'X': PlayerThreePositionX,
        'Y': PlayerThreePositionY,
        'SPRITE': 'Down',
        'ACTION': 'Static',
        'SCORE': 0
    }

    # All Player Config
    Players = {
        'Player1': PlayerOneInformation,
        'Player2': PlayerTwoInformation,
        'Player3': PlayerThreeInformation
    }
    PlayersList = [
        'Player1',
        'Player2',
        'Player3'
    ]

    # Connection to Client
    for player in PlayersList:
        Client, Address = ServerSock.accept()  # Accept connection
        Clients[player] = [Client, Address]  # Accept data of Client
        print("Connected to", {Clients[player][1]})  # Printing for me
        Server.DynamicSend(Clients[player][0], player.encode('utf-8'))  # Send name of Client
        Server.DynamicSend(Clients[player][0], pickle.dumps(Players))  # Send X and Y
        Server.DynamicSend(Clients[player][0], Map.encode('utf-8'))

    # Start working
    while True:
        Data = {}  # Creation of data list
        for player in PlayersList:
            Players[player]['ACTION'] = 'Static'
            # ServerSock.settimeout(0.1)
            # Trying to recv PlayerOne action
            try:
                Data = Server.DynamicRecv(Clients[player][0])  # Recv
            except ConnectionError:
                print("Connection Error")  # Say of Error

            # Trying to read action
            try:
                # If we have action
                if Data != None:
                    # If action is normal
                    if int(Data):
                        Information = int(Data)  # Read action
                        if GetInformation(Information, 0, 1):
                            Players[player]['SCORE'] += 1
                            Information -= 1
                        # If action is not right
                        if Information == 192:
                            Information = 0
                        elif Information == 48:
                            Information = 0
                        Players[player] = EditPosition(Information,
                                                       Players[player],
                                                       Walls,
                                                       TileScale)  # Making new position
            except:
                print("Data has benn broken")

            # If we can send without problem
            if Server.DynamicSend(Clients[player][0], pickle.dumps(Players)) != 0:
                try:
                    Clients[player] = Server.Accept(ServerSock,
                                                    Players,
                                                    player,
                                                    Map)  # Try to create new connection
                except:
                    print("Bad")


main()
