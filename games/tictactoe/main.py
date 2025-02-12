# tictactoe with two players that can move between squares, but they dont do anything yet
import player
import board
import pygame

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)

screen_size = 700
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption('Tic Tac Toe')
clock = pygame.time.Clock()


board = board.Board((45, 45), 615, 5)
playerX = player.Player(board.rect.right, 50, 'X', board)
playerO = player.Player(board.rect.left, 50, 'O', board)
marker = 'X'
winner = None

while True:
    screen.fill(black)
    board.draw(screen)

    playerX.handle_movement()
    playerX.handle_collision()
    pygame.draw.rect(screen, blue, playerX.get_rect())

    playerO.handle_movement()
    playerO.handle_collision()
    pygame.draw.rect(screen, red, playerO.get_rect())

    winner = board.check_win()
    if winner is not None:
        marker = 'X'
        board.display_win(winner)
        winner = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and winner is None:
            x, y = pygame.mouse.get_pos()
            if board.place_marker(x, y, marker):
                marker = 'O' if marker == 'X' else 'X'
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                playerX.jump_down()
            if event.key == pygame.K_s:
                playerO.jump_down()
            if event.key == pygame.K_UP and playerX.jumping:
                playerX.jump_up()
            if event.key == pygame.K_w and playerO.jumping:
                playerO.jump_up()

    pygame.display.flip()
    clock.tick(60)
