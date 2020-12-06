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

# menu
def menu():
    # set color
    color_black = (0, 0, 0)
    color_white = (255, 255, 255)
    color_green = (0, 255, 0)

    # open window
    width = 640
    height = 480
    size = (width, height)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Pong Game")

    # make font for menu
    menu_font = pygame.font.Font(None, 50)

    # get menu text size
    text_width, text_height = menu_font.size("Start vs Computer")

    # credit text and font
    credit_font = pygame.font.Font(None, 20)
    credit_text = "Developed By Muhammad Afdhal Arrazy (180535632536)"

    # make color list of menu
    menu_color = [
        color_green,
        color_white,
        color_white,
        color_white,
        color_white
    ]

    # make list of menu
    menu_list = [
        "Start vs Computer",
        "Start vs Player",
        "Exit"
    ]

    # current menu
    current_menu = 0

    # game menu condition
    menu = True

    while menu:
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                menu = False
            
            # release key event
            if event.type == pygame.KEYUP:

                # if key up released
                if event.key == pygame.K_UP:
                    # if current_menu out of bound, set to last menu, else substract menu by 1
                    if current_menu - 1 < 0:
                        current_menu = len(menu_list) - 1
                    else:
                        current_menu -= 1

                    # change all menu color to white
                    for i in range(len(menu_color)):
                        menu_color[i] = color_white

                    # change current menu color to green
                    menu_color[current_menu] = color_green

                # if key down released
                if event.key == pygame.K_DOWN:
                    # if current_menu out of bound, set to first menu, else add menu by 1
                    if current_menu + 1 > len(menu_list) - 1:
                        current_menu = 0
                    else:
                        current_menu += 1

                    # change all menu color to white
                    for i in range(len(menu_color)):
                        menu_color[i] = color_white

                    # change current menu color to green
                    menu_color[current_menu] = color_green

                # if key enter released
                if event.key == pygame.K_RETURN:
                    # quit loop
                    menu = False

                    # if current_menu == 0, start the game vs computer
                    if current_menu == 0:
                        start_game(True)
                    # if current_menu == 1, start the game vs player
                    elif current_menu == 1:
                        start_game(False)

        # fill screen with black color
        screen.fill(color_black)

        # draw menu on screen
        for i in range(len(menu_list)):
            # draw menu on middle of screen
            x = (width / 2) - (text_width / 2)
            y = ((height / 2) - 100) + (i * (text_height + 10))

            # draw
            text = menu_font.render(menu_list[i], 1, menu_color[i])
            screen.blit(text, (x, y))

        credit = credit_font.render(credit_text, 1, (0, 0, 255))
        credit_width, credit_height = credit_font.size(credit_text)
        screen.blit(credit, ((width / 2) - (credit_width / 2), 450))

        # update render
        pygame.display.flip()

# start game
def start_game(computer):
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

    # set computer speed
    enemy_speed = 6

    # ball
    ball = Ball(color_green, 10, 10)
    ball.rect.x = 315
    ball.rect.y = 210

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

    # start_game condition
    start = True

    # pause condition
    pause = False

    # win condition
    win = False

    # add clock
    clock = pygame.time.Clock()

    # game start
    while start:
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                start = False
            
            # release key event
            if event.type == pygame.KEYUP:
                # if key q released
                if event.key == pygame.K_q:
                    # go to game menu
                    start = False
                    menu()

                # if key enter released
                if event.key == pygame.K_RETURN:
                    # pause game
                    pause = True

        # fill screen with black color
        screen.fill(color_black)

        # draw white line on middle of screen
        pygame.draw.line(screen, color_white, [(width / 2) - 1, 0], [(width / 2) - 1, height], 5)

        # draw white line on bottom of the score text
        pygame.draw.line(screen, color_white, [0, 50], [width, 50], 5)

        # capture keyboard press
        keys = pygame.key.get_pressed()

        # moving the paddle 1
        if (keys[pygame.K_w]):
            paddle1.goUp(speed)

        if (keys[pygame.K_s]):
            paddle1.goDown(speed)

        # enable key press for paddle 2 if enemy is player
        if (not computer):
            if (keys[pygame.K_UP]):
                paddle2.goUp(speed)

            if (keys[pygame.K_DOWN]):
                paddle2.goDown(speed)

        # auto paddle 2 movement if enemy is computer
        else:
            # if ball position x on enemy side and move towards enemy paddle
            if ball.rect.x >= (height / 2) - 5 and ball.velocity[0] > 0:
                
                # random enemy speed
                enemy_speed = randint(3, 8)

                # if ball y position not on the center of paddle 2
                if ball.rect.y + (ball.rect.h / 2) > paddle2.rect.y + (paddle2.rect.h / 2):
                    paddle2.goDown(enemy_speed)
                elif ball.rect.y + (ball.rect.h / 2) < paddle2.rect.y + (paddle2.rect.h / 2):
                    paddle2.goUp(enemy_speed)
                

        # update the list of paddle
        sprite_list.update()

        # if player win
        if (score_player1 == 10) or (score_player2 == 10):
            win = True

        # ball get through player 2
        if ball.rect.x > 630:
            # add player 1 score
            score_player1 += 1

            # random ball position
            ball.velocity = [random_velocity(), randint(-8, 8)]

            # set ball position to center of screen
            ball.rect.x = 315
            ball.rect.y = 210
        
        # ball get through player 1
        if ball.rect.x < 0:
            # add player 2 score
            score_player2 += 1

            # random ball position
            ball.velocity = [-random_velocity(), randint(-8, 8)]

            # set ball position to center of screen
            ball.rect.x = 315
            ball.rect.y = 210

        if ball.rect.y >= 470 or ball.rect.y <= 55:
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
                    start = False
                    win = False
                
                # release key event
                if event.type == pygame.KEYUP:
                    # if key q released
                    if event.key == pygame.K_q:
                        # go to game menu
                        start = False
                        win = False
                        menu()

                    # if key n released
                    if event.key == pygame.K_n:
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

            # measure win text width and height
            win_width, win_height = font.size("Player 1 Win")

            # if player 1 win
            if (score_player1 == 10):
                win_text = font.render("P1 Win", 1, color_green)

                # draw text
                screen.blit(win_text, (200, 10))

            # if player 2 win
            else:
                win_text = font.render("P2 Win", 1, color_green)

                # draw text
                screen.blit(win_text, (width - 200, 10))

            # new game text
            newgame_text = font.render("Enter N for New Game, Q for Back to Menu", 1, color_red)

            # measure new game text width and height
            newgame_width, newgame_height = font.size("Enter N for New Game, Q for Back to Menu")

            # draw new game text to screen
            screen.blit(newgame_text, ((width / 2) - (newgame_width / 2), (height / 2) - (newgame_height / 2)))

            # update display
            pygame.display.flip()

        while pause:
            for event in pygame.event.get():
                # quit event
                if event.type == pygame.QUIT:
                    start = False
                    pause = False
                
                # release key event
                if event.type == pygame.KEYUP:
                    # if key q released
                    if event.key == pygame.K_q:
                        # go to game menu
                        start = False
                        pause = False
                        menu()

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
    menu()