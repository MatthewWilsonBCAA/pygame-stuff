import pygame
import random
import rooms
from angles import get_angle, project


#color initialization
colors = {
    "Black": (0, 0, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 245, 5),
    "Green": (0, 255, 0),
    "Purple": (255, 0, 255),
    "Red": (255, 0, 0)
    }

#all of the initialization
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont('Consolas', 30)

#screen initialization
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#frame rate stuff
FRAMERATE = 80

speed = 3
enemy_speed = 1
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -speed)
            if pygame.sprite.spritecollideany(player, walls):
                self.rect.move_ip(0, speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, speed)
            if pygame.sprite.spritecollideany(player, walls):
                self.rect.move_ip(0, -speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-speed, 0)
            if pygame.sprite.spritecollideany(player, walls):
                self.rect.move_ip(speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(speed, 0)
            if pygame.sprite.spritecollideany(player, walls):
                self.rect.move_ip(-speed, 0)
        #collisions
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
    def __init__(self, cor, size):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface(size)
        self.surf.fill((colors["Red"]))
        self.rect = self.surf.get_rect(center=cor)
    def update (self):
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
        if pygame.sprite.spritecollideany(self, walls):
            if cur_x != 0:
                cur_x *= -3
            elif cur_y != 0:
                cur_y *= -3
        self.rect.move_ip(cur_x * enemy_speed, cur_y * enemy_speed)

door_warp_list = []
selected_room = {}
def enter_room(ID):
    for wall in walls:
        wall.kill()
    for door in doors:
        door.kill()
    for enemy in enemies:
        enemy.kill()
    global selected_room
    global door_warp_list
    selected_room = rooms.room_list[ID]
    door_warp_list = []
    for wall in selected_room:
        cor = selected_room[wall]["cor"]
        size = selected_room[wall]["size"]
        if "exit" in wall:
            door_warp_list.append(wall)
            new_door = Door(cor, size)
            doors.add(new_door) 
            all_sprites.add(new_door)
        elif "enemy" in wall:
            new_enemy = Enemy(cor, size)
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)  
        else:
            color = selected_room[wall]["color"]
            new_wall = Wall(cor, size, color)
            walls.add(new_wall) 
            all_sprites.add(new_wall)

#defines the user inputs
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#used for initializing doors, enemies, and walls
walls = pygame.sprite.Group()
doors = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enter_room(0)


#player stats and stuff
player_hp = 5

running = True
while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(colors["Black"])
    z = 0
    for door in doors:
        if pygame.sprite.collide_rect(player, door):
            player.rect = player.surf.get_rect(center=selected_room[door_warp_list[z]]["warp"])
            enter_room(selected_room[door_warp_list[z]]["id"])
        z += 1
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    for enemy in enemies:
        if pygame.sprite.collide_rect(player, enemy):
            enemy.kill()
            player_hp -= 1

    if player_hp <= 0:
        player.kill()
        running = False
    text = str(player_hp)
    screen.blit(font.render(text, True, (255, 255, 0)), (30, 30))

    #gets the player input, and changes the game state accordingly
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    walls.update()
    enemies.update()
    doors.update()



    
    #renders the player
    screen.blit(player.surf, player.rect)

    # Flip the display
    pygame.display.flip()
    clock.tick(FRAMERATE)