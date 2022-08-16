import pygame


class Grid:
    """поле для игры"""

    def __init__(self, game):
        self.settings = game.settings
        self.screen = game.screen
        self.blanc = ''

        self.grid = []

    def reset_grid(self):
        """очистка поля"""
        for row in range(self.settings.row):
            self.grid.append([])
            for column in range(self.settings.column):
                self.grid[row].append(self.blanc)

        # 2 вариант создать двумерный массив 10x10 и заполнить "0"
        # self.grid = [[0 for x in range(10)] for y in range(10)]

    def update_grid(self):
        """обновление поля"""
        for column in range(self.settings.column):
            for row in range(self.settings.row):
                x = (self.settings.margin + self.settings.width) * column + \
                    self.settings.margin + self.settings.width // 2
                y = (self.settings.margin + self.settings.height) * row + \
                    self.settings.margin + self.settings.height // 2
                if self.grid[row][column] == 'O':
                    pygame.draw.circle(self.screen, self.settings.nil_color, (x, y), 35, 4)
                if self.grid[row][column] == 'X':
                    pygame.draw.line(self.screen, self.settings.cross_color, (x - 30, y - 30), (x + 30, y + 30), 7)
                    pygame.draw.line(self.screen, self.settings.cross_color, (x - 30, y + 30), (x + 30, y - 30), 7)

    def winner_line(self, line_win):
        # линия победы
        coord_1 = line_win[0]
        coord_2 = line_win[2]
        x_1 = (self.settings.margin + self.settings.width) * coord_1[1] + \
              self.settings.margin + self.settings.width // 2
        y_1 = (self.settings.margin + self.settings.height) * coord_1[0] + \
              self.settings.margin + self.settings.height // 2
        x_2 = (self.settings.margin + self.settings.width) * coord_2[1] + \
              self.settings.margin + self.settings.width // 2
        y_2 = (self.settings.margin + self.settings.height) * coord_2[0] \
              + self.settings.margin + self.settings.height // 2
        pygame.draw.line(self.screen, self.settings.win_color, (x_1, y_1), (x_2, y_2), 7)
