import pygame
from pygame.locals import *
import sys
import os


def resource_path(relative_path, sub):
    try:
        base_path = os.path.join(sys._MEIPASS, sub)
    except Exception:
        base_path = os.path.abspath(os.path.join("..", sub))

    return os.path.join(base_path, relative_path)


background = resource_path('background.jpg', 'img')
font = resource_path('kalam.ttf', 'font')


class Game:

    def __init__(self):
        self.__pygame = pygame
        self.__resolution = {'width': 450,
                             'height': 399}
        self.__center = (self.__resolution['width'] // 2, self.__resolution['height'] // 2)
        self.__colors = {'white': (255, 255, 255),
                         'black': (0, 0, 0),
                         'red': (255, 0, 0),
                         'gray': (183, 193, 204),
                         'yellow': (249, 217, 54),
                         'blue': (0, 15, 85),
                         'green': (50, 205, 50)}
        self.__message = ''
        self.__button = ''
        self.__screen = ''
        self.__mouse_pos = ()
        self.__mouse_click = ()
        self.__images = {'background': self.__pygame.image.load(background)}
        self.__clock = self.__pygame.time.Clock()
        self.__font_type = font
        self.__fields_pos = []
        self.__field_size = ()
        self.__board_size = 0
        self.__board_pos = ()
        self.__board_fields_count = []

    @property
    def mouse_pos(self) -> tuple:
        return self.__mouse_pos

    @property
    def mouse_click(self) -> tuple:
        return self.__mouse_click

    @mouse_click.setter
    def mouse_click(self, val: tuple):
        self.__mouse_click = val

    @property
    def colors(self) -> dict:
        return self.__colors

    @property
    def center(self) -> tuple:
        return self.__center

    def screen_fill(self, clr):
        self.__screen.fill(clr)

    def get_mouse_pos(self):
        self.__mouse_pos = self.__pygame.mouse.get_pos()

    def get_mouse_click(self):
        self.__mouse_click = self.__pygame.mouse.get_pressed()

    def background_display(self):
        self.__screen.blit(self.__images['background'], (0, 0))

    def init(self, lang: dict, board_size: int, board_pos: tuple, board_fields_count=(3, 3)):
        self.__pygame.init()
        self.__screen = self.__pygame.display.set_mode((self.__resolution['width'], self.__resolution['height']))
        self.__pygame.display.set_caption(lang['title'])
        self.__board_size = board_size
        self.__board_pos = board_pos
        self.__board_fields_count = board_fields_count
        self.__get_fields_pos()
        self.__get_grid_pos()

    def caption_change(self, lang: dict):
        self.__pygame.display.set_caption(lang['title'])

    def win_line(self, start_pos: tuple, end_pos: tuple):
        self.__pygame.draw.line(self.__screen, self.__colors['red'], start_pos, end_pos, 4)

    def fill_board(self, board: list):
        self.message_display(board[6], 30, self.__colors['blue'], (self.__center[0] - 60, self.__center[1] - 90))
        self.message_display(board[3], 30, self.__colors['blue'], (self.__center[0] - 60, self.__center[1] - 30))
        self.message_display(board[0], 30, self.__colors['blue'], (self.__center[0] - 60, self.__center[1] + 30))
        self.message_display(board[7], 30, self.__colors['blue'], (self.__center[0], self.__center[1] - 90))
        self.message_display(board[4], 30, self.__colors['blue'], (self.__center[0], self.__center[1] - 30))
        self.message_display(board[1], 30, self.__colors['blue'], (self.__center[0], self.__center[1] + 30))
        self.message_display(board[8], 30, self.__colors['blue'], (self.__center[0] + 60, self.__center[1] - 90))
        self.message_display(board[5], 30, self.__colors['blue'], (self.__center[0] + 60, self.__center[1] - 30))
        self.message_display(board[2], 30, self.__colors['blue'], (self.__center[0] + 60, self.__center[1] + 30))

    def draw_board(self):
        self.__pygame.draw.line(self.__screen, self.__colors['blue'], (self.__center[0] - 30, self.__center[1] - 120), (self.__center[0] - 30, self.__center[1] + 60), 4)
        self.__pygame.draw.line(self.__screen, self.__colors['blue'], (self.__center[0] + 30, self.__center[1] - 120), (self.__center[0] + 30, self.__center[1] + 60), 4)
        self.__pygame.draw.line(self.__screen, self.__colors['blue'], (self.__center[0] - 90, self.__center[1] - 60), (self.__center[0] + 90, self.__center[1] - 60), 4)
        self.__pygame.draw.line(self.__screen, self.__colors['blue'], (self.__center[0] - 90, self.__center[1]), (self.__center[0] + 90, self.__center[1]), 4)

    def draw_board_2(self):
        pass

    def __get_fields_pos(self):
        field_size = (self.__board_size // self.__board_fields_count[0], self.__board_size // self.__board_fields_count[1])
        fields_pos = []
        offset = 0
        for row in range(self.__board_fields_count[1]):
            current_field_position = (self.__board_pos[0], self.__board_pos[1] + offset)
            for field in range(self.__board_fields_count[0]):
                current_field_position = (current_field_position[0], current_field_position[1])
                fields_pos.append(current_field_position)
                current_field_position = (current_field_position[0] + field_size[0], current_field_position[1])
            offset += field_size[1]
        self.__fields_pos = fields_pos
        self.__field_size = field_size

    def __get_grid_pos(self):
        x_left = self.__fields_pos[0][0]
        x_right = self.__fields_pos[0][0] + self.__board_size
        y_high = self.__fields_pos[0][1]
        y_low = self.__fields_pos[0][1] + self.__board_size
        grid_pos = []
        x_offset = self.__field_size[0]
        y_offset = self.__field_size[1]
        x_pos = 0
        y_pos = 0
        for line in range(self.__board_fields_count[1] - 1):
            x_pos += x_offset
            grid_pos.append(((x_pos, y_high), (x_pos, y_low)))
        for line in range(self.__board_fields_count[0] - 1):
            y_pos += y_offset
            grid_pos.append(((x_left, y_pos), (x_right, y_pos)))
        print(grid_pos)
        self.__grid_pos = grid_pos

    def events(self):
        events = self.__pygame.event.get()
        for e in events:
            if e.type == QUIT:
                sys.exit(0)

    def display_update(self):
        self.__pygame.display.update()
        self.__clock.tick(60)

    def player_move(self, board: object, player_sign: str):
        self.button_display('', self.__center[0] - 90, self.__center[1] - 120, 60, 60, board.update_board, args=(6, player_sign))
        self.button_display('', self.__center[0] - 90, self.__center[1] - 60, 60, 60, board.update_board, args=(3, player_sign))
        self.button_display('', self.__center[0] - 90, self.__center[1], 60, 60, board.update_board, args=(0, player_sign))
        self.button_display('', self.__center[0] - 30, self.__center[1] - 120, 60, 60, board.update_board, args=(7, player_sign))
        self.button_display('', self.__center[0] - 30, self.__center[1] - 60, 60, 60, board.update_board, args=(4, player_sign))
        self.button_display('', self.__center[0] - 30, self.__center[1], 60, 60, board.update_board, args=(1, player_sign))
        self.button_display('', self.__center[0] + 30, self.__center[1] - 120, 60, 60, board.update_board, args=(8, player_sign))
        self.button_display('', self.__center[0] + 30, self.__center[1] - 60, 60, 60, board.update_board, args=(5, player_sign))
        self.button_display('', self.__center[0] + 30, self.__center[1], 60, 60, board.update_board, args=(2, player_sign))

    def message_display(self, text: str, size: int, clr: tuple, pos: tuple):
        my_font = self.__pygame.font.Font(self.__font_type, size)
        label = my_font.render(text, 1, clr)
        label_rect = label.get_rect(center=pos)
        self.__screen.blit(label, label_rect)

    def button_display(self, name: str, x: int, y: int, w: int, h: int, fun, args=None):
        text = h // 2
        if x < self.__mouse_pos[0] < x + w and y < self.__mouse_pos[1] < y + h:
            self.message_display(name, int(text + text * 0.2), self.__colors['red'], (x + w / 2, y + h / 3))
            if self.__mouse_click[0] == 1:
                br = False
                while not br:
                    events = self.__pygame.event.get()
                    self.get_mouse_pos()
                    for e in events:
                        if e.type == MOUSEBUTTONUP and x < self.__mouse_pos[0] < x + w and y < self.__mouse_pos[1] < y + h:
                            if args:
                                fun(*args)
                                br = True
                            else:
                                fun()
                                br = True
                        else:
                            br = True
        else:
            self.message_display(name, text, self.__colors['blue'], (x + w / 2, y + h / 3))
