#!/usr/bin/python
# coding=utf-8

def main():
    # ################################## #
    # Preparation: variables and set ups #
    # ################################## #

    import pygame
    import time
    import random
    # initiates the pygame functionalities
    pygame.init()
    # initiates the functionalities of the pygame library

    # Setting up the display and images #

    # 800x600 is the side of the window. It is passed as a tuple, ergo the ()
    # a tuple, because it's not 2 args, but just one with 2 numbers in it
    display_width = 800
    display_height = 600

    # Car image
    car_img = pygame.image.load('sports-car.jpeg')
    car_width = 60
    # making the car icon in the window. The proper icon is 32x32, but on mac, it doesn't show.
    pygame.display.set_icon(car_img)
    # Setting up the colors
    black = (0, 0, 0)
    # colors are set in rgb
    white = (255, 255, 255)
    red = (255, 0, 0)
    red2 = (245, 80, 70)
    green = (0, 205, 12)

    #sets the pause variable for the pause button
    on_pause = False

    # loads sounds
    crash_sound = pygame.mixer.Sound("bomb.wav")
    pygame.mixer.music.load("opening.wav")

    gameDisplay = pygame.display.set_mode((display_width, display_height))
    # this determines what will be at the top of the window
    pygame.display.set_caption('The game is on')

    # ############## #
    # Game functions #
    # ############## #


    # and the function that positions the car in the page:
    def car(x, y):
        # blit adds arg1 to the position of arg2(tuple)
        gameDisplay.blit(car_img, (x, y))

    def button(msg, x_pos, y_pos, width, height, active_color, inactive_color, click_action=None):
        # getting the mouse position in the display
        mouse = pygame.mouse.get_pos()
        # print(mouse)
        #getting the clicks
        click = pygame.mouse.get_pressed()
        # making the buttons
        # the rectangle is drawn with x, y position plus the sizes w and z
        if x_pos + width > mouse[0] > x_pos and y_pos + height > mouse[1] > y_pos:
            pygame.draw.rect(gameDisplay, active_color, (x_pos, y_pos, width, height))
            if click[0] == 1 and click_action != None:
                if click_action == "Play":
                    gameloop()
                elif click_action == "Quit":
                    game_quit()
                elif click_action == "Continue":
                    global on_pause
                    on_pause = False
        else:
            pygame.draw.rect(gameDisplay, inactive_color, (x_pos, y_pos, width, height))
        # text in the button
        myfont = pygame.font.SysFont(None, 60)
        text_surf, text_rect = text_objects(msg, myfont)
        text_rect.center = ((x_pos + (width / 2)), (y_pos + (height / 2)))
        gameDisplay.blit(text_surf, text_rect)
        # put it on the screen
        pygame.display.update()

    def pause():
        global on_pause
        on_pause = True
        while on_pause:
            k = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
           # Display the welcome text
            gameDisplay.fill(white)
            myfont = pygame.font.SysFont(None, 80)
            text_surf, text_rect = text_objects(" - Game paused - ", myfont)
            text_rect.center = ((display_width / 2), (display_height / 2))
            gameDisplay.blit(text_surf, text_rect)
            # adds the buttons
            # using the button(msg, x_pos, y_pos, width, height, active_color, inactive_color, click_action) function
            button("Cont..", 150, 450, 100, 50, black, green, "Continue")
            button("Quit", 550, 450, 100, 50, red, red2, "Quit")

    def game_intro():
        #plays entry music once (1) - you make it (-1) for an indefinite sound loop
        pygame.mixer.music.play(1)
        #sets the loop
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
           # Display the welcome text
            gameDisplay.fill(white)
            myfont = pygame.font.SysFont(None, 80)
            text_surf, text_rect = text_objects(" - Welcome - ", myfont)
            text_rect.center = ((display_width / 2), (display_height / 2))
            gameDisplay.blit(text_surf, text_rect)
            # adds the buttons
            # using the button(msg, x_pos, y_pos, width, height, active_color, inactive_color, click_action) function
            button("Go", 150, 450, 100, 50, black, green, "Play")
            button("Quit", 550, 450, 100, 50, red, red2, "Quit")

    def crash():
        #stop the music:
        pygame.mixer.music.stop()
        #play the crash sound:
        pygame.mixer.Sound.play(crash_sound)
        crashed = True
        while crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
           # Display the welcome text
            gameDisplay.fill(white)
            myfont = pygame.font.SysFont(None, 80)
            text_surf, text_rect = text_objects(" - You Crashed - ", myfont)
            text_rect.center = ((display_width / 2), (display_height / 2))
            gameDisplay.blit(text_surf, text_rect)
            # adds the buttons
            # using the button(msg, x_pos, y_pos, width, height, active_color, inactive_color, click_action) function
            button("Again", 150, 450, 100, 50, black, green, "Play")
            button("Quit", 550, 450, 100, 50, red, red2, "Quit")

    # the functions for text messaging
    def text_objects(text, font):
        text_surface = font.render(text, True, red)
        return text_surface, text_surface.get_rect()

    def message_display(text):
        myfont = pygame.font.SysFont(None, 80)
        text_surf, text_rect = text_objects(text, myfont)
        text_rect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(text_surf, text_rect)
        pygame.display.update()
        # display for 1 sec:
        time.sleep(3)
        # re-starts the game
        gameloop()
        # quit()


    # obstacles
    def obstacles(x_pos, y_pos, obs_w, obs_h, color):
        pygame.draw.rect(gameDisplay, color, [x_pos, y_pos, obs_w, obs_h])

    # The score
    def score(count):
        font = pygame.font.SysFont(None, 46)
        text = font.render("Scaped " + str(count), True, black)
        gameDisplay.blit(text, (0, 0))

    def game_quit():
        pygame.quit()
        quit()

    # ################## #
    # Game loop function #
    # ################## #

    def gameloop():
        # making an initial car position in the middle:
        x = (display_width * 0.45)
        y = (display_height * 0.45)
        x_change = 0

        #making obstacles
        obs_startx = random.randrange(0, display_width)
        obs_starty = - 300
        obs_speed = 7
        obs_width = 100
        obs_height = 100
        dodge = 0

        clock = pygame.time.Clock()

        game_exit = False
        while not game_exit:
            for event in pygame.event.get():
                # Quiting routine (including 'x' of the window)
                if event.type == pygame.QUIT:
                    game_exit = True
                    # end of the game #
                    pygame.quit()
                    quit()
                # moving routine
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_change = -5
                    elif event.key == pygame.K_RIGHT:
                        x_change = 5
                    elif event.key == pygame.K_p:
                        pause()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        x_change = 0

            #making a background color
            gameDisplay.fill(white)

            # the x_change moves the car
            x += x_change

            # adding the obstacles (def obstacles(x_pos, y_pos, obs_w, obs_h, color))
            obstacles(obs_startx, obs_starty, obs_width, obs_height, black)
            obs_starty += obs_speed

            # adding the car
            car(x, y)
            score(dodge)

            # checking for going beyong boundaries of the screen:
            if x > display_width - car_width or x < 0:
                crash()

            # checking obstacle out of the screen:
            if obs_starty > display_height:
                obs_starty = 0 - obs_height
                obs_startx = random.randrange(0, display_width)
                dodge += 1
                obs_speed += 1


            # checking for colision:
            # 1) for colision, the object must be lower or at the same pos
            # as the car (above, it simply didn't hit the car
            if y < obs_starty + obs_height:
                # crossed y axis
                if x > obs_startx and x < obs_startx + obs_width:
                    crash()
                elif x + car_width > obs_startx and x + car_width < obs_startx + obs_width:
                    crash()


            # update(or flip) goes to the next stage in the animation process
            # this is closely related to the clock.tick that determines frames per second
            pygame.display.update()
            # clock.tick determines the frames per second. Higher number = smoother
            clock.tick(60)

    # ##################### #
    # Start the game        #
    # ##################### #

    # intro
    game_intro()
    # Since the game starts from the intro, you don't need to call that function here




if __name__ == '__main__':
    main()