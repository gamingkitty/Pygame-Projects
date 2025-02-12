import pygame

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)

class Player:
    def __init__(self, x, y, player, board):
        self.x = x
        self.y = y
        self.size = 30
        self.board = board
        self.speed = 5
        self.jump_strength = 13
        self.velocity_y = 0
        self.gravity = 0.75
        self.jumping = False
        self.color = blue if player == 'X' else red
        self.player = player

    def handle_movement(self):
        keys = pygame.key.get_pressed()

        if self.player == 'X':
            if keys[pygame.K_LEFT]:
                self.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.x += self.speed
            if keys[pygame.K_UP] and not self.jumping:
                self.velocity_y = -self.jump_strength
                self.jumping = True
        elif self.player == 'O':
            if keys[pygame.K_a]:
                self.x -= self.speed
            if keys[pygame.K_d]:
                self.x += self.speed
            if keys[pygame.K_w] and not self.jumping:
                self.velocity_y = -self.jump_strength
                self.jumping = True

        self.velocity_y += self.gravity
        self.y += self.velocity_y

    def jump_down(self):
        self.y += self.board.height / 3 if self.y < self.board.rect.top + 2 * self.board.height / 3 else 0

    def jump_up(self):
        self.y -= self.board.height / 3 if self.y > self.board.rect.top + self.board.height / 3 else 0

    def handle_collision(self):
        for platform_y in self.board.platforms:
            platform_y -= self.size
            if platform_y <= self.y < platform_y + 20 and self.velocity_y > 0:
                self.y = platform_y
                self.velocity_y = 0
                self.jumping = False

        if self.x < self.board.rect.left + self.board.line_width:
            self.x = self.board.rect.left + self.board.line_width
        if self.x > self.board.rect.right - self.size - self.board.line_width:
            self.x = self.board.rect.right - self.size - self.board.line_width

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)