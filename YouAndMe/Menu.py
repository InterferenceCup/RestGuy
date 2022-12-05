import subprocess
import JsonReadTest as Config
import time
from threading import Thread

import arcade
import arcade.gui


class Timer:  # 9
    def __init__(self):
        self._start_time = None

    def start(self):
        self._start_time = time.perf_counter()

    def stop(self):
        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        return elapsed_time

    def get(self):
        elapsed_time = time.perf_counter() - self._start_time
        return elapsed_time


# Creating MainGame class
class MainGame(arcade.Window):
    def __init__(self,
                 screen_width,
                 screen_height,
                 title):
        super().__init__(width=screen_width,
                         height=screen_height,
                         title=title)

        # Changing background color of screen
        arcade.set_background_color(arcade.color.BLACK)

        self.screen_width = screen_width
        self.screen_height = screen_height

        # Creating a UI MANAGER to handle the UI
        self.uimanager = {}
        self.menu = {}
        self.now_menu = 'main_menu'
        self.button_height = 60
        self.button_width = 200
        self.setup_menu_labels()
        self.setup_manager()
        self.set_manager()

        self.host = None
        self.host_console_tread = None
        self.host_text = ''

        self.host_player = None
        self.host_player_console_tread = None
        self.host_player_text = ''

        self.player = None
        self.player_console_tread = None
        self.player_text = ''

    def on_play_button_click(self, event):
        self.now_menu = 'play'
        self.set_manager()

    def on_back_to_menu_button_click(self, event):
        self.now_menu = 'main_menu'
        self.set_manager()

    def on_connect_button_click(self, event):
        if self.player != None:
            self.player.kill()
            self.player = None
        self.now_menu = 'player'
        self.set_manager()

    def on_exit_button_click(self, event):
        self.close()

    def on_back_from_host_button_click(self, event):
        self.now_menu = 'play'
        self.set_manager()
        self.host.kill()
        self.host_console_tread = None
        self.host_text = None
        self.host = None
        self.host_player.kill()
        self.host_player_console_tread = None
        self.host_player_text = None
        self.host_player = None

    def on_back_from_player_button_click(self, event):
        self.now_menu = 'play'
        self.set_manager()
        if self.player != None:
            self.player.kill()
        self.player_console_tread = None
        self.player_text = None
        self.player = None
        self.menu['player']['player_console'].child.text = "---PLAYER OUTPUT---\n"

    def on_host_button_click(self, event):
        self.now_menu = 'host'
        self.set_manager()
        if self.host == None:
            self.host = subprocess.Popen(['python', 'ThreadingServer.py'],
                                         stdout=subprocess.PIPE,
                                         stdin=subprocess.DEVNULL,
                                         stderr=subprocess.STDOUT)
        if self.host_player == None:
            self.host_player = subprocess.Popen(['python', 'YouAndMeHostClient.py'],
                                                stdout=subprocess.PIPE,
                                                stdin=subprocess.DEVNULL,
                                                stderr=subprocess.STDOUT)
        print("Server start!")

    def on_connect_to_host_button_click(self, event):
        if self.player == None:
            Config.SetLastIp(self.menu['player']['ip_input'].child.text)
            Config.SetLastPort(self.menu['player']['port_input'].child.text)
            self.player = subprocess.Popen(['python', 'YouAndMePlayerClient.py'],
                                           stdout=subprocess.PIPE,
                                           stdin=subprocess.DEVNULL,
                                           stderr=subprocess.STDOUT)

        print("Server start!")

    def player_console(self):
        self.player_text = "---PLAYER OUTPUT---\n"
        while True and self.player:
            output = self.player.stdout.readline().decode()
            if output != None and self.player_text != None:
                print(output)
                self.player_text = self.player_text + output
        print("Stop reading")

    def host_console(self):
        self.host_text = "---HOST OUTPUT---\n"
        while True and self.host:
            output = self.host.stdout.readline().decode()
            if output != None and self.host_text != None:
                print(output)
                self.host_text = self.host_text + output
        print("Stop reading")

    def host_player_console(self):
        self.host_player_text = "---HOST PLAYER OUTPUT---\n"
        while True and self.host_player:
            output = self.host_player.stdout.readline().decode()
            if output != None and self.host_player_text != None:
                print(output)
                self.host_player_text = self.host_player_text + output
        print("Stop reading")

    # Creating on_draw() function to draw on the screen
    def on_draw(self):
        arcade.start_render()

        # Drawing our ui manager
        if self.now_menu == 'host':
            if self.host_console_tread == None:
                self.host_console_tread = Thread(target=self.host_console)
                self.host_console_tread.start()
            if self.host_player_console_tread == None:
                self.host_player_console_tread = Thread(target=self.host_player_console)
                self.host_player_console_tread.start()
            if self.host_text != None:
                self.menu['host']['host_console'].child.text = self.host_text
            if self.host_player_text != None:
                self.menu['host']['host_player_console'].child.text = self.host_player_text
        if self.now_menu == 'player' and self.player != None:
            if self.player_console_tread == None:
                self.player_console_tread = Thread(target=self.player_console)
                self.player_console_tread.start()
            if self.player_text != None:
                self.menu['player']['player_console'].child.text = self.player_text
        self.uimanager[self.now_menu].draw()

    def set_manager(self):
        for manager in self.uimanager:
            self.uimanager[manager].disable()
        self.uimanager[self.now_menu].enable()

    def setup_menu_labels(self):
        # MAIN MENU
        """
        MAIN MENU STRUCT:
            - PLAY - TAP IT TO START GAME
            - EXIT - TAP IT TO EXIT FROM GAME
        """
        #   OBJECTS
        play_button = arcade.gui.UIFlatButton(text="Play",
                                              width=self.button_width,
                                              height=self.button_height)
        exit_button = arcade.gui.UIFlatButton(text="Exit",
                                              width=self.button_width,
                                              height=self.button_height)
        #   CLICKS
        play_button.on_click = self.on_play_button_click
        exit_button.on_click = self.on_exit_button_click

        # PLAY
        #   OBJECTS
        back_to_menu_button = arcade.gui.UIFlatButton(text="Back",
                                                      width=self.button_width,
                                                      height=self.button_height)
        host_button = arcade.gui.UIFlatButton(text="Host",
                                              width=self.button_width,
                                              height=self.button_height)
        connect_button = arcade.gui.UIFlatButton(text="Connect",
                                                 width=self.button_width,
                                                 height=self.button_height)
        #   CLICKS
        back_to_menu_button.on_click = self.on_back_to_menu_button_click
        host_button.on_click = self.on_host_button_click
        connect_button.on_click = self.on_connect_button_click

        # HOST LOBBY
        #   OBJECTS
        host_console = arcade.gui.UITextArea(text="",
                                             width=(self.width - self.button_width / 2) / 2,
                                             height=self.height / 2,
                                             font_name="Kenney Blocks")
        host_console_bordered = arcade.gui.UIBorder(child=host_console,
                                                    border_width=12,
                                                    border_color=arcade.color.WHITE)
        host_player_console = arcade.gui.UITextArea(text="",
                                                    width=(self.width - self.button_width / 2) / 2,
                                                    height=self.height / 2,
                                                    font_name="Kenney Blocks")
        host_player_console_bordered = arcade.gui.UIBorder(child=host_player_console,
                                                           border_width=12,
                                                           border_color=arcade.color.WHITE)
        back_from_host = arcade.gui.UIFlatButton(text="Back",
                                                 width=self.button_width,
                                                 height=self.button_height)
        #   CLICKS
        back_from_host.on_click = self.on_back_from_host_button_click

        # PLAYER MENU
        #   OBJECTS
        player_console = arcade.gui.UITextArea(text="---PLAYER OUTPUT---\n",
                                               width=self.width - self.button_width / 4,
                                               height=self.height / 2,
                                               font_name="Kenney Blocks",
                                               text_color=arcade.color.WHITE)
        player_console_bordered = arcade.gui.UIBorder(child=player_console,
                                                      border_width=12,
                                                      border_color=arcade.color.WHITE)
        back_from_player = arcade.gui.UIFlatButton(text="Back",
                                                   width=self.button_width,
                                                   height=self.button_height)

        ip_input = arcade.gui.UIInputText(text=Config.GetLastIp(),
                                          font_name="Kenney Blocks",
                                          width=self.button_width * 2,
                                          height=self.button_height / 2,
                                          text_color=arcade.color.WHITE)
        ip_input_bordered = arcade.gui.UIBorder(child=ip_input,
                                                border_width=12,
                                                border_color=arcade.color.WHITE)
        port_input = arcade.gui.UIInputText(text=Config.GetLastPort(),
                                            font_name="Kenney Blocks",
                                            width=self.button_width,
                                            height=self.button_height / 2,
                                            text_color=arcade.color.WHITE)
        port_input_bordered = arcade.gui.UIBorder(child=port_input,
                                                  border_width=12,
                                                  border_color=arcade.color.WHITE)
        connect_to_host_button = arcade.gui.UIFlatButton(text="Connect",
                                                         width=self.button_width,
                                                         height=self.button_height)
        #   CLICKS
        back_from_player.on_click = self.on_back_from_player_button_click
        connect_to_host_button.on_click = self.on_connect_to_host_button_click

        self.menu = {
            'main_menu': {
                'play_button': play_button,
                'exit': exit_button
            },
            'play': {
                'host_button': host_button,
                'connect_button': connect_button,
                'back_button': back_to_menu_button
            },
            'host': {
                'host_console': host_console_bordered,
                'back_button': back_from_host,
                'host_player_console': host_player_console_bordered
            },
            'player': {
                'ip_input': ip_input_bordered,
                'port_input': port_input_bordered,
                'back_button': back_from_player,
                'connect': connect_to_host_button,
                'player_console': player_console_bordered
            }
        }

    def setup_manager(self):
        for menu in self.menu:
            self.uimanager[menu] = arcade.gui.UIManager()
            self.uimanager[menu].enable()
            y_position = (self.button_height / 2 + self.button_height / 8) * (len(self.menu[menu]) - 1)
            if menu != 'host' and menu != 'player':
                for objects in self.menu[menu]:
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="center_x",
                            anchor_y="center_y",
                            align_y=y_position,
                            child=self.menu[menu][objects],
                        )
                    )
                    y_position -= self.button_height + self.button_height / 8
            else:
                if menu == 'host':
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8,
                            align_y=self.button_height / 8,
                            child=self.menu[menu]['back_button'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8,
                            child=self.menu[menu]['host_console'],
                        )
                    ),
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="right",
                            anchor_y="top",
                            align_x=-self.button_height / 8,
                            child=self.menu[menu]['host_player_console'],
                        )
                    )
                else:
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['ip_input'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 4 + self.menu[menu]['ip_input'].width,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['port_input'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="right",
                            anchor_y="bottom",
                            align_x=-self.button_height / 8,
                            align_y=self.button_height / 8,
                            child=self.menu[menu]['connect'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_y=-self.menu[menu]['ip_input'].height - self.button_height / 4,
                            align_x=self.button_height / 8,
                            child=self.menu[menu]['player_console']
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8,
                            align_y=self.button_height / 8,
                            child=self.menu[menu]['back_button'],
                        )
                    )


# Calling MainGame class
def Main():
    Height = 700
    Width = 900
    Title = "Menu"

    MainGame(Width, Height, Title)
    arcade.run()


Main()
