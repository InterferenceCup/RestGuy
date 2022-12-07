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
        super().__init__(fullscreen=True)
        '''width=screen_width,
                         height=screen_height,
                         title=title'''

        # Changing background color of screen
        arcade.set_background_color(arcade.color.BLACK)

        self.screen_width = screen_width
        self.screen_height = screen_height

        # Creating a UI MANAGER to handle the UI
        self.hand_menu = [
            'host',
            'player',
            'log_in',
            'information',
            'change_name',
            'change_password',
            'delete_account',
            'leaders_board',
            'see_all_rating',
            'add/delete/change'
        ]
        self.uimanager = {}
        self.menu = {}
        self.now_menu = 'main_menu'
        self.log_in_console_text = "Hello!"
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

    def on_log_in_button_click(self, event):
        self.now_menu = 'log_in'
        self.set_manager()

    def on_account_button_click(self, event):
        self.now_menu = 'account'
        self.set_manager()

    def on_acc_settings_button_click(self, event):
        self.now_menu = 'information'
        self.set_manager()

    def on_change_name_button_click(self, event):
        self.now_menu = 'change_name'
        self.set_manager()

    def on_change_password_button_click(self, event):
        self.now_menu = 'change_password'
        self.set_manager()

    def on_delete_account_button_click(self, event):
        self.now_menu = 'delete_account'
        self.set_manager()

    def on_maps_button_click(self, event):
        self.now_menu = 'see_all_rating'
        self.set_manager()

    def on_add_delete_change_button_click(self, event):
        self.now_menu = 'add/delete/change'
        self.set_manager()

    def on_leaders_board_button_click(self, event):
        self.now_menu = 'leaders_board'
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
        #   OBJECTS
        play_button = arcade.gui.UIFlatButton(text="Play",
                                              width=self.button_width,
                                              height=self.button_height, )
        exit_button = arcade.gui.UIFlatButton(text="Exit",
                                              width=self.button_width,
                                              height=self.button_height)
        account_button = arcade.gui.UIFlatButton(text="Account",
                                                 width=self.button_width,
                                                 height=self.button_height)
        leaders_button = arcade.gui.UIFlatButton(text="Leaders board",
                                                 width=self.button_width,
                                                 height=self.button_height)
        #   CLICKS
        play_button.on_click = self.on_play_button_click
        exit_button.on_click = self.on_exit_button_click
        account_button.on_click = self.on_account_button_click
        leaders_button.on_click = self.on_leaders_board_button_click

        # ACCOUNT BOARD
        #   OBJECTS
        log_in_button = arcade.gui.UIFlatButton(text="Log In / Register",
                                                width=self.button_width,
                                                height=self.button_height)
        acc_settings_button = arcade.gui.UIFlatButton(text="Account settings",
                                                      width=self.button_width,
                                                      height=self.button_height)
        maps = arcade.gui.UIFlatButton(text="Maps rating",
                                       width=self.button_width,
                                       height=self.button_height)
        # CLICKS
        log_in_button.on_click = self.on_log_in_button_click
        acc_settings_button.on_click = self.on_acc_settings_button_click
        maps.on_click = self.on_maps_button_click

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

        # LOG IN MENU
        #   OBJECTS
        log_in_console = arcade.gui.UITextArea(text=self.log_in_console_text,
                                               width=self.width - self.button_height / 8 * 2 - 12 * 2,
                                               height=self.height / 2,
                                               font_name="Kenney Blocks",
                                               text_color=arcade.color.WHITE)
        username_text = arcade.gui.UITextArea(text="USERNAME",
                                              width=self.button_width * 2,
                                              height=self.button_height,
                                              font_name="Kenney Blocks",
                                              text_color=arcade.color.WHITE)
        password_text = arcade.gui.UITextArea(text="PASSWORD",
                                              width=self.button_width,
                                              height=self.button_height,
                                              font_name="Kenney Blocks",
                                              text_color=arcade.color.WHITE)
        log_in_console_bordered = arcade.gui.UIBorder(child=log_in_console,
                                                      border_width=12,
                                                      border_color=arcade.color.WHITE)
        back_from_log_in = arcade.gui.UIFlatButton(text="Back",
                                                   width=self.button_width,
                                                   height=self.button_height)
        username = arcade.gui.UIInputText(text='Config.GetLastIp()',
                                          font_name="Kenney Blocks",
                                          width=self.button_width * 2,
                                          height=self.button_height / 2,
                                          text_color=arcade.color.WHITE)
        username_bordered = arcade.gui.UIBorder(child=ip_input,
                                                border_width=12,
                                                border_color=arcade.color.WHITE)
        password = arcade.gui.UIInputText(text='Config.GetLastPort()',
                                          font_name="Kenney Blocks",
                                          width=self.button_width * 2,
                                          height=self.button_height / 2,
                                          text_color=arcade.color.WHITE)
        password_bordered = arcade.gui.UIBorder(child=port_input,
                                                border_width=12,
                                                border_color=arcade.color.WHITE)
        try_to_log_in = arcade.gui.UIFlatButton(text="Log In",
                                                width=self.button_width,
                                                height=self.button_height)
        register_button = arcade.gui.UIFlatButton(text="Register",
                                                  width=self.button_width,
                                                  height=self.button_height)
        #   CLICKS
        back_from_log_in.on_click = self.on_account_button_click

        # ACCOUNT SETTINGS
        #   OBJECTS
        confirm_button = arcade.gui.UIFlatButton(text="Confirm",
                                                 width=self.button_width,
                                                 height=self.button_height)
        information_button = arcade.gui.UIFlatButton(text="Information",
                                                     width=self.button_width,
                                                     height=self.button_height)
        information_console = arcade.gui.UIBorder(child=arcade.gui.UITextArea(text="Hello, I'm information",
                                                                              width=self.width - self.button_height / 8 * 2 - 12 * 2,
                                                                              height=self.height / 2,
                                                                              font_name="Kenney Blocks",
                                                                              text_color=arcade.color.WHITE),
                                                  border_width=12,
                                                  border_color=arcade.color.WHITE)
        old_password_text = arcade.gui.UITextArea(text="Current password",
                                                  width=self.button_width * 2,
                                                  height=self.button_height / 2,
                                                  font_name="Kenney Blocks",
                                                  text_color=arcade.color.WHITE)
        new_password_text = arcade.gui.UITextArea(text="New password",
                                                  width=self.button_width * 2,
                                                  height=self.button_height / 2,
                                                  font_name="Kenney Blocks",
                                                  text_color=arcade.color.WHITE)
        old_password_input = arcade.gui.UIBorder(child=arcade.gui.UIInputText(text='Config.GetLastPort()',
                                                                              font_name="Kenney Blocks",
                                                                              width=self.button_width * 2,
                                                                              height=self.button_height / 2,
                                                                              text_color=arcade.color.WHITE),
                                                 border_width=12,
                                                 border_color=arcade.color.WHITE)
        new_password_input = arcade.gui.UIBorder(child=arcade.gui.UIInputText(text='Config.GetLastPort()',
                                                                              font_name="Kenney Blocks",
                                                                              width=self.button_width * 2,
                                                                              height=self.button_height / 2,
                                                                              text_color=arcade.color.WHITE),
                                                 border_width=12,
                                                 border_color=arcade.color.WHITE)
        change_name_button = arcade.gui.UIFlatButton(text="Change Username",
                                                     width=self.button_width,
                                                     height=self.button_height)
        change_password_button = arcade.gui.UIFlatButton(text="Change Password",
                                                         width=self.button_width,
                                                         height=self.button_height)
        delete_acc_button = arcade.gui.UIFlatButton(text="Delete account",
                                                    width=self.button_width,
                                                    height=self.button_height)
        # CLIKS
        information_button.on_click = self.on_acc_settings_button_click
        change_name_button.on_click = self.on_change_name_button_click
        change_password_button.on_click = self.on_change_password_button_click
        delete_acc_button.on_click = self.on_delete_account_button_click

        # LEADERS BOARD
        leaders_board = arcade.gui.UIBorder(child=arcade.gui.UITextArea(text="---LEADERS BOARD---",
                                                                        width=self.width - self.button_height / 8 * 2 - 12 * 2,
                                                                        height=self.height - self.button_height / 8 * 3 - 12 * 2 - self.button_height,
                                                                        font_name="Kenney Blocks",
                                                                        text_color=arcade.color.WHITE),
                                            border_width=12,
                                            border_color=arcade.color.WHITE)

        # MAPS
        # OBJECTS
        see_all_rating = arcade.gui.UIFlatButton(text="See all rating",
                                                 width=self.button_width,
                                                 height=self.button_height)
        add_delete_change_map_rating = arcade.gui.UIFlatButton(text="Add/Delete/Change your rating",
                                                               width=self.button_width,
                                                               height=self.button_height)
        confirm_rating = arcade.gui.UIFlatButton(text="Confirm",
                                                 width=self.button_width,
                                                 height=self.button_height)
        delete_rating = arcade.gui.UIFlatButton(text="Delete",
                                                width=self.button_width,
                                                height=self.button_height)
        rating_information = arcade.gui.UIBorder(child=arcade.gui.UITextArea(text="Hello, I'm information",
                                                                             width=self.width - self.button_height / 8 * 2 - 12 * 2,
                                                                             height=self.height / 2,
                                                                             font_name="Kenney Blocks",
                                                                             text_color=arcade.color.WHITE),
                                                 border_width=12,
                                                 border_color=arcade.color.WHITE)
        map_name_text = arcade.gui.UITextArea(text="Map name",
                                              width=self.button_width * 2,
                                              height=self.button_height / 2,
                                              font_name="Kenney Blocks",
                                              text_color=arcade.color.WHITE)
        map_name_input = arcade.gui.UIBorder(child=arcade.gui.UIInputText(text="Enter map name",
                                                                          font_name="Kenney Blocks",
                                                                          width=self.button_width * 2,
                                                                          height=self.button_height / 2,
                                                                          text_color=arcade.color.WHITE),
                                             border_width=12,
                                             border_color=arcade.color.WHITE)
        rating_text = arcade.gui.UITextArea(text="Rating",
                                            width=self.button_width * 2,
                                            height=self.button_height / 2,
                                            font_name="Kenney Blocks",
                                            text_color=arcade.color.WHITE)
        rating_one = arcade.gui.UIFlatButton(text="1",
                                             width=self.button_height / 2 + 12 * 2,
                                             height=self.button_height / 2 + 12 * 2)
        rating_two = arcade.gui.UIFlatButton(text="2",
                                             width=self.button_height / 2 + 12 * 2,
                                             height=self.button_height / 2 + 12 * 2)
        rating_three = arcade.gui.UIFlatButton(text="3",
                                               width=self.button_height / 2 + 12 * 2,
                                               height=self.button_height / 2 + 12 * 2)
        rating_fourth = arcade.gui.UIFlatButton(text="4",
                                                width=self.button_height / 2 + 12 * 2,
                                                height=self.button_height / 2 + 12 * 2)
        rating_five = arcade.gui.UIFlatButton(text="5",
                                              width=self.button_height / 2 + 12 * 2,
                                              height=self.button_height / 2 + 12 * 2)
        # CLICKS
        see_all_rating.on_click = self.on_maps_button_click
        add_delete_change_map_rating.on_click = self.on_add_delete_change_button_click

        self.menu = {
            'main_menu': {
                'account': account_button,
                'play_button': play_button,
                'leaders': leaders_button,
                'exit': exit_button
            },
            'account': {
                'log_in': log_in_button,
                'settings': acc_settings_button,
                'maps': maps,
                'back': back_to_menu_button
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
            },
            'log_in': {
                'username': username_bordered,
                'password': password_bordered,
                'back_button': back_from_log_in,
                'log_in': try_to_log_in,
                'log_console': log_in_console_bordered,
                'username_text': username_text,
                'password_text': password_text,
                'register': register_button
            },
            'information': {
                'back': back_from_log_in,
                'information_button': information_button,
                'change_name': change_name_button,
                'information': information_console,
                'change_password': change_password_button,
                'delete_account': delete_acc_button
            },
            'change_name': {
                'back': back_from_log_in,
                'information_button': information_button,
                'change_name': change_name_button,
                'change_password': change_password_button,
                'delete_account': delete_acc_button,
                'information': information_console,
                'username_text': username_text,
                'username': username_bordered,
                'confirm': confirm_button
            },
            'change_password': {
                'back': back_from_log_in,
                'information_button': information_button,
                'change_name': change_name_button,
                'change_password': change_password_button,
                'delete_account': delete_acc_button,
                'information': information_console,
                'old_password_text': old_password_text,
                'new_password_text': new_password_text,
                'old_password_input': old_password_input,
                'new_password_input': new_password_input,
                'confirm': confirm_button
            },
            'delete_account': {
                'back': back_from_log_in,
                'information_button': information_button,
                'change_name': change_name_button,
                'information': information_console,
                'change_password': change_password_button,
                'delete_account': delete_acc_button,
                'confirm': confirm_button
            },
            'leaders_board': {
                'back': back_to_menu_button,
                'leaders_board': leaders_board
            },
            'see_all_rating': {
                'back': back_from_log_in,
                'see_all_rating': see_all_rating,
                'add/delete/change': add_delete_change_map_rating,
                'information': rating_information
            },
            'add/delete/change': {
                'back': back_from_log_in,
                'see_all_rating': see_all_rating,
                'add/delete/change': add_delete_change_map_rating,
                'information': rating_information,
                'map_name_text': map_name_text,
                'rating_text': rating_text,
                'map_name_input': map_name_input,
                'one': rating_one,
                'two': rating_two,
                'three': rating_three,
                'fourth': rating_fourth,
                'five': rating_five,
                'confirm': confirm_rating,
                'delete': delete_rating
            }
        }

    def setup_manager(self):
        for menu in self.menu:
            self.uimanager[menu] = arcade.gui.UIManager()
            self.uimanager[menu].enable()
            y_position = (self.button_height / 2 + self.button_height / 8) * (len(self.menu[menu]) - 1)
            if menu not in self.hand_menu:
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
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['host_console'],
                        )
                    ),
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="right",
                            anchor_y="top",
                            align_x=-self.button_height / 8,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['host_player_console'],
                        )
                    )
                elif menu == 'player':
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
                elif menu == 'log_in':
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 + 12,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['username_text'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8,
                            align_y=-self.button_height / 8 * 2 - self.button_height / 2,
                            child=self.menu[menu]['username'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 * 2 + self.menu[menu]['username_text'].width + 12 * 3,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['password_text'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 * 2 + self.menu[menu]['username'].width,
                            align_y=-self.button_height / 8 * 2 - self.button_height / 2,
                            child=self.menu[menu]['password'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="right",
                            anchor_y="bottom",
                            align_x=-self.button_height / 8,
                            align_y=self.button_height / 8,
                            child=self.menu[menu]['log_in'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="right",
                            anchor_y="bottom",
                            align_x=-self.button_height / 8 * 2 - self.button_width,
                            align_y=self.button_height / 8,
                            child=self.menu[menu]['register'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_y=-self.button_height - self.button_height / 2 - 12 * 2,
                            align_x=self.button_height / 8,
                            child=self.menu[menu]['log_console']
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
                elif menu == 'change_name':
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8,
                            align_y=self.button_height / 8,
                            child=self.menu[menu]['back'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="right",
                            anchor_y="bottom",
                            align_x=-self.button_height / 8,
                            align_y=self.button_height / 8,
                            child=self.menu[menu]['confirm'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['information_button'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 * 2 + self.button_width,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['change_name'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 * 3 + self.button_width * 2,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['change_password'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 * 4 + self.button_width * 3,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['delete_account'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 + 12,
                            align_y=-self.button_height / 8 * 4 - self.button_height - self.height / 2 - 12 * 2,
                            child=self.menu[menu]['username_text'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8,
                            align_y=-self.button_height / 8 * 4 - self.button_height * 2 - self.height / 2,
                            child=self.menu[menu]['username'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8,
                            align_y=-self.button_height / 8 * 2 - self.button_height,
                            child=self.menu[menu]['information'],
                        )
                    )
                elif menu == 'information':
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8,
                            align_y=self.button_height / 8,
                            child=self.menu[menu]['back'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['information_button'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 * 2 + self.button_width,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['change_name'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 * 3 + self.button_width * 2,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['change_password'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 * 4 + self.button_width * 3,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['delete_account'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8,
                            align_y=-self.button_height / 8 * 2 - self.button_height,
                            child=self.menu[menu]['information'],
                        )
                    )
                elif menu == 'change_password':
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8,
                            align_y=self.button_height / 8,
                            child=self.menu[menu]['back'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['information_button'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 * 2 + self.button_width,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['change_name'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 * 3 + self.button_width * 2,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['change_password'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 * 4 + self.button_width * 3,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['delete_account'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8,
                            align_y=-self.button_height / 8 * 2 - self.button_height,
                            child=self.menu[menu]['information'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 + 12,
                            align_y=-self.button_height / 8 * 4 - self.button_height - self.height / 2 - 12 * 2,
                            child=self.menu[menu]['old_password_text'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8,
                            align_y=-self.button_height / 8 * 4 - self.button_height * 2 - self.height / 2,
                            child=self.menu[menu]['old_password_input'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 * 2 + 12 * 3 + self.button_width * 2,
                            align_y=-self.button_height / 8 * 4 - self.button_height - self.height / 2 - 12 * 2,
                            child=self.menu[menu]['new_password_text'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 * 2 + 12 * 2 + self.button_width * 2,
                            align_y=-self.button_height / 8 * 4 - self.button_height * 2 - self.height / 2,
                            child=self.menu[menu]['new_password_input'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="right",
                            anchor_y="bottom",
                            align_x=-self.button_height / 8,
                            align_y=self.button_height / 8,
                            child=self.menu[menu]['confirm'],
                        )
                    )
                elif menu == 'delete_account':
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8,
                            align_y=self.button_height / 8,
                            child=self.menu[menu]['back'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['information_button'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 * 2 + self.button_width,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['change_name'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 * 3 + self.button_width * 2,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['change_password'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 * 4 + self.button_width * 3,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['delete_account'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8,
                            align_y=-self.button_height / 8 * 2 - self.button_height,
                            child=self.menu[menu]['information'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="right",
                            anchor_y="bottom",
                            align_x=-self.button_height / 8,
                            align_y=self.button_height / 8,
                            child=self.menu[menu]['confirm'],
                        )
                    )
                elif menu == 'leaders_board':
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8,
                            align_y=self.button_height / 8,
                            child=self.menu[menu]['back'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['leaders_board'],
                        )
                    )
                elif menu == 'see_all_rating':
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8,
                            align_y=self.button_height / 8,
                            child=self.menu[menu]['back'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8,
                            align_y=-self.button_height / 8 * 2 - self.button_height,
                            child=self.menu[menu]['information'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['see_all_rating'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 * 2 + self.button_width,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['add/delete/change'],
                        )
                    )
                elif menu == 'add/delete/change':
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8,
                            align_y=self.button_height / 8,
                            child=self.menu[menu]['back'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8,
                            align_y=-self.button_height / 8 * 2 - self.button_height,
                            child=self.menu[menu]['information'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['see_all_rating'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 * 2 + self.button_width,
                            align_y=-self.button_height / 8,
                            child=self.menu[menu]['add/delete/change'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="right",
                            anchor_y="bottom",
                            align_x=-self.button_height / 8 * 2 - self.button_width,
                            align_y=self.button_height / 8,
                            child=self.menu[menu]['delete'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="right",
                            anchor_y="bottom",
                            align_x=-self.button_height / 8,
                            align_y=self.button_height / 8,
                            child=self.menu[menu]['confirm'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 + 12,
                            align_y=-self.button_height / 8 * 4 - self.button_height - self.height / 2 - 12 * 2,
                            child=self.menu[menu]['map_name_text'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8,
                            align_y=-self.button_height / 8 * 4 - self.button_height * 2 - self.height / 2,
                            child=self.menu[menu]['map_name_input'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 * 2 + 12 * 3 + self.button_width * 2,
                            align_y=-self.button_height / 8 * 4 - self.button_height - self.height / 2 - 12 * 2,
                            child=self.menu[menu]['rating_text'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 * 2 + 12 * 2 + self.button_width * 2,
                            align_y=-self.button_height / 8 * 4 - self.button_height * 2 - self.height / 2,
                            child=self.menu[menu]['one'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 * 3 + 12 * 2 + self.button_width * 2 + self.menu[menu][
                                'one'].width,
                            align_y=-self.button_height / 8 * 4 - self.button_height * 2 - self.height / 2,
                            child=self.menu[menu]['two'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 * 4 + 12 * 2 + self.button_width * 2 + self.menu[menu][
                                'one'].width * 2,
                            align_y=-self.button_height / 8 * 4 - self.button_height * 2 - self.height / 2,
                            child=self.menu[menu]['three'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 * 5 + 12 * 2 + self.button_width * 2 + self.menu[menu][
                                'one'].width * 3,
                            align_y=-self.button_height / 8 * 4 - self.button_height * 2 - self.height / 2,
                            child=self.menu[menu]['fourth'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 * 6 + 12 * 2 + self.button_width * 2 + self.menu[menu][
                                'one'].width * 4,
                            align_y=-self.button_height / 8 * 4 - self.button_height * 2 - self.height / 2,
                            child=self.menu[menu]['five'],
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
