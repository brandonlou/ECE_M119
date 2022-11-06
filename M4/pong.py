import pygame
from Ball import Ball
from Paddle import Paddle

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SIZE = (700, 500)
INITIAL_SCORE = 100
AX_THRESHOLD = 0.3
PADDLE_SPEED = 10 # Pixels per frame
FPS = 30 # Frames per second


"""
What: Pong Tutorial using Pygame
Where: https://www.101computing.net/pong-tutorial-using-pygame-getting-started
Why: In the pong game, users control paddles to prevent a ball from going into
     their goal. Reusing this code saves me time from learning how to program
     games/graphics in Python and enables me to focus on programming the BLE
     connectivity with the Arduino. The code in Paddle.py and Ball.py are also
     referenced from this resource.
"""

def run_pong(ax):
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Pong')

    paddle = Paddle(WHITE, 10, 100)
    paddle.rect.x = 20
    paddle.rect.y = 200

    ball = Ball(WHITE, 10, 10)
    ball.rect.x = 345
    ball.rect.y = 195

    sprites = pygame.sprite.Group()
    sprites.add(paddle)
    sprites.add(ball)

    running = True
    clock = pygame.time.Clock()

    score = INITIAL_SCORE

    # Main program loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if ax.value >= AX_THRESHOLD:
            paddle.move(-PADDLE_SPEED)
        elif ax.value <= -AX_THRESHOLD:
            paddle.move(PADDLE_SPEED)

        sprites.update()

        # Update the ball
        if ball.rect.x >= 690:
            ball.velocity.x = -ball.velocity.x
        if ball.rect.x <= 0:
            score -= 1;
            ball.velocity.x = -ball.velocity.x
        if ball.rect.y > 490 or ball.rect.y < 0:
            ball.velocity.y = -ball.velocity.y

        if pygame.sprite.collide_mask(ball, paddle):
            ball.bounce()

        # Draw
        screen.fill(BLACK) # Screen
        pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5) # Net
        sprites.draw(screen) # Sprites
        font = pygame.font.Font(None, 72)
        text = font.render(str(score), 1, WHITE)
        screen.blit(text, (600, 15)) # Score text

        # Update the screen
        pygame.display.flip()

        # Limit to 60 frames per second
        clock.tick(FPS)

    pygame.quit()
