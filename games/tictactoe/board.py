import pygame

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)

class Board:
    def __init__(self, pos, size, line_width):
        self.topleft = pos
        self.size = size
        self.rect = pygame.Rect(pos, (size, size))
        self.height = self.rect.h
        self.width = self.rect.w
        self.line_width = line_width
        self.platforms = [self.rect.top + self.height / 3 - self.line_width / 4, self.rect.top + 2 * self.height / 3 - self.line_width / 4, self.rect.bottom - self.line_width]
        self.win_display_time = 20
        self.win_display_timer = 0
        self.displaying_win = False
        self.cells = [' ' for _ in range(9)]
        self.tokens = [[0, 0, ' '] for _ in range(9)]
        self.num_spaces_taken = 0

    def draw(self, screen):
        pygame.draw.line(screen, white, (self.rect.left, self.rect.top + self.height / 3), (self.rect.right - self.line_width, self.rect.top + self.height / 3), self.line_width)
        pygame.draw.line(screen, white, (self.rect.left, self.rect.top + 2 * self.height / 3), (self.rect.right - self.line_width, self.rect.top + 2 * self.height / 3), self.line_width)
        pygame.draw.line(screen, white, (self.rect.left + self.width / 3, self.rect.top), (self.rect.left + self.width / 3, self.rect.bottom - self.line_width), self.line_width)
        pygame.draw.line(screen, white, (self.rect.left + 2 * self.width / 3, self.rect.top), (self.rect.left + 2 * self.width / 3, self.rect.bottom - self.line_width), self.line_width)
        pygame.draw.rect(screen, white, self.rect, self.line_width)
        for token in self.tokens:
            if token[2] == 'X':
                pygame.draw.line(screen, blue, (token[0] - 25, token[1] - 25), (token[0] + 25, token[1] + 25), 5)
                pygame.draw.line(screen, blue, (token[0] + 25, token[1] - 25), (token[0] - 25, token[1] + 25), 5)
            elif token[2] == 'O':
                pygame.draw.circle(screen, red, (token[0], token[1]), 25, 5)
        if self.displaying_win:
            if self.win_display_timer >= self.win_display_time:
                self.clear()
                self.win_display_timer = 0
                self.displaying_win = False
            else:
                self.win_display_timer += 1


    def place_marker(self, x, y, marker):
        col = (x - self.topleft[0]) // (self.width // 3)
        row = (y - self.topleft[1]) // (self.width // 3)
        choice = row * 3 + col

        if self.cells[choice] == ' ':
            self.num_spaces_taken += 1
            self.cells[choice] = marker
            center_x = self.topleft[1] + (1 + col * 2) * self.width / 6
            center_y = self.topleft[0] + (1 + row * 2) * self.height / 6
            self.tokens[choice] = [center_x, center_y, marker]
            return True
        return False

    def check_win(self):
        if self.cells[0] == self.cells[1] == self.cells[2] != ' ':
            return self.cells[0]
        elif self.cells[3] == self.cells[4] == self.cells[5] != ' ':
            return self.cells[3]
        elif self.cells[6] == self.cells[7] == self.cells[8] != ' ':
            return self.cells[6]
        elif self.cells[0] == self.cells[3] == self.cells[6] != ' ':
            return self.cells[0]
        elif self.cells[1] == self.cells[4] == self.cells[7] != ' ':
            return self.cells[1]
        elif self.cells[2] == self.cells[5] == self.cells[8] != ' ':
            return self.cells[2]
        elif self.cells[0] == self.cells[4] == self.cells[8] != ' ':
            return self.cells[0]
        elif self.cells[2] == self.cells[4] == self.cells[6] != ' ':
            return self.cells[2]
        if self.num_spaces_taken == 9:
            self.clear()
        return None

    def clear(self):
        self.cells = [' ' for _ in range(9)]
        self.tokens = [[0, 0, ' '] for _ in range(9)]
        self.num_spaces_taken = 0

    def fill(self, marker):
        for row in range(3):
            for col in range(3):
                space = row * 3 + col
                self.cells[space] = marker
                center_x = self.topleft[1] + (1 + col * 2) * self.width / 6
                center_y = self.topleft[0] + (1 + row * 2) * self.height / 6
                self.tokens[space] = [center_x, center_y, marker]

    def display_win(self, marker):
        self.fill(marker)
        self.displaying_win = True