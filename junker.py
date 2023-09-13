import random

import pygame
from pygame import Rect
import pygame.freetype
import pygame_menu
pygame.freetype.init()
title_Font = pygame_menu.font.FONT_8BIT # pygame.freetype.SysFont('bahnschrift',20)
text_Font = pygame_menu.font.FONT_MUNRO # pygame.freetype.SysFont('bahnschrift',14)
import pygame_menu, pygame_gui
from pygame_gui.core import ObjectID

menu_theme = pygame_menu.themes.THEME_ORANGE
menu_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE

class Card:
    def __init__(self, title, text, width, height, x, y, color=(255,255,255)):
        self.title = title
        self.text = text
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color
        self.rect = Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        pygame.draw.rect(surface,self.color,self.rect)
        title_Font.render_to(surface,(self.x,self.y),self.title,(0,0,0))




class Hand:
    def  __init__(self, surface, map_width, card_width):
        self.card_one_XY = (surface.get_width()-map_width, 5)
        self.card_two_XY = (self.card_one+card_width, 5)
        self.card_three_XY = (self.card_two + card_width, 5)
        self.card_four_XY = (self.card_three + card_width, 5)
        self.card_five_XY = (self.card_four + card_width, 5)
        self.hand_contents = []

    def buildHand(self):
        for card in self.hand_contents:
            pass


class Player:
    def __init__(self):
        self.name = ""
        self.gold = 0
        self.metal = 0
        self.wood = 0
        self.scrap = 0
        self.contract_list = []
        self.junkin_map = ""

class Character:
    def __init__(self, name, profession, trust=0):
        self.name = name
        self.profession = profession
        self.trust = trust

class Scenario:
   #Codes on scenario results. A = add resource; L = lose resource; M = Metal, W = Wood, J = Junk, G = Gold

    def __init__(self, number, player, surface, background='Assets/wasteland2.jpg', menu_title="Title", menu_height=300, menu_text = "",
                 menu_buttons=None):
        if menu_buttons is None:
            menu_buttons = [('Button 1', 'AM'), ('Button 2', 'LM'), ('Button 3', 'AJ')]
        self.title = 'Scenario #%s' % number
        self.option_chain = []
        self.image = pygame.image.load(background)
        self.menu_width = surface.get_width()
        self.menu_height = menu_height
        self.menu = pygame_menu.Menu(menu_title, self.menu_width, menu_height, theme=menu_theme)
        self.menu.set_absolute_position(0, surface.get_height()-menu_height)

        if menu_text != "":
            self.menu.add.label(menu_text, wordwrap=True)
        for button in menu_buttons:
            if button[1] == 'AM':
                self.menu.add.button(button[0], self.add_metal, player)
            elif button[1] == 'LM':
                self.menu.add.button(button[0], self.lose_metal, player)
            elif button[1] == 'AJ':
                self.menu.add.button(button[0], self.add_junk, player)

    def add_metal(self, player):
        metal_gained = random.randint(1, 10)
        player.metal = player.metal + metal_gained
        return player

    def lose_metal(self, player):
        metal_lost = random.randint(1, 10)
        player.metal = player.metal - metal_lost
        return player

    def add_junk(self, player):
        junk_gained = random.randint(1, 10)
        player.junk = player.junk + junk_gained
        return player



    def draw_scen(self, surface):
        self.menu.draw(surface)


class JunkinMap:
    def __init__(self, surface, map_width, map_height):
        # self.map = pygame_menu.Menu("Where do you want to search?", surface.get_width(), surface.get_height(), columns=2, rows=2)
        # self.map.add.button("The Quarry", self.quarry)
        # self.map.add.button("The Junkyard", self.quarry)
        # self.map.add.button("The Forest", self.quarry)
        # self.map.add.button("The Wasteland", self.quarry)
        self.map_width = map_width
        self.map_height = map_height
        self.area_list = []
        self.map_dict = {}
        self.map_created = False


    def create_map(self, manager, surface):
        map_rect = pygame.Rect(0, 0, surface.get_width(), surface.get_height() - 200)
        map_window = pygame_gui.elements.UIWindow(map_rect, manager=manager)
        buffer = 10
        area_width = (map_rect.width - buffer * (self.map_width + 4)) / self.map_width
        area_height = (map_rect.height - buffer * (self.map_height + 7)) / self.map_height
        current_rect = pygame.Rect(map_rect.left-area_width, map_rect.top-area_height, area_width, area_height)
        cur_width, cur_height = self.map_width, self.map_height
        grid_object_id = ObjectID(class_id="@friendly_button", object_id="#normal")
        while cur_width > 0:
            while cur_height > 0:
                draw_rect = pygame.Rect(current_rect.left+(buffer+area_width)*cur_height, current_rect.top+(buffer+area_height)*cur_width,
                                        area_width, area_height)
                cur_button = pygame_gui.elements.UIButton(draw_rect, "Unknown", manager=manager, container=map_window)
                cur_button.object_id = grid_object_id
                self.area_list.append(cur_button)
                self.map_dict.update({(cur_width, cur_height): cur_button})
                cur_height -= 1
            cur_width -= 1
            cur_height = self.map_height
        self.map_created = True
        return manager

    def update_map(self, manager, surface, areas_to_update):
        if not self.map_created:
            pass
        else:
            for area in areas_to_update:
                if area[1] == "start":
                    self.map_dict[area[0]].object_id = ObjectID(class_id="@friendly_button", object_id='#selectable')
                    self.map_dict[area[0]].text = "Start Here"
            return self.draw_map(manager, surface)

    def draw_map(self, manager, surface):
        map_rect = pygame.Rect(0, 0, surface.get_width(), surface.get_height() - 200)
        map_window = pygame_gui.elements.UIWindow(map_rect, manager=manager)
        buffer = 10
        area_width = (map_rect.width - buffer * (self.map_width + 4)) / self.map_width
        area_height = (map_rect.height - buffer * (self.map_height + 7)) / self.map_height

        current_rect = pygame.Rect(map_rect.left-area_width, map_rect.top-area_height, area_width, area_height)
        for area in self.map_dict:
            draw_rect = pygame.Rect(current_rect.left + (buffer + area_width) * area[0],
                                    current_rect.top + (buffer + area_height) * area[1], area_width, area_height)
            cur_button = pygame_gui.elements.UIButton(draw_rect, self.map_dict[area].text, manager=manager, container=map_window, object_id=self.map_dict[area].object_id)

        return manager
    def choose_start(self, manager, surface):
        pass


def create_Scenarios(player, surface):
    scenario_list = []

    scenario_list.append(
        Scenario(1, player, surface,
            menu_title="Scorpion Attack",
            menu_text="You've been confronted by a huge scorpion, what do you do?",
            menu_buttons=[("Run Away", 'AM'), ("Stand and Fight", 'LM'), ("Hide", 'AJ')])
        )

    return scenario_list


class Contract:
    def __init__(self, title, contractor, needed, reward, description):
        self.title = title
        self.contractor = contractor
        self.needed = needed
        self.reward = reward
        self.description = description
        self.lines = 0

        if len(description) > 20:
            description_return = ["", "", "", "", ""]
            description_lines = description.split()
            count = 0
            line = 0
            for word in description_lines:
                description_return[line] = description_return[line]+ word + " "
                count += 1
                if count == 10:
                    count = 0
                    line += 1
            self.description = description_return
            self.lines = line


def create_Contracts():
    contract_list = []

    contract_list.append(
        Contract(
            "Building a new tool shed",
            Character("Randy", "Carpenter"),
            [("Metal", 100), ("Wood", 50)],
            [("Scrap", 300)],
            "With the Startsville growth projects i've had a lot more work lately. I need "
            "materials to build a new tool shed that my employees can use."
        )
    )

    return contract_list
