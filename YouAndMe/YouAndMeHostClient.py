import sys
import socket
import arcade
import pickle
import ServerFunctions as Client
import Sprites.JsonReadTest as TileMap


class Player:
    def __init__(self,
                 pos_x,
                 pos_y,
                 change_x,
                 change_y,
                 radius,
                 color,
                 number):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.change_x = change_x
        self.change_y = change_y
        self.radius = radius
        self.color = color
        self.player_information = 0
        self.number = number

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
    def __init__(self,
                 width,
                 height,
                 title,
                 data,
                 playernumber,
                 sock):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.ASH_GREY)

        self.PlayersList = [
            'Player1',
            'Player2'
        ]
        self.players = {}
        for players in self.PlayersList:
            if players == playernumber:
                self.player = Player(data[playernumber]['X'],
                                     data[playernumber]['Y'],
                                     0,
                                     0,
                                     15,
                                     arcade.color_from_hex_string(data[playernumber]['COLOR']),
                                     playernumber)
            else:
                self.players[players] = OtherPlayer(data[players]['X'],
                                                    data[players]['Y'],
                                                    15,
                                                    arcade.color_from_hex_string(data[players]['COLOR']))

        self.set_mouse_visible(False)
        self.floor_list = None
        self.wall_list = None
        self.tile_map = None
        self.sock = sock

    def setup(self, Map):
        TileScale = TileMap.GetScale(Map)

        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()

        self.tile_map = arcade.load_tilemap(Map + '.json', scaling=TileScale)
        self.floor_list = self.tile_map.sprite_lists["Base"]
        self.wall_list = self.tile_map.sprite_lists["Walls"]

    def on_draw(self):
        arcade.start_render()

        self.floor_list.draw()
        self.wall_list.draw()
        self.player.draw()

        for players in self.PlayersList:
            if players != self.player.number:
                self.players[players].draw()

    def update(self, delta_time):
        if Client.DynamicSend(self.sock, str(self.player.player_information).encode()) != 0:
            print("Bad")

        try:
            Data = pickle.loads(Client.DynamicRecv(self.sock))
        except:
            Data = None

        if Data != None:
            for players in self.PlayersList:
                if players == self.player.number:
                    self.player.set_position(Data[players]['X'], Data[players]['Y'])
                else:
                    self.players[players].set_position(Data[players]['X'], Data[players]['Y'])

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
    # Window config
    Window = TileMap.GetConfig("config")

    # Socket config
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 5000

    # Create Socket
    ClientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connection to server
    while True:
        try:
            ClientSock.connect((HOST, PORT))
            print("Ok")
            break
        except ConnectionError:
            print("Trying to connect to server")

    # Listen PlayerNumber
    PlayerNumber = Client.DynamicRecv(ClientSock).decode('utf-8')
    print(PlayerNumber)  # Print it for me

    # Listen Data for balls
    while True:
        try:
            Data = Client.DynamicRecv(ClientSock)  # Listen data
            Data = pickle.loads(Data)  # Process data
            print(Data)  # Print it for me
            break
        except ConnectionError:
            print("Waiting another players")

    # Listen map
    Map = Client.DynamicRecv(ClientSock).decode('utf-8')

    # Create Game
    #   Create window
    window = TheGame(Window[1],
                     Window[0],
                     Window[2],
                     Data,
                     PlayerNumber,
                     ClientSock)
    #   Setup window
    window.setup(Map)
    #   Start game
    arcade.run()


main()
