import os 
import random
import math
import pygame as pg
from os import listdir
from os.path import isfile, join

pg.init()
pg.display.set_caption("Game.exe")

WIDTH, HEIGHT = 1000, 800
FPS = 60  

window = pg.display.set_mode((WIDTH,HEIGHT))

def flip(sprites):
    return[pg.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheet(dir1, dir2, width, height, direction = False):
    path = join("assets", dir1, dir2)
    images = [i for i in listdir(path) if isfile(join(path, i))]

    all_sprites = {}

    for image in images :
        sprite_sheet = pg.image.load(join(path, image)).convert_alpha() # allow transparent background

        sprites = []

        for i in range(sprite_sheet.get_width() // width):
            surface = pg.Surface((width, height),pg.SRCALPHA, 32)
            rect = pg.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0,0), rect)
            sprites.append(pg.transform.scale2x(surface))
        
        if direction :
            all_sprites[image.replace(".png", "")+ ("_right")] = sprites
            all_sprites[image.replace(".png", "")+ ("_left")] = flip(sprites)
        else :
            all_sprites[image.replace(".png","")] = sprites

    return all_sprites

class Player(pg.sprite.Sprite):
    VELOCITY = 5
    COLOR = (45, 200, 255)
    GRAVITY = 1
    SPRITES = load_sprite_sheet("MainCharacters", "NinjaFrog", 32, 32, True )

    def __init__(self, x, y, width, height):
        self.rect = pg.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
    
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy 

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self,vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        # self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
    
    def draw(self, window):
        self.sprite = self.SPRITES["idle_" + self.direction][0]
        window.blit(self.sprite, (self.rect.x, self.rect.y))

def get_background(bg_name):
    image = pg.image.load(join("assets", "Background", bg_name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range (WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            position = (i * width, j * height)
            tiles.append(position)

    return tiles,image

def draw(window, background, bg_image, player):
    for tile in background:
        window.blit(bg_image, tile)

    player.draw(window)

    pg.display.update()

def move_handling(player):
    key = pg.key.get_pressed()

    player.x_vel = 0
    if key[pg.K_LEFT] or key[pg.K_a]:
        player.move_left(player.VELOCITY)
    if key[pg.K_RIGHT] or key[pg.K_d]:
        player.move_right(player.VELOCITY)

    player.y_vel = 0
    

def main(window):
    clock = pg.time.Clock()
    background, bg_image = get_background("Brown.png")

    player = Player(100, 100, 50, 50)

    run = True
    while run:
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
        
        player.loop(FPS)
        move_handling(player)
        draw(window, background, bg_image, player)
        
    pg.quit()
    quit()

if __name__ == "__main__":

    main(window)