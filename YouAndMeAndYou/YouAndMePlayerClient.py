import copy
import queue
import random
import sys
import socket
import arcade
import pickle
import ServerFunctions as Client
import JsonReadTest as TileMap


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

    def plus_information(self, number_of_bit, change):
        if change == 1:
            mask = 1
            mask = mask << number_of_bit
            self.player_information += mask

    def set_position(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def get_sprite(self):
        self.sprite = self.player_sprite[self.last + self.action]

    def set_sprite(self, last, action):
        self.last = last
        self.action = action


class OtherPlayer:
    def __init__(self, pos_x, pos_y, radius):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.sprite = None
        self.player_sprite = {}
        self.last = ''
        self.action = ''

    def draw(self):
        self.sprite.set_position(self.pos_x, self.pos_y)
        self.sprite.draw()

    def set_position(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def get_sprite(self):
        self.sprite = self.player_sprite[self.last + self.action]

    def set_sprite(self, last, action):
        self.last = last
        self.action = action


class Camera:

    def __init__(self, height, width, height_map, width_map):
        self.height = height
        self.width = width
        self.camera = arcade.Camera(width, height)
        self.camera_x = self.height / 2
        self.camera_y = self.width / 2
        self.height_map = height_map
        self.width_map = width_map
        self.players = []
        self.score = {}

    def set_position(self, x, y):
        if not x - self.width / 2 <= 0:
            if not x + self.width / 2 >= self.width_map:
                self.camera_x = x
        if not y - self.height / 2 <= 0:
            if not y >= self.height_map:
                self.camera_y = y
        self.camera.move([self.camera_x - self.width / 2, self.camera_y - self.height / 2])

    def draw(self):
        self.camera.use()
        delta = 20
        for players in self.players:
            arcade.draw_text(players + ": " + str(self.score[players]),
                             self.camera_x - self.width / 2 + 5,
                             self.camera_y + self.height / 2 - delta,
                             arcade.color.WHITE,
                             font_size=14,
                             font_name="Kenney Blocks")
            delta += 20

    def set_score(self, player, score):
        if player not in self.players:
            self.players.append(player)
        self.score[player] = score

    def plus_score(self, player, score):
        self.score[player] += score


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

        self.PlayersList = [
            'Player1',
            'Player2',
            'Player3'
        ]
        self.players = {}
        for players in self.PlayersList:
            if players == playernumber:
                self.player = Player(data[playernumber]['X'],
                                     data[playernumber]['Y'],
                                     0,
                                     0,
                                     15,
                                     playernumber)
            else:
                self.players[players] = OtherPlayer(data[players]['X'],
                                                    data[players]['Y'],
                                                    15)
        self.set_mouse_visible(False)
        self.decore = None
        self.floor_list = None
        self.objects = None
        self.tile_map = None
        self.sock = sock
        self.map = Map
        self.camera = Camera(height, width, TileMap.GetBoards(self.map)[1], TileMap.GetBoards(self.map)[0])
        for players in self.PlayersList:
            path = 'PlayersSprites/' + players + '/Animations/'
            if players == playernumber:
                self.player.player_sprite = {
                    'Up': arcade.load_animated_gif(path + 'Up.gif'),
                    'Down': arcade.load_animated_gif(path + 'Down.gif'),
                    'Left': arcade.load_animated_gif(path + 'Left.gif'),
                    'Right': arcade.load_animated_gif(path + 'Right.gif'),
                    'UpStatic': arcade.Sprite(path + 'Up.png'),
                    'DownStatic': arcade.Sprite(path + 'Down.png'),
                    'LeftStatic': arcade.Sprite(path + 'Left.png'),
                    'RightStatic': arcade.Sprite(path + 'Right.png')
                }
                for sprite in self.player.player_sprite:
                    self.player.player_sprite[sprite].scale = 1
                self.player.set_sprite(data[playernumber]['SPRITE'], data[playernumber]['ACTION'])
                self.player.get_sprite()
            else:
                self.players[players].player_sprite = {
                    'Up': arcade.load_animated_gif(path + 'Up.gif'),
                    'Down': arcade.load_animated_gif(path + 'Down.gif'),
                    'Left': arcade.load_animated_gif(path + 'Left.gif'),
                    'Right': arcade.load_animated_gif(path + 'Right.gif'),
                    'UpStatic': arcade.Sprite(path + 'Up.png'),
                    'DownStatic': arcade.Sprite(path + 'Down.png'),
                    'LeftStatic': arcade.Sprite(path + 'Left.png'),
                    'RightStatic': arcade.Sprite(path + 'Right.png')
                }
                for sprite in self.players[players].player_sprite:
                    self.players[players].player_sprite[sprite].scale = 1
                self.players[players].set_sprite(data[playernumber]['SPRITE'], data[playernumber]['ACTION'])
                self.players[players].get_sprite()
            self.camera.set_score(players, 0)
        self.BasePath = None
        self.Path = None
        self.Target = None  # I need a place to go to, don't I?

    def setup(self, Map):
        TileScale = TileMap.GetScale(Map)

        self.floor_list = arcade.SpriteList()

        self.tile_map = arcade.load_tilemap("Maps/" + Map + "/" + Map + '.json', scaling=TileScale)
        self.floor_list = self.tile_map.sprite_lists["Base"]
        self.objects = self.tile_map.sprite_lists["Objects"]
        self.decore = self.tile_map.sprite_lists["Decore"]

        self.BasePath = TileMap.GetPath(Map)

        # first target
        self.Target = [random.randint(1, 28), random.randint(1, 28)]
        while self.BasePath[self.Target[1]][self.Target[0]] == -1:
            self.Target = [random.randint(1, 28), random.randint(1, 28)]

        self.camera.set_position(self.player.pos_x, self.player.pos_y)

    def on_draw(self):
        arcade.start_render()

        self.floor_list.draw()
        self.objects.draw()
        self.decore.draw()

        if self.Target:
            arcade.draw_circle_filled(
                (self.Target[0] * 64 + 32),
                (self.Target[1] * 64 + 32),
                12,
                [128, 0, 0]  # that means red (maroon actually)
            )
        if self.Path:
            s = copy.copy(self.Target)
            while self.Path[s[1]][s[0]] != -1:
                e = self.Path[s[1]][s[0]]
                arcade.draw_line(
                    (s[0] * 64 + 32),
                    (s[1] * 64 + 32),
                    (e[1] * 64 + 32),
                    (e[0] * 64 + 32),
                    [128, 0, 0],
                    7
                )
                s[0] = e[1]
                s[1] = e[0]

        for players in self.PlayersList:
            if players != self.player.number:
                self.players[players].draw()
            else:
                self.player.draw()

        for players in self.PlayersList:
            if players == self.player.number:
                arcade.draw_text(self.player.number,
                                 self.player.pos_x + 2,
                                 self.player.pos_y + 38,
                                 arcade.color.WHITE,
                                 font_size=14,
                                 font_name="Kenney Blocks",
                                 anchor_x='center')
            else:
                arcade.draw_text(players,
                                 self.players[players].pos_x + 2,
                                 self.players[players].pos_y + 38,
                                 arcade.color.WHITE,
                                 font_size=14,
                                 font_name="Kenney Blocks",
                                 anchor_x='center')

        self.camera.draw()

    def update(self, delta_time):
        for players in self.PlayersList:
            if players == self.player.number:
                if self.player.action != 'Static':
                    self.player.sprite.update_animation()
            else:
                if self.players[players].action != 'Static':
                    self.players[players].sprite.update_animation()

        if Client.DynamicSend(self.sock, str(self.player.player_information).encode()) != 0:
            print("Bad")

        try:
            Data = pickle.loads(Client.DynamicRecv(self.sock))
        except:
            Data = None

        if Data != None:
            self.camera.set_position(Data[self.player.number]['X'], Data[self.player.number]['Y'])
            for players in self.PlayersList:
                if players == self.player.number:
                    self.player.set_position(Data[players]['X'], Data[players]['Y'])
                    self.player.set_sprite(Data[self.player.number]['SPRITE'], Data[self.player.number]['ACTION'])
                    self.camera.set_score(players, Data[self.player.number]['SCORE'])
                else:
                    self.players[players].set_position(Data[players]['X'], Data[players]['Y'])
                    self.players[players].set_sprite(Data[players]['SPRITE'], Data[players]['ACTION'])
                    self.camera.set_score(players, Data[players]['SCORE'])
        else:
            for players in self.PlayersList:
                if players == self.player.number:
                    self.player.set_sprite(self.player.last, '')
                else:
                    self.players[players].set_sprite(self.players[players].last, '')

        for players in self.PlayersList:
            if players == self.player.number:
                self.player.get_sprite()
                self.player.set_information(0, 0)
            else:
                self.players[players].get_sprite()

        # Setting a Target
        if self.Target == TileMap.GetTile(self.player.pos_x, self.player.pos_y, 64):
            self.player.plus_information(0, 1)
            self.Target = [random.randint(1, 28), random.randint(1, 28)]
            while self.BasePath[self.Target[1]][self.Target[0]] == -1:
                self.Target = [random.randint(1, 28), random.randint(1, 28)]

        # Pathfinding time!
        self.Path = copy.deepcopy(self.BasePath)  # Reset pathing board
        v = TileMap.GetTile(self.player.pos_x, self.player.pos_y, 64)  # Player pos
        q = queue.Queue()  # BFS main queue
        q.put(v)
        self.Path[v[1]][v[0]] = -1
        while not q.empty():
            v = q.get()
            if self.Path[v[1] - 1][v[0]] == 1:  # DOWN
                q.put([v[0], v[1] - 1])
                self.Path[v[1] - 1][v[0]] = [v[1], v[0]]
            if self.Path[v[1]][v[0] - 1] == 1:  # LEFT
                q.put([v[0] - 1, v[1]])
                self.Path[v[1]][v[0] - 1] = [v[1], v[0]]
            if self.Path[v[1] + 1][v[0]] == 1:  # UP
                q.put([v[0], v[1] + 1])
                self.Path[v[1] + 1][v[0]] = [v[1], v[0]]
            if self.Path[v[1]][v[0] + 1] == 1:  # RIGHT
                q.put([v[0] + 1, v[1]])
                self.Path[v[1]][v[0] + 1] = [v[1], v[0]]

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
    HOST = input()
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
