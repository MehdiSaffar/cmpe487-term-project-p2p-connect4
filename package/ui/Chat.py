import pygame_gui
from ..constants import *

from colorhash import ColorHash

import random
import pygame
from pygame_gui.elements.ui_text_entry_line import UITextEntryLine
from pygame_gui.elements.ui_text_box import UITextBox

from ..Packet import chat_message_packet


class Chat:
    def __init__(self, app) -> None:
        self.app = app

        self.chatbox = None

        self.ui = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.prepare_chatbox()
        self.prepare_inputbox()

    @property
    def is_focused(self):
        return self.inputbox.is_focused

    def update(self):
        self.ui.update(self.app.time_delta)

    def draw(self):
        self.ui.draw_ui(self.app.screen)

    def handle_event(self, event):
        self.ui.process_events(event)
        if event.type == 'new_message':
            self.prepare_chatbox()
        if event.type == pygame.USEREVENT:
            if event.user_type == 'ui_text_entry_finished':
                print('Chat.handle_event', event)
                self.handle_inputbox_press_enter(event)

    def handle_inputbox_press_enter(self, event):
        print('LobbyScene.handle_inputbox_press_enter event', event)
        text = event.text
        self.app.messages.append(('regular', self.app.my_name, text))
        self.prepare_chatbox()

        for player in self.app.players.values():
            print('LobbyScene.handle_inputbox_press_enter send to', player, text)
            self.app.network.send(('tcp', player['ip'], chat_message_packet(
                self.app.my_name, self.app.network.ip,  text)))
        self.inputbox.set_text('')

    def show(self):
        self.chatbox.show()
        self.inputbox.show()

    def hide(self):
        self.chatbox.hide()
        self.inputbox.hide()

    def finalize(self):
        self.chatbox.hide()
        self.inputbox.hide()

        self.chatbox.kill()
        self.inputbox.kill()

    def prepare_chatbox(self):
        text = ''

        for type, auth, txt in self.app.messages:
            if type == 'regular':
                text += f"""<font color="{ColorHash(auth).hex}">{auth}</font>: {txt}<br/>"""
            elif type == 'event':
                text += f"""<font color="#FAA237">{txt}</font><br/>"""

        if self.chatbox is None:
            self.chatbox = UITextBox(text, pygame.Rect(
                (560, 0), (300, SCREEN_HEIGHT - 60)), self.ui)
        else:
            self.chatbox.html_text = text
            self.chatbox.rebuild()
            if self.chatbox.scroll_bar:
                scroll_bar = self.chatbox.scroll_bar
                scroll_bar.scroll_wheel_down = False
                scroll_bar.scroll_position += (250 * 1)
                scroll_bar.scroll_position = min(scroll_bar.scroll_position,
                                                 scroll_bar.bottom_limit - scroll_bar.sliding_button.rect.height)
                x_pos = scroll_bar.rect.x + scroll_bar.shadow_width + scroll_bar.border_width
                y_pos = scroll_bar.scroll_position + scroll_bar.rect.y + scroll_bar.shadow_width + \
                    scroll_bar.border_width + scroll_bar.button_height
                scroll_bar.sliding_button.set_position(
                    pygame.math.Vector2(x_pos, y_pos))

                scroll_bar.start_percentage = scroll_bar.scroll_position / \
                    scroll_bar.scrollable_height
                if not scroll_bar.has_moved_recently:
                    scroll_bar.has_moved_recently = True

    def prepare_inputbox(self):
        self.inputbox = UITextEntryLine(pygame.Rect(
            (560, SCREEN_HEIGHT - 60), (300, 60)), self.ui)
