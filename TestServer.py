import socket
import pickle

# Client Config
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
RADIUS = 15

# HOST CONFIG
HOST = '192.168.31.11'
PORT = 5000
MOVEMENT_SPEED = 10

# Player Two Config
PlayerTwoPositionX = 50
PlayerTwoPositionY = 50
PlayerTwoColor = "EB5284"
PlayerTwoInformation = {
    'X': PlayerTwoPositionX,
    'Y': PlayerTwoPositionY,
    'COLOR': PlayerTwoColor
}



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
        if get_information(information, 7, 1):
            if PlayerInformation['X'] - MOVEMENT_SPEED >= RADIUS:
                PlayerInformation['X'] += -MOVEMENT_SPEED
            else:
                PlayerInformation['X'] = RADIUS
        elif get_information(information, 6, 1):
            if PlayerInformation['X'] + MOVEMENT_SPEED <= SCREEN_WIDTH - RADIUS:
                PlayerInformation['X'] += MOVEMENT_SPEED
            else:
                PlayerInformation['X'] = SCREEN_WIDTH - RADIUS

        if get_information(information, 5, 1):
            if PlayerInformation['Y'] + MOVEMENT_SPEED <= SCREEN_HEIGHT - RADIUS:
                PlayerInformation['Y'] += MOVEMENT_SPEED
            else:
                PlayerInformation['Y'] = SCREEN_HEIGHT - RADIUS

        elif get_information(information, 4, 1):
            if PlayerInformation['Y'] - MOVEMENT_SPEED >= RADIUS:
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
    PlayerOnePositionX = 50
    PlayerOnePositionY = 50
    PlayerOneColor = "007CAD"
    PlayerOneInformation = {
        'X': PlayerOnePositionX,
        'Y': PlayerOnePositionY,
        'COLOR': PlayerOneColor
    }

    # Player Two Config
    PlayerTwoPositionX = 100
    PlayerTwoPositionY = 50
    PlayerTwoColor = "EB5284"

    PlayerTwoInformation = {
        'X': PlayerTwoPositionX,
        'Y': PlayerTwoPositionY,
        'COLOR': PlayerTwoColor
    }

    # Config
    Players = {
        'Player1': PlayerOneInformation,
        'Player2': PlayerTwoInformation
    }

    Client, Address = ServerSock.accept()

    Clients['Player1'] = [Client, Address]
    print("Connected to", {Clients['Player1'][1]})

    Client, Address = ServerSock.accept()

    Clients['Player2'] = [Client, Address]
    print("Connected to", {Clients['Player2'][1]})

    Clients['Player1'][0].send('Player1'.encode())
    Clients['Player1'][0].send('Player2'.encode())

    Clients['Player2'][0].send('Player2'.encode())
    Clients['Player2'][0].send('Player1'.encode())

    Clients['Player1'][0].send(pickle.dumps(Players))
    Clients['Player2'][0].send(pickle.dumps(Players))

    Connection = True
    while Connection:
        try:
            Data = Clients['Player1'][0].recv(1024)
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

        try:
            Data = Clients['Player2'][0].recv(1024)
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

        Clients['Player1'][0].send(pickle.dumps(Players))
        Clients['Player2'][0].send(pickle.dumps(Players))


main()
