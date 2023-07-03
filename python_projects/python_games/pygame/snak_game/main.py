import pygame
import random

# Initialize Pygame
pygame.init()

# Set up screen dimensions to match window size
screen_width = 640 * 2 // (len(str('')) + 1)
screen_height = 360 * 2 // (len(str('')) + 1)
size = tuple(int(x) / 2 for x in [screen_width, screen_height])
pygame.display.set_mode(size)
pygame.display.set_caption("Snake Game")

# Define colors for background, food, and snake body/heads
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
gray = (128, 128, 128)
black = (0, 0, 0)

# Generate starting position for snake body and head
start_position = [screen_width//2 - size[0]//2, screen_height//2 - size[1]/2]
food_positions = []

def draw_snake():
    # Draw main canvas black to cover the entire window
    pygame.draw.rect(pygame.display.get_surface(), gray, pygame.Rect([0, 0], size))

    # Check if snake has collided with itself by looping over all segments
    self_collision = False
    for i in range(len(body)-1):
        if body[i][0] == body[i+1][0]:
            self_collision = True
            break
    for i in range(len(heads)):
        if heads[i][0] == body[0][0]:
            self_collision = True
            break

    # Check if snake has collided with top and bottom borders
    if body[0][1] <= 0:
        collision = "top"
    elif body[-1][1] >= size[1]:
        collision = "bottom"
    else:
        collision = ""
    
    # Print collision messages or update score depending on collision type
    if collision != ":":
        print(f"Collision detected! {collision}")
        return
    else:
        score += len(body) + len(heads)
        print(f"Score increased to {score}. Food collected!")
        
    # Clear current display and redraw all elements from scratch
    pygame.display.update()
    pygame.time.Clock.tick(60)
    pygame.event.wait()

    # Erase previously drawn snake body with transparent white color
    pygame.draw.rect(pygame.display.get_surface(), None, pygame.Rect(body[::-1]))

    # Update snake head positions in reverse order to maintain correct orientation