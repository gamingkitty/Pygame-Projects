import pygame
import sys
import player
import sans_enemy
import rock_lobber
import random
import bar
import button
import shopitem
import BossMain
import medpack
import relic


# KEEP CODE CLEAN
# KCC


while True:
    pygame.init()
    pygame.event.set_allowed([pygame.KEYDOWN, pygame.QUIT, pygame.KEYUP, pygame.MOUSEBUTTONDOWN])

    SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption('Ghost Game')

    screen_width = SCREEN.get_width()
    screen_height = SCREEN.get_height()

    # Just takes into account the screen width to maintain aspect ratio on images.
    screen_scaler = (screen_width/1920 + screen_height/1080)/2

    CLOCK = pygame.time.Clock()
    TimeTracker = pygame.time.Clock()
    time_elapsed_since_last_second = 0
    FPS = 60
    seconds = 00
    minutes = 00
    hours = 00

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (28, 128, 28)
    YELLOW = (230, 230, 0)
    BROWN = (118, 92, 72)
    GRAY = (175, 175, 175)
    DARK_GRAY = (99, 102, 106)
    BLUE = (12, 246, 242)
    AQUA = (5, 195, 221)
    RED = (255, 0, 0)

    # speed, max_hp, attack_power, projectile_speed, scream_delay, max_bullets, pierce, shield_duration, reload_speed, shield_cooldown_time, reload_bar, medpack_chance, size=(64, 64)
    ghost_player = player.Player(5, 300, 10, 10, 60, 10, 1, 300, 120, 1800, bar.Bar(0, (51, 9), (200, 120), YELLOW, DARK_GRAY, 1, 1), 5, (int(64 * screen_scaler), int(64 * screen_scaler)))
    ghost_player.rect.center = (screen_width/2, screen_height/2)

    screams = []
    sanses = []
    rocks = []
    Bosses = []
    missles = []
    rock_lobbers = []
    medpacks = []

    sans_spawn_timer = 200
    sans_spawn_delay = 500

    #only starts spawning after some time
    rock_lobber_timer = 6000
    rock_lobber_spawn_delay = 1000


    #screen visuals for menus
    #button: image_path, size, location
    quit_button = button.Button(pygame.image.load("Sprites/quit.png"), (int(262 * screen_scaler), int(92 * screen_scaler)), (screen_width / 2, screen_height / 1.8))

    replay_button = button.Button(pygame.image.load("Sprites/replay.png"), (int(262 * screen_scaler), int(82 * screen_scaler)), (screen_width / 2, screen_height / 1.53))

    darken_surface = pygame.Surface((screen_width, screen_height))
    darken_surface.set_alpha(128)
    darken_surface.fill((0, 0, 0))

    #shop visuals
    shop_rectangle = pygame.Rect((screen_width * 0.75, 0), (screen_width * 0.25, screen_height))
    shop_surface = pygame.Surface((screen_width * 0.25, screen_height))
    shop_surface.fill(BROWN)

    #shop items
    #price, price_increase, display_text, text_color, font_size, background_color, size, location, upgrade_type, upgrade_amount, max_amount
    attack_upgrade = shopitem.ShopItem(1, 1, "Attack", YELLOW, int(60 * screen_scaler), DARK_GRAY, (int(130 * screen_scaler), int(40 * screen_scaler)), (screen_width * 0.88, 60 + int(140 * screen_scaler)), "attack", 5, 15, screen_scaler)
    hp_upgrade = shopitem.ShopItem(1, 1, "Health", YELLOW, int(60 * screen_scaler), DARK_GRAY, (int(135 * screen_scaler), int(40 * screen_scaler)), (screen_width * 0.88, 60 + int(230 * screen_scaler)), "hp", 50, 30, screen_scaler)
    speed_upgrade = shopitem.ShopItem(1, 2, "Speed", YELLOW, int(60 * screen_scaler), DARK_GRAY, (int(125 * screen_scaler), int(40 * screen_scaler)), (screen_width * 0.88, 60 + int(320 * screen_scaler)), "speed", 1, 10, screen_scaler)
    pierce_upgrade = shopitem.ShopItem(3, 3, "Pierce", YELLOW, int(60 * screen_scaler), DARK_GRAY, (int(130 * screen_scaler), int(40 * screen_scaler)), (screen_width * 0.88, 60 + int(410 * screen_scaler)), "pierce", 1, 5, screen_scaler)
    attack_speed_upgrade = shopitem.ShopItem(1, 1, "Attack Speed", YELLOW, int(60 * screen_scaler), DARK_GRAY, (int(270 * screen_scaler), int(40 * screen_scaler)), (screen_width * 0.88, 60 + int(500 * screen_scaler)), "attack_speed", 5, 10, screen_scaler)
    bullets_upgrade = shopitem.ShopItem(1, 0, "Screams", YELLOW, int(60 * screen_scaler), DARK_GRAY, (int(152 * screen_scaler), int(40 * screen_scaler)), (screen_width * 0.88, 60 + int(590 * screen_scaler)), "max_bullets", 10, 5, screen_scaler)
    shield_unlock_upgrade = shopitem.ShopItem(3, 0, "Unlock Shield", YELLOW, int(60 * screen_scaler), DARK_GRAY, (int(282 * screen_scaler), int(40 * screen_scaler)), (screen_width * 0.88, 60 + int(680 * screen_scaler)), "shield_unlock", 2, 1, screen_scaler)

    #relics
    medpack_relic = relic.Relic(pygame.image.load("Sprites/Relics/medpackrelic.png"), (120, 200),
                                (-500, screen_height/2), "medpack")
    reload_relic = relic.Relic(pygame.image.load("Sprites/Relics/reloadrelic.png"), (120, 200),
                               (-500, screen_height / 2), "reload")
    lifesteal_relic = relic.Relic(pygame.image.load("Sprites/Relics/lifestealrelic.png"), (120, 200),
                                  (-500, screen_height / 2), "lifesteal")
    max_upgrade_relic = relic.Relic(pygame.image.load("Sprites/Relics/maxupgraderelic.png"), (120, 200),
                                    (-500, screen_height / 2), "maxupgrade")
    scream_shield_relic = relic.Relic(pygame.image.load("Sprites/Relics/screamshieldrelic.png"), (120, 200),
                                      (-500, screen_height / 2), "screamshield")
    upgrade_point_relic = relic.Relic(pygame.image.load("Sprites/Relics/upgradepointrelic.png"), (120, 200),
                                      (-500, screen_height / 2), "upgradepoint")
    heal_relic = relic.Relic(pygame.image.load("Sprites/Relics/healrelic.png"), (120, 200),
                             (-500, screen_height / 2), "heal")
    heat_seeking_relic = relic.Relic(pygame.image.load("Sprites/Relics/heatseekingrelic.png"), (120, 200),
                               (-500, screen_height / 2), "heatseeking")
    spawn_rate_relic = relic.Relic(pygame.image.load("Sprites/Relics/spawnraterelic.png"), (120, 200),
                                (-500, screen_height/2), "spawnrate")

    offered_relics = [medpack_relic, reload_relic, lifesteal_relic, max_upgrade_relic, scream_shield_relic,
                      upgrade_point_relic, heal_relic, heat_seeking_relic, spawn_rate_relic]

    #bars
    #percent_full, size, location, color, background_color, border_percentx, border_percenty
    #the border_percentx/y is just like how much bigger the border is than the bar, 1, 1 is same size
    exp_bar = bar.Bar(1, (int(301 * screen_scaler), int(25 * screen_scaler)), (50 + int((301 * screen_scaler)/2), 50 + int(30 * screen_scaler)), BLUE, DARK_GRAY, 0.98, 0.8)
    hp_bar = bar.Bar(1, (int(301 * screen_scaler), int(25 * screen_scaler)), (50 + int((301 * screen_scaler)/2), 50 + int(70 * screen_scaler)), RED, DARK_GRAY, 0.98, 0.8)

    def spawn_sans(attack_power, speed, attack_speed, max_hp):
        new_sans = sans_enemy.Sans(attack_power * (1 + ghost_player.level / 12), speed * (1 + ghost_player.level / 35), attack_speed, max_hp * (1 + ghost_player.level / 10), bar.Bar(1, (51, 9), (0, 0), RED, DARK_GRAY, 1, 1), (int(74 * screen_scaler), int(74 * screen_scaler)))
        new_sans.rect.center = (random.choice([0, screen_width]), random.choice([0, screen_height]))
        sanses.append(new_sans)

    def spawn_rock_lobber(attack_power, speed, attack_speed, max_hp, rock_time):
        new_rock_lobber = rock_lobber.RockLobber(attack_power * (1 + ghost_player.level / 12),
                                                 speed * (1 + ghost_player.level / 35),
                                                 attack_speed * 2,
                                                 attack_speed * (1 + ghost_player.level / 15),
                                                 max_hp * (1 + ghost_player.level / 10),
                                                 bar.Bar(1, (51, 9), (0, 0), RED, DARK_GRAY, 1, 1),
                                                 rock_time + ghost_player.level * 15, (int(74 * screen_scaler), int(74 * screen_scaler)))
        new_rock_lobber.rect.center = (random.choice([0, screen_width]), random.choice([0, screen_height]))
        rock_lobbers.append(new_rock_lobber)

    def create_medpack(location, heal_amount):
        new_medpack = medpack.Medpack(heal_amount, (int(32 * screen_scaler), int(38 * screen_scaler)))
        new_medpack.rect.center = location
        medpacks.append(new_medpack)

    def spawn_boss(power):
        new_boss = BossMain.Boss(1, power * 20, bar.Bar(1, (102, 18), (0, 0), RED, DARK_GRAY, 1, 1), power, (int(159 * screen_scaler), int(168 * screen_scaler)))
        new_boss.rect.center = (ghost_player.rect.centerx + random.choice([200,-200]), ghost_player.rect.centery + random.choice([200, -200]))
        Bosses.append(new_boss)

    def draw_text(text, color, size, x, y, aligned="center"):
        size = int(size * screen_scaler)
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if aligned == "center":
            text_rect.center = (x, y)
        elif aligned == "topleft":
            text_rect.topleft = (x, y)
        SCREEN.blit(text_surface, text_rect)

    def draw_hud():
        draw_text(str(ghost_player.level), BLUE, 36, 50 + int((301 * screen_scaler)/2), 50)
        draw_text(str(hours) + " : " + str(minutes) + " : " + str(seconds), GREEN, 20, screen_width/2, 50)
        draw_text("Screams: " + str(ghost_player.bullets), BLUE, 36, 50, 80 + int(80 * screen_scaler), "topleft")
        if ghost_player.has_shield:
            if ghost_player.shield_cooldown <= 0:
                draw_text("Shield: Press q", BLUE, 36, 50, 80 + int(110 * screen_scaler), "topleft")
            else:
                draw_text("Shield: On Cooldown For " + str(round(ghost_player.shield_cooldown / 60)) + " Seconds", BLUE, 36, 50, 80 + int(110 * screen_scaler), "topleft")
        draw_text("Press TAB to open the shop!", YELLOW, 36, screen_width * 0.9, 35)
        #bars
        exp_bar.load(SCREEN)
        exp_bar.set_percent_full(ghost_player.score/ghost_player.level_up_cost)
        hp_bar.load(SCREEN)
        hp_bar.set_percent_full(ghost_player.hp/ghost_player.max_hp)


    def draw_pause_screen():
        SCREEN.blit(darken_surface, (0, 0))
        draw_text("Paused", AQUA, 200, screen_width / 2, screen_height / 2.7)
        draw_text("Press ESC to resume", BLUE, 50, screen_width / 2, screen_height / 2.2)
        quit_button.load(SCREEN)

    def draw_death_screen():
        SCREEN.blit(darken_surface, (0, 0))
        draw_text("You died!", RED, 200, screen_width / 2, screen_height / 2.7)
        quit_button.load(SCREEN)
        replay_button.load(SCREEN)

    def draw_shop_screen():
        SCREEN.blit(darken_surface, (0, 0))
        SCREEN.blit(shop_surface, shop_rectangle)
        draw_text("Shop", YELLOW, 75, screen_width * 0.875, 60)
        draw_text("Upgrade Points: " + str(ghost_player.upgrade_points), BLUE, 63, screen_width * 0.875, 60 + int(70 * screen_scaler))
        attack_upgrade.load(SCREEN)
        attack_upgrade.load(SCREEN)
        hp_upgrade.load(SCREEN)
        speed_upgrade.load(SCREEN)
        pierce_upgrade.load(SCREEN)
        attack_speed_upgrade.load(SCREEN)
        bullets_upgrade.load(SCREEN)
        shield_unlock_upgrade.load(SCREEN)

    move_left = False
    move_right = False
    move_up = False
    move_down = False

    paused = False

    can_pause = True

    paused_screen = False

    death_screen = False

    shop_screen = False

    relic_screen = False

    replay = False

    dont_spawn_boss = False

    relic_picked = False

    spawn_rate_shift = 0

    while True:
        SCREEN.fill(BLACK)
        CLOCK.tick(FPS)
        time = TimeTracker.tick()
        ghost_player.stay_on_screen(screen_width, screen_height)

        sans_spawn_delay = 600 * 0.85**(minutes - spawn_rate_shift)
        rock_lobber_spawn_delay = 1500 * 0.85**(minutes - 1 - spawn_rate_shift)

        if not paused:
            if sans_spawn_timer <= 0:
                spawn_sans(random.randint(15, 25), random.randint(2, 4), random.randint(30, 90), random.randint(15, 45))
                sans_spawn_timer = sans_spawn_delay
            else:
                sans_spawn_timer -= 1

            if rock_lobber_timer <= 0:
                spawn_rock_lobber(random.randint(15, 25), random.randint(2, 4), random.randint(50, 90), random.randint(15, 45), random.randint(400, 800))
                rock_lobber_timer = rock_lobber_spawn_delay
            else:
                rock_lobber_timer -= 1

            time_elapsed_since_last_second += time
            if time_elapsed_since_last_second > 1000:
                seconds += 1
                if seconds >= 60:
                    minutes += 1
                    seconds = 0
                    if minutes >= 60:
                        hours += 1
                        minutes = 0
                time_elapsed_since_last_second = 0

        if not paused:
            if seconds == 3 and minutes % 3 == 0 and minutes != 0:
                dont_spawn_boss = False
            if seconds == 1 and minutes % 3 == 0 and minutes != 0 and not dont_spawn_boss:
                spawn_boss(minutes*10)
                dont_spawn_boss = True
        for scream in screams:
            scream.load(SCREEN)
            if not paused:
                scream.move([sanses, Bosses, rock_lobbers])
                if not SCREEN.get_rect().contains(scream.rect):
                    screams.remove(scream)
        for missle in missles:
            missle.load(SCREEN)
            if not paused:
                missle.move(ghost_player, missles)
                if not SCREEN.get_rect().contains(missle.rect):
                    missles.remove(missle)

        for sans in sanses:
            sans.load(SCREEN)
            if not paused:
                sans.move(ghost_player, screams)

        for rock_object in rocks:
            rock_object.load(SCREEN, paused)
            if not paused:
                rock_object.attack(ghost_player)
                if not SCREEN.get_rect().contains(rock_object.rect):
                    rocks.remove(rock_object)

        for Boss_list in Bosses:
            Boss_list.load(SCREEN)
            if not paused:
                if Boss_list.move(ghost_player, screams, missles, Bosses, SCREEN):
                    relic_screen = True
                    paused = True
                    relic_picked = False
                Boss_list.attack(ghost_player, missles, SCREEN)

        for rock_lobber_instance in rock_lobbers:
            rock_lobber_instance.load(SCREEN)
            if not paused:
                rock_lobber_instance.move(ghost_player, screams, rocks)
        pop_iterable = 0
        for i in range(len(medpacks)):
            medpacks[i - pop_iterable].load(SCREEN)
            if medpacks[i - pop_iterable].rect.colliderect(ghost_player.rect):
                medpacks[i - pop_iterable].heal(ghost_player)
                medpacks.pop(i - pop_iterable)
                pop_iterable += 1

        ghost_player.load(SCREEN, paused)

        if ghost_player.hp <= 0:
            death_screen = True
            paused = True
            draw_death_screen()

        draw_hud()


        if relic_screen:
            if not relic_picked:
                offered_relics_copy = []
                for relic in offered_relics:
                    offered_relics_copy.append(relic)
                relic1 = random.choice(offered_relics_copy)
                offered_relics_copy.remove(relic1)
                relic2 = random.choice(offered_relics_copy)
                offered_relics_copy.remove(relic2)
                relic3 = random.choice(offered_relics_copy)

                relic1.button.rect.center = ((screen_width / 2) - 200, screen_height / 2)
                relic2.button.rect.center = (screen_width / 2, screen_height / 2)
                relic3.button.rect.center = ((screen_width / 2) + 200, screen_height / 2)
                relic_picked = True

            SCREEN.blit(darken_surface, (0, 0))

            draw_text("Pick a relic:", YELLOW, 50, screen_width / 2, (screen_height / 2) - 200)

            relic1.load(SCREEN)
            relic2.load(SCREEN)
            relic3.load(SCREEN)

        if paused_screen:
            draw_pause_screen()

        if shop_screen:
            draw_shop_screen()

        if not paused:
            pop_iterable = 0
            for i in range(len(sanses)):
                if sanses[i - pop_iterable].hp <= 0:
                    if random.randint(1, 100) <= ghost_player.medpack_chance:
                        create_medpack(sanses[i - pop_iterable].rect.center, ghost_player.max_hp/random.randint(3, 5))
                    ghost_player.score += sanses[i - pop_iterable].attack_power-10
                    ghost_player.hp += ghost_player.lifesteal
                    sanses.pop(i - pop_iterable)
                    pop_iterable += 1

            pop_iterable = 0
            for i in range(len(rock_lobbers)):
                if rock_lobbers[i - pop_iterable].hp <= 0:
                    if random.randint(1, 100) <= ghost_player.medpack_chance:
                        create_medpack((rock_lobbers[i - pop_iterable].rect.center), ghost_player.max_hp/random.randint(3, 5))
                    ghost_player.score += rock_lobbers[i - pop_iterable].attack_power - 10
                    ghost_player.hp += ghost_player.lifesteal
                    rock_lobbers.pop(i - pop_iterable)
                    pop_iterable += 1

            pop_iterable = 0
            for i in range(len(rocks)):
                if rocks[i - pop_iterable].rock_time <= 0:
                    rocks.pop(i - pop_iterable)
                    pop_iterable += 1

            if ghost_player.hp > ghost_player.max_hp:
                ghost_player.hp = ghost_player.max_hp

            ghost_player.try_level_up()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if not paused:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        move_down = True
                    if event.key == pygame.K_w:
                        move_up = True
                    if event.key == pygame.K_a:
                        move_left = True
                    if event.key == pygame.K_d:
                        move_right = True
                    if event.key == pygame.K_q and ghost_player.shield_cooldown <= 0 and ghost_player.has_shield:
                        ghost_player.set_shield(SCREEN)
                        ghost_player.shield_up_timer = ghost_player.shield_duration
                        ghost_player.shield_cooldown = ghost_player.shield_cooldown_time

                        if ghost_player.has_scream_shield:
                            ghost_player.burst_scream(screams)
                    if event.key == pygame.K_ESCAPE:
                        if not relic_screen:
                            paused = True
                        paused_screen = True
                    if event.key == pygame.K_TAB:
                        if not relic_screen:
                            paused = True
                        shop_screen = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_s:
                        move_down = False
                    if event.key == pygame.K_w:
                        move_up = False
                    if event.key == pygame.K_a:
                        move_left = False
                    if event.key == pygame.K_d:
                        move_right = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    ghost_player.scream(screams, screen_scaler)
            else:
                if paused_screen:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        paused = False
                        paused_screen = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if quit_button.is_mouse_hovering():
                            sys.exit()
                if death_screen:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if quit_button.is_mouse_hovering():
                            sys.exit()
                        if replay_button.is_mouse_hovering():
                            replay = True
                            break
                if shop_screen:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_TAB or event.key == pygame.K_ESCAPE:
                            paused = False
                            shop_screen = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if attack_upgrade.button.is_mouse_hovering() and not attack_upgrade.maxed and ghost_player.upgrade_points >= attack_upgrade.price:
                            attack_upgrade.buy(ghost_player)
                        if hp_upgrade.button.is_mouse_hovering() and not hp_upgrade.maxed and ghost_player.upgrade_points >= hp_upgrade.price:
                            hp_upgrade.buy(ghost_player)
                        if speed_upgrade.button.is_mouse_hovering() and not speed_upgrade.maxed and ghost_player.upgrade_points >= speed_upgrade.price:
                            speed_upgrade.buy(ghost_player)
                        if pierce_upgrade.button.is_mouse_hovering() and not pierce_upgrade.maxed and ghost_player.upgrade_points >= pierce_upgrade.price:
                            pierce_upgrade.buy(ghost_player)
                        if attack_speed_upgrade.button.is_mouse_hovering() and not attack_speed_upgrade.maxed and ghost_player.upgrade_points >= attack_speed_upgrade.price:
                            attack_speed_upgrade.buy(ghost_player)
                        if bullets_upgrade.button.is_mouse_hovering() and not bullets_upgrade.maxed and ghost_player.upgrade_points >= bullets_upgrade.price:
                            bullets_upgrade.buy(ghost_player)
                        if shield_unlock_upgrade.button.is_mouse_hovering() and not shield_unlock_upgrade.maxed and ghost_player.upgrade_points >= shield_unlock_upgrade.price:
                            shield_unlock_upgrade.buy(ghost_player)
                if relic_screen:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if relic1.button.is_mouse_hovering():
                            relic1.buy(ghost_player, offered_relics, [speed_upgrade, hp_upgrade, attack_upgrade, attack_speed_upgrade,
                                                      bullets_upgrade, pierce_upgrade])
                            if relic1.type == "spawnrate":
                                spawn_rate_shift += 2
                            relic_screen = False
                            paused = False
                        elif relic2.button.is_mouse_hovering():
                            relic2.buy(ghost_player, offered_relics, [speed_upgrade, hp_upgrade, attack_upgrade, attack_speed_upgrade,
                                                      bullets_upgrade, pierce_upgrade])
                            if relic2.type == "spawnrate":
                                spawn_rate_shift += 2
                            relic_screen = False
                            paused = False
                        elif relic3.button.is_mouse_hovering():
                            relic3.buy(ghost_player, offered_relics, [speed_upgrade, hp_upgrade, attack_upgrade, attack_speed_upgrade,
                                                      bullets_upgrade, pierce_upgrade])
                            if relic3.type == "spawnrate":
                                spawn_rate_shift += 2
                            relic_screen = False
                            paused = False


        if replay:
            break

        if paused:
            move_up = False
            move_down = False
            move_left = False
            move_right = False

        if move_up:
            ghost_player.move_up()
        if move_down:
            ghost_player.move_down()
        if move_left:
            ghost_player.move_left()
        if move_right:
            ghost_player.move_right()
        pygame.display.flip()
