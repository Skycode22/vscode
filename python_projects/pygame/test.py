import pygame

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
paddle1_y = win_height/2 - paddle_height/2
paddle2_x = win_width - 20 - paddle_width
paddle2_y = win_height/2 - paddle_height/2

# Set the ball size and position
ball_size = 10
ball_x = win_width/2 - ball_size/2
ball_y = win_height/2 - ball_size/2

# Set the ball speed
ball_speed_x = 3
ball_speed_y = 3

# Set the game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Check for ball collision with walls
    if ball_x < 0 or ball_x > win_width - ball_size:
        ball_speed_x *= -1
    if ball_y < 0 or ball_y > win_height - ball_size:
        ball_speed_y *= -1

    # Check for ball collision with paddles
    if ball_x < paddle1_x + paddle_width and ball_y > paddle1_y and ball_y < paddle1_y + paddle_height:
        ball_speed_x *= -1
    if ball_x > paddle2_x and ball_y > paddle2_y and ball_y < paddle2_y + paddle_height:
        ball_speed_x *= -1

    # Clear the screen
    window.fill((255, 255, 255))

    # Draw the paddles and ball
    pygame.draw.rect(window, (0, 0, 0), (paddle1_x, paddle1_y, paddle_width, paddle_height))
    pygame.draw.rect(window, (0, 0, 0), (paddle2_x, paddle2_y, paddle_width, paddle_height))
    pygame.draw.circle(window, (0, 0, 0), (int(ball_x), int(ball_y)), ball_size)

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
