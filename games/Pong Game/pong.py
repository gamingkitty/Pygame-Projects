import pygame
import sys
import os
from moviepy.editor import VideoFileClip
import random
import tictactoe
import os
# Initialize Pygame
pygame.init()
dirname = os.path.dirname(__file__)
# Constants
WIDTH, HEIGHT = 800, 600
BORDER_SIZE = 10
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(pygame.font.get_default_font(), 36)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
tic_tac_toe_game = tictactoe.TicTacToe()

# Load your ads for the video
video_folder = dirname  # Update this path to the folder containing your videos
video_files = sorted([os.path.join(video_folder, file) for file in os.listdir(video_folder) if file.endswith(".mp4")])
current_video = 0

# Paddle and Ball Constants
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 60
BALL_SIZE = 10

# Initialize paddles and ball
player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Initialize ball speed
ball_speed = [4, 4]

# Initialize opponent's paddle speed
opponent_speed = 3

# Initialize scores
player_score = 0
opponent_score = 0

# Flag to check if an ad is currently being displayed
ad_displayed = False
ad_start_time = 0
skip_wait_min = 10  # Minimum wait time before allowing skipping (in seconds)

# Function to play video with embedded audio
def play_video(video_path):
    global ad_displayed, ad_start_time

    print(f"Playing Video: {video_path}")

    # Load the video clip
    clip = VideoFileClip(video_path)

    # Save the audio to a temporary file
    audio_temp_path = "temp_audio.wav"
    clip.audio.write_audiofile(audio_temp_path)

    # Load the audio using Pygame mixer
    pygame.mixer.Sound(audio_temp_path).play()

    # Record the ad start time
    ad_start_time = pygame.time.get_ticks()

    # Loop through frames and display them
    for frame in clip.iter_frames(fps=FPS):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Skip the ad when the space key is pressed
                pygame.mixer.stop()
                os.remove(audio_temp_path)
                ad_displayed = False
                return

        # Convert the frame to a Pygame surface
        pygame_frame = pygame.image.fromstring(frame.tobytes(), clip.size, "RGB")

        # Display the frame
        screen.blit(pygame_frame, (0, 0))
        pygame.display.flip()

        # Cap the frame rate
        pygame.time.Clock().tick(FPS)

    # Remove the temporary audio file
    os.remove(audio_temp_path)

    # Set the flag to indicate that the ad has been displayed
    ad_displayed = False

# Function to display ads as a small screen
def display_ad(ad_path):
    global ad_displayed, ad_start_time, skip_text_displayed

    if ad_displayed:
        return  # If an ad is already being displayed, exit the function

    # Load the ad video clip
    ad_clip = VideoFileClip(ad_path)
    # Save the audio to a temporary file
    audio_temp_path = "temp_audio.wav"
    ad_clip.audio.write_audiofile(audio_temp_path)

    # Play the audio using Pygame mixer
    pygame.mixer.music.load(audio_temp_path)
    pygame.mixer.music.play()

    # Record the ad start time
    ad_start_time = pygame.time.get_ticks()

    # Reset skip text flag
    skip_text_displayed = False

    # Loop through frames and display them
    for frame in ad_clip.iter_frames(fps=FPS):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Skip the ad when the space key is pressed
                pygame.mixer.music.stop()
                ad_displayed = False
                return

        # Convert the frame to a Pygame surface
        pygame_frame = pygame.image.fromstring(frame.tobytes(), ad_clip.size, "RGB")

        # Display the frame in a smaller screen
        screen.blit(pygame.transform.scale(pygame_frame, (WIDTH // 2, HEIGHT // 2)), (WIDTH // 4, HEIGHT // 4))

        # Check if the skip text needs to be displayed
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - ad_start_time) // 1000  # Convert to seconds

        # Display Skip Ad button in the bottom right corner after 10 seconds
        if elapsed_time >= 10 and not skip_text_displayed:
            skip_ad_text = FONT.render("Press Space to Skip Ad", True, WHITE)
            screen.blit(skip_ad_text, (WIDTH - skip_ad_text.get_width() - 10, HEIGHT - skip_ad_text.get_height() - 10))
            skip_text_displayed = True

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        pygame.time.Clock().tick(FPS)

        # Check if the ad duration has passed and end the ad
        if current_time - ad_start_time >= ad_clip.duration * 1000:
            break

    # Stop playing audio after ad ends or is skipped
    pygame.mixer.music.stop()

    # Set the flag to indicate that the ad has been displayed
    ad_displayed = True
# Function to reset paddles and scores
def reset_game():
    global player_paddle, opponent_paddle, ball, ball_speed, player_score, opponent_score
    player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    opponent_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH,
                                  PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
    ball_speed = [4, 4]

# Game loop
while True:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()

    keys = pygame.key.get_pressed()

    if not ad_displayed:
        # Move player paddle only when an ad is not being displayed
        if keys[pygame.K_UP] and player_paddle.top > BORDER_SIZE:
            player_paddle.y -= 5
        if keys[pygame.K_DOWN] and player_paddle.bottom < HEIGHT - BORDER_SIZE:
            player_paddle.y += 5

    # Move the opponent paddle based on difficulty
    if opponent_paddle.centery < ball.centery:
        opponent_paddle.y += opponent_speed
    elif opponent_paddle.centery > ball.centery:
        opponent_paddle.y -= opponent_speed

    # Update ball position
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Ball collision with paddles
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_speed[0] = -ball_speed[0]

    # Ball collision with walls
    if ball.top <= BORDER_SIZE or ball.bottom >= HEIGHT - BORDER_SIZE:
        ball_speed[1] = -ball_speed[1]

    # Ball out of bounds
    if ball.left <= 0:
        opponent_score += 1
        reset_game()  # Reset the game after the score
        if video_files:
            # Play video ad if there are video files available
            display_ad(random.choice(video_files))

    if ball.right >= WIDTH:
        result = tic_tac_toe_game.play_game(screen)
        if result == 'Player':
            player_score += 1
            reset_game()
            tic_tac_toe_game.reset()
        elif result == 'AI':
            player_score -= 1
            reset_game()
            tic_tac_toe_game.reset()

        elif result == 'Tie':
            tic_tac_toe_game.reset()

    # Increase opponent's paddle speed over time
    if player_score + opponent_score >= 5:
        opponent_speed = 4
    if player_score + opponent_score >= 10:
        opponent_speed = 5

    # Draw everything
    screen.fill(BLACK)

    # Draw borders
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, BORDER_SIZE))
    pygame.draw.rect(screen, WHITE, (0, HEIGHT - BORDER_SIZE, WIDTH, BORDER_SIZE))
    pygame.draw.rect(screen, WHITE, (0, 0, BORDER_SIZE, HEIGHT))
    pygame.draw.rect(screen, WHITE, (WIDTH - BORDER_SIZE, 0, BORDER_SIZE, HEIGHT))

    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Draw scores with a retro-style font
    player_text = FONT.render(str(player_score), True, WHITE)
    opponent_text = FONT.render(str(opponent_score), True, WHITE)
    screen.blit(player_text, (WIDTH // 4 - player_text.get_width() // 2, 20))
    screen.blit(opponent_text, (3 * WIDTH // 4 - opponent_text.get_width() // 2, 20))

    if ad_displayed:
        # Draw Skip Ad text in the bottom right corner during ad display
        pygame.display.flip()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(FPS)