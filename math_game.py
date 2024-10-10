from __future__ import annotations

import json
import locale
import pygame
import time

from typing import Callable, override


# Eigene Imports:
from basic_classes import *
from help_functions import *
from problems import *


class Button:

    def __init__(self, x: float, y: float, width: int, height: int, bg_color: tuple[int, int, int],
                 on_action: Callable[[], None]) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # self.rect = (x, y, width, height)
        self.bg_color = bg_color
        self.on_action = on_action
        self.hovered = False
        self.pressed = False
        self.active = True


    def render(self, screen: pygame.Surface, y_offset: float = 0) -> None:
        if self.pressed:
            bg_color = brighter(self.bg_color)
        elif self.hovered:
            bg_color = darker(self.bg_color)
        else:
            bg_color = self.bg_color
        # die Schaltfläche rendern:
        pygame.draw.rect(screen, bg_color, (self.x, self.y + y_offset, self.width, self.height), border_radius=10)


    def check_hovered(self, y_offset: float) -> None:
        if self.active:
            self.hovered = mouse_on_rect((self.x, self.y + y_offset, self.width, self.height))


    def deactivate(self) -> None:
        self.active = False
        self.hovered = False
        self.pressed = False


class TextButton(Button):

    def __init__(self, text: str, x: float, y: float, width: int, bg_color: tuple[int, int, int],
                 on_action: Callable[[], None]) -> None:
        super().__init__(x, y, width, TEXT_BUTTON_HEIGHT, bg_color, on_action)
        self.text = text


    def render(self, screen: pygame.Surface, y_offset: int = 0) -> None:
        super().render(screen, y_offset)
        pygame.draw.rect(screen, Color.WHITE, (self.x, self.y + y_offset, self.width, self.height), width=3, border_radius=10)
        render_text(screen, self.text, BUTTON_FONT, self.x + self.width / 2, self.y + 16 + y_offset, TextAlign.CENTER)


class MenuButton(TextButton):

    def __init__(self, text: str, y: float, bg_color: tuple[int, int, int], on_action: Callable[[], None]) -> None:
        super().__init__(text, (WIDTH - MENU_BUTTON_WIDTH) / 2, y, MENU_BUTTON_WIDTH, bg_color, on_action)


class OptionButton(TextButton):

    def __init__(self, option: int, x: float, bg_color: tuple[int, int, int],
                 on_action: Callable[[], None]) -> None:
        super().__init__(str(option), x, 320, OPTION_BUTTON_WIDTH, bg_color, on_action)
        self.option = option
        self.feedback_border_color: tuple[int, int, int] | None = None


    def render(self, screen: pygame.Surface, y_offset: int = 0) -> None:
        if self.feedback_border_color is not None:
            pygame.draw.rect(screen, self.feedback_border_color, (self.x - 10, self.y + y_offset - 10, self.width + 20, self.height + 20),
                             border_radius=10)
        super().render(screen, y_offset)


class ButtonContainer:

    def __init__(self, buttons: tuple[Button, ...]) -> None:
        self.buttons = buttons
        self.buttons_y_offset: float = 0


    def render(self, screen: pygame.Surface) -> None:
        for b in self.buttons:
            b.render(screen, self.buttons_y_offset)


    def check_buttons_hovered(self) -> None:
        for b in self.buttons:
            b.check_hovered(self.buttons_y_offset)


    def check_button_pressed(self) -> None:
        for b in self.buttons:
            b.pressed = b.hovered
            if b.pressed:
                return


    def check_button_released(self) -> None:
        for b in self.buttons:
            if b.pressed:
                b.pressed = False
                if b.hovered:
                    b.on_action()
                return


class Keyboard(ButtonContainer):

    def __init__(self) -> None:
        super().__init__(Keyboard.make_buttons())


    def render(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, Color.LIGHT_GRAY, KEYBOARD_RECT)
        super().render(screen)


    # def set_language(self, language: str) -> None:
    #     if language == 'de':
    #         self.buttons[5].text = 'Z'
    #         self.buttons[19].text = 'Y'
    #     else:
    #         self.buttons[5].text = 'Y'
    #         self.buttons[19].text = 'Z'


    @staticmethod
    def make_buttons() -> tuple[TextButton, ...]:
        top_row = Keyboard.make_button_row('QWERTYUIOP', 0, 0)
        middle_row = Keyboard.make_button_row('ASDFGHJKL', 20, 80)
        bottom_row = Keyboard.make_button_row('ZXCVBNM', 40, 160)
        delete_button = TextButton('>delete', KEYBOARD_X + 625, KEYBOARD_Y + 175, 180, Color.GRAY, delete_char_in_initials_input)
        return top_row + middle_row + bottom_row + (delete_button,)


    @staticmethod
    def make_button_row(chars: str, start_x: float, y: float) -> tuple[TextButton, ...]:
        start_x += KEYBOARD_X + 15
        y += KEYBOARD_Y + 15
        return tuple(TextButton(c, start_x + i * 80, y, 70, Color.GRAY, lambda c=c: type_into_initals_input(c))
                     for (i, c) in enumerate(chars))


class ProblemDisplay(ButtonContainer):

    def __init__(self, problem: Problem) -> None:
        self.term = problem.term
        option_button_1 = ProblemDisplay.make_button(problem.options[0], WIDTH / 2 - OPTION_BUTTON_WIDTH * 1.7, Color.BLUE)
        option_button_2 = ProblemDisplay.make_button(problem.options[1], WIDTH / 2 - OPTION_BUTTON_WIDTH * 0.5, Color.YELLOW)
        option_button_3 = ProblemDisplay.make_button(problem.options[2], WIDTH / 2 + OPTION_BUTTON_WIDTH * 0.7, Color.RED)
        cancel_game_button = Button(WIDTH - 45, HEIGHT - 45, 30, 30, Color.RED, lambda: open_menu(GAME_CANCELED_MENU))
        self.option_buttons = (option_button_1, option_button_2, option_button_3)
        super().__init__(self.option_buttons + (cancel_game_button,))


    def render(self, screen: pygame.Surface) -> None:
        screen.fill(Color.DARK_GRAY)
        render_text(screen, self.term, TITLE_FONT, WIDTH / 2, 180, TextAlign.CENTER)
        super().render(screen)


    @staticmethod
    def make_button(option: int, x: float, bg_color: tuple[int, int, int]) -> OptionButton:
        return OptionButton(option, x, bg_color, on_action=lambda: log_in_answer(option))


class Menu(ButtonContainer):

    def __init__(self, title: str, render_content_func: Callable[[pygame.Surface], None] | None,
                 button_data: tuple[ButtonData, ...]) -> None:
        self.title = title
        self.init_buttons(button_data)
        self.render_content_func = render_content_func


    def render(self, screen: pygame.Surface) -> None:
        screen.fill(Color.DARK_GRAY)
        render_text(screen, self.title, TITLE_FONT, WIDTH / 2, 80, TextAlign.CENTER)
        super().render(screen)


    def init_buttons(self, button_data: tuple[ButtonData, ...]) -> None:
        buttons = tuple(MenuButton(d.text, i * 90 + 230, d.bg_color, d.on_action) for (i, d) in enumerate(button_data))
        super().__init__(buttons)


class ResultMenu(Menu):

    @override
    def check_buttons_hovered(self) -> None:
        super().check_buttons_hovered()
        if is_place_on_leaderboard:
            KEYBOARD.check_buttons_hovered()


    @override
    def check_button_pressed(self) -> None:
        super().check_button_pressed()
        if is_place_on_leaderboard:
            KEYBOARD.check_button_pressed()


    @override
    def check_button_released(self) -> None:
        super().check_button_released()
        if is_place_on_leaderboard:
            KEYBOARD.check_button_released()


TRANSLATIONS: dict[str, dict[str, str]]  # die Übersetzungen aus der Datei translations.json
BAD_WORDS: list[str]  # die Liste der bösen Wörter aus drei Buchstaben, die man nicht als Namenskürzel verwenden kann

WIDTH: int  # die Breite der Anzeige (wird in init_constants() gesetzt)
HEIGHT: int  # die Höhe der Anzeige (wird in init_constants() gesetzt)

TEXT_BUTTON_HEIGHT = 70
MENU_BUTTON_WIDTH = 350
OPTION_BUTTON_WIDTH = 180
KEYBOARD_WIDTH = 820  # die Breite der Bildschirmtastatur
KEYBOARD_HEIGHT = 260  # die Höhe der Bildschirmtastatur
KEYBOARD_X: float
KEYBOARD_Y: float
KEYBOARD_RECT: tuple[float, float, float, float]

FPS = 100  # die Bildfrequenz
FEEDBACK_SYMBOL_SHOWING_TIME = int(FPS * 1.2)  # wie lange ein Feedback-Symbol (Haken oder Kreuz) angezeigt wird

N_PROBLEMS_FOR_OPERATOR = (3, 3, 2, 2)
N_PROBLEMS = sum(N_PROBLEMS_FOR_OPERATOR)

TITLE_FONT: pygame.font.Font
TEXT_FONT: pygame.font.Font
BUTTON_FONT: pygame.font.Font
TABLE_FONT: pygame.font.Font
INPUT_FONT: pygame.font.Font

MAIN_MENU: Menu
RESULT_MENU: Menu
LEADERBOARD_MENU: Menu
GAME_CANCELED_MENU: Menu
SETTINGS_MENU: Menu
LANGUAGE_MENU: Menu
CREDITS_MENU: Menu
KEYBOARD: Keyboard


running = True  # so lange wahr, solange das Spiel läuft
language: str
opened_menu: Menu | None
high_scores: list[Score]
input_initials: str

# Variablen, die für jeden Durchlauf benötigt werden:
problems: tuple[Problem]  # die in einem Durchlauf zu lösenden Probleme
problem_index: int  # der Index des aktuellen Problems
problem_display: ProblemDisplay | None  # die Anzeige des aktuellen Problems
correct_answers: list[bool]
is_correct_answer: bool
n_correct: int
game_ticks: int
solving_time: float
score: float
place: int
is_place_on_leaderboard: bool
timestamp: int
feedback_symbol_showing_ticks: int


# Die main()-Funktion:
def main() -> None:    
    pygame.init()  # Pygame initialisieren
    pygame.font.init()  # das Rendern von Schrift in Pygame initialisieren

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # das Fenster im Vollbildmodus anlegen
    init(screen)  # dieses Spiel initialisieren

    open_menu(MAIN_MENU)  # das Hauptmenü öffnen

    clock = pygame.time.Clock()  # Mit dieser Uhr kann die Bildfrequenz geregelt werden

    # Spielloop:
    while running:
        # Event-Handling:
        for event in pygame.event.get():
            match event.type:
                case pygame.MOUSEMOTION:  # bei einem Mausbewegungsevent
                    handle_mouse_motion_event()
                case pygame.MOUSEBUTTONDOWN:  # bei einem Mausdruckevent
                    handle_mouse_button_down_event(event)
                case pygame.MOUSEBUTTONUP:  # bei einem Maustaste-loslass-Event
                    handle_mouse_button_up_event(event)
                case pygame.QUIT:  # bei einem Spiel-beendet-Event
                    quit_game()

        update()  # die Funktion update() aktualisiert den Spielzustand
        render(screen)  # die Funktion render() rendert alles, was angezeigt werden soll
        pygame.display.flip()  # das neu gerenderte Bild im Fenster anzeigen

        clock.tick(FPS)  # das Programm so lange zur Ruhe legen, dass 60 Bilder pro Sekunde erreicht werden

    # Nach der Spielschleife:
    if opened_menu is RESULT_MENU:  # falls das Ergebnismenü geöffnet ist
        add_score_to_high_scores()  # die Punktzahl zu den Highscores hinzufügen, falls sie ein Highscore ist
    save_data()  # die Sprache und die Highscores in der Datei data.json speichern
    pygame.font.quit()  # das Rendern von Schrift in Pygame beenden
    pygame.mixer.quit()  # den Soundmixer von Pygame beenden
    pygame.quit()  # das Spiel sauber beenden


# Initialisierungsfunktionen

def init(screen: pygame.Surface) -> None:
    global BAD_WORDS, TRANSLATIONS, KEYBOARD
    BAD_WORDS = load_bad_words()
    TRANSLATIONS = load_translations()
    init_constants(screen)
    init_fonts()
    init_menus()
    KEYBOARD = Keyboard()
    load_data()


def init_constants(screen: pygame.Surface) -> None:
    global WIDTH, HEIGHT, KEYBOARD_X, KEYBOARD_Y, KEYBOARD_RECT
    (WIDTH, HEIGHT) = screen.get_size()
    KEYBOARD_X = (WIDTH - KEYBOARD_WIDTH) / 2
    KEYBOARD_Y = HEIGHT - KEYBOARD_HEIGHT
    KEYBOARD_RECT = (KEYBOARD_X, KEYBOARD_Y, KEYBOARD_WIDTH, KEYBOARD_HEIGHT)


def init_fonts() -> None:
    global TITLE_FONT, TEXT_FONT, BUTTON_FONT, TABLE_FONT, INPUT_FONT
    TITLE_FONT = pygame.font.SysFont('Arial', 70, bold=True)
    TEXT_FONT = pygame.font.SysFont('Arial', 40, bold=True)
    BUTTON_FONT = pygame.font.SysFont('Arial', 35, bold=True)
    TABLE_FONT = pygame.font.SysFont('Arial', 35, bold=True)
    INPUT_FONT = pygame.font.SysFont('Arial', 85, bold=True)


def init_menus() -> None:
    global MAIN_MENU, RESULT_MENU, LEADERBOARD_MENU, GAME_CANCELED_MENU, SETTINGS_MENU, LANGUAGE_MENU, CREDITS_MENU
    MAIN_MENU = Menu(title='>title', render_content_func=None, button_data=(
        ButtonData(text='>newGame', bg_color=Color.GREEN, on_action=new_game),
        ButtonData(text='>leaderboard', bg_color=Color.TURQUOISE, on_action=open_leaderboard_menu),
        ButtonData(text='>settings', bg_color=Color.ORANGE, on_action=lambda: open_menu(SETTINGS_MENU)),
        ButtonData(text='>credits', bg_color=Color.BLUE, on_action=lambda: open_menu(CREDITS_MENU)),
        ButtonData(text='>quitGame', bg_color=Color.RED, on_action=quit_game)
    ))
    RESULT_MENU = ResultMenu(title='>result', render_content_func=show_result, button_data=(
        ButtonData(text='>newGame', bg_color=Color.GREEN, on_action=lambda: (add_score_to_high_scores(), new_game())),
        ButtonData(text='>toMainMenu', bg_color=Color.PURPLE, on_action=lambda: (add_score_to_high_scores(), open_menu(MAIN_MENU)))
    ))
    LEADERBOARD_MENU = Menu(title='>leaderboard', render_content_func=show_high_scores, button_data=(
        ButtonData(text='>back', bg_color=Color.PURPLE, on_action=lambda: open_menu(MAIN_MENU)),
    ))
    GAME_CANCELED_MENU = Menu(title='>gameCanceled', render_content_func=None, button_data=(
        ButtonData(text='>newGame', bg_color=Color.GREEN, on_action=new_game),
        ButtonData(text='>toMainMenu', bg_color=Color.PURPLE, on_action=lambda: open_menu(MAIN_MENU))
    ))
    SETTINGS_MENU = Menu(title='>settings', render_content_func=None, button_data=(
        ButtonData(text='>language', bg_color=Color.YELLOW, on_action=lambda: open_menu(LANGUAGE_MENU)),
        ButtonData(text='>back', bg_color=Color.PURPLE, on_action=lambda: open_menu(MAIN_MENU))
    ))
    LANGUAGE_MENU = Menu(title='>language', render_content_func=None, button_data=(
        ButtonData(text='English', bg_color=Color.BLUE, on_action=lambda: set_language('en')),
        ButtonData(text='Deutsch', bg_color=Color.RED, on_action=lambda: set_language('de')),
        ButtonData(text='Esperanto', bg_color=Color.GREEN, on_action=lambda: set_language('eo')),
        ButtonData(text='>back', bg_color=Color.PURPLE, on_action=lambda: open_menu(SETTINGS_MENU))
    ))
    CREDITS_MENU = Menu(title='>credits', render_content_func=show_credits, button_data=(
        ButtonData(text='>back', bg_color=Color.PURPLE, on_action=lambda: open_menu(MAIN_MENU)),
    ))
    CREDITS_MENU.buttons_y_offset = 130


# Aktualisierungsfunktionen

def update() -> None:
    global game_ticks, feedback_symbol_showing_ticks
    if opened_menu is None:
        if feedback_symbol_showing_ticks == -1:
            game_ticks += 1
        else:
            feedback_symbol_showing_ticks += 1
            if feedback_symbol_showing_ticks == FEEDBACK_SYMBOL_SHOWING_TIME:
                feedback_symbol_showing_ticks = -1
                show_next_problem()


# Rendering-Funktionen

def render(screen: pygame.Surface) -> None:
    if opened_menu is None:
        problem_display.render(screen)
        show_progress(screen)
        show_time(screen)
        if feedback_symbol_showing_ticks != -1:
            (show_hook if is_correct_answer else show_cross)(screen, WIDTH)
    else:
        opened_menu.render(screen)
        if opened_menu.render_content_func is not None:
            opened_menu.render_content_func(screen)


# Mausevent-Funktionen

def handle_mouse_motion_event() -> None:
    get_opened().check_buttons_hovered()


def handle_mouse_button_down_event(event: pygame.event.Event) -> None:
    if event.button == pygame.BUTTON_LEFT:
        get_opened().check_button_pressed()


def handle_mouse_button_up_event(event: pygame.event.Event) -> None:
    if event.button == pygame.BUTTON_LEFT:
        get_opened().check_button_released()


# Weitere Funktionen ohne Rückgaben

def new_game() -> None:
    global problems, problem_index, correct_answers, n_correct, game_ticks, is_correct_answer, feedback_symbol_showing_ticks
    open_menu(None)
    problems = random_problems(N_PROBLEMS_FOR_OPERATOR)
    problem_index = -1
    correct_answers = []
    n_correct = 0
    is_correct_answer = False
    game_ticks = 0
    feedback_symbol_showing_ticks = -1
    show_next_problem()


def show_next_problem() -> None:
    global problem_display, problem_index
    problem_index += 1
    if problem_index == N_PROBLEMS:
        open_result_menu()
    else:
        problem_display = ProblemDisplay(problems[problem_index])
        problem_display.check_buttons_hovered()


def open_menu(menu: Menu | None) -> None:
    global opened_menu
    opened_menu = menu
    if opened_menu is not None:
        opened_menu.check_buttons_hovered()


def open_leaderboard_menu() -> None:
    LEADERBOARD_MENU.buttons_y_offset = len(high_scores) * 50 + 20
    open_menu(LEADERBOARD_MENU)


def open_result_menu() -> None:
    global solving_time, score, place, is_place_on_leaderboard, timestamp, input_initials
    timestamp = int(time.time())
    solving_time = game_ticks / FPS
    n_incorrect = N_PROBLEMS - n_correct
    score = solving_time + n_incorrect * 5
    place = get_ranking()
    is_place_on_leaderboard = place != -1
    input_initials = ''
    RESULT_MENU.buttons_y_offset = 400 if is_place_on_leaderboard else 120
    open_menu(RESULT_MENU)


def set_language(lang: str) -> None:
    global language
    language = lang
    locale.setlocale(locale.LC_ALL, 'en_US' if lang == 'en' else 'de_DE')
    pygame.display.set_caption(get_translation('title'))
    # KEYBOARD.set_language(language)


def log_in_answer(answer: int) -> None:
    global n_correct, is_correct_answer, feedback_symbol_showing_ticks
    is_correct_answer = answer == problems[problem_index].solution
    correct_answers.append(is_correct_answer)
    if is_correct_answer:
        n_correct += 1
        get_option_button_with_value(answer).feedback_border_color = Color.SPRING_GREEN
    else:
        get_option_button_with_value(answer).feedback_border_color = Color.BRIGHT_RED
        get_option_button_with_value(problems[problem_index].solution).feedback_border_color = Color.SPRING_GREEN
    for b in problem_display.option_buttons:
        b.deactivate()
    feedback_symbol_showing_ticks = 0


def add_score_to_high_scores() -> None:
    global high_scores
    player_name = input_initials
    high_scores.append(Score(score, n_correct, solving_time, timestamp, player_name))
    high_scores.sort(key=lambda s: s.score)
    high_scores = high_scores[:10]


def show_progress(screen: pygame.Surface) -> None:
    # pygame.draw.line(screen, Color.BRIGHT_RED, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))
    for i in range(N_PROBLEMS):
        color = Color.LIGHT_GRAY if i == problem_index else Color.GRAY
        pygame.draw.circle(screen, color, (WIDTH / 2 + (0.5 - N_PROBLEMS / 2 + i) * 56, 40), 24)
    for (i, a) in enumerate(correct_answers):
        x = WIDTH / 2 + (i + 0.5 - N_PROBLEMS / 2) * 56 - 15
        (show_small_hook if a else show_small_cross)(screen, x)


def show_time(screen: pygame.Surface) -> None:
    render_text(screen, format_float(game_ticks / FPS, False), TITLE_FONT, WIDTH - 20, 24, TextAlign.RIGHT)


def show_result(screen: pygame.Surface) -> None:
    render_text(screen, f'{n_correct}/{N_PROBLEMS}', TEXT_FONT, WIDTH / 2, 200, TextAlign.CENTER)
    render_text(screen, format_float(solving_time, True), TEXT_FONT, WIDTH / 2, 255, TextAlign.CENTER)
    if is_place_on_leaderboard:
        render_text(screen, get_translation('placeOnLeaderboard', place + 1), TEXT_FONT, WIDTH / 2, 310, TextAlign.CENTER)
        render_text(screen, '>enterInitials', TEXT_FONT, WIDTH / 2, 400, TextAlign.CENTER)
        show_initials_input(screen)
        KEYBOARD.render(screen)


def show_initials_input(screen: pygame.Surface) -> None:
    cursor = len(input_initials)
    for i in range(3):
        color = Color.WHITE if i == cursor else Color.GRAY
        pygame.draw.rect(screen, color, (WIDTH / 2 - 210 + i * 145, 470, 130, 130), width=4, border_radius=13)
    if cursor < 3:
        pygame.draw.line(screen, Color.WHITE, (WIDTH / 2 - 190 + cursor * 145, 580), (WIDTH / 2 - 100 + cursor * 145, 580), width=4)
    for (i, c) in enumerate(input_initials):
        render_text(screen, c, INPUT_FONT, WIDTH / 2 + (i - 1) * 145, 490, TextAlign.CENTER)


def show_high_scores(screen: pygame.Surface) -> None:
    # pygame.draw.rect(screen, (255, 0, 0), (WIDTH / 2 - 450, 160, 900, 700), width=1)
    for (i, h) in enumerate(high_scores):
        y = i * 50 + 200
        if len(h.player_name) == 3 and h.player_name not in BAD_WORDS:
            player_name = h.player_name
        else:
            player_name = '–'
        render_text(screen, f'{i + 1}.', TABLE_FONT, WIDTH / 2 - 402, y, TextAlign.RIGHT)
        render_text(screen, f'{h.n_correct}/{N_PROBLEMS}', TABLE_FONT, WIDTH / 2 - 280, y, TextAlign.RIGHT)
        render_text(screen, format_float(h.time, True), TABLE_FONT, WIDTH / 2 - 70, y, TextAlign.RIGHT)
        render_text(screen, date_and_time(h.timestamp, language), TABLE_FONT, WIDTH / 2 - 30, y, TextAlign.LEFT)
        render_text(screen, player_name, TABLE_FONT, WIDTH / 2 + 363, y, TextAlign.LEFT)


def show_credits(screen: pygame.Surface) -> None:
    render_text(screen, '>developedByJH', TEXT_FONT, WIDTH / 2, 200, TextAlign.CENTER)
    render_text(screen, '(https://github.com/julian-hoelz)', TEXT_FONT, WIDTH / 2, 250, TextAlign.CENTER)


def type_into_initals_input(char: str) -> None:
    global input_initials
    if len(input_initials) < 3:
        input_initials += char


def delete_char_in_initials_input() -> None:
    global input_initials
    input_initials = input_initials[:-1]


def render_text(screen: pygame.Surface, text: str, font: pygame.font.Font, x: float, y: float, text_align: TextAlign) -> None:
    if text.startswith('>'):
        text = get_translation(text[1:])
    surface = font.render(text, True, Color.WHITE)
    if text_align is TextAlign.RIGHT:
        x -= surface.get_width()
    elif text_align is TextAlign.CENTER:
        x -= surface.get_width() / 2
    screen.blit(surface, (x, y))


def load_data() -> None:
    global high_scores
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        set_language('en')
        high_scores = []
        return
    set_language(data['language'])
    high_scores = [Score(h['score'], h['nCorrect'], h['time'], h['timestamp'], h['playerName']) for h in data['highScores']]


def save_data() -> None:
    data = {
        'language': language,
        'highScores': [h.to_dict() for h in high_scores]
    }
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)


def quit_game() -> None:
    global running
    running = False


def get_translation(key: str, ordnum: int = 0) -> str:
    return TRANSLATIONS[language][key].replace('*', ordinary_number(ordnum, language))


def get_ranking() -> int:
    for (i, h) in enumerate(high_scores):
        if score < h.score:
            return i
    if len(high_scores) < 10:
        return len(high_scores)
    return -1


def format_float(f: float, sec: bool) -> str:
    result = locale.format_string('%.2f', f)
    if sec:
        result += ' ' + get_translation('sec')
    return result


def get_opened() -> ButtonContainer:
    return problem_display if opened_menu is None else opened_menu


def get_option_button_with_value(value: int) -> OptionButton:
    for b in problem_display.option_buttons:
        if b.option == value:
            return b


# der Aufruf der main()-Funktion
if __name__ == '__main__':
    main()