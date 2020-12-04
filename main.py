from classes import *
import rooms
import json

try:
    sudo = open("save.json", "r")
    loading = True
except:
    loading = False

# all of the initialization

clock = pygame.time.Clock()
font = pygame.font.SysFont("Consolas", 30)
font_half = pygame.font.SysFont("Consolas", 15)

# screen initialization

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

door_warp_list = []
selected_room = {}


def enter_room(ID):
    for wall in walls:
        wall.kill()
    for door in doors:
        door.kill()
    for enemy in enemies:
        enemy.kill()
    for pick in pick_ups:
        pick.kill()
    for merch in merchants:
        merch.kill()
    global selected_room
    global door_warp_list
    global room_text
    global room_text_cor
    pygame.mixer.music.stop()
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
            hp = selected_room[wall]["hp"]
            xp = selected_room[wall]["xp"]
            power = selected_room[wall]["power"]
            name = selected_room[wall]["name"]
            speed = selected_room[wall]["speed"]
            ai = selected_room[wall]["ai"]
            new_enemy = Enemy(cor, size, hp, xp, power, name, speed, ai)
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif "pick" in wall:
            p_type = selected_room[wall]["p_type"]
            pick_up = PickUp(cor, size, p_type)
            pick_ups.add(pick_up)
            all_sprites.add(pick_up)
        elif "music" in wall:
            mus = selected_room[wall]["id"]
            pygame.mixer.music.load(mus)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.2)
        elif "name" in wall:
            room_text = selected_room[wall]["name"]
            room_text_cor = cor
        elif "npc" in wall:
            name = selected_room[wall]["name"]
            n_type = selected_room[wall]["type"]
            merch = Merchant(cor, size, name, n_type)
            merchants.add(merch)
            all_sprites.add(merch)
        else:
            color = selected_room[wall]["color"]
            new_wall = Wall(cor, size, color)
            walls.add(new_wall)
            all_sprites.add(new_wall)


# defines the user inputs


player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# used for initializing doors, enemies, and walls
walls = pygame.sprite.Group()
doors = pygame.sprite.Group()
enemies = pygame.sprite.Group()
blasts = pygame.sprite.Group()
pick_ups = pygame.sprite.Group()
merchants = pygame.sprite.Group()
room_text = ""
room_text_cor = (0, 0)

debug = False

if loading:
    with open("save.json") as json_file:
        main_save = json.load(json_file)
        roomID = main_save[0]
        enter_room(roomID)
        player_hp = main_save[1]
        player_max_hp = main_save[2]
        player_xp = main_save[3]
        player_lv = main_save[4]
        player_str = main_save[5]
        player_pow = main_save[6]
        player_def = main_save[7]
        gold = main_save[8]
        weapon_power = main_save[9]
        weapon_length_mod = main_save[10]
        player.rect.left = main_save[11]
        player.rect.top = main_save[12]
else:
    enter_room(0)
    roomID = 0
    player_hp = 25
    player_max_hp = 25
    player_xp = 0
    player_lv = 1
    player_str = 1
    player_pow = 1
    player_def = 1
    gold = 15
    # for weapon stats
    weapon_power = -1
    weapon_length_mod = 0
attack = False
attack_input = ""
i_timer = 0
timer = 0
running = True
showStats = False


while running == True:

    if debug:
        breakpoint()
        debug = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == pygame.K_t:
                attack_input = "t"
                attack = True
            elif event.key == pygame.K_f:
                attack_input = "f"
                attack = True
            elif event.key == pygame.K_g:
                attack_input = "g"
                attack = True
            elif event.key == pygame.K_h:
                attack_input = "h"
                attack = True
            elif event.key == pygame.K_b:
                debug = True

            if event.key == pygame.K_s:
                showStats = not showStats
            if event.key == pygame.K_w:
                for i in merchants:
                    if pygame.sprite.collide_rect(player, i):
                        if gold >= (weapon_length_mod + 1) * 10:
                            gold -= (weapon_length_mod + 1) * 10
                            weapon_length_mod += 2
                            weapon_power += 1

    screen.fill(colors["Black"])
    z = 0
    for door in doors:
        if pygame.sprite.collide_rect(player, door):
            player.rect = player.surf.get_rect(
                center=selected_room[door_warp_list[z]]["warp"]
            )
            roomID = selected_room[door_warp_list[z]][
                "id"
            ]  # used for saving their location!!!!
            enter_room(roomID)
        z += 1

    for pick in pick_ups:
        if pick.p_type == 0:
            screen.blit(
                font_half.render("Healing", True, (255, 255, 0)),
                (pick.rect.left, pick.rect.top - 20),
            )
            if pygame.sprite.collide_rect(player, pick):
                player_hp += 5
                pick.kill()
        elif pick.p_type == 1:
            screen.blit(
                font_half.render("10 Gold", True, (255, 255, 0)),
                (pick.rect.left, pick.rect.top - 20),
            )
            if pygame.sprite.collide_rect(player, pick):
                gold += 10
                pick.kill()
        elif pick.p_type == 2:
            screen.blit(
                font_half.render("20 Gold", True, (255, 255, 0)),
                (pick.rect.left, pick.rect.top - 20),
            )
            if pygame.sprite.collide_rect(player, pick):
                gold += 20
                pick.kill()

    if player_hp > player_max_hp:
        player_hp = player_max_hp
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    for merch in merchants:
        screen.blit(
            font_half.render("Stand on and press W", True, (255, 255, 0)),
            (merch.rect.left, merch.rect.top - 40),
        )
        screen.blit(
            font_half.render(
                "to upgrade weapon. Price: " + str((weapon_length_mod + 1) * 20),
                True,
                (255, 255, 0),
            ),
            (merch.rect.left, merch.rect.top - 20),
        )
    for enemy in enemies:
        screen.blit(
            font_half.render(enemy.name + ": " + str(enemy.hp), True, (255, 255, 0)),
            (enemy.rect.left, enemy.rect.top - 20),
        )
        if pygame.sprite.collide_rect(player, enemy) and i_timer == 0:
            player_hp -= max(enemy.power - player_def, 1)
            i_timer = 60

        if blasts and pygame.sprite.collide_rect(blast, enemy):
            enemy.hp -= weapon_power + player_str
            if enemy.hp <= 0:
                player_xp += enemy.xp
                enemy.kill()

    if player_hp <= 0:
        player.kill()
        running = False
    if i_timer > 0:
        i_timer -= 1

    # this is for attacking
    if attack == True and timer == 0:
        if attack_input == "t":
            blast = Weapon(
                (player.rect.left + 12, player.rect.top - 12 - weapon_length_mod),
                (10, 60 + weapon_length_mod),
            )
        elif attack_input == "f":
            blast = Weapon(
                (player.rect.left - 12 - weapon_length_mod, player.rect.top + 12),
                (60 + weapon_length_mod, 10),
            )
        elif attack_input == "g":
            blast = Weapon(
                (player.rect.left + 12, player.rect.top + 36 + weapon_length_mod),
                (10, 60 + weapon_length_mod),
            )
        elif attack_input == "h":
            blast = Weapon(
                (player.rect.left + 36 + weapon_length_mod, player.rect.top + 12),
                (60 + weapon_length_mod, 10),
            )
        blasts.add(blast)
        all_sprites.add(blast)
        timer = 40

    if timer > 0:
        timer -= 1
        # if timer >= 20:

        if timer < 10:
            blast.kill()
        if timer == 0:
            attack = False

    if player_xp > (player_lv * 50):
        player_xp -= player_lv * 50
        player_lv += 1
        player_max_hp += random.randint(2, 4)
        player_str += random.randint(1, 2)
        player_pow += random.randint(1, 2)
        player_def += random.randint(1, 2)

    # used for drawing stats on screen
    text = "HP: " + str(player_hp) + " / " + str(player_max_hp)
    screen.blit(
        font_half.render(text, True, (255, 255, 0)),
        (player.rect.left, player.rect.top - 25),
    )
    if showStats == True:
        text = "Lv " + str(player_lv) + " / XP: " + str(player_xp)
        screen.blit(
            font_half.render(text, True, (255, 255, 0)),
            (player.rect.left - 25, player.rect.top + 25),
        )
        text = "STR: " + str(player_str) + " / POW: " + str(player_pow)
        screen.blit(
            font_half.render(text, True, (255, 255, 0)),
            (player.rect.left - 35, player.rect.top + 40),
        )
        text = "DEF: " + str(player_def) + " / Gold: " + str(gold)
        screen.blit(
            font_half.render(text, True, (255, 255, 0)),
            (player.rect.left - 35, player.rect.top + 55),
        )
        text = "Weapon Lv: " + str(weapon_power)
        screen.blit(
            font_half.render(text, True, (255, 255, 0)),
            (player.rect.left - 35, player.rect.top + 70),
        )

    screen.blit(font.render(room_text, True, (255, 255, 0)), room_text_cor)
    # gets the player input, and changes the game state accordingly
    if timer == 0:
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys, walls)
    walls.update()
    enemies.update(player, walls, enemies, debug)
    doors.update()

    # renders the player
    screen.blit(player.surf, player.rect)

    # Flip the display
    pygame.display.flip()
    clock.tick(FRAMERATE)
if player_hp > 0:
    with open("save.json", "w") as json_file:
        main = []
        main.append(roomID)
        main.append(player_hp)
        main.append(player_max_hp)
        main.append(player_xp)
        main.append(player_lv)
        main.append(player_str)
        main.append(player_pow)
        main.append(player_def)
        main.append(gold)
        main.append(weapon_power)
        main.append(weapon_length_mod)
        main.append(player.rect.left)
        main.append(player.rect.top)
        json.dump(main, json_file)