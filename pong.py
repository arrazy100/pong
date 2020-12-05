import pygame
from random import randint

from paddle import Paddle
from ball import Ball

pygame.init()

# random velocity exclude few number
def random_velocity():
    exclude = [-3, -2, -1, 0, 1, 2, 3]
    rand = randint(-8, 8)
    return random_velocity() if rand in exclude else rand

def start_game():
    # set color
    color_black = (0, 0, 0)
    color_white = (255, 255, 255)
    color_red = (255, 0, 0)
    color_green = (0, 255, 0)
    color_blue = (0, 0, 255)

    # open window
    width = 640
    height = 480
    size = (width, height)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Pong Game")

    # player 1 paddle
    paddle1 = Paddle(color_red, 10, (height / 5))
    paddle1.rect.x = 20
    paddle1.rect.y = (height / 5) * 2

    # player 2 paddle
    paddle2 = Paddle(color_blue, 10, (height / 5))
    paddle2.rect.x = width - 30;
    paddle2.rect.y = (height / 5) * 2

    # set paddle speed
    speed = 8

    # ball
    ball = Ball(color_green, 10, 10)
    ball.rect.x = 345
    ball.rect.y = 195

    # list of paddle
    sprite_list = pygame.sprite.Group()

    # add player 1 and player 2 paddle to list
    sprite_list.add(paddle1)
    sprite_list.add(paddle2)
    sprite_list.add(ball)

    # set score
    score_player1 = 0
    score_player2 = 0

    # make font for score
    font = pygame.font.Font(None, 30)

    # run condition
    running = True

    # pause condition
    pause = False

    # win condition
    win = False

    # add clock
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                running = False
            
            # release key event
            if event.type == pygame.KEYUP:
                # if key q released
                if event.key == pygame.K_q:
                    # quit loop
                    running = False

                # if key enter released
                if event.key == pygame.K_RETURN:
                    # pause game
                    pause = True

        # fill screen with black color
        screen.fill(color_black)

        # draw white line on middle of screen
        pygame.draw.line(screen, color_white, [(width / 2) - 1, 0], [(width / 2) - 1, height], 5)

        # capture keyboard press
        keys = pygame.key.get_pressed()

        # moving the paddle 1
        if (keys[pygame.K_w]):
            paddle1.goUp(speed)

        if (keys[pygame.K_s]):
            paddle1.goDown(speed)

        # moving the paddle 2
        if (keys[pygame.K_UP]):
            paddle2.goUp(speed)

        if (keys[pygame.K_DOWN]):
            paddle2.goDown(speed)

        # update the list of paddle
        sprite_list.update()

        # if player win
        if (score_player1 == 10) or (score_player2 == 10):
            win = True

        # player 2 goal
        if ball.rect.x > 630:
            # add player 1 score
            score_player1 += 1

            # random ball position
            ball.velocity = [random_velocity(), randint(-8, 8)]
            ball.rect.x = randint((width / 2) - 5, (width / 2) + 5)
            ball.rect.y = randint(200, 280)
        
        # player 1 goal
        if ball.rect.x < 0:
            # add player 2 score
            score_player2 += 1

            # random ball position
            ball.velocity = [random_velocity(), randint(-8, 8)]
            ball.rect.x = randint((width / 2) - 5, (width / 2) + 5)
            ball.rect.y = randint(200, 280)

        if ball.rect.y >= 470:
            # inverse the velocity of y
            ball.velocity[1] = -ball.velocity[1]

        if ball.rect.y <= 0:
            # inverse the velocity of y
            ball.velocity[1] = -ball.velocity[1]

        # detect ball colide with paddle 1 or paddle 2
        if pygame.sprite.collide_mask(ball, paddle1) or pygame.sprite.collide_mask(ball, paddle2):
            ball.bounce()

        # draw the list of paddle
        sprite_list.draw(screen)

        # display player score
        text_score_player1 = font.render(str(score_player1), 1, color_white)
        text_score_player2 = font.render(str(score_player2), 1, color_white)
        screen.blit(text_score_player1, (100, 10))
        screen.blit(text_score_player2, (width - 100, 10))

        # update render
        pygame.display.flip()

        # limit fps to 60
        clock.tick(60)

        while win:
            for event in pygame.event.get():
                # quit event
                if event.type == pygame.QUIT:
                    running = False
                    win = False
                
                # release key event
                if event.type == pygame.KEYUP:
                    # if key q released
                    if event.key == pygame.K_q:
                        # quit loop
                        running = False
                        win = False

                    # if key enter released
                    if event.key == pygame.K_RETURN:
                        # new game and reset all variable
                        score_player1 = 0
                        score_player2 = 0
                        paddle1.rect.x = 20;
                        paddle1.rect.y = (height / 5) * 2
                        paddle2.rect.x = width - 30;
                        paddle2.rect.y = (height / 5) * 2
                        ball.rect.x = 345
                        ball.rect.y = 195
                        win = False

            # if player 1 win
            if (score_player1 == 10):
                win_text = font.render("Player 1 Win", 1, color_green)
            else: # if player 2 win
                win_text = font.render("Player 2 Win", 1, color_green)
        
            # measure win text width and height
            win_width, win_height = font.size("Player 1 Win")

            # draw win text to screen
            screen.blit(win_text, ((width / 2) - (win_width / 2), 50))

            # update display
            pygame.display.flip()

        while pause:
            for event in pygame.event.get():
                # quit event
                if event.type == pygame.QUIT:
                    running = False
                    pause = False
                
                # release key event
                if event.type == pygame.KEYUP:
                    # if key q released
                    if event.key == pygame.K_q:
                        # quit loop
                        running = False
                        pause = False

                    # if key enter released
                    if event.key == pygame.K_RETURN:
                        # resume game
                        pause = False
            
            # pause text
            pause_text = font.render("Game Paused", 1, color_red)

            # measure pause text width and height
            pause_width, pause_height = font.size("Game Paused")

            # draw pause text to screen
            screen.blit(pause_text, ((width / 2) - (pause_width / 2), (height / 2) - (pause_height / 2)))

            # update display
            pygame.display.flip()

# main function
if __name__ == "__main__":
    start_game()