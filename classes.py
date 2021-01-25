import pygame
import random
from constants import *

pygame.init()
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    K_t,
    K_f,
    K_g,
    K_h,
    K_s,
    K_w,
    K_b,
    KEYDOWN,
    QUIT,
)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill(colors["White"])
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys, walls):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -speed)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(0, speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, speed)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(0, -speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-speed, 0)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(speed, 0)
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.move_ip(-speed, 0)
        # collisions
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Wall(pygame.sprite.Sprite):
    def __init__(self, cor, size, color):
        super(Wall, self).__init__()
        self.surf = pygame.Surface(size)
        self.surf.fill(colors[color])
        self.rect = self.surf.get_rect(center=cor)


class Door(pygame.sprite.Sprite):
    def __init__(self, cor, size):
        super(Door, self).__init__()
        self.surf = pygame.Surface(size)
        self.surf.fill(colors["Yellow"])
        self.rect = self.surf.get_rect(center=cor)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, cor, image_name, hp, xp, power, name, speed, ai):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(image_name).convert_alpha()
        # self.surf.fill((colors["Red"]))
        self.hp = hp
        self.xp = xp
        self.power = power
        self.name = name
        self.rect = self.surf.get_rect(center=cor)
        self.speed = speed
        self.ai = ai
        self.timer = 0

    def update(self, player, walls, enemies, debug):
        self_x = self.rect.left
        self_y = self.rect.top
        p_x = player.rect.left
        p_y = player.rect.top
        cur_x = 0
        cur_y = 0
        if self_x > p_x:
            if self_y > p_y:
                cur_x = -1
                cur_y = -1
            elif self_y < p_y:
                cur_x = -1
                cur_y = 1
            else:
                cur_x = -1
                cur_y = 0
        elif self_x < p_x:
            if self_y > p_y:
                cur_x = 1
                cur_y = -1
            elif self_y < p_y:
                cur_x = 1
                cur_y = 1
            else:
                cur_x = 1
                cur_y = 0
        else:
            if self_y > p_y:
                cur_x = 0
                cur_y = -1
            elif self_y < p_y:
                cur_x = 0
                cur_y = 1
        hit = False
        is_enemy = False
        for i in walls:
            if pygame.sprite.collide_rect(self, i):
                hit = True
                temp = i
        for i in enemies:
            if pygame.sprite.collide_rect(self, i) and i != self:
                hit = True
                is_enemy = True
                temp = i
        if hit == True:
            if cur_x != 0 and cur_y != 0:
                if is_enemy == False:
                    obj_wid = int(temp.surf.get_size()[0] / 2)
                    obj_hi = int(temp.surf.get_size()[1] / 2)
                else:
                    obj_wid = 50
                    obj_hi = 50
                is_dumb = 0
                if self.rect.left >= temp.rect.left + obj_wid:
                    cur_x = -1
                    cur_y = 0
                    is_dumb += 1
                if self.rect.left < temp.rect.left + obj_wid:
                    cur_x = 1
                    cur_y = 0
                    is_dumb += 1
                if self.rect.top >= temp.rect.top + obj_hi:
                    cur_y = -1
                    cur_x = 0
                    is_dumb += 1
                if self.rect.top < temp.rect.top + obj_hi:
                    cur_y = 1
                    cur_x = 0
                    is_dumb += 1
                if is_dumb > 1:
                    cur_y *= -1
                    cur_x *= -1
                # else:
                #     cur_y = random.randint(-10, 10)
                #     cur_x = random.randint(-10, 10)
            elif cur_x != 0 and cur_y == 0:
                # if self_y < p_y:
                #     cur_y = 1
                # else:
                #     cur_y = -1
                cur_y = cur_x
                cur_x = 0
            elif cur_x == 0 and cur_y != 0:
                # if self_x < p_x:
                #     cur_x = 1
                # else:
                #     cur_x = -1
                cur_x = cur_y
                cur_y = 0
            if is_enemy == True:
                cur_x = random.randint(-2, 2)
                cur_y = random.randint(-2, 2)
        self.rect.move_ip(cur_x * self.speed, cur_y * self.speed)
        if debug:
            print(f"{self.name}: {cur_x}, {cur_y}")
        # this is for summoners
        if self.ai == 1:
            self.timer += 1
            if self.timer > 400:
                self.timer = 0
                new_enemy = Enemy(
                    (
                        self.rect.left
                        + self.surf.get_size()[0]
                        + random.randint(20, 40),
                        self.rect.top,
                    ),
                    "knight.png",
                    100,
                    1,
                    5,
                    "Minion",
                    2,
                    0,
                )
                enemies.add(new_enemy)
                # all_sprites.add(new_enemy)


class Weapon(pygame.sprite.Sprite):
    def __init__(self, cor, size):
        super(Weapon, self).__init__()
        self.surf = pygame.Surface(size)
        self.surf.fill((colors["Blue"]))
        self.rect = self.surf.get_rect(center=cor)


class PickUp(pygame.sprite.Sprite):
    def __init__(self, cor, size, p_type):
        super(PickUp, self).__init__()
        self.surf = pygame.Surface(size)
        self.surf.fill((colors["Purple"]))
        self.rect = self.surf.get_rect(center=cor)
        self.p_type = p_type  # 0 is healing, 1 is gold


class Merchant(pygame.sprite.Sprite):
    def __init__(self, cor, size, name, n_type):
        super(Merchant, self).__init__()
        self.surf = pygame.Surface(size)
        self.surf.fill((colors["White"]))
        self.rect = self.surf.get_rect(center=cor)
        self.name = name
        self.n_type = n_type
