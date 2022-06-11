import sys
from time import sleep
import pygame
import random
from settings import Settings
from grid import Grid


class TicTacToe:

    def __init__(self):
        """инициализация и создание ресурсов"""
        pygame.init()
        self.settings = Settings()

        pygame.display.set_icon(self.settings.icon)
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.caption)

        self.ways_to_win = (([2, 0], [2, 1], [2, 2]),
                            ([1, 0], [1, 1], [1, 2]),
                            ([0, 0], [0, 1], [0, 2]),
                            ([2, 0], [1, 0], [0, 0]),
                            ([2, 1], [1, 1], [0, 1]),
                            ([2, 2], [1, 2], [0, 2]),
                            ([2, 0], [1, 1], [0, 2]),
                            ([2, 2], [1, 1], [0, 0]))

        self.board = Grid(self)

        self.player = 'X'
        self.comp = 'O'
        self.turn = 'player'  # переход хода
        self.first_move = 1  # первый ход в игре
        self.board.reset_grid()
        self.line_win = []
        self.game_is_playing = True

    def run_game(self):
        """Запуск основного цикла игры."""

        while True:
            if self.game_is_playing:
                self._check_events()
                if self.turn == 'comp':
                    self.computer_move()
            else:
                self.new_game()

            self._update_screen()

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши. Получает ход игрока"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.turn == 'player':
                    mouse_pos = pygame.mouse.get_pos()
                    self.player_move(mouse_pos)
                else:
                    pass

    def player_move(self, mouse_pos):
        # переводим координаты экрана в координаты сетки. Ход игрока. Передача хода компьютеру
        x, y = mouse_pos
        column = int(x // (self.settings.width + self.settings.margin))
        row = int(y // (self.settings.height + self.settings.margin))

        if row < self.settings.row and column < self.settings.column:
            if self.is_space_free(row, column):
                self.board.grid[row][column] = self.player
                # проверить победу или ничью
                self.win_or_draw()

    def win_or_draw(self):
        """проверка на победу или ничью и передача хода"""
        if self.is_winner():
            self.game_is_playing = False
        else:
            if self.is_board_full():
                self.game_is_playing = False
            else:
                if self.turn == 'player':
                    self.turn = 'comp'
                else:
                    self.turn = 'player'

    def legal_moves(self):
        """создает список доступных ходов"""
        moves = []
        for column in range(self.settings.column):
            for row in range(self.settings.row):
                if self.board.grid[row][column] == '':
                    moves.append([row, column])
        return moves

    def computer_move(self):
        """определяет ход компьютера"""
        if self.player == 'X':
            self.comp = 'O'
        else:
            self.comp = 'X'
        move = self.art_int()
        self.board.grid[move[0]][move[1]] = self.comp

        # проверить на победу и ничью
        self.win_or_draw()

    def is_winner(self):
        """определяет победителя"""
        for row in self.ways_to_win:
            if self.board.grid[row[0][0]][row[0][1]] == self.board.grid[row[1][0]][row[1][1]] \
                    == self.board.grid[row[2][0]][row[2][1]] != '':
                self.line_win = row
                return True

    def is_board_full(self):
        # Возвращает True, если клетка на игровом поле занята. В противном случае, возвращает False.
        for column in range(self.settings.column):
            for row in range(self.settings.row):
                if self.is_space_free(column, row):
                    return False
        return True

    def is_space_free(self, column, row):
        # Возвращает True, если сделан ход в свободную клетку.
        return self.board.grid[column][row] == ''

    def art_int(self):
        """ИИ для игры"""
        board = self.board.grid
        corner_moves = [[2, 0], [2, 2], [0, 0], [0, 2]]
        center_move = [1, 1]
        side_moves = [[2, 1], [1, 0], [1, 2], [0, 1]]
        moves = self.legal_moves()

        # 1 - если можно победить, делаем этот ход
        for move in moves:
            board[move[0]][move[1]] = self.comp
            for piece in self.ways_to_win:
                if board[piece[0][0]][piece[0][1]] == board[piece[1][0]][piece[1][1]] \
                        == board[piece[2][0]][piece[2][1]] != '':
                    return move
            board[move[0]][move[1]] = ''

        # 2 -если может победить игрок, блокируем этот ход
        for move in moves:
            board[move[0]][move[1]] = self.player
            for piece in self.ways_to_win:
                if board[piece[0][0]][piece[0][1]] == board[piece[1][0]][piece[1][1]] \
                        == board[piece[2][0]][piece[2][1]] != '':
                    return move
            board[move[0]][move[1]] = ''

        # 3 - поскольку никто не может победить, выбираем лучшее из доступных полей
        random.shuffle(corner_moves)  # перемешиваем список угловых полей
        for move in corner_moves:
            if move in moves:
                return move

        if center_move in moves:
            return center_move

        random.shuffle(side_moves)
        for an_move in side_moves:
            if an_move in moves:
                return an_move

        # TODO 4 - невозможный уровень (?) - если игрок делает ход в угловое поле - комп занимает центр

    def new_game(self):
        """новая игра"""
        sleep(2)
        # первый ход
        self.first_move += 1
        if self.first_move % 2 == 0:
            self.turn = 'comp'
        else:
            self.turn = 'player'
        # смена Х и О
        if self.player == 'X':
            self.player = 'O'
            self.comp = 'X'
        else:
            self.player = 'X'
            self.comp = 'O'

        del self.board
        self.board = Grid(self)
        self.board.reset_grid()
        self.line_win = []
        self.game_is_playing = True

    def new_screen(self):
        """рисуем пустые ячейки"""
        for column in range(self.settings.column):
            for row in range(self.settings.row):
                # Do the math to figure out where the box is
                x = (self.settings.margin + self.settings.width) * column + self.settings.margin
                y = (self.settings.margin + self.settings.height) * row + self.settings.margin

                pygame.draw.rect(self.screen, self.settings.cell_color,
                                 (x, y, self.settings.width, self.settings.height))

    def _update_screen(self):
        """обновление экрана"""
        self.screen.fill(self.settings.bg_color)
        self.new_screen()
        self.board.update_grid()
        if self.is_winner():
            self.board.winner_line(self.line_win)
        # Отображение последнего прорисованного экрана.
        pygame.display.flip()


if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    tic_tac_toe = TicTacToe()
    tic_tac_toe.run_game()
