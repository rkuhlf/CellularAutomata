import pygame
import sys
from cell import Cell
from button import Button
from ruleCard import RuleCard
import pickle
import copy
import wrapText

# Button to increase and decrease the cell_size
# you can make a cell locked as activated or inactivated
# inspired by conway's game of life and cellular automata
# Write explanation

pygame.init()
pygame.font.init()
running = False
scene = "home"

cell_size = 50
frameRate = 60

# size = width, height = 1300, 800
# screen = pygame.display.set_mode(size)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
size = width, height = pygame.display.Info().current_w, pygame.display.Info().current_h

rules = []
try:
    with open('rules.pickle', 'rb') as fp:
        rules = pickle.load(fp)

    if len(rules) == 0:
        rules = [
            [2, 2, 2],
            [1, 0, 1],
            [2, 2, 2]
        ]
except IOError:
    rules = [
        [
            [2, 2, 2],
            [1, 0, 1],
            [2, 2, 2]
        ]
    ]

currentRuleIndex = 0

currentRuleCard = RuleCard(screen, rules[0])


def incRule():
    global currentRuleIndex
    global currentRuleCard
    currentRuleIndex += 1
    currentRuleIndex = currentRuleIndex % len(rules)
    # set new RuleCard
    currentRuleCard = RuleCard(screen, rules[currentRuleIndex])


def decRule():
    global currentRuleIndex
    global currentRuleCard
    currentRuleIndex -= 1
    currentRuleIndex = (currentRuleIndex + len(rules)) % len(rules)
    currentRuleCard = RuleCard(screen, rules[currentRuleIndex])


def addRule():
    global currentRuleIndex
    global currentRuleCard
    rules.append([
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ])
    currentRuleIndex = len(rules) - 1
    currentRuleCard = RuleCard(screen, rules[currentRuleIndex])
    save_rules()


def duplicateRule():
    global currentRuleIndex
    global currentRuleCard
    currentRule = copy.deepcopy(rules[currentRuleIndex])

    rules.append(currentRule)
    currentRuleIndex = len(rules) - 1
    currentRuleCard = RuleCard(screen, rules[currentRuleIndex])
    save_rules()


def deleteRule():
    if len(rules) == 1:
        return
    del rules[currentRuleIndex]
    decRule()
    save_rules()


def resetRules():
    rules = [
        [2, 2, 2],
        [2, 1, 2],
        [2, 2, 2]
    ]

    currentRuleIndex = 0
    save_rules()


def edit_rules(x, y, click_type):
    if click_type == 0:
        if rules[currentRuleIndex][y][x] == 0:
            rules[currentRuleIndex][y][x] = 1
        elif rules[currentRuleIndex][y][x] == 1:
            rules[currentRuleIndex][y][x] = 0
    elif click_type == 1:
        if rules[currentRuleIndex][y][x] == 2:
            rules[currentRuleIndex][y][x] = 0
        elif rules[currentRuleIndex][y][x] != 2:
            rules[currentRuleIndex][y][x] = 2
    save_rules()


def save_rules():
    with open('rules.pickle', 'wb') as fp:
        pickle.dump(rules, fp)


def get_index(x, y):
    cols = width // cell_size
    rows = height // cell_size
    return y * cols + x


cells = []

for y in range(0, height - cell_size + 1, cell_size):
    for x in range(0, width - cell_size + 1, cell_size):
        cells.append(Cell(screen, x, y, cell_size, cell_size))


def clear_cells():
    for cell in cells:
        cell.activated = False


buttons = []

font = pygame.font.SysFont("Arial", 32)
big_font = pygame.font.SysFont("Arial", 64)


def change_scene(new_scene):
    global scene
    scene = new_scene


play_button = Button(screen, font, width / 2, height / 2, 200, 50, "Play", on_click=lambda: change_scene("game"))
rules_button = Button(screen, font, width / 2, height / 2 + 100, 200, 50, "Edit Rules",
                      on_click=lambda: change_scene("rules"))
explanation_button = Button(screen, font, width / 2, height / 2 + 200, 200, 50, "Explanation",
                            on_click=lambda: change_scene("explanation"))
buttons.extend([play_button, rules_button, explanation_button])

rule_buttons = []

back_button = Button(screen, font, 60, 40, 100, 50, "Back", on_click=lambda: change_scene("home"))
previous_button = Button(screen, font, width * 0.15, height / 2, 150, 50, "Previous", on_click=lambda: decRule())
next_button = Button(screen, font, width * 0.85, height / 2, 150, 50, "Next", on_click=lambda: incRule())
reset_button = Button(screen, font, width * 0.9, height / 2 + 200, 100, 50, "Reset", on_click=lambda: resetRules())
delete_button = Button(screen, font, 180, height * 0.9, 100, 50, "Delete", on_click=lambda: deleteRule())
add_button = Button(screen, font, 60, height * 0.9, 100, 50, "Add", on_click=lambda: addRule())
duplicate_button = Button(screen, font, width / 2, height * 0.9, 170, 50, "Duplicate", on_click=lambda: duplicateRule())
rule_buttons.extend(
    [back_button, previous_button, next_button, reset_button, delete_button, add_button, duplicate_button])


def get_cell_value(index):
    if (index < 0 or index >= len(cells)):
        return -1
    else:
        return 1 if cells[index].activated else 0


def simulate():
    # pass each cell its neighbors
    # figure out how to calculate index based on x and y (and cell size)
    for cell in cells:
        cell_x = cell.x // cell_size
        cell_y = cell.y // cell_size
        data = []

        for y in range(-1, 2):  # returns (-1, 0, 1)
            data_row = []
            for x in range(-1, 2):
                new_index = get_index(cell_x + x, cell_y + y)
                data_row.append(get_cell_value(new_index))

            data.append(data_row)

        cell.get_next_phase(rules, data)

    for cell in cells:
        cell.trigger_next_phase()


frame = 0
while 1:
    if scene == "game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                if event.key == pygame.K_RETURN:
                    simulate()
                if event.key == pygame.K_BACKSPACE:
                    clear_cells()
                if event.key == pygame.K_LEFT:
                    change_scene("home")
                if event.key == pygame.K_DOWN:
                    frameRate += 1
                if event.key == pygame.K_UP:
                    frameRate -= 1
                    frameRate = max(1, frameRate)
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                for cell in cells:
                    cell.handle_click(pos)

        screen.fill(pygame.Color(255, 255, 255))

        if running:
            frame += 1
            if frame == frameRate:
                frame = 0
                simulate()

        for cell in cells:
            cell.render()

        for x in range(0, width, cell_size):
            pygame.draw.line(screen, pygame.Color(0, 0, 0), (x, 0), (x, height), 2)

        for y in range(0, height, cell_size):
            pygame.draw.line(screen, pygame.Color(0, 0, 0), (0, y), (width, y), 2)

    elif scene == "home":
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    button.handle_click(pos)

        screen.fill(pygame.Color(255, 255, 255))
        text = big_font.render("Automata", True, pygame.Color(0, 0, 0))

        textRect = text.get_rect()

        textRect.center = (width / 2, height * 0.25)
        screen.blit(text, textRect)

        for button in buttons:
            button.render()

    elif scene == "rules":
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for rule_button in rule_buttons:
                    rule_button.handle_click(pos)
                if event.button == 1:
                    currentRuleCard.handle_click(pos, edit_rules, 0)
                elif event.button == 3:
                    currentRuleCard.handle_click(pos, edit_rules, 1)

        screen.fill(pygame.Color(255, 255, 255))
        text = big_font.render("Rules", True, pygame.Color(0, 0, 0))

        textRect = text.get_rect()

        textRect.center = (width / 2, height * 0.10)
        screen.blit(text, textRect)

        currentRuleCard.render()

        for rule_button in rule_buttons:
            rule_button.render()

    elif scene == "explanation":
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                back_button.handle_click(pos)

        screen.fill(pygame.Color(255, 255, 255))
        text = big_font.render("Explanation", True, pygame.Color(0, 0, 0))

        textRect = text.get_rect()

        textRect.center = (width / 2, height * 0.10)
        screen.blit(text, textRect)

        # main text
        # text render "settings"
        text_width = width * 0.7
        line_height = 40
        text_top = height * 0.2

        line_number = 0

        explanationText = "This is a customizeable cellular automata simulator that allows you to create your own " \
                          "rules to 'simulate' life. You can head back to the main menu and make some custom rules by " \
                          "clicking to toggle the cells from black to white and right clicking to toggle grey. The " \
                          "program loops through all of the cells and sees if the three by three at a certain cell " \
                          "matches any of the rules. If it does, that cell will become alive next round. Also note " \
                          "that grey cells are not considered. For example, if one of the rules has grey on every " \
                          "tile except the middle, and the middle is black, all cells that were black the previous " \
                          "round will remain black the next round. During the simulation, you can press the enter key " \
                          "to simulate a round, press the spacebar to toggle the automatic simulation of rounds, " \
                          "and press backspace to clear the screen. Press the left arrow key to return to the main " \
                          "screen. "

        text_portions = wrapText.wrap_line(explanationText, font, text_width)

        for text in text_portions:
            rendered_text = font.render(text, True, pygame.Color(0, 0, 0))

            text_rect = rendered_text.get_rect()

            text_rect.center = (width / 2, text_top + line_height * line_number)
            screen.blit(rendered_text, text_rect)
            line_number += 1

        back_button.render()

    pygame.display.update()
