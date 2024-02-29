import pygame
import random

class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.player_marker = 'X'
        self.ai_marker = 'O'
        self.font = pygame.font.Font(None, 40)

    def print_board(self, screen):
        for row in range(3):
            for col in range(3):
                pygame.draw.rect(screen, (255, 255, 255), (col * 100, row * 100, 100, 100), 2)
                text_surface = self.font.render(self.board[row][col], True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(col * 100 + 50, row * 100 + 50))
                screen.blit(text_surface, text_rect)

    def check_winner(self, marker):
        # Check rows
        for row in self.board:
            if all(cell == marker for cell in row):
                return True
        # Check columns
        for col in range(3):
            if all(self.board[row][col] == marker for row in range(3)):
                return True
        # Check diagonals
        if all(self.board[i][i] == marker for i in range(3)) or \
                all(self.board[i][2 - i] == marker for i in range(3)):
            return True
        return False

    def is_full(self):
        return all(cell != ' ' for row in self.board for cell in row)

    def get_available_positions(self):
        return [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == ' ']

    def player_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.player_marker
            return True
        return False

    def ai_move(self):
        available_positions = self.get_available_positions()

        # Check for winning move
        for row, col in available_positions:
            self.board[row][col] = self.ai_marker
            if self.check_winner(self.ai_marker):
                return row, col
            self.board[row][col] = ' '

        # Check for blocking move
        for row, col in available_positions:
            self.board[row][col] = self.player_marker
            if self.check_winner(self.player_marker):
                self.board[row][col] = self.ai_marker
                return row, col
            self.board[row][col] = ' '

        # Otherwise, make a random move
        if available_positions:
            return random.choice(available_positions)
        return None

    def reset(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

    def play_game(self, screen):
        while not self.is_full():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // 100
                    row = pos[1] // 100
                    if self.player_move(row, col):
                        if self.check_winner(self.player_marker):
                            return 'Player'
                        elif self.is_full():
                            return 'Tie'

                        ai_row, ai_col = self.ai_move()
                        self.board[ai_row][ai_col] = self.ai_marker
                        if self.check_winner(self.ai_marker):
                            return 'AI'
                        elif self.is_full():
                            return 'Tie'

            screen.fill((0, 0, 0))
            self.print_board(screen)
            pygame.display.flip()
