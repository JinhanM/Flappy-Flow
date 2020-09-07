"""
The classic game of flappy bird. Make with python
and pygame.
一时兴起

Date created: Sep 2, 2020
Author: JinhanM
Reference: techwithtim
"""

import pygame
import time
import os
import random

pygame.font.init()
WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
GAMEOVER_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "gameover.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROL_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def fly(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        self.y = self.y + d

        # 向上升
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            # 向下降?
            if self.tilt > -90:
                self.tilt -= self.ROL_VEL

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 100

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        t_point = bird_mask.overlap(top_mask, top_offset)
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)

        if t_point or b_point:
            return True
        return False


class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_active(win, bird, pipes, score):
    win.blit(BG_IMG, (0, 0))

    pygame.display.update()
    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, ((WIN_WIDTH - 10 - text.get_width())/2, 10))

    bird.draw(win)


def draw_game_over(win, score, highest_score):
    win.blit(BG_IMG, (0, 0))

    score_text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(score_text, ((WIN_WIDTH - 10 - score_text.get_width())/2, 40))

    high_score_text = STAT_FONT.render("Highest score: " + str(highest_score), 1, (255, 255, 255))
    win.blit(high_score_text, ((WIN_WIDTH - 20 - high_score_text.get_width())/2, 550))

    win.blit(GAMEOVER_IMG, GAMEOVER_IMG.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2)))


def cal_high_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def main():
    bird = Bird(230, 350)
    base = Base(700)
    pipes = [Pipe(700)]
    pygame.init()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    MESSAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "message.png")).convert_alpha())
    score, high_score = 0, 0

    first_run, run = True, False
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and run:
                if event.key == pygame.K_SPACE:
                    bird.fly()
            if event.type == pygame.KEYDOWN and not run:
                time.sleep(0.5)
                first_run, run = False, True
                score = 0
                bird.y = 350
                pipes = [Pipe(700)]
        if first_run:
            win.blit(BG_IMG, (0, 0))
            win.blit(MESSAGE, MESSAGE.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2)))
        else:
            if run:
                bird.move()
                add_pipe = False
                rem = []
                for pipe in pipes:
                    if pipe.collide(bird):
                        run = False
                    if bird.y + bird.img.get_height() >= 730:
                        run = False
                    if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                        rem.append(pipe)

                    if not pipe.passed and pipe.x < bird.x:
                        pipe.passed = True
                        add_pipe = True

                    pipe.move()

                if add_pipe:
                    score += 1
                    pipes.append(Pipe(550))

                for r in rem:
                    pipes.remove(r)
                draw_active(win, bird, pipes, score)
            else:
                # print("not run now")
                high_score = cal_high_score(score, high_score)
                draw_game_over(win, score, high_score)
        base.move()
        base.draw(win)

        pygame.display.update()


if __name__ == '__main__':
    main()
