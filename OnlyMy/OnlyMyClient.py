import sys
import socket
import arcade
import pickle
import ServerFunctions as Client
import OnlyMy.JsonReadTest as TileMap


class Player:
    def __init__(self,
                 pos_x,
                 pos_y,
                 change_x,
                 change_y,
                 radius,
                 number):
        self.sprite = None
        self.player_sprite = {}
        self.last = ''
        self.action = ''
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.change_x = change_x
        self.change_y = change_y
        self.radius = radius
        self.player_information = 0
        self.player_information_demo = 0
        self.number = number

    def draw(self):
        self.sprite.set_position(self.pos_x, self.pos_y)
        self.sprite.draw()

    def set_information(self, number_of_bit, change):
        if change == 1:
            mask = 1
            mask = mask << number_of_bit
            self.player_information = mask
            self.player_information_demo = self.player_information_demo | mask
            if self.player_information == 0:
                self.player_information = self.player_information_demo
        else:
            mask = 255
            mask = mask - pow(2, number_of_bit)
            self.player_information = self.player_information & mask
            self.player_information_demo = self.player_information_demo & mask
            if self.player_information == 0:
                self.player_information = self.player_information_demo

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

    def get_sprite(self):
        self.sprite = self.player_sprite[self.last + self.action]

    def set_sprite(self, last, action):
        self.last = last
        self.action = action


class TheGame(arcade.Window):

    def __init__(self,
                 width,
                 height,
                 title,
                 data,
                 playernumber,
                 sock,
                 Map):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK)

        self.set_mouse_visible(False)
        self.player = Player(data[playernumber]['X'],
                             data[playernumber]['Y'],
                             0,
                             0,
                             15,
                             playernumber)
        self.decore = None
        self.floor_list = None
        self.objects = []
        self.tile_map = None
        self.sock = sock
        self.player.player_sprite = {
            'Up': arcade.load_animated_gif('PlayersSprite/Up.gif'),
            'Down': arcade.load_animated_gif('PlayersSprite/Down.gif'),
            'Left': arcade.load_animated_gif('PlayersSprite/Left.gif'),
            'Right': arcade.load_animated_gif('PlayersSprite/Right.gif'),
            'UpStatic': arcade.Sprite('PlayersSprite/Up.png'),
            'DownStatic': arcade.Sprite('PlayersSprite/Down.png'),
            'LeftStatic': arcade.Sprite('PlayersSprite/Left.png'),
            'RightStatic': arcade.Sprite('PlayersSprite/Right.png')
        }
        for sprite in self.player.player_sprite:
            self.player.player_sprite[sprite].scale = 1
        self.player.set_sprite(data[playernumber]['SPRITE'], data[playernumber]['ACTION'])
        self.player.get_sprite()
        self.map = Map
        self.width_map = TileMap.GetBoards(self.map)[0]
        self.height_map = TileMap.GetBoards(self.map)[1]
        self.width = width
        self.height = height
        self.camera = arcade.Camera(width, height)
        self.camera_x = self.player.pos_x
        self.camera_y = self.player.pos_y

    def setup(self, Map):
        TileScale = TileMap.GetScale(Map)

        self.floor_list = arcade.SpriteList()

        self.tile_map = arcade.load_tilemap("Maps/" + Map + "/" + Map + '.json', scaling=TileScale)
        self.floor_list = self.tile_map.sprite_lists["Base"]
        for layers in TileMap.GetConfigMap(Map)["layers"]:
            self.objects.append(self.tile_map.sprite_lists[layers])
        self.decore = self.tile_map.sprite_lists["Decore"]

    def on_draw(self):
        arcade.start_render()

        self.camera.use()
        self.floor_list.draw()
        for i in range(len(self.objects)):
            self.objects[i].draw()
        self.decore.draw()
        self.player.draw()

    def update(self, delta_time):
        if self.player.action != 'Static':
            self.player.sprite.update_animation()

        if Client.DynamicSend(self.sock, str(self.player.player_information).encode()) != 0:
            print("Bad")

        try:
            Data = pickle.loads(Client.DynamicRecv(self.sock))
        except:
            Data = None

        if Data != None:
            if not Data[self.player.number]['X'] - self.width / 2 <= 0:
                if not Data[self.player.number]['X'] + self.width / 2 >= self.width_map:
                    self.camera_x = Data[self.player.number]['X']
            if not Data[self.player.number]['Y'] - self.height / 2 <= 0:
                if not Data[self.player.number]['Y'] + self.height / 2 >= self.height_map:
                    self.camera_y = Data[self.player.number]['Y']
            self.camera.move([self.camera_x - self.width / 2, self.camera_y - self.height / 2])

            self.player.set_position(Data[self.player.number]['X'], Data[self.player.number]['Y'])
            self.player.set_sprite(Data[self.player.number]['SPRITE'], Data[self.player.number]['ACTION'])
        else:
            self.player.set_sprite(self.player.last, '')
        self.player.get_sprite()

        # elf.camera.move([self.player.pos_x - self.width / 2, self.player.pos_y - self.height / 2])

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
                     ClientSock,
                     Map)
    #   Setup window
    window.setup(Map)
    #   Start game
    arcade.run()


main()
