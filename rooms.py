from enemies import *

entry_room = {
    "name": {"cor": (380, 50), "size": (0, 0), "name": "Entry"},
    "1": {"cor": (100, 200), "size": (20, 500), "color": "Green"},
    "2": {"cor": (300, 300), "size": (20, 400), "color": "Green"},
    "3": {"cor": (500, 100), "size": (40, 400), "color": "Blue"},
    "exit": {"cor": (500, 400), "size": (10, 200), "warp": (20, 300), "id": 1},
}

main_hall = {
    "name": {"cor": (150, 50), "size": (0, 0), "name": "Main Entrance Hall"},
    "1": {"cor": (300, 185), "size": (600, 30), "color": "Blue"},
    "2": {"cor": (300, 415), "size": (600, 30), "color": "Blue"},
    "exit_L": {"cor": (0, 300), "size": (10, 200), "warp": (480, 400), "id": 0},
    "exit_R": {"cor": (500, 300), "size": (10, 200), "warp": (20, 300), "id": 2},
    "enemy_1": hound,
    "music": {"cor": (0, 0), "size": (0, 0), "id": "dubstep.ogg"},
}

throne_room = {
    "name": {"cor": (250, 350), "size": (0, 0), "name": "Throne Room"},
    "1": {"cor": (250, 250), "size": (50, 50), "color": "Blue"},
    "2": {"cor": (0, 50), "size": (20, 300), "color": "Blue"},
    "3": {"cor": (0, 450), "size": (20, 100), "color": "Blue"},
    "4": {"cor": (100, 0), "size": (200, 20), "color": "Blue"},
    "5": {"cor": (400, 0), "size": (200, 20), "color": "Blue"},
    "6": {"cor": (500, 50), "size": (20, 300), "color": "Blue"},
    "7": {"cor": (500, 450), "size": (20, 100), "color": "Blue"},
    "exit_L": {"cor": (0, 300), "size": (10, 200), "warp": (480, 300), "id": 1},
    "exit_U": {"cor": (250, 00), "size": (100, 10), "warp": (250, 480), "id": 3},
    "exit_R": {"cor": (500, 300), "size": (10, 200), "warp": (20, 300), "id": 4},
    "exit_D": {"cor": (250, 500), "size": (100, 10), "warp": (250, 20), "id": 5},
    "pick_1": {"cor": (300, 250), "size": (15, 15), "p_type": 0},
    "pick_2": {"cor": (200, 250), "size": (15, 15), "p_type": 0},
    "pick_3": {"cor": (250, 300), "size": (15, 15), "p_type": 0},
    "music": {"cor": (0, 0), "size": (0, 0), "id": "dubstep.ogg"},
}

balcony = {
    "name": {"cor": (150, 0), "size": (0, 0), "name": "Balcony"},
    "1": {"cor": (250, 350), "size": (500, 10), "color": "Blue"},
    "2": {"cor": (100, 100), "size": (10, 50), "color": "Green"},
    "3": {"cor": (250, 100), "size": (10, 50), "color": "Green"},
    "4": {"cor": (90, 200), "size": (10, 50), "color": "Green"},
    "exit_D": {"cor": (250, 500), "size": (100, 10), "warp": (250, 20), "id": 2},
    "music": {"cor": (0, 0), "size": (0, 0), "id": "wind.ogg"},
    "npc_1": {"cor": (200, 400), "size": (30, 30), "name": "John", "type": 0},
}
eatery = {
    "name": {"cor": (250, 30), "size": (0, 0), "name": "Eatery"},
    "exit_L": {"cor": (0, 300), "size": (10, 200), "warp": (480, 300), "id": 2},
    "1": {"cor": (250, 250), "size": (300, 40), "color": "Blue"},
    "2": {"cor": (0, 50), "size": (20, 300), "color": "Blue"},
    "3": {"cor": (0, 450), "size": (20, 100), "color": "Blue"},
    "4": {"cor": (250, 0), "size": (500, 20), "color": "Blue"},
    "pick_1": {"cor": (400, 350), "size": (15, 15), "p_type": 1},
    "enemy_1": guard,
    "enemy_2": guard,
    "enemy_3": summoner,
}
eatery["enemy_2"]["cor"] = (300, 300)
lower_castle = {
    "name": {"cor": (150, 450), "size": (0, 0), "name": "Lower Castle Halls"},
    "1": {"cor": (250, 200), "size": (400, 80), "color": "Blue"},
    "exit_U": {"cor": (250, 0), "size": (100, 10), "warp": (250, 480), "id": 2},
    "enemy_1": dragon,
    "pick_1": {"cor": (100, 350), "size": (15, 15), "p_type": 2},
    "pick_2": {"cor": (100, 400), "size": (15, 15), "p_type": 2},
    "pick_3": {"cor": (100, 450), "size": (15, 15), "p_type": 2},
    "exit_R": {"cor": (500, 50), "size": (10, 100), "warp": (20, 50), "id": 6},
}
lower_castle_halls = {
    "name": {"cor": (150, 450), "size": (0, 0), "name": "Lower Castle Halls"},
    "1": {"cor": (250, 200), "size": (400, 80), "color": "Blue"},
    "exit_L": {"cor": (0, 50), "size": (10, 100), "warp": (480, 50), "id": 5},
}

room_list = [
    entry_room,
    main_hall,
    throne_room,
    balcony,
    eatery,
    lower_castle,
    lower_castle_halls,
]
