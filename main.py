# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pygame
import pygame_menu
import pygame_widgets
import pygame_gui
from pygame_widgets.textbox import TextBox
import junker
import os
import pygame.freetype
import random
from junker import Scenario, Player, JunkinMap

run = True
main_map = pygame.image.load('Assets/Junker Initial Map.png') # 929 x 615
wasteland = pygame.image.load('Assets/BKgr2.png')
startsville = pygame.image.load('Assets/startsville2.jpg')
map_width = main_map.get_width()
map_height = main_map.get_height()
clock = pygame.time.Clock()
screen_width = 1300
screen_height = 900
surface_x = 100
surface_y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (surface_x, surface_y)
card_width = 100
card_height = 150
menu_theme = pygame_menu.themes.THEME_ORANGE
widget_font = pygame_menu.font.FONT_MUNRO
title_font = pygame_menu.font.FONT_8BIT

menu_theme.widget_font = widget_font
menu_theme.title_font = title_font
menu_theme.title_font_size = 27
#menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
player_name = "You"


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')


pygame.init()
pygame.display.set_caption('Junker Legacy')
surface = pygame.display.set_mode((1300, 900))

# below is the process for using the pygame_gui
manager = pygame_gui.UIManager((1300, 900))

def set_difficulty(value, difficulty):
    # Do the job here !
    pass


def main_menu():
    main_menu_running = True
    game_surface = pygame.display.set_mode((screen_width, screen_height))
    menu_width, menu_height = 400, 300
    play_rect = pygame.Rect(0, -20, 100, 20)
    quit_rect = pygame.Rect(0, 20, 100, 20)
    menu_rect = pygame.Rect((game_surface.get_width()-menu_width)/2, (game_surface.get_height()-menu_height)/2, menu_width, menu_height)
    menu_window = pygame_gui.elements.UIWindow(menu_rect, manager=manager,)
    play_button = pygame_gui.elements.UIButton(relative_rect=play_rect, text="Play",
                                               manager=manager, container=menu_window,
                                               anchors={'center': 'center'}, object_id='#play_button')
    quit_button = pygame_gui.elements.UIButton(relative_rect=quit_rect, text="Quit",
                                               manager=manager, container=menu_window,
                                               anchors={'center': 'center'}, object_id='quit_button')

    '''
    # Old code with Pygame_menu functionality.
    start_theme = menu_theme.copy()
    start_theme.widget_alignment = pygame_menu.locals.ALIGN_CENTER
    menu = pygame_menu.Menu('Welcome', 400, 300,
                            theme=start_theme)

    test_name = menu.add.text_input('Name :', default=' Jimmy P')
    # menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
    menu.add.button('Play', start_the_game, test_name.get_value())
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(surface)
    '''
    while main_menu_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu_running = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == play_button:
                    start_the_game("Jimmy P", ["TC Tyler", "Scrappy", "Jimmy P", "Tommy Tanks"])
                    print("At least this worked")
                if event.ui_element == quit_button:
                    main_menu_running = False

            manager.process_events(event)

        manager.update(time_delta)
        game_surface.fill((0, 0, 0))
        manager.draw_ui(game_surface)
        pygame.display.update()


def go_to_town(game_surface, contract_list):

    def add_contract_to_player(contract):
        pass

    def display_details(contract): #ADDING THIS TO THE SAME MENU AS CHOOSING FROM. WOULD BE BETTER TO CREATE SEPARATE MENU AND EACH LINE BE NEW LABEL.
                                    # Could have remaining screen taken up by second menu, so more detail and art can be added to contracts later.
        new_menu = pygame_menu.Menu("Contracts", game_surface.get_width()-300, game_surface.get_height(), theme=menu_theme)
        new_menu.set_absolute_position(300, 0)
        new_menu.add.label("Title: " + contract.title)
        new_menu.add.label("Offered by: " + contract.contractor.name + " The " + contract.contractor.profession)
        new_menu.add.label("Needed: ")
        for need in contract.needed:
            new_menu.add.label(str(need[1]) + " " + need[0])
        new_menu.add.label("Reward: ")

        for reward in contract.reward:
            new_menu.add.label(str(reward[1]) + " " + reward[0])

        new_menu.add.label(contract.description, wordwrap=True)
        new_menu.add.button("Accept", add_contract_to_player, contract)
        new_menu.draw(game_surface)
        pygame.display.flip()

    def contracts():

        looking_at_contracts = True
        def back_out(button):
            #break
            #button.set_onreturn(False)
            pass

        contract_title, contract_offered_by, reward1, reward_amt1, description = "", "", "", 0, ""
        display_pack = [contract_title, contract_offered_by, reward1, reward_amt1, description]

        contract_menu = pygame_menu.Menu("Contracts", 300, game_surface.get_height(), theme=menu_theme)
        contract_menu.set_absolute_position(0, 0)

        for contract in contract_list:
            contract_menu.add.button(contract.title, display_details, contract)
        contract_menu.add.button("Back", back_out, button_id="back")


        while looking_at_contracts: # CREATING THE CONTRACT DISPLAY SCREEN
            clock.tick(60)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    looking_at_contracts = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass
            #if contract_menu.get_widget("back").apply() == False:
            #    looking_at_contracts = False
            contract_menu.draw(game_surface)
            contract_menu.update(events)

            pygame.display.flip()




    global currently_townin
    currently_townin = True
    def break_out():
        global currently_townin
        currently_townin = False
    town_menu = pygame_menu.Menu('Startsville', game_surface.get_width(), 300,
                            theme=menu_theme)
    town_menu.set_absolute_position(0, game_surface.get_height()-300)
    current_contracts = contract_list
    town_menu.add.button("Browse Contracts", contracts)
    town_menu.add.button("Back to Map", break_out)




    while currently_townin:
         clock.tick(60)
         events = pygame.event.get()
         for event in events:
             if event.type == pygame.QUIT:
                 currently_townin = False

         game_surface.fill((0, 0, 0))
         game_surface.blit(startsville, (0, 0))
         town_menu.draw(game_surface)
         town_menu.update(events)
         pygame.display.flip()

def contract_set(contract_list): #for now returns contract list, in future will determine who needs what and what they can offer.
    return contract_list

def hit_the_road():
    pass

def junkin(game_surface, scenario, player):
    currently_junkin = False
    choosing_junk_loc = True
    scen_menu = scenario.menu
    junk_map = JunkinMap(player, game_surface)
   # for buttons in scenario.menu_buttons:

    while choosing_junk_loc:
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                choosing_junk_loc = False
        junk_map.map.draw(game_surface)
        junk_map.map.update(events)
        pygame.display.flip()

    while currently_junkin:
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                currently_junkin = False
        game_surface.fill((0, 0, 0))
        game_surface.blit(wasteland, (0, 0))
        scen_menu.draw(game_surface)
        scen_menu.update(events)
        pygame.display.flip()


def scenario_set(scenario_list):
    scen_numbers = 1
    scen_list = scenario_list

    first_check = random.randint(0, 0)

    next_scen = scen_list[first_check]

    return next_scen


def setup_scenarios(player, surface): #Creates a complete scenario list for all possible scenarios
    scen_list = junker.create_Scenarios(player, surface)
    return scen_list

def look_at_contracts():
    for contract in contract_list:
        contract_menu.add.button(contract.title, display_details, contract)
    contract_menu.add.button("Back", back_out)

    while looking_at_contracts:  # CREATING THE CONTRACT DISPLAY SCREEN
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                looking_at_contracts = False
        contract_menu.draw(game_surface)
        contract_menu.update(events)
        pygame.display.flip()

def start_the_game(player_name,ranked_list):
    turn_start = True
    run_round = True
    turn_num = 1
    weather = "Sunny"
    global player
    player = Player()
    player.name = player_name
    game_surface = pygame.display.set_mode((screen_width, screen_height))
    scenario_list = setup_scenarios(player, game_surface)
    next_scen = scenario_set(scenario_list)

    contract_list = junker.create_Contracts()
    current_contracts = contract_set(contract_list)

    turn_list = TextBox(game_surface, 100, 100, 800, 80, fontSize=50,
                        borderColour=(0, 0, 0), textColour=(100, 99, 98))
    turn_list.text = 'Day %s                Weather: %s' % (str(turn_num), weather)


    while turn_start:
        clock.tick(60) / 1000.0
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                turn_start = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                turn_start = False

        turn_list.draw()
        pygame.display.update()

    start_manager = pygame_gui.UIManager((1300, 900))
    name1_rect = pygame.Rect(0, -40, screen_width-map_width-50, 300)
    name2_rect = pygame.Rect(0, name1_rect.y+20, screen_width-map_width-50, 300)
    name3_rect = pygame.Rect(0, name2_rect.y+20, screen_width-map_width-50, 300)
    name4_rect = pygame.Rect(0, name3_rect.y+20, screen_width-map_width-50, 300)

    rank_width, rank_height, action_height = screen_width-map_width, 300, 400
    #play_rect = pygame.Rect(0, -20, 100, 20)
    #quit_rect = pygame.Rect(0, 20, 100, 20)
    rank_rect = pygame.Rect(0, 0, rank_width, rank_height)
    action_rect = pygame.Rect(0, rank_rect.y+rank_height, rank_width, action_height)
    button_width = 200
    button_height = 50
    go_to_town_rect = pygame.Rect(0, -((action_height-240)/2), button_width, button_height)
    junkin_rect = pygame.Rect(0,go_to_town_rect.y+80, button_width, button_height)
    hit_the_road_rect = pygame.Rect(0,junkin_rect.y+80, button_width, button_height)
    ranking_list_window = pygame_gui.elements.UIWindow(rank_rect, manager=start_manager, window_display_title="Ranking List")
    name1 = pygame_gui.elements.UILabel(name1_rect, ranked_list[0], manager=start_manager, container=ranking_list_window,
                                        anchors={'center': 'center'})
    name2 = pygame_gui.elements.UILabel(name2_rect, ranked_list[1], manager=start_manager, container=ranking_list_window,
                                        anchors={'center': 'center'})
    name3 = pygame_gui.elements.UILabel(name3_rect, ranked_list[2], manager=start_manager, container=ranking_list_window,
                                        anchors={'center': 'center'})
    name4 = pygame_gui.elements.UILabel(name4_rect, ranked_list[3], manager=start_manager, container=ranking_list_window,
                                        anchors={'center': 'center'})
    #ranking_list = pygame_gui.elements.UILabel(rank_rect, ranked_names, manager=start_manager, container=ranking_list_window,
    #                                           anchors={'center': 'center'}, object_id='#ranking_list')

    action_list_window = pygame_gui.elements.UIWindow(action_rect, manager=start_manager, window_display_title="Action List")
    go_to_town_button = pygame_gui.elements.UIButton(relative_rect=go_to_town_rect, text="Go To Town",
                                               manager=start_manager, container=action_list_window,
                                               anchors={'center': 'center'}, object_id='#go_to_town_button')
    junkin_button = pygame_gui.elements.UIButton(relative_rect=junkin_rect, text="Get Junkin'",
                                               manager=start_manager, container=action_list_window,
                                               anchors={'center': 'center'}, object_id='#junkin_button')
    hit_the_road_button = pygame_gui.elements.UIButton(relative_rect=hit_the_road_rect, text="Hit The Road",
                                               manager=start_manager, container=action_list_window,
                                               anchors={'center': 'center'}, object_id='#hit_the_road_button')

    start_menu = True
    while start_menu:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_menu = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == go_to_town_button:
                    go_to_town(game_surface, contract_list)
                if event.ui_element == junkin_button:
                    junkin(game_surface, next_scen, player)
                if event.ui_element == hit_the_road_button:
                    hit_the_road()
            start_manager.process_events(event)

        start_manager.update(time_delta)
        game_surface.fill((0, 0, 0))
        game_surface.blit(wasteland, (game_surface.get_width()-wasteland.get_width(), 0))

        start_manager.draw_ui(game_surface)

        pygame.display.update()

    '''
    play_button = pygame_gui.elements.UIButton(relative_rect=play_rect, text="Play",
                                               manager=manager, container=menu_window,
                                               anchors={'center': 'center'}, object_id='#play_button')
    quit_button = pygame_gui.elements.UIButton(relative_rect=quit_rect, text="Quit",
                                               manager=manager, container=menu_window,
                                               anchors={'center': 'center'}, object_id='quit_button')
    '''
    '''
    ranking_list = pygame_menu.Menu('Junker Legacy', screen_width-map_width, 300,
                                theme=menu_theme)
    ranking_list.set_absolute_position(0, 0)
    ranked_names = 'TC Tyler\n' \
                   'Scrappy\n'\
                   '%s\n' \
                   'Tommy Tanks\n' % player_name
    ranking_list.add.label("Rankings", max_char=-1, font_size=30)
    ranking_list.add.label(ranked_names, max_char=-1, font_size=20)
    '''

    '''
    actions_list = pygame_menu.Menu("Actions", ranking_list.get_width(), map_height-ranking_list.get_height(), theme=menu_theme)
    actions_list.set_absolute_position(0, ranking_list.get_height())
    actions_list.add.button("Go to Town", go_to_town, game_surface, current_contracts)
    actions_list.add.button("Hit the road", hit_the_road, game_surface)
    actions_list.add.button("Get Junkin' & end turn", junkin, game_surface, next_scen, player)

    player_summary = pygame_menu.Menu(player_name, game_surface.get_width(), game_surface.get_height()-main_map.get_height(), columns=3, rows=2)
    #player_summary.add.button("Inventory", look_at_inventory)
    #player_summary.add.button("Contracts", look_at_contracts)
    #player_summary.add.button("Workers", look_at_workers)
    #.add.frame_h(game_surface.get_width()/2,player_summary.get_height()-20)





    #card_test = junker.Card("Go to Town", "Perform 1 action in the town you're in",card_width, card_height, game_surface.get_width()-map_width,0)

    while run_round:
        junkin_options = []
        time_delta = clock.tick(60)/1000.0
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run_round = False
        game_surface.fill((0, 0, 0))
        game_surface.blit(main_map, (game_surface.get_width()-map_width, 0))
        ranking_list.update(events)
        ranking_list.draw(game_surface)
        actions_list.update(events)
        actions_list.draw(game_surface)
        #card_test.draw(game_surface)
        pygame.display.update()

    pass
'''


main_menu()

#while run:
#    menu.mainloop(surface)

#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            run = False


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
