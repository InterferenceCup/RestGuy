import subprocess
from os import listdir

import requests

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
        '''width=screen_width,
                         height=screen_height,
                         title=title'''

        # Changing background color of screen
        arcade.set_background_color(arcade.color.BLACK)

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.background = arcade.load_texture("MenuTextures/fon.png")
        self.borders = int(self.width * 0.03)

        self.sp = arcade.load_texture("MenuTextures/star_pressed.png")
        self.snp = arcade.load_texture("MenuTextures/star_not_pressed.png")

        self.button_style = {
            'bg_color': arcade.color_from_hex_string("d1b591"),
            'bg_color_pressed': arcade.color_from_hex_string("2e2117"),
            'font_name': "Kenney Mini Square",
            'font_color': arcade.color_from_hex_string("2e2117"),
            'font_color_pressed': arcade.color_from_hex_string("d1b591"),
            'font_size': 12,
            'border_color': arcade.color_from_hex_string("d1b591"),
            'border_color_pressed': arcade.color_from_hex_string("2e2117"),
            'border_width': 5
        }

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
        self.helper = {}
        self.name = 'Unknown'
        self.set_helper()
        self.uimanager = {}
        self.menu = {}
        self.now_menu = 'main_menu'
        self.log_in_console_text = "Hello!"
        self.button_width = int(self.width * 0.16)
        self.button_height = int(self.button_width * 0.4)
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

        self.maps = None
        self.feedbacks = None
        self.rating = 1

    def on_play_button_click(self, event):
        self.now_menu = 'play'
        self.set_manager()

    def on_back_to_menu_button_click(self, event):
        self.now_menu = 'main_menu'
        self.set_manager()

    def on_log_in_button_click(self, event):
        self.now_menu = 'log_in'
        self.menu[self.now_menu]['log_console'].child.text = self.helper[self.now_menu]['hello']
        self.menu[self.now_menu]['username'].child.text = Config.GetLastUsername()
        self.menu[self.now_menu]['password'].child.text = Config.GetLastPassword()
        self.set_manager()

    def on_account_button_click(self, event):
        self.now_menu = 'account'
        self.set_manager()

    def on_acc_settings_button_click(self, event):
        if self.name != "Unknown":
            self.now_menu = 'information'
            payload = {
                'username': self.name
            }
            try:
                with requests.Session() as s:
                    result = str(s.post('http://localhost:8080/find/account', data=payload).content.decode()).split(
                        sep='|')
                    print(result)
                self.menu[self.now_menu]['information'].child.text = (
                        self.helper[self.now_menu]['information'] +
                        self.helper[self.now_menu]['name'] + result[0] +
                        self.helper[self.now_menu]['password'] + result[1] +
                        self.helper[self.now_menu]['score'] + result[2] +
                        self.helper[self.now_menu]['steps'] + result[3] +
                        self.helper[self.now_menu]['final']
                )
            except:
                self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu]['connection_error']

            self.set_manager()

    def on_confirm_click(self, event):
        if self.now_menu == 'change_name':
            self.try_to_change_name()
        elif self.now_menu == 'change_password':
            self.try_to_change_password()
        elif self.now_menu == 'delete_account':
            self.try_to_delete()

    def try_to_change_name(self):
        payload = {
            'username': self.menu[self.now_menu]['username'].child.text.lower()
        }
        try:
            with requests.Session() as s:
                result = str(s.post('http://localhost:8080/find/account', data=payload).content.decode()).split(sep='|')
            if len(result) != 1:
                self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu]['no']
            else:
                payload = {
                    'username': self.name,
                    'newusername': self.menu[self.now_menu]['username'].child.text.lower()
                }
                with requests.Session() as s:
                    result = str(s.post('http://localhost:8080/name', data=payload).content.decode())
                if result == "Successful update.":
                    self.name = payload['newusername']
                    Config.SetLastUsername(self.name)
                    self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu][
                                                                             'successful'] + self.name
                else:
                    self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu]['connection_error']
        except:
            self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu]['connection_error']

    def try_to_change_password(self):
        try:
            payload = {
                'username': self.name,
                'password': Config.GetLastPassword().lower(),
                'newpassword': self.menu[self.now_menu]['new_password'].child.text.lower()
            }
            with requests.Session() as s:
                result = str(s.post('http://localhost:8080/password', data=payload).content.decode())
            print(result)
            if result == "Successful changes.":
                Config.SetLastPassword(self.menu[self.now_menu]['new_password'].child.text)
                self.menu[self.now_menu]['information'].child.text = (self.helper[self.now_menu]['successful'] +
                                                                      self.menu[self.now_menu][
                                                                          'new_password'].child.text
                                                                      )
            else:
                self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu]['connection_error']
        except:
            self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu]['connection_error']

    def try_to_delete(self):
        payload = {
            'username': self.name
        }
        try:
            with requests.Session() as s:
                result = str(s.post('http://localhost:8080/delete', data=payload).content.decode())
            if result == "Successful delete.":
                self.now_menu = 'main_menu'
                self.set_manager()
            else:
                self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu]['error']
        except:
            self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu]['connection_error']

    def on_change_name_button_click(self, event):
        self.now_menu = 'change_name'
        self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu]['hello']
        self.menu[self.now_menu]['username'].child.text = self.name
        self.set_manager()

    def on_change_password_button_click(self, event):
        self.now_menu = 'change_password'
        self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu]['hello']
        self.set_manager()

    def on_delete_account_button_click(self, event):
        self.now_menu = 'delete_account'
        self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu]['hello']
        self.set_manager()

    def on_maps_button_click(self, event):
        if self.name != 'Unknown':
            self.now_menu = 'see_all_rating'
            try:
                with requests.Session() as s:
                    result = s.get('http://localhost:8080/ratings').text
                result = result.split(sep='|')
                text = '------LEADERS BOARD------\n'
                for i in range(len(result) - 1):
                    result[i] = result[i].split(sep='-')
                result = self.sorting(result, 1)
                for i in range(len(result) - 1):
                    text = text + str(i + 1) + ')        ' + result[i][0].strip() + '        with rating        ' + str(
                        result[i][1].strip()) + '        and number of feedbacks        ' + str(
                        result[i][2].strip()) + '\n'
                self.menu[self.now_menu]['information'].child.text = text
            except:
                self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu]['connection_error']
            self.set_manager()

    def on_add_delete_change_button_click(self, event):
        self.now_menu = 'add/delete/change'
        self.update_maps()
        self.set_manager()

    def update_maps(self):
        files = [f for f in listdir("Maps/")]
        payload = {
            'username': self.name
        }
        try:
            with requests.Session() as s:
                result = str(s.post('http://localhost:8080/ratings/find/user', data=payload).content.decode())
            if len(result) != 0:
                result = result.split(sep="|")
                result.remove(result[-1])
                for i in range(len(result)):
                    result[i] = result[i].lower()
                self.feedbacks = result
                for i in range(len(result)):
                    if result[i] not in files:
                        files.append(result[i])
            else:
                self.feedbacks = None
            for i in range(len(files)):
                files[i] = files[i].lower()
            text = self.helper[self.now_menu]['hello'] + "\n"
            for i in range(len(files)):
                text = text + str(i + 1) + ") " + files[i] + "\n"
            self.menu[self.now_menu]['information'].child.text = text
            self.maps = files
        except:
            self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu]['connection_error']

    def on_delete_map_click(self, event):
        map_name = self.menu[self.now_menu]['map_name_input'].child.text.lower()
        if map_name in self.maps:
            if self.feedbacks and map_name in self.feedbacks:
                payload = {
                    'username': self.name
                }
                try:
                    with requests.Session() as s:
                        result = str(s.post('http://localhost:8080/ratings/delete/user', data=payload).content.decode())
                    if result == "Successful delete.":
                        self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu][
                            'successful_delete']
                    else:
                        self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu][
                            'connection_error']
                except:
                    self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu]['connection_error']
                self.update_maps()
            else:
                self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu]['no_in_feedback']
        else:
            self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu]['no_in_maps']

    def on_confirm_rating_click(self, event):
        map_name = self.menu[self.now_menu]['map_name_input'].child.text.lower()
        if map_name in self.maps:
            if self.feedbacks and map_name in self.feedbacks:
                payload = {
                    'map': map_name,
                    'rating': self.rating,
                    'username': self.name
                }
                try:
                    with requests.Session() as s:
                        result = str(s.post('http://localhost:8080/ratings/change', data=payload).content.decode())
                    if result == "Successful added":
                        self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu][
                            'successful_add']
                    else:
                        self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu][
                            'connection_error']
                except:
                    self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu]['connection_error']
                self.update_maps()
            else:
                payload = {
                    'map': map_name,
                    'rating': self.rating,
                    'username': self.name
                }
                try:
                    with requests.Session() as s:
                        result = str(s.post('http://localhost:8080/ratings/add', data=payload).content.decode())
                    if result == "Successful added":
                        self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu][
                            'successful_add']
                    else:
                        self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu][
                            'connection_error']
                except:
                    self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu]['connection_error']
                self.update_maps()
        else:
            self.menu[self.now_menu]['information'].child.text = self.helper[self.now_menu]['no_in_maps']

    def on_one_tap(self, event):
        self.rating = 1
        self.menu[self.now_menu]["one"].texture = self.sp
        self.menu[self.now_menu]["two"].texture = self.snp
        self.menu[self.now_menu]["three"].texture = self.snp
        self.menu[self.now_menu]["fourth"].texture = self.snp
        self.menu[self.now_menu]["five"].texture = self.snp

    def on_two_tap(self, event):
        self.rating = 2
        self.menu[self.now_menu]["one"].texture = self.sp
        self.menu[self.now_menu]["two"].texture = self.sp
        self.menu[self.now_menu]["three"].texture = self.snp
        self.menu[self.now_menu]["fourth"].texture = self.snp
        self.menu[self.now_menu]["five"].texture = self.snp

    def on_three_tap(self, event):
        self.rating = 3

        self.menu[self.now_menu]["one"].texture = self.sp
        self.menu[self.now_menu]["two"].texture = self.sp
        self.menu[self.now_menu]["three"].texture = self.sp
        self.menu[self.now_menu]["fourth"].texture = self.snp
        self.menu[self.now_menu]["five"].texture = self.snp

    def on_fourth_tap(self, event):
        self.rating = 4
        self.menu[self.now_menu]["one"].texture = self.sp
        self.menu[self.now_menu]["two"].texture = self.sp
        self.menu[self.now_menu]["three"].texture = self.sp
        self.menu[self.now_menu]["fourth"].texture = self.sp
        self.menu[self.now_menu]["five"].texture = self.snp

    def on_five_tap(self, event):
        self.rating = 5
        self.menu[self.now_menu]["one"].texture = self.sp
        self.menu[self.now_menu]["two"].texture = self.sp
        self.menu[self.now_menu]["three"].texture = self.sp
        self.menu[self.now_menu]["fourth"].texture = self.sp
        self.menu[self.now_menu]["five"].texture = self.sp

    def on_leaders_board_button_click(self, event):
        self.now_menu = 'leaders_board'
        try:
            with requests.Session() as s:
                result = s.get('http://localhost:8080/users').text
            result = result.split(sep='|')
            text = '------LEADERS BOARD------\n'
            for i in range(len(result) - 1):
                result[i] = result[i].split(sep='-')
            result = self.sorting(result, 2)
            for i in range(len(result) - 1):
                text = text + str(i + 1) + ')        ' + result[i][0].strip() + '        with score        ' + str(
                    result[i][2].strip()) + '\n'
            self.menu[self.now_menu]['leaders_board'].child.text = text
        except:
            self.menu[self.now_menu]['leaders_board'].child.text = self.helper[self.now_menu]['connection_error']
        self.set_manager()

    def on_connect_button_click(self, event):
        if self.player != None:
            self.player.kill()
            self.player = None
        self.now_menu = 'player'
        self.set_manager()

    def on_exit_button_click(self, event):
        self.close()

    def on_try_to_log_in_button_click(self, event):
        Config.SetLastUsername(self.menu[self.now_menu]['username'].child.text.lower())
        Config.SetLastPassword(self.menu[self.now_menu]['password'].child.text.lower())
        payload = {
            'username': self.menu[self.now_menu]['username'].child.text.lower(),
            'password': self.menu[self.now_menu]['password'].child.text.lower()
        }
        try:
            with requests.Session() as s:
                result = str(s.post('http://localhost:8080/login', data=payload).content.decode())
        except:
            result = "Connection Error"
        if result == 'Incorrect password':
            self.menu[self.now_menu]['log_console'].child.text = self.helper[self.now_menu]['incorrect_password']
        elif result == 'Login failed':
            self.menu[self.now_menu]['log_console'].child.text = self.helper[self.now_menu]['error_with_log_in']
        elif result == "Connection Error":
            self.menu[self.now_menu]['log_console'].child.text = self.helper[self.now_menu]['connection_error']
        else:
            self.name = result
            self.menu[self.now_menu]['log_console'].child.text = self.helper[self.now_menu]['successful'] + self.name

    def on_register_button_click(self, event):
        Config.SetLastUsername(self.menu[self.now_menu]['username'].child.text.lower())
        Config.SetLastPassword(self.menu[self.now_menu]['password'].child.text.lower())
        payload = {
            'username': self.menu[self.now_menu]['username'].child.text.lower(),
            'password': self.menu[self.now_menu]['password'].child.text.lower()
        }
        try:
            with requests.Session() as s:
                result = str(s.post('http://localhost:8080/register', data=payload).content.decode())
        except:
            result = "Connection Error"
        if result == "Connection Error":
            self.menu[self.now_menu]['log_console'].child.text = self.helper[self.now_menu]['connection_error']
        elif result == "User with that name has already been.":
            self.menu[self.now_menu]['log_console'].child.text = self.helper[self.now_menu]['error_with_register']
        else:
            self.name = Config.GetLastUsername()
            self.menu[self.now_menu]['log_console'].child.text = self.helper[self.now_menu]['successful'] + self.name

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
        Config.WriteName(self.name)
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
            Config.WriteName(self.name)
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

    def sorting(self, massive, num):
        copy = []
        for _ in range(len(massive) - 1):
            for i in range(len(massive) - 2):
                if int(massive[i][num].split(sep='.')[0]) < int(massive[i + 1][num].split(sep='.')[0]):
                    for j in range(len(massive[i])):
                        copy.append(massive[i][j])
                    for j in range(len(massive[i])):
                        massive[i][j] = massive[i+1][j]
                    for j in range(len(massive[i])):
                        massive[i+1][j] = copy[j]
                    copy = []
        return massive

    def host_console(self):
        self.host_text = "---HOST OUTPUT---\n"
        while True and self.host:
            output = self.host.stdout.readline().decode()
            if output != None and self.host_text != None:
                print(output)
                self.host_text = self.host_text + output
        print("Stop reading")

    def host_player_console(self):
        try:
            self.host_player_text = "---HOST PLAYER OUTPUT---\n"
            while True and self.host_player:
                output = self.host_player.stdout.readline().decode()
                if output != None and self.host_player_text != None:
                    print(output)
                    self.host_player_text = self.host_player_text + output
        except:
            print("Stop reading")
        print("Stop reading")

    # Creating on_draw() function to draw on the screen
    def on_draw(self):
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.screen_width, self.screen_height,
                                            self.background)

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
                                              height=self.button_height,
                                              style=self.button_style)
        exit_button = arcade.gui.UIFlatButton(text="Exit",
                                              width=self.button_width,
                                              height=self.button_height,
                                              style=self.button_style)
        account_button = arcade.gui.UIFlatButton(text="Account",
                                                 width=self.button_width,
                                                 height=self.button_height,
                                                 style=self.button_style)
        leaders_button = arcade.gui.UIFlatButton(text="Leaders board",
                                                 width=self.button_width,
                                                 height=self.button_height,
                                                 style=self.button_style)
        #   CLICKS
        play_button.on_click = self.on_play_button_click
        exit_button.on_click = self.on_exit_button_click
        account_button.on_click = self.on_account_button_click
        leaders_button.on_click = self.on_leaders_board_button_click

        # ACCOUNT BOARD
        #   OBJECTS
        log_in_button = arcade.gui.UIFlatButton(text="Log In / Register",
                                                width=self.button_width,
                                                height=self.button_height,
                                                style=self.button_style)
        acc_settings_button = arcade.gui.UIFlatButton(text="Account settings",
                                                      width=self.button_width,
                                                      height=self.button_height,
                                                      style=self.button_style)
        maps = arcade.gui.UIFlatButton(text="Maps rating",
                                       width=self.button_width,
                                       height=self.button_height,
                                       style=self.button_style)
        # CLICKS
        log_in_button.on_click = self.on_log_in_button_click
        acc_settings_button.on_click = self.on_acc_settings_button_click
        maps.on_click = self.on_maps_button_click

        # PLAY
        #   OBJECTS
        back_to_menu_button = arcade.gui.UIFlatButton(text="Back",
                                                      width=self.button_width,
                                                      height=self.button_height,
                                                      style=self.button_style)
        host_button = arcade.gui.UIFlatButton(text="Host",
                                              width=self.button_width,
                                              height=self.button_height,
                                              style=self.button_style)
        connect_button = arcade.gui.UIFlatButton(text="Connect",
                                                 width=self.button_width,
                                                 height=self.button_height,
                                                 style=self.button_style)
        #   CLICKS
        back_to_menu_button.on_click = self.on_back_to_menu_button_click
        host_button.on_click = self.on_host_button_click
        connect_button.on_click = self.on_connect_button_click

        # HOST LOBBY
        #   OBJECTS
        host_console = arcade.gui.UITextArea(text="",
                                             width=((self.width - self.borders * 2 - int(
                                                 self.width * 0.04)) / 2 - self.button_height / 8 * 2 - 12 * 2),
                                             height=(
                                                            self.height - self.borders * 2) / 2 - self.button_height / 8 * 4 - self.button_height - 12 * 2,
                                             font_name="Kenney Mini Square",
                                             text_color=arcade.color_from_hex_string("2e2117"))
        host_console_bordered = arcade.gui.UIBorder(child=host_console,
                                                    border_width=12,
                                                    border_color=arcade.color_from_hex_string("2e2117"))
        host_player_console = arcade.gui.UITextArea(text="",
                                                    width=((self.width - self.borders * 2 - int(
                                                        self.width * 0.04)) / 2 - self.button_height / 8 * 2 - 12 * 2),
                                                    height=(
                                                                   self.height - self.borders * 2) / 2 - self.button_height / 8 * 4 - self.button_height - 12 * 2,
                                                    font_name="Kenney Mini Square",
                                                    text_color=arcade.color_from_hex_string("2e2117"))
        host_player_console_bordered = arcade.gui.UIBorder(child=host_player_console,
                                                           border_width=12,
                                                           border_color=arcade.color_from_hex_string("2e2117"))
        back_from_host = arcade.gui.UIFlatButton(text="Back",
                                                 width=self.button_width,
                                                 height=self.button_height,
                                                 style=self.button_style)
        #   CLICKS
        back_from_host.on_click = self.on_back_from_host_button_click

        # PLAYER MENU
        #   OBJECTS
        player_console = arcade.gui.UITextArea(text="---PLAYER OUTPUT---\n",
                                               width=((self.width - self.borders * 2 - int(
                                                   self.width * 0.04)) / 2 - self.button_height / 8 * 2 - 12 * 2),
                                               height=self.height - self.borders * 2 - self.button_height - self.button_height / 2 * 2 - self.button_height / 8 * 5 - 12 * 6,
                                               font_name="Kenney Mini Square",
                                               text_color=arcade.color_from_hex_string("2e2117"))
        player_console_bordered = arcade.gui.UIBorder(child=player_console,
                                                      border_width=12,
                                                      border_color=arcade.color_from_hex_string("2e2117"))
        back_from_player = arcade.gui.UIFlatButton(text="Back",
                                                   width=self.button_width,
                                                   height=self.button_height,
                                                   style=self.button_style)
        ip_input = arcade.gui.UIInputText(text=Config.GetLastIp(),
                                          font_name="Kenney Mini Square",
                                          width=self.button_width * 2,
                                          height=self.button_height / 2,
                                          text_color=arcade.color_from_hex_string("2e2117"))
        ip_input_bordered = arcade.gui.UIBorder(child=ip_input,
                                                border_width=12,
                                                border_color=arcade.color_from_hex_string("2e2117"))
        port_input = arcade.gui.UIInputText(text=Config.GetLastPort(),
                                            font_name="Kenney Mini Square",
                                            width=self.button_width,
                                            height=self.button_height / 2,
                                            text_color=arcade.color_from_hex_string("2e2117"))
        port_input_bordered = arcade.gui.UIBorder(child=port_input,
                                                  border_width=12,
                                                  border_color=arcade.color_from_hex_string("2e2117"))
        connect_to_host_button = arcade.gui.UIFlatButton(text="Connect",
                                                         width=self.button_width,
                                                         height=self.button_height,
                                                         style=self.button_style)
        #   CLICKS
        back_from_player.on_click = self.on_back_from_player_button_click
        connect_to_host_button.on_click = self.on_connect_to_host_button_click

        # LOG IN MENU
        #   OBJECTS
        log_in_console = arcade.gui.UITextArea(text=self.log_in_console_text,
                                               width=((self.width - self.borders * 2 - int(
                                                   self.width * 0.04)) / 2 - self.button_height / 8 * 3 - 12 * 2),
                                               height=self.height - self.borders * 2 - self.button_height - self.button_height / 2 * 4 - self.button_height / 8 * 6 - 12 * 6,
                                               font_name="Kenney Mini Square",
                                               text_color=arcade.color_from_hex_string("2e2117"))
        username_text = arcade.gui.UITextArea(text="USERNAME",
                                              width=self.button_width * 2,
                                              height=self.button_height,
                                              font_name="Kenney Mini Square",
                                              text_color=arcade.color_from_hex_string("2e2117"))
        password_text = arcade.gui.UITextArea(text="PASSWORD",
                                              width=self.button_width,
                                              height=self.button_height,
                                              font_name="Kenney Mini Square",
                                              text_color=arcade.color_from_hex_string("2e2117"))
        log_in_console_bordered = arcade.gui.UIBorder(child=log_in_console,
                                                      border_width=12,
                                                      border_color=arcade.color_from_hex_string("2e2117"))
        back_from_log_in = arcade.gui.UIFlatButton(text="Back",
                                                   width=self.button_width,
                                                   height=self.button_height,
                                                   style=self.button_style)
        username = arcade.gui.UIInputText(text='Config.GetLastIp()',
                                          font_name="Kenney Mini Square",
                                          width=self.button_width * 2,
                                          height=self.button_height / 2,
                                          text_color=arcade.color_from_hex_string("2e2117"))
        username_bordered = arcade.gui.UIBorder(child=ip_input,
                                                border_width=12,
                                                border_color=arcade.color_from_hex_string("2e2117"))
        password = arcade.gui.UIInputText(text='Config.GetLastPort()',
                                          font_name="Kenney Mini Square",
                                          width=self.button_width * 2,
                                          height=self.button_height / 2,
                                          text_color=arcade.color_from_hex_string("2e2117"))
        password_bordered = arcade.gui.UIBorder(child=port_input,
                                                border_width=12,
                                                border_color=arcade.color_from_hex_string("2e2117"))
        try_to_log_in = arcade.gui.UIFlatButton(text="Log In",
                                                width=self.button_width,
                                                height=self.button_height,
                                                style=self.button_style)
        register_button = arcade.gui.UIFlatButton(text="Register",
                                                  width=self.button_width,
                                                  height=self.button_height,
                                                  style=self.button_style)
        #   CLICKS
        back_from_log_in.on_click = self.on_account_button_click
        try_to_log_in.on_click = self.on_try_to_log_in_button_click
        register_button.on_click = self.on_register_button_click

        # ACCOUNT SETTINGS
        #   OBJECTS
        confirm_button = arcade.gui.UIFlatButton(text="Confirm",
                                                 width=self.button_width,
                                                 height=self.button_height,
                                                 style=self.button_style)
        information_button = arcade.gui.UIFlatButton(text="Information",
                                                     width=self.button_width,
                                                     height=self.button_height,
                                                     style=self.button_style)
        information_console_information = arcade.gui.UIBorder(child=arcade.gui.UITextArea(text="Hello, I'm information",
                                                                                          width=((
                                                                                                         self.width - self.borders * 2 - int(
                                                                                                     self.width * 0.04)) / 2 - self.button_height / 8 * 2 - 12 * 2),
                                                                                          height=self.height - self.borders * 2 - self.button_height - self.button_height / 8 * 3 - 12 * 2,
                                                                                          font_name="Kenney Mini Square",
                                                                                          text_color=arcade.color_from_hex_string(
                                                                                              "2e2117")),

                                                              border_width=12,
                                                              border_color=arcade.color_from_hex_string("2e2117"))
        information_console_change_name = arcade.gui.UIBorder(child=arcade.gui.UITextArea(text="Hello, I'm information",
                                                                                          width=((
                                                                                                         self.width - self.borders * 2 - int(
                                                                                                     self.width * 0.04)) / 2 - self.button_height / 8 * 2 - 12 * 2),
                                                                                          height=self.height - self.borders * 2 - self.button_height - self.button_height / 8 * 4 - 12 * 5 - self.button_height / 2 * 2,
                                                                                          font_name="Kenney Mini Square",
                                                                                          text_color=arcade.color_from_hex_string(
                                                                                              "2e2117")),

                                                              border_width=12,
                                                              border_color=arcade.color_from_hex_string("2e2117"))
        information_console_change_password = arcade.gui.UIBorder(
            child=arcade.gui.UITextArea(text="Hello, I'm information",
                                        width=((self.width - self.borders * 2 - int(
                                            self.width * 0.04)) / 2 - self.button_height / 8 * 3 - 12 * 2),
                                        height=self.height - self.borders * 2 - self.button_height - self.button_height / 2 * 4 - self.button_height / 8 * 6 - 12 * 6,
                                        font_name="Kenney Mini Square",
                                        text_color=arcade.color_from_hex_string("2e2117")),

            border_width=12,
            border_color=arcade.color_from_hex_string("2e2117"))
        information_console_delete = arcade.gui.UIBorder(child=arcade.gui.UITextArea(text="Hello, I'm information",
                                                                                     width=((
                                                                                                    self.width - self.borders * 2 - int(
                                                                                                self.width * 0.04)) / 2 - self.button_height / 8 * 2 - 12 * 2),
                                                                                     height=self.height - self.borders * 2 - self.button_height - self.button_height / 8 * 3 - 12 * 2,
                                                                                     font_name="Kenney Mini Square",
                                                                                     text_color=arcade.color_from_hex_string(
                                                                                         "2e2117")),

                                                         border_width=12,
                                                         border_color=arcade.color_from_hex_string("2e2117"))
        old_password_text = arcade.gui.UITextArea(text="Current password",
                                                  width=self.button_width * 2,
                                                  height=self.button_height / 2,
                                                  font_name="Kenney Mini Square",
                                                  text_color=arcade.color_from_hex_string("2e2117"))
        new_password_text = arcade.gui.UITextArea(text="New password",
                                                  width=self.button_width * 2,
                                                  height=self.button_height / 2,
                                                  font_name="Kenney Mini Square",
                                                  text_color=arcade.color_from_hex_string("2e2117"))
        old_password = arcade.gui.UIBorder(child=arcade.gui.UIInputText(text=Config.GetLastPassword(),
                                                                        font_name="Kenney Mini Square",
                                                                        width=self.button_width * 2,
                                                                        height=self.button_height / 2,
                                                                        text_color=arcade.color_from_hex_string(
                                                                            "2e2117")),
                                           border_width=12,
                                           border_color=arcade.color_from_hex_string("2e2117"))
        new_password = arcade.gui.UIBorder(child=arcade.gui.UIInputText(text='',
                                                                        font_name="Kenney Mini Square",
                                                                        width=self.button_width * 2,
                                                                        height=self.button_height / 2,
                                                                        text_color=arcade.color_from_hex_string(
                                                                            "2e2117")),
                                           border_width=12,
                                           border_color=arcade.color_from_hex_string("2e2117"))
        new_username_input = arcade.gui.UIBorder(child=arcade.gui.UIInputText(text='',
                                                                              font_name="Kenney Mini Square",
                                                                              width=self.button_width * 2,
                                                                              height=self.button_height / 2,
                                                                              text_color=arcade.color_from_hex_string(
                                                                                  "2e2117")),
                                                 border_width=12,
                                                 border_color=arcade.color_from_hex_string("2e2117"))
        change_name_button = arcade.gui.UIFlatButton(text="Change Username",
                                                     width=self.button_width,
                                                     height=self.button_height,
                                                     style=self.button_style)
        change_password_button = arcade.gui.UIFlatButton(text="Change Password",
                                                         width=self.button_width,
                                                         height=self.button_height,
                                                         style=self.button_style)
        delete_acc_button = arcade.gui.UIFlatButton(text="Delete account",
                                                    width=self.button_width,
                                                    height=self.button_height,
                                                    style=self.button_style)
        # CLIKS
        information_button.on_click = self.on_acc_settings_button_click
        change_name_button.on_click = self.on_change_name_button_click
        change_password_button.on_click = self.on_change_password_button_click
        delete_acc_button.on_click = self.on_delete_account_button_click
        confirm_button.on_click = self.on_confirm_click

        # LEADERS BOARD
        leaders_board = arcade.gui.UIBorder(child=arcade.gui.UITextArea(text="---LEADERS BOARD---",
                                                                        width=((
                                                                                       self.width - self.borders * 2 - int(
                                                                                   self.width * 0.04)) / 2 - self.button_height / 8 * 2 - 12 * 2),
                                                                        height=self.height - self.borders * 2 - self.button_height - self.button_height / 8 * 3 - 12 * 2,
                                                                        font_name="Kenney Mini Square",
                                                                        text_color=arcade.color_from_hex_string(
                                                                            "2e2117")),
                                            border_width=12,
                                            border_color=arcade.color_from_hex_string("2e2117"))

        # MAPS
        # OBJECTS
        see_all_rating = arcade.gui.UIFlatButton(text="See all rating",
                                                 width=self.button_width,
                                                 height=self.button_height,
                                                 style=self.button_style)
        add_delete_change_map_rating = arcade.gui.UIFlatButton(text="Add, Delete, Change feedbacks",
                                                               width=self.button_width,
                                                               height=int(self.button_height * 1.5),
                                                               style=self.button_style)
        confirm_rating = arcade.gui.UIFlatButton(text="Confirm",
                                                 width=self.button_width,
                                                 height=self.button_height,
                                                 style=self.button_style)
        delete_rating = arcade.gui.UIFlatButton(text="Delete",
                                                width=self.button_width,
                                                height=self.button_height,
                                                style=self.button_style)
        rating_information = arcade.gui.UIBorder(child=arcade.gui.UITextArea(text="Hello, I'm information",
                                                                             width=((
                                                                                            self.width - self.borders * 2 - int(
                                                                                        self.width * 0.04)) / 2 - self.button_height / 8 * 2 - 12 * 2),
                                                                             height=self.height - self.borders * 2 - self.button_height - self.button_height / 8 * 3 - 12 * 2,
                                                                             font_name="Kenney Mini Square",
                                                                             text_color=arcade.color_from_hex_string(
                                                                                 "2e2117")),
                                                 border_width=12,
                                                 border_color=arcade.color_from_hex_string("2e2117"))
        rating_information_change = arcade.gui.UIBorder(child=arcade.gui.UITextArea(text="Hello, I'm information",
                                                                                    width=((
                                                                                                   self.width - self.borders * 2 - int(
                                                                                               self.width * 0.04)) / 2 - self.button_height / 8 * 3 - 12 * 2),
                                                                                    height=self.height - self.borders * 2 - self.button_height * 3 - self.button_height / 2 * 3 - self.button_height / 8 * 6 - 12 * 4,
                                                                                    font_name="Kenney Mini Square",
                                                                                    text_color=arcade.color_from_hex_string(
                                                                                        "2e2117")),
                                                        border_width=12,
                                                        border_color=arcade.color_from_hex_string("2e2117"))
        map_name_text = arcade.gui.UITextArea(text="Map name",
                                              width=self.button_width * 2,
                                              height=self.button_height / 2,
                                              font_name="Kenney Mini Square",
                                              text_color=arcade.color_from_hex_string("2e2117"))
        map_name_input = arcade.gui.UIBorder(child=arcade.gui.UIInputText(text="Enter map name",
                                                                          font_name="Kenney Mini Square",
                                                                          width=self.button_width * 2,
                                                                          height=self.button_height / 2,
                                                                          text_color=arcade.color_from_hex_string(
                                                                              "2e2117")),
                                             border_width=12,
                                             border_color=arcade.color_from_hex_string("2e2117"))
        rating_text = arcade.gui.UITextArea(text="Rating",
                                            width=self.button_width * 2,
                                            height=self.button_height / 2,
                                            font_name="Kenney Mini Square",
                                            text_color=arcade.color_from_hex_string("2e2117"))
        rating_one = arcade.gui.UITextureButton(text="",
                                                width=self.button_height / 2 + 12 * 2,
                                                height=int((self.button_height / 2 + 12 * 2) * 0.94),
                                                texture=self.snp,
                                                texture_hovered=self.sp,
                                                texture_pressed=self.sp)
        rating_two = arcade.gui.UITextureButton(text="",
                                                width=self.button_height / 2 + 12 * 2,
                                                height=int((self.button_height / 2 + 12 * 2) * 0.94),
                                                texture=self.snp,
                                                texture_hovered=self.sp,
                                                texture_pressed=self.sp)
        rating_three = arcade.gui.UITextureButton(text="",
                                                width=self.button_height / 2 + 12 * 2,
                                                height=int((self.button_height / 2 + 12 * 2) * 0.94),
                                                texture=self.snp,
                                                texture_hovered=self.sp,
                                                texture_pressed=self.sp)
        rating_fourth = arcade.gui.UITextureButton(text="",
                                                width=self.button_height / 2 + 12 * 2,
                                                height=int((self.button_height / 2 + 12 * 2) * 0.94),
                                                texture=self.snp,
                                                texture_hovered=self.sp,
                                                texture_pressed=self.sp)
        rating_five = arcade.gui.UITextureButton(text="",
                                                width=self.button_height / 2 + 12 * 2,
                                                height=int((self.button_height / 2 + 12 * 2) * 0.94),
                                                texture=self.snp,
                                                texture_hovered=self.sp,
                                                texture_pressed=self.sp)
        # CLICKS
        see_all_rating.on_click = self.on_maps_button_click
        add_delete_change_map_rating.on_click = self.on_add_delete_change_button_click
        rating_one.on_click = self.on_one_tap
        rating_two.on_click = self.on_two_tap
        rating_three.on_click = self.on_three_tap
        rating_fourth.on_click = self.on_fourth_tap
        rating_five.on_click = self.on_five_tap
        confirm_rating.on_click = self.on_confirm_rating_click
        delete_rating.on_click = self.on_delete_map_click

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
                'information': information_console_information,
                'change_password': change_password_button,
                'delete_account': delete_acc_button
            },
            'change_name': {
                'back': back_from_log_in,
                'information_button': information_button,
                'change_name': change_name_button,
                'change_password': change_password_button,
                'delete_account': delete_acc_button,
                'information': information_console_change_name,
                'username_text': username_text,
                'username': new_username_input,
                'confirm': confirm_button
            },
            'change_password': {
                'back': back_from_log_in,
                'information_button': information_button,
                'change_name': change_name_button,
                'change_password': change_password_button,
                'delete_account': delete_acc_button,
                'information': information_console_change_password,
                'old_password_text': old_password_text,
                'new_password_text': new_password_text,
                'old_password': old_password,
                'new_password': new_password,
                'confirm': confirm_button
            },
            'delete_account': {
                'back': back_from_log_in,
                'information_button': information_button,
                'change_name': change_name_button,
                'information': information_console_delete,
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
                'information': rating_information_change,
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
                            align_x=int(self.width * 0.16) + int(self.button_width / 2),
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
                            align_x=self.button_height / 8 + self.borders,
                            align_y=self.button_height / 8 + self.borders,
                            child=self.menu[menu]['back_button'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=-self.button_height / 8 - self.borders,
                            child=self.menu[menu]['host_console'],
                        )
                    ),
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=-self.button_height / 8 * 2 - self.borders - self.menu[menu][
                                'host_console'].height - 12 * 2,
                            child=self.menu[menu]['host_player_console'],
                        )
                    )
                elif menu == 'player':
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.borders + self.button_height / 8,
                            align_y=self.borders + self.button_height / 8 * 3 + self.button_height + self.button_height / 2 + 12 * 2,
                            child=self.menu[menu]['ip_input'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.borders + self.button_height / 8,
                            align_y=self.borders + self.button_height / 8 * 2 + self.button_height,
                            child=self.menu[menu]['port_input'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.borders + self.button_height / 8 * 2 + self.button_width - 7,
                            align_y=self.button_height / 8 + self.borders,
                            child=self.menu[menu]['connect'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=-self.button_height / 8 - self.borders,
                            child=self.menu[menu]['player_console']
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=self.button_height / 8 + self.borders,
                            child=self.menu[menu]['back_button'],
                        )
                    )
                elif menu == 'log_in':
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 + self.borders + 12,
                            align_y=self.borders + self.button_height + self.button_height / 8 * 3 + self.button_height / 2 * 4,
                            child=self.menu[menu]['username_text'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=self.borders + self.button_height + self.button_height / 8 * 3 + self.button_height / 2 * 3,
                            child=self.menu[menu]['username'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 + self.borders + 12,
                            align_y=self.borders + self.button_height + self.button_height / 8 * 2 + self.button_height / 2,
                            child=self.menu[menu]['password_text'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=self.borders + self.button_height + self.button_height / 8 * 2,
                            child=self.menu[menu]['password'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="center_x",
                            anchor_y="center_y",
                            align_x=int(self.width * 0.16) + int(self.button_width / 2),
                            align_y=self.button_height / 8 / 2 + self.button_height / 2,
                            child=self.menu[menu]['log_in'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="center_x",
                            anchor_y="center_y",
                            align_x=int(self.width * 0.16) + int(self.button_width / 2),
                            align_y=-self.button_height / 8 / 2 - self.button_height / 2,
                            child=self.menu[menu]['register'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=-self.button_height / 8 - self.borders,
                            child=self.menu[menu]['log_console']
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=self.button_height / 8 + self.borders,
                            child=self.menu[menu]['back_button'],
                        )
                    )
                elif menu == 'change_name':
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=self.button_height / 8 + self.borders,
                            child=self.menu[menu]['back'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.borders + self.button_height / 8 * 2 + self.button_width - 7,
                            align_y=self.button_height / 8 + self.borders,
                            child=self.menu[menu]['confirm'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="center_x",
                            anchor_y="center_y",
                            align_x=int(self.width * 0.16) + int(self.button_width / 2),
                            align_y=self.button_height / 8 / 2 + self.button_height / 8 + self.button_height / 2 + self.button_height,
                            child=self.menu[menu]['information_button'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="center_x",
                            anchor_y="center_y",
                            align_x=int(self.width * 0.16) + int(self.button_width / 2),
                            align_y=self.button_height / 8 / 2 + self.button_height / 2,
                            child=self.menu[menu]['change_name'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="center_x",
                            anchor_y="center_y",
                            align_x=int(self.width * 0.16) + int(self.button_width / 2),
                            align_y=-self.button_height / 8 / 2 - self.button_height / 2,
                            child=self.menu[menu]['change_password'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="center_x",
                            anchor_y="center_y",
                            align_x=int(self.width * 0.16) + int(self.button_width / 2),
                            align_y=-self.button_height / 8 / 2 - self.button_height / 8 - self.button_height / 2 - self.button_height,
                            child=self.menu[menu]['delete_account'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=-self.button_height / 8 - self.borders,
                            child=self.menu[menu]['information'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 + self.borders + 12,
                            align_y=self.borders + self.button_height + self.button_height / 8 * 2 + self.button_height / 2,
                            child=self.menu[menu]['username_text'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=self.borders + self.button_height + self.button_height / 8 * 2,
                            child=self.menu[menu]['username'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=-self.button_height / 8 - self.borders,
                            child=self.menu[menu]['information'],
                        )
                    )
                elif menu == 'information':
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=self.button_height / 8 + self.borders,
                            child=self.menu[menu]['back'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="center_x",
                            anchor_y="center_y",
                            align_x=int(self.width * 0.16) + int(self.button_width / 2),
                            align_y=self.button_height / 8 / 2 + self.button_height / 8 + self.button_height / 2 + self.button_height,
                            child=self.menu[menu]['information_button'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="center_x",
                            anchor_y="center_y",
                            align_x=int(self.width * 0.16) + int(self.button_width / 2),
                            align_y=self.button_height / 8 / 2 + self.button_height / 2,
                            child=self.menu[menu]['change_name'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="center_x",
                            anchor_y="center_y",
                            align_x=int(self.width * 0.16) + int(self.button_width / 2),
                            align_y=-self.button_height / 8 / 2 - self.button_height / 2,
                            child=self.menu[menu]['change_password'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="center_x",
                            anchor_y="center_y",
                            align_x=int(self.width * 0.16) + int(self.button_width / 2),
                            align_y=-self.button_height / 8 / 2 - self.button_height / 8 - self.button_height / 2 - self.button_height,
                            child=self.menu[menu]['delete_account'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=-self.button_height / 8 - self.borders,
                            child=self.menu[menu]['information'],
                        )
                    )
                elif menu == 'change_password':
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=self.button_height / 8 + self.borders,
                            child=self.menu[menu]['back'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="center_x",
                            anchor_y="center_y",
                            align_x=int(self.width * 0.16) + int(self.button_width / 2),
                            align_y=self.button_height / 8 / 2 + self.button_height / 8 + self.button_height / 2 + self.button_height,
                            child=self.menu[menu]['information_button'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="center_x",
                            anchor_y="center_y",
                            align_x=int(self.width * 0.16) + int(self.button_width / 2),
                            align_y=self.button_height / 8 / 2 + self.button_height / 2,
                            child=self.menu[menu]['change_name'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="center_x",
                            anchor_y="center_y",
                            align_x=int(self.width * 0.16) + int(self.button_width / 2),
                            align_y=-self.button_height / 8 / 2 - self.button_height / 2,
                            child=self.menu[menu]['change_password'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="center_x",
                            anchor_y="center_y",
                            align_x=int(self.width * 0.16) + int(self.button_width / 2),
                            align_y=-self.button_height / 8 / 2 - self.button_height / 8 - self.button_height / 2 - self.button_height,
                            child=self.menu[menu]['delete_account'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=-self.button_height / 8 - self.borders,
                            child=self.menu[menu]['information'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 + self.borders + 12,
                            align_y=self.borders + self.button_height + self.button_height / 8 * 3 + self.button_height / 2 * 5,
                            child=self.menu[menu]['old_password_text'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=self.borders + self.button_height + self.button_height / 8 * 3 + self.button_height / 2 * 3,
                            child=self.menu[menu]['old_password'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 + self.borders + 12,
                            align_y=self.borders + self.button_height + self.button_height / 8 * 2 + self.button_height / 2 * 2,
                            child=self.menu[menu]['new_password_text'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=self.borders + self.button_height + self.button_height / 8 * 2,
                            child=self.menu[menu]['new_password'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.borders + self.button_height / 8 * 2 + self.button_width - 7,
                            align_y=self.button_height / 8 + self.borders,
                            child=self.menu[menu]['confirm'],
                        )
                    )
                elif menu == 'delete_account':
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=self.button_height / 8 + self.borders,
                            child=self.menu[menu]['back'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="center_x",
                            anchor_y="center_y",
                            align_x=int(self.width * 0.16) + int(self.button_width / 2),
                            align_y=self.button_height / 8 / 2 + self.button_height / 8 + self.button_height / 2 + self.button_height,
                            child=self.menu[menu]['information_button'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="center_x",
                            anchor_y="center_y",
                            align_x=int(self.width * 0.16) + int(self.button_width / 2),
                            align_y=self.button_height / 8 / 2 + self.button_height / 2,
                            child=self.menu[menu]['change_name'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="center_x",
                            anchor_y="center_y",
                            align_x=int(self.width * 0.16) + int(self.button_width / 2),
                            align_y=-self.button_height / 8 / 2 - self.button_height / 2,
                            child=self.menu[menu]['change_password'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="center_x",
                            anchor_y="center_y",
                            align_x=int(self.width * 0.16) + int(self.button_width / 2),
                            align_y=-self.button_height / 8 / 2 - self.button_height / 8 - self.button_height / 2 - self.button_height,
                            child=self.menu[menu]['delete_account'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=-self.button_height / 8 - self.borders,
                            child=self.menu[menu]['information'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.borders + self.button_height / 8 * 2 + self.button_width - 7,
                            align_y=self.button_height / 8 + self.borders,
                            child=self.menu[menu]['confirm'],
                        )
                    )
                elif menu == 'leaders_board':
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=self.button_height / 8 + self.borders,
                            child=self.menu[menu]['back'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=-self.button_height / 8 - self.borders,
                            child=self.menu[menu]['leaders_board'],
                        )
                    )
                elif menu == 'see_all_rating':
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=self.button_height / 8 + self.borders,
                            child=self.menu[menu]['back'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=-self.button_height / 8 - self.borders,
                            child=self.menu[menu]['information'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="center_x",
                            anchor_y="center_y",
                            align_x=int(self.width * 0.16) + int(self.button_width / 2),
                            align_y=self.button_height / 8 / 2 + self.button_height / 2,
                            child=self.menu[menu]['see_all_rating'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="center_x",
                            anchor_y="center_y",
                            align_x=int(self.width * 0.16) + int(self.button_width / 2),
                            align_y=-self.button_height / 8 / 2 - int(self.button_height * 1.5 / 2),
                            child=self.menu[menu]['add/delete/change'],
                        )
                    )
                elif menu == 'add/delete/change':
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=self.button_height / 8 + self.borders,
                            child=self.menu[menu]['back'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="top",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=-self.button_height / 8 - self.borders,
                            child=self.menu[menu]['information'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="center_x",
                            anchor_y="center_y",
                            align_x=int(self.width * 0.16) + int(self.button_width / 2),
                            align_y=self.button_height / 8 / 2 + self.button_height / 2,
                            child=self.menu[menu]['see_all_rating'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="center_x",
                            anchor_y="center_y",
                            align_x=int(self.width * 0.16) + int(self.button_width / 2),
                            align_y=-self.button_height / 8 / 2 - self.button_height / 2,
                            child=self.menu[menu]['add/delete/change'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=self.button_height / 8 * 2 + self.borders + self.button_height,
                            child=self.menu[menu]['delete'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 * 2 + self.borders + self.button_width,
                            align_y=self.button_height / 8 * 2 + self.borders + self.button_height,
                            child=self.menu[menu]['confirm'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 + self.borders + 12,
                            align_y=self.button_height / 8 * 4 + self.borders + self.button_height + self.button_height + self.button_height + self.button_height / 2 * 2 + 12 * 2,
                            child=self.menu[menu]['map_name_text'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=self.button_height / 8 * 4 + self.borders + self.button_height + self.button_height + self.button_height + self.button_height / 2,
                            child=self.menu[menu]['map_name_input'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 + self.borders + 12,
                            align_y=self.button_height / 8 * 3 + self.borders + self.button_height + self.button_height + self.button_height,
                            child=self.menu[menu]['rating_text'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 + self.borders,
                            align_y=self.button_height / 8 * 3 + self.borders + self.button_height + self.button_height,
                            child=self.menu[menu]['one'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 * 2 + self.borders + self.menu[menu][
                                'one'].width,
                            align_y=self.button_height / 8 * 3 + self.borders + self.button_height + self.button_height,
                            child=self.menu[menu]['two'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 * 3 + self.borders + self.menu[menu][
                                'one'].width * 2,
                            align_y=self.button_height / 8 * 3 + self.borders + self.button_height + self.button_height,
                            child=self.menu[menu]['three'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 * 4 + self.borders + self.menu[menu][
                                'one'].width * 3,
                            align_y=self.button_height / 8 * 3 + self.borders + self.button_height + self.button_height,
                            child=self.menu[menu]['fourth'],
                        )
                    )
                    self.uimanager[menu].add(
                        arcade.gui.UIAnchorWidget(
                            anchor_x="left",
                            anchor_y="bottom",
                            align_x=self.button_height / 8 * 5 + self.borders + self.menu[menu][
                                'one'].width * 4,
                            align_y=self.button_height / 8 * 3 + self.borders + self.button_height + self.button_height,
                            child=self.menu[menu]['five'],
                        )
                    )

    def set_helper(self):
        self.helper = {
            'log_in': {
                'hello': """Hello, waiter. I'm Chef Victor. Since you're here, it's time to tell you how to use the account.\n
                            1) To register, enter an username and password and tap on REGISTER-BUTTON.\n
                            2) If you already have an account, just enter your details and get access to it.\n
                            3) Don't worry, I'll tell you if something goes wrong.""",
                'successful': "Welcome to game, ",
                'incorrect_password': "Hm... You may have entered an incorrect password. Try again.",
                'error_with_log_in': "Hm... You may have entered an incorrect username. Try again.",
                'error_with_register': "O, no! A waiter with that name already exists. Try to think of something else.",
                'help': """ 1) To register, enter an username and password and tap on REGISTER-BUTTON.\n
                           2) If you already have an account, just enter your details and get access to it.\n
                           3) Don't worry, I'll tell you if something goes wrong.""",
                'connection_error': "Oh... It seems the connection is broken. The problem can be both on your side and on our side."
            },
            'information': {
                'information': "Let's see, what you have!\n",
                'name': "\tSo,your name is\t\t",
                'password': "\n\tPassword is\t\t\t",
                'score': "\n\tHo-ho! Your score is\t",
                'steps': "\n\tAnd you've run over\t",
                'final': "\tsteps!\nYou are very good waiter!",
                'connection_error': "Oh... It seems the connection is broken. The problem can be both on your side and on our side."
            },
            'change_name': {
                'hello': "So, here you can change your username. To do this, just enter a new username and click confirm",
                'successful': "All right! Now your name is ",
                'no': "User with this name is already exist.",
                'connection_error': "Oh... It seems the connection is broken. The problem can be both on your side and on our side."
            },
            'change_password': {
                'hello': "So, here you can change your password. To do this, just enter a old and new password and click confirm",
                'successful': "All right! Now your password is ",
                'connection_error': "Oh... It seems the connection is broken. The problem can be both on your side and on our side."
            },
            'delete_account': {
                'hello': "So, here you can delete your account. To do this, just tap on confirm",
                'error': "Something goes wrong. Try again.",
                'connection_error': "Oh... It seems the connection is broken. The problem can be both on your side and on our side."
            },
            'leaders_board': {
                'connection_error': "Oh... It seems the connection is broken. The problem can be both on your side and on our side."
            },
            'see_all_rating': {
                'connection_error': "Oh... It seems the connection is broken. The problem can be both on your side and on our side."
            },
            'add/delete/change': {
                "hello": "Here you can add, delete or change your feedbacks og maps. To change or add rating you must write map name to input block, click on star and tap on confirm-button. To delete you must write map name and tap on delete-button. List of maps you can use:\n",
                'successful_add': "You added a rating!",
                'successful_delete': "You delete a rating!",
                'connection_error': "Oh... It seems the connection is broken. The problem can be both on your side and on our side.",
                'no_in_maps': "So, there isn't this map in your game directory or feedback list",
                'no_in_feedback': "So, there isn't this map in your feedback list"
            }
        }


# Calling MainGame class
def Main():
    Width, Height = arcade.get_display_size()
    Width = int(Width * 0.8 * 0.8)
    Height = int(Height * 0.8)
    if Width > 1280:
        Width = 1280
    if Height > 900:
        Height = 900
    Title = "RestGuy"

    MainGame(Width, Height, Title)
    arcade.run()


Main()
