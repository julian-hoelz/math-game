import pygame
import json

from datetime import datetime

from basic_classes import Color


# -----------

def load_bad_words() -> list[str]:
    with open('bad_words.txt') as file:
        return file.read().split('\n')


def load_translations() -> dict[str, dict[str, str]]:
    with open('translations.json', encoding='UTF-8') as file:
        return json.load(file)


# ----------

def show_hook(screen: pygame.Surface, screen_width: int) -> None:
    points = [(92, 0), (120, 20), (50, 120), (0, 70), (30, 45), (50, 70)]
    show_feedback_symbol(screen, points, Color.SPRING_GREEN, screen_width)


def show_cross(screen: pygame.Surface, screen_width: int) -> None:
    points = [(25, 0), (60, 35), (95, 0), (120, 25), (85, 60), (120, 95), (95, 120), (60, 85), (25, 120), (0, 95), (35, 60), (0, 25)]
    show_feedback_symbol(screen, points, Color.BRIGHT_RED, screen_width)


def show_small_hook(screen: pygame.Surface, x: float) -> None:
    points = [(23, 0), (30, 5), (12.5, 30), (0, 17.5), (7.5, 11.25), (12.5, 17.5)]
    show_small_feedback_symbol(screen, points, x, Color.SPRING_GREEN)
    

def show_small_cross(screen: pygame.Surface, x: float) -> None:
    points = [(6.25, 0), (15, 8.75), (23.75, 0), (30, 6.25), (21.25, 15), (30, 23.75), (23.75, 30), (15, 21.25), (6.25, 30),
              (0, 23.75), (8.75, 15), (0, 6.25)]
    show_small_feedback_symbol(screen, points, x, Color.BRIGHT_RED)


def show_feedback_symbol(screen: pygame.Surface, points: list[tuple[float, float]], color: tuple[int, int, int], screen_width: int) -> None:
    make_points_relative(points, screen_width / 2 - 60, 440)
    pygame.draw.polygon(screen, color, points)
    

def show_small_feedback_symbol(screen: pygame.Surface, points: list[tuple[float, float]], x: float, color: tuple[int, int, int]) -> None:
    make_points_relative(points, x, 25)
    pygame.draw.polygon(screen, color, points)
    

def make_points_relative(points: list[tuple[float, float]], relative_x: float, relative_y: float) -> list[tuple[float, float]]:
    for (i, (x, y)) in enumerate(points):
        points[i] = (x + relative_x, y + relative_y)
    return points


# Funktionen für Farben:

def brighter(color: tuple[int, int, int]) -> tuple[int, int, int]:
    return __scale_color(color, 1.25)


def darker(color: tuple[int, int, int]) -> tuple[int, int, int]:
    return __scale_color(color, 0.75)


def __scale_color(color: tuple[int, int, int], factor: float) -> tuple[int, int, int]:
    (red, green, blue) = color
    scaled_red = min(255, round(red * factor))
    scaled_green = min(255, round(green * factor))
    scaled_blue = min(255, round(blue * factor))
    return (scaled_red, scaled_green, scaled_blue)

# ----------

def mouse_on_rect(rect: tuple[float, float, float, float]) -> bool:
    (x, y, width, height) = rect
    (mouse_x, mouse_y) = pygame.mouse.get_pos()
    if mouse_x < x:
        return False
    if mouse_x >= x + width:
        return False
    if mouse_y < y:
        return False
    if mouse_y >= y + height:
        return False
    return True

# -----------

def date_and_time(timestamp: int, language: str) -> str:
    language_to_date_and_time_function = {
        'en': date_and_time_en,
        'de': date_and_time_de,
        'eo': date_and_time_eo
    }
    dt = datetime.fromtimestamp(timestamp)
    return language_to_date_and_time_function[language](dt)


def date_and_time_en(dt: datetime) -> str:
    date_str = dt.strftime('%m/%d/%Y')
    hour = dt.hour
    am_or_pm = 'a.m.' if hour < 12 else 'p.m.'
    if hour > 12:
        hour -= 12
    time_str = '%02d:%02d %s' % (hour, dt.minute, am_or_pm)
    return '%s, %s' % (date_str, time_str)


def date_and_time_de(dt: datetime) -> str:
    return dt.strftime('%d.%m.%Y, %H:%M Uhr')


def date_and_time_eo(dt: datetime) -> str:
    return dt.strftime('%d.%m.%Y, %H:%M')


# -----------

def ordinary_number(num: int, language: str) -> str:
    language_to_ordinary_number_function = {
        'en': ordinary_number_en,
        'de': ordinary_number_de,
        'eo': ordinary_number_eo
    }
    return language_to_ordinary_number_function[language](num)


def ordinary_number_en(num: int) -> str:
    ordinal_suffixes = ('st', 'nd', 'rd', 'th')
    return f'{num}{ordinal_suffixes[min(3, num - 1)]}'


def ordinary_number_de(num: int) -> str:
    return str(num)


def ordinary_number_eo(num: int) -> str:
    return f'{num}a'