import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the game window size
win_width = 640
win_height = 480
window = pygame.display.set_mode((win_width, win_height))

# Set the paddle size and position
paddle_width = 10
paddle_height = 60
paddle1_x = 20
paddle2_x = win_width - 20 - paddle_width

# Set the ball size
ball_size = 10

# Set the initial ball speed
initial_ball_speed_x = .3
initial_ball_speed_y = .3

# Paddle speed
paddle_speed = 1

def play_game():
    # Score
    score1 = 0
    score2 = 0

    # Paddle position
    paddle1_y = win_height / 2 - paddle_height / 2
    paddle2_y = win_height / 2 - paddle_height / 2

    # Ball position and speed
    ball_x = win_width / 2 - ball_size / 2
    ball_y = win_height / 2 - ball_size / 2
    ball_speed_x = initial_ball_speed_x
    ball_speed_y = initial_ball_speed_y

    # Set initial ball direction
    ball_direction = 1

    # Set the game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Control the paddles
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddle1_y -= paddle_speed
        if keys[pygame.K_s]:
            paddle1_y += paddle_speed
        if keys[pygame.K_UP]:
            paddle2_y -= paddle_speed
        if keys[pygame.K_DOWN]:
            paddle2_y += paddle_speed

        # Paddle boundaries
        if paddle1_y < 0:
            paddle1_y = 0
        if paddle1_y > win_height - paddle_height:
            paddle1_y = win_height - paddle_height
        if paddle2_y < 0:
            paddle2_y = 0
        if paddle2_y > win_height - paddle_height:
            paddle2_y = win_height - paddle_height

        # Move the ball
        ball_x += ball_speed_x * ball_direction
        ball_y += ball_speed_y

        # Check for ball collision with walls and scoring
        if ball_x < 0:
            score2 += 1
            ball_x, ball_y = win_width/2 - ball_size/2, win_height/2 - ball_size/2
            ball_speed_x, ball_speed_y = initial_ball_speed_x, initial_ball_speed_y
            ball_direction *= -1
        if ball_x > win_width - ball_size:
            score1 += 1
            ball_x, ball_y = win_width/2 - ball_size/2, win_height/2 - ball_size/2
            ball_speed_x, ball_speed_y = initial_ball_speed_x, initial_ball_speed_y
            ball_direction *= -1
        if ball_y < 0 or ball_y > win_height - ball_size:
            ball_speed_y *= -1

        # Check for ball collision with paddles and increase speed
        if (ball_x < paddle1_x + paddle_width and ball_y > paddle1_y and ball_y < paddle1_y + paddle_height) or \
            (ball_x > paddle2_x and ball_y > paddle2_y and ball_y < paddle2_y + paddle_height):
            ball_speed_x *= -1.1
            ball_speed_y *= 1.1

        # Clear the screen
        window.fill((255, 255, 255))

        # Draw the paddles and ball
        pygame.draw.rect(window, (0, 0, 0), (paddle1_x, paddle1_y, paddle_width, paddle_height))
        pygame.draw.rect(window, (0, 0, 0), (paddle2_x, paddle2_y, paddle_width, paddle_height))
        pygame.draw.circle(window, (0, 0, 0), (int(ball_x), int(ball_y)), ball_size)

        # Draw the score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Player 1: {score1}  Player 2: {score2}", True, (0, 0, 0))
        window.blit(text, (win_width/2 - text.get_width() // 2, 10))

        if score1 >= 10:
            text = font.render("Player 1 Wins!", True, (0, 0, 0))
            window.blit(text, (win_width/2 - text.get_width() // 2, win_height/2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.wait(3000)
            running = False
        elif score2 >= 10:
            text = font.render("Player 2 Wins!", True, (0, 0, 0))
            window.blit(text, (win_width/2 - text.get_width() // 2, win_height/2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.wait(3000)
            running = False

        # Update the display
        pygame.display.update()

    return score1, score2

def main():
    while True:
        score1, score2 = play_game()
        # Show the end of game screen and ask if the player wants to play again
        if show_endgame_screen(score1, score2):
            break
    pygame.quit()

def show_endgame_screen(score1, score2):
    # Set the endgame screen
    window.fill((255, 255, 255))
    font = pygame.font.Font(None, 36)
    text = font.render(f"Player 1: {score1}  Player 2: {score2}", True, (0, 0, 0))
    window.blit(text, (win_width/2 - text.get_width() // 2, win_height/2 - text.get_height() // 2))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                return False

if __name__ == "__main__":
    main()
