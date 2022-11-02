import arcade

SPRITE_SCALING = 0.45
TILE_SCALING = 0.5
GRID_PIXEL_SIZE = 64

DEFAULT_SCREEN_WIDTH = 640
DEFAULT_SCREEN_HEIGHT = 640
SCREEN_TITLE = "Tiles"

PLAYER_MOVEMENT_SPEED = 7

class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.ASH_GREY)

        self.player_list = None
        self.floor_list = None
        self.wall_list = None
        self.player_sprite = None
    
        self.physics_engine = None

        self.tile_map = None

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()

        self.player_sprite = arcade.Sprite("Sprites/Square.png", scale = SPRITE_SCALING)
        self.player_sprite.center_x = 32
        self.player_sprite.center_y = 32
        self.player_list.append(self.player_sprite)

        self.tile_map = arcade.load_tilemap("Sprites/test_map_1.json", scaling = TILE_SCALING)
        self.floor_list = self.tile_map.sprite_lists["Base"]
        self.wall_list = self.tile_map.sprite_lists["Walls"]

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

    def on_draw(self):
        arcade.start_render()
        
        self.floor_list.draw()
        self.wall_list.draw()
        self.player_list.draw()
        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = False
        if key == arcade.key.RIGHT:
            self.right_pressed = False
        if key == arcade.key.UP:
            self.up_pressed = False
        if key == arcade.key.DOWN:
            self.down_pressed = False

    def on_update(self, delta_time):
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

        self.physics_engine.update()

def main():
    window = MyGame(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

main()