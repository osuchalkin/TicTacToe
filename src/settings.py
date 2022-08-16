import pygame


class Settings:
    """класс для хранения всех настроек игры"""

    def __init__(self):
        """Инициализирует статические настройки игры"""
        # параметры сетки, кол-во колонок и строк
        self.row = 3
        self.column = 3
        # ширина и высота одной клетки в сетке
        self.width = 100
        self.height = 100
        # граница между ячейками
        self.margin = 5

        # параметры экрана
        self.screen_width = (self.width + self.margin) * self.column + self.margin
        self.screen_height = (self.height + self.margin) * self.row + self.margin
        # цвета
        self.bg_color = (0, 0, 0)
        self.cell_color = (0, 106, 78)
        self.cross_color = (0, 0, 255)
        self.nil_color = (255, 174, 66)
        self.win_color = (250, 235, 215)

        self.caption = "Tic Tac Toe 2.0"
        self.icon = pygame.image.load("tic-tac-toe.png")
