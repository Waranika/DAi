import pygame

pygame.init()

screen = pygame.display.set_mode((500, 500))

# Initialize the game window with a size of 500x500

pygame.display.set_caption("Snake")

snake = [(200, 200), (210, 200), (220, 200)]

direction = "RIGHT"

speed = 10

score = 0

font = pygame.font.Font(None, 36)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction = "UP"
            elif event.key == pygame.K_DOWN:
                direction = "DOWN"
            elif event.key == pygame.K_LEFT:
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT:
                direction = "RIGHT"

    # Update snake position based on the current direction
    if direction == "UP":
        snake[0] = (snake[0][0], snake[0][1] - speed)
    elif direction == "DOWN":
        snake[0] = (snake[0][0], snake[0][1] + speed)
    elif direction == "LEFT":
        snake[0] = (snake[0][0] - speed, snake[0][1])
    elif direction == "RIGHT":
        snake[0] = (snake[0][0] + speed, snake[0][1])

    # Move the rest of the snake body
    for i in range(len(snake) - 1, 0, -1):
        snake[i] = (snake[i-1][0], snake[i-1][1])

    # Fill the screen with black color
    screen.fill((0, 0, 0))

    # Draw the snake on the screen
    for x, y in snake:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x, y, 10, 10))

    # Display the player's score on the screen
    score_text = font.render("Score: {}".format(score), 1, (255, 255, 255))
    screen.blit(score_text, (5, 5))

    # Update the display
    pygame.display.flip()