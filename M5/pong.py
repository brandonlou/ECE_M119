import pygame
from enum import Enum
from Ball import Ball
from Paddle import Paddle

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SIZE = (700, 500)
AX_THRESHOLD = 0.3
PADDLE_SPEED = 10 # Pixels per frame
FPS = 30 # Frames per second

class Gesture(Enum):
    UP = 0
    DOWN = 1
    STOP = 2

"""
What: Pong Tutorial using Pygame
Where: https://www.101computing.net/pong-tutorial-using-pygame-getting-started
Why: In the pong game, users control paddles to prevent a ball from going into
     their goal. Reusing this code saves me time from learning how to program
     games/graphics in Python and enables me to focus on programming the BLE
     connectivity with the Arduino. The code in Paddle.py and Ball.py are also
     referenced from this resource.
"""

def run_pong(gesture_1, gesture_2):
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Pong')

    left_paddle = Paddle(WHITE, 10, 100)
    left_paddle.rect.x = 20
    left_paddle.rect.y = 200

    right_paddle = Paddle(WHITE, 10, 100)
    right_paddle.rect.x = 670
    right_paddle.rect.y = 200

    ball = Ball(WHITE, 10, 10)
    ball.rect.x = 345
    ball.rect.y = 195

    sprites = pygame.sprite.Group()
    sprites.add(left_paddle)
    sprites.add(right_paddle)
    sprites.add(ball)

    running = True
    clock = pygame.time.Clock()

    left_score = 0
    right_score = 0

    # Main program loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if gesture_1.value == Gesture.UP.value:
            left_paddle.move(-PADDLE_SPEED)
        elif gesture_1.value == Gesture.DOWN.value:
            left_paddle.move(PADDLE_SPEED)

        if gesture_2.value == Gesture.UP.value:
            right_paddle.move(-PADDLE_SPEED)
        elif gesture_2.value == Gesture.DOWN.value:
            right_paddle.move(PADDLE_SPEED)

        sprites.update()

        # Increment score and reset ball when it hits the left or right wall
        if ball.rect.x >= 690:
            # ball.velocity.x = -ball.velocity.x
            left_score += 1
            ball.reset()
        if ball.rect.x <= 0:
            # ball.velocity.x = -ball.velocity.x
            right_score += 1
            ball.reset()

        # Bounce the ball off the top and bottom wall
        if ball.rect.y > 490 or ball.rect.y < 0:
            ball.velocity.y = -ball.velocity.y

        # Bounce the ball off the paddle
        if pygame.sprite.collide_mask(ball, left_paddle) or pygame.sprite.collide_mask(ball, right_paddle):
            ball.bounce()

        # Draw screen
        screen.fill(BLACK)

        # Draw net
        pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5) # Net

        # Draw sprites
        sprites.draw(screen)

        # Draw score text
        font = pygame.font.Font(None, 74)
        text = font.render(str(left_score), 1, WHITE)
        screen.blit(text, (250, 10))
        text = font.render(str(right_score), 1, WHITE)
        screen.blit(text, (420, 10))

        # Update the screen
        pygame.display.flip()

        # Limit the FPS
        clock.tick(FPS)

    pygame.quit()
