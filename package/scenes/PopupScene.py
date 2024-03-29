from package.Packet import game_request_packet, discover_packet, game_reply_packet
from .. import scenes
import pygame
import pygame_menu
from ..constants import *


class PopupScene:
    def __init__(self, app, win_state, player_name):
        self.app = app
        self.win_state = win_state
        self.player_name = player_name

        self.init_themes()

        print("Game ended: ", win_state)

        self.show_result_popup()

        if win_state == 'win':
            self.increase_my_score()
        elif win_state == 'lose':
            self.decrease_my_score()

    def init_themes(self):
        self.request_menu_theme = pygame_menu.themes.Theme(
            background_color=Color.LIGHT_BLUE,  # transparent background
            title_shadow=True,
            title_background_color=(4, 47, 126), widget_font_color=Color.WHITE)

        self.draw_menu_theme = pygame_menu.themes.Theme(
            background_color=Color.LIGHT_SLATE_GRAY,
            title_font_size=18,
            title_background_color=Color.DARK_GRAY_2,
            widget_font_color=Color.WHITE,
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE)

        self.win_menu_theme = pygame_menu.themes.Theme(
            background_color=Color.PALE_GREEN,
            title_font_size=18,
            title_background_color=Color.DARK_GREEN,
            widget_font_color=Color.WHITE,
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE)

        self.lose_menu_theme = pygame_menu.themes.Theme(
            title_font_size=18,
            background_color=Color.INDIAN_RED,
            title_background_color=Color.DARK_RED,
            widget_font_color=Color.WHITE,
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE)

    def show_result_popup(self):
        config = {
            'draw': dict(
                theme=self.draw_menu_theme,
                title="It's a Tie!"
            ),
            'win': dict(
                theme=self.win_menu_theme,
                title='Congratulations you won!'
            ),
            'lose': dict(
                theme=self.lose_menu_theme,
                title='Sorry, game over...'
            ),
            'game_aborted': dict(
                theme=self.draw_menu_theme,
                title="Game aborted"
            ),
            'request_cancelled': dict(
                theme=self.draw_menu_theme,
                title="Request cancelled"
            ),
            'request_declined': dict(
                theme=self.draw_menu_theme,
                title="Request declined"
            ),
        }

        label = {
            'game_aborted': f'{self.player_name} quit the game',
            'request_cancelled': f'{self.player_name} cancelled your request',
            'request_declined': f'{self.player_name} declined your request'
        }

        self.menu = pygame_menu.Menu(
            SCREEN_HEIGHT//2, SCREEN_WIDTH//2, **config[self.win_state])
        if self.win_state in ['win', 'draw', 'lose']:
            self.menu.add_button('Rematch', self.handle_rematch)
        else:
            self.menu.add_label(label[self.win_state])

        self.menu.add_button('Return to Lobby', self.handle_return_to_lobby)

    def handle_return_to_lobby(self):
        self.app.scene = scenes.LobbyScene(self.app)

    def handle_rematch(self):
        self.app.scene = scenes.SendRequestScene(self.app)

    def increase_my_score(self):
        self.app.my_all_scores[self.app.my_name] += 10
        self.app.my_score += 10
        self.app.players[self.player_name]['score'] -= 10
        self.app.write_my_score_into_file()
        print("my score: ", self.app.my_all_scores[self.app.my_name])

    def decrease_my_score(self):
        self.app.my_all_scores[self.app.my_name] -= 10
        self.app.my_score -= 10
        self.app.players[self.player_name]['score'] += 10
        self.app.write_my_score_into_file()
        print("my score: ", self.app.my_all_scores[self.app.my_name])

    def handle_event(self, event):
        if event.type == 'tcp':
            if event.data['type'] == 'game_request':
                self.state = {'type': 'invited', 'packet': event.data}
                print("preparing invite menu")
                self.prepare_rematch_invite_menu()
        self.menu.update([event])

    def prepare_rematch_invite_menu(self):
        player_name = self.state['packet']['name']

        self.menu = pygame_menu.Menu(
            SCREEN_HEIGHT, SCREEN_WIDTH, 'Game request', theme=self.request_menu_theme)
        self.menu.add_label(f"{player_name} wants a rematch")
        self.menu.add_button('Accept', self.handle_accept_invite)
        self.menu.add_button('Decline', self.handle_reject_invite)

    def handle_accept_invite(self):
        self.app.player_name = self.state['packet']['name']
        self.app.network.send(('tcp', self.state['packet']['ip'], game_reply_packet(
            self.app.my_name, self.app.network.ip, True)))
        self.app.scene = scenes.PlayScene(
            self.app, is_my_turn=True, my_player_number=PLAYER1)

    def handle_reject_invite(self):
        self.app.network.send(('tcp', self.state['packet']['ip'], game_reply_packet(
            self.app.my_name, self.app.network.ip, False)))
        self.state = {'type': 'normal'}
        self.show_result_popup()

    def update(self):
        pass

    def draw(self):
        self.menu.draw(self.app.screen)
