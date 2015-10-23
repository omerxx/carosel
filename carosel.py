# Welcome to Carousel game!
# The game consists of an 8 seat carousel with a start point on its left and finish on its right
# To gain points, try jumping on free seats and get back down without falling
# Hit 'ENTER' to make every move
# Created using PyGame 1.9

import math
import sys
import pygame
from pygame.locals import *


class SeatSprite(pygame.sprite.Sprite):
    def __init__(self, image, position, is_vacant, degree):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.position = position
        self.is_vacant = is_vacant
        self.degree = degree

    def update(self, rect, deg):
        x = rect.center[0] + radius*math.cos(math.radians(self.degree+deg))
        y = rect.center[1] + radius*math.sin(math.radians(self.degree+deg))
        self.position = (x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def update_image(self, image):
        self.image = pygame.image.load(image)

    def distance(self, to_point):
        return math.sqrt(((self.position[0]-to_point[0])**2) + ((self.position[1]-to_point[1])**2))


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/boy_1.png')
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def update_image(self, image):
        self.image = pygame.image.load(image)


class FinishSprite(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/finish.png')
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def update_image(self, image):
        self.image = pygame.image.load(image)


def create_carousel_sprites(rect):
    # Creating a list of 8 seats on a circle
    global carousel_sprites
    for s in range(1, 9):
        new_angle = 0 if None else math.radians((s-1)*45)
        if s % 2 != 0:
            carousel_sprites.append(SeatSprite('images/boy_4.png', (rect.center[0] + radius * math.cos(new_angle),
                                                                    rect.center[1] + radius * math.sin(new_angle)),
                                               (s % 2 == 0), (s-1)*45))

        else:
            carousel_sprites.append(SeatSprite('images/free_seat.png', (rect.center[0] + radius * math.cos(new_angle),
                                                                        rect.center[1] + radius * math.sin(new_angle)),
                                               (s % 2 == 0), (s-1)*45))


def closest_seat_sprite(player_pos):
    # Receives the player's position and returns the nearest seat
    min_dist = 2 * radius
    chosen_seat = 0
    for seat in carousel_sprites:
        if seat.distance(player_pos) < min_dist:
            chosen_seat = seat
            min_dist = seat.distance(player_pos)
    return chosen_seat


def game_over(screen):
    screen.fill((0, 0, 0))
    largetext = pygame.font.SysFont("comicsansms", 80)
    smalltext = pygame.font.SysFont("comicsansms", 30)
    text = largetext.render("GAME OVER", 1, (255, 255, 0))
    text2 = smalltext.render("Hit any key to exit", 1, (255, 255, 0))
    text3 = smalltext.render("Your score is: " + str(score), 1, (255, 255, 0))

    screen.blit(text, (225, 200))
    screen.blit(text2, (330, 350))
    screen.blit(text3, (330, 400))

    while True:
        for event in pygame.event.get():
            if not hasattr(event, 'key'):
                continue
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                quit()

        pygame.display.update()


def control(target1, target2, img1, img2, upscore, newseat, upspeed=0):
    global score, sitted, speed
    target1.update_image('images/' + img1)
    target2.update_image('images/' + img2)
    score += upscore
    sitted = newseat
    speed += upspeed


# GLOBALS
carousel_sprites = []
radius = 150
score = 0
sitted = -1
speed = 1


def main():
    global speed, score, sitted
    deg = 0
    start_position = (150, 275)
    lives = 3

    pygame.init()
    myfont = pygame.font.SysFont("monospace", 30)
    screen = pygame.display.set_mode((940, 560), 0, 32)
    rect = screen.get_rect()
    player = PlayerSprite((150, 275))
    finish = FinishSprite((775, 275))

    create_carousel_sprites(rect)
    seat_0 = carousel_sprites[0]
    seat_1 = carousel_sprites[1]
    seat_2 = carousel_sprites[2]
    seat_3 = carousel_sprites[3]
    seat_4 = carousel_sprites[4]
    seat_5 = carousel_sprites[5]
    seat_6 = carousel_sprites[6]
    seat_7 = carousel_sprites[7]
    seats_group = pygame.sprite.RenderPlain(seat_0, seat_1, seat_2, seat_3, seat_4, seat_5, seat_6, seat_7)
    player_group = pygame.sprite.RenderPlain(player)
    finish_group = pygame.sprite.RenderPlain(finish)

    # GAME LOOP
    while True:
        if lives == 0:
            game_over(screen)

        # USER INPUT
        for event in pygame.event.get():
            if not hasattr(event, 'key'):
                continue

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == K_RETURN:
                    if sitted == (-1):                                          # player is still at starting point
                        target_seat = closest_seat_sprite(start_position)
                        if target_seat.is_vacant:
                            control(player, target_seat, 'start.png', 'boy_1.png', 10, target_seat)
                        else:
                            lives -= 1

                    elif sitted == 8:                                           # player is at finish point
                        target_seat = closest_seat_sprite(finish.position)
                        if target_seat.is_vacant:
                            control(finish, target_seat, 'finish.png', 'boy_1.png', 10, target_seat)
                        else:
                            lives -= 1

                    else:                                                       # player is on the carousel
                        target_seat = closest_seat_sprite(finish.position)
                        target_seat2 = closest_seat_sprite(start_position)
                        if target_seat == sitted:
                            control(finish, sitted, 'boy_1.png', 'free_seat.png', 50, 8, 1)
                        elif target_seat2 == sitted:
                            control(player, sitted, 'boy_1.png', 'free_seat.png', 50, -1, 1)
                        else:
                            lives -= 1

        # RENDERING
        screen.fill((0, 0, 0))
        deg += speed

        score_label = myfont.render("Score: " + str(score), 1, (255, 255, 0))
        lives_label = myfont.render("Lives: " + str(lives), 1, (255, 255, 0))
        speed_label = myfont.render("Speed: " + str(speed), 1, (255, 255, 0))
        text_label = myfont.render("Press ENTER to jump, or ESC to quit", 1, (255, 255, 0))

        screen.blit(score_label, (50, 35))
        screen.blit(lives_label, (50, 70))
        screen.blit(speed_label, (50, 105))
        screen.blit(text_label, (160, 500))

        finish_group.draw(screen)
        player_group.draw(screen)

        seats_group.update(rect, deg)
        seats_group.draw(screen)
        pygame.display.flip()

main()
