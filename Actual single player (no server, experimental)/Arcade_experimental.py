import copy
import queue
import random
import arcade
import Sprites.JsonReadTest as TileMap


class Player:
    def __init__(self, pos_x, pos_y):
        self.sprite = None
        self.player_sprite = {}
        self.last = ''
        self.action = ''
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.change_x = 0
        self.change_y = 0

    def draw(self):
        self.sprite.set_position(self.pos_x, self.pos_y)
        self.sprite.draw()

    def set_position(self, pos_x, pos_y):
        self.pos_x = pos_x + self.change_x
        self.pos_y = pos_y + self.change_y

    def get_sprite(self):
        self.sprite = self.player_sprite[self.last + self.action]

    def set_sprite(self, last, action):
        self.last = last
        self.action = action


class TheGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.ASH_GREY)

        self.set_mouse_visible(False)
        self.player = Player(60, 60)
        self.floor_list = None
        self.wall_list = None
        self.tile_map = None
        self.tile_scale = None
        self.physics_engine = None
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
        self.player.set_sprite('Down', 'Static')
        self.player.get_sprite()

        self.width_map = TileMap.GetBoards("test_map_1")[0]
        self.height_map = TileMap.GetBoards("test_map_1")[1]
        self.width = width
        self.height = height
        self.camera = arcade.Camera(width, height)
        self.camera_x = self.player.pos_x
        self.camera_y = self.player.pos_y

        self.internal_counter = 0
        self.Walls = None    # didn't use it here
        self.BasePath = None
        self.Path = None
        self.Target = None   # I need a place to go to, don't I?

    def setup(self, _map):

        self.player.sprite = arcade.Sprite('PlayersSprite/Down.png')

        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()

        self.tile_scale = TileMap.GetScale(_map)
        self.tile_map = arcade.load_tilemap(_map + '.json', scaling=self.tile_scale)
        self.floor_list = self.tile_map.sprite_lists["Base"]
        self.wall_list = self.tile_map.sprite_lists["Walls"]

        # Rip collisions, but im kinda lazy
        self.Walls, self.BasePath = TileMap.ReadJson('Sprites/Test_map_1')
        self.internal_counter = 0

        # first target
        self.Target = [random.randint(1, 18), random.randint(1, 18)]
        while self.BasePath[self.Target[0]][self.Target[1]] == -1:
            self.Target = [random.randint(1, 18), random.randint(1, 18)]

    def on_draw(self):
        arcade.start_render()

        self.camera.use()
        self.floor_list.draw()
        self.wall_list.draw()

        if self.Target:
            arcade.draw_circle_filled(
                (self.Target[0] * 64 + 32) * self.tile_scale,
                (self.Target[1] * 64 + 32) * self.tile_scale,
                12,
                [128, 0, 0]   # that means red (maroon actually)
            )
        if self.Path:
            s = copy.copy(self.Target)
            while self.Path[s[0]][s[1]] != -1:
                e = self.Path[s[0]][s[1]]
                arcade.draw_line(
                    (s[0] * 64 + 32) * self.tile_scale,
                    (s[1] * 64 + 32) * self.tile_scale,
                    (e[0] * 64 + 32) * self.tile_scale,
                    (e[1] * 64 + 32) * self.tile_scale,
                    [128, 0, 0],
                    7
                )
                s = e

        self.player.draw()

    def update(self, delta_time):
        if self.player.action != 'Static':
            self.player.sprite.update_animation()

        if not self.player.pos_x - self.width / 2 <= 0:
            if not self.player.pos_x + self.width / 2 >= self.width_map:
                self.camera_x = self.player.pos_x
        if not self.player.pos_y - self.height / 2 <= 0:
            if not self.player.pos_y + self.height / 2 >= self.height_map:
                self.camera_y = self.player.pos_y
        self.camera.move([self.camera_x - self.width / 2, self.camera_y - self.height / 2])

        self.player.set_position(self.player.pos_x, self.player.pos_y)

        if self.player.change_y == 0 and self.player.change_x == 0:
            self.player.action = 'Static'
        else:
            self.player.action = ''
            if self.player.change_y > 0:
                self.player.last = 'Up'
            elif self.player.change_y < 0:
                self.player.last = 'Down'
            elif self.player.change_x > 0:
                self.player.last = 'Right'
            elif self.player.change_x < 0:
                self.player.last = 'Left'

        self.player.set_sprite(self.player.last, self.player.action)
        self.player.get_sprite()

        # self.camera.move([self.player.pos_x - self.width / 2, self.player.pos_y - self.height / 2])

        # Setting a Target
        if self.Target == TileMap.GetTile(self.player.pos_x / 64, self.player.pos_y / 64, self.tile_scale):
            self.Target = [random.randint(1, 18), random.randint(1, 18)]
            while self.BasePath[self.Target[0]][self.Target[1]] == -1:
                self.Target = [random.randint(1, 18), random.randint(1, 18)]

        # Pathfinding time!
        self.Path = copy.deepcopy(self.BasePath)                                               # Reset pathing board
        v = TileMap.GetTile(self.player.pos_x / 64, self.player.pos_y / 64, self.tile_scale)   # Player pos
        q = queue.Queue()                                                                      # BFS main queue
        q.put(v)
        self.Path[v[0]][v[1]] = -1
        while not q.empty():
            v = q.get()
            if self.Path[v[0] - 1][v[1]] == 1:                # Left
                q.put([v[0] - 1, v[1]])
                self.Path[v[0] - 1][v[1]] = [v[0], v[1]]
            if self.Path[v[0]][v[1] - 1] == 1:                # Down
                q.put([v[0], v[1] - 1])
                self.Path[v[0]][v[1] - 1] = [v[0], v[1]]
            if self.Path[v[0] + 1][v[1]] == 1:                # Right
                q.put([v[0] + 1, v[1]])
                self.Path[v[0] + 1][v[1]] = [v[0], v[1]]
            if self.Path[v[0]][v[1] + 1] == 1:                # Up
                q.put([v[0], v[1] + 1])
                self.Path[v[0]][v[1] + 1] = [v[0], v[1]]

    def on_key_press(self, key, modifiers):
        self.player.action = ''
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -5
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 5
        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = 5
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = -5

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            if not self.player.change_x == 5:
                self.player.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            if not self.player.change_x == -5:
                self.player.change_x = 0
        if key == arcade.key.UP or key == arcade.key.W:
            if not self.player.change_y == -5:
                self.player.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            if not self.player.change_y == 5:
                self.player.change_y = 0


def main():
    # Window config
    _window = TileMap.GetConfig("config")

    # Create window
    window = TheGame(_window[1], _window[0], _window[2])
    # Setup window
    window.setup('Sprites/test_map_1')
    # Start game
    arcade.run()


main()
