import sys
import socket
import arcade
import pickle

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
MOVEMENT_SPEED = 10

HOST = input()
PORT = 5000

ClientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Data = {}

Connection = True
while Connection:
    try:
        ClientSock.connect((HOST, PORT))
        Connection = False
    except ConnectionError:
        print("Trying to connect to server")
        Connection = True

PlayerNumber = ClientSock.recv(1024).decode()
PlayerAnotherNumber = ClientSock.recv(1024).decode()

print(PlayerNumber, PlayerAnotherNumber)

Connection = True
while Connection:
    try:
        Data = pickle.loads(ClientSock.recv(1024))
        Connection = False
    except ConnectionError:
        print("Waiting another players")
        Connection = True


class Player:
    player_information = int

    def __init__(self, pos_x, pos_y, change_x, change_y, radius, color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.change_x = change_x
        self.change_y = change_y
        self.radius = radius
        self.color = color
        self.player_information = 0

    def draw(self):
        arcade.draw_circle_filled(self.pos_x,
                                  self.pos_y,
                                  self.radius,
                                  self.color)

    def set_information(self, number_of_bit, change):
        if change == 1:
            mask = 1
            mask = mask << number_of_bit
            self.player_information = self.player_information | mask
        else:
            mask = 255
            mask = mask - pow(2, number_of_bit)
            self.player_information = self.player_information & mask

    def print_information(self):
        print('{0:08b}'.format(self.player_information), sys.getsizeof(self.player_information))

    def change_information(self, new_information):
        self.player_information = new_information

    def get_information(self, number_of_bite, value):
        mask = 1
        mask = mask << number_of_bite
        if value == 1:
            if self.player_information & mask != 0:
                return 1
            else:
                return 0
        else:
            if self.player_information & mask != 0:
                return 0
            else:
                return 1

    def set_position(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

class OtherPlayer:

    def __init__(self, pos_x, pos_y, radius, color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.color = color

    def draw(self):
        arcade.draw_circle_filled(self.pos_x,
                                  self.pos_y,
                                  self.radius,
                                  self.color)

    def set_position(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y


class TheGame(arcade.Window):

    def __init__(self, width, height, title):

        super().__init__(width, height, title)

        self.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.ASH_GREY)

        self.player = Player(Data[PlayerNumber]['X'], Data[PlayerNumber]['Y'], 0, 0, 15, arcade.color_from_hex_string(Data[PlayerNumber]['COLOR']))
        self.player2 = OtherPlayer(Data[PlayerAnotherNumber]['X'], Data[PlayerAnotherNumber]['Y'], 15, arcade.color_from_hex_string(Data[PlayerAnotherNumber]['COLOR']))

    def on_draw(self):
        arcade.start_render()
        self.player.draw()
        self.player2.draw()

    def update(self, delta_time):
        ClientSock.send(str(self.player.player_information).encode())

        Data = pickle.loads(ClientSock.recv(2048))

        # print(Data)
        self.player.set_position(Data[PlayerNumber]['X'], Data[PlayerNumber]['Y'])
        self.player2.set_position(Data[PlayerAnotherNumber]['X'], Data[PlayerAnotherNumber]['Y'])

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.set_information(7, 1)
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.set_information(6, 1)
        elif key == arcade.key.UP or key == arcade.key.W:
            self.player.set_information(5, 1)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.set_information(4, 1)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.set_information(7, 0)
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.set_information(6, 0)
        elif key == arcade.key.UP or key == arcade.key.W:
            self.player.set_information(5, 0)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.set_information(4, 0)


def main():
    window = TheGame(640, 480, "Drawing Example")
    arcade.run()

main()
