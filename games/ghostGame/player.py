import pygame
import math
import scream


class Player:
    def __init__(self, speed, max_hp, attack_power, projectile_speed, scream_delay, max_bullets, pierce, shield_duration, reload_speed, shield_cooldown_time, reload_bar, medpack_chance, size=(64, 64)):
        # stats
        self.speed = speed
        self.projectile_speed = projectile_speed
        self.scream_delay = scream_delay
        self.max_hp = max_hp
        self.attack_power = attack_power
        self.pierce = pierce
        self.shield_duration = shield_duration
        self.max_bullets = max_bullets
        self.reload_speed = reload_speed
        self.shield_cooldown_time = shield_cooldown_time
        self.medpack_chance = medpack_chance
        self.has_shield = False
        self.has_scream_shield = False
        self.lifesteal = 0
        self.has_heat_seeking = False

        self.upgrade_points = 0
        self.level = 1
        self.level_up_cost = 50
        self.hp = max_hp
        self.bullets = max_bullets

        # shield
        self.shield = False
        self.shield_rect = pygame.Rect((0, 0), (80, 80))
        self.shield_image = pygame.image.load("Sprites/shield.png")

        # timers
        self.reload_cooldown = reload_speed
        self.shield_cooldown = 0
        self.scream_cooldown = 0
        self.shield_up_timer = 0

        # misc
        self.image = pygame.image.load("Sprites/player_ghost.png")
        self.rect = pygame.Rect((0, 0), size)
        self.score = 0
        self.reload_bar = reload_bar

    def load(self, SCREEN, paused):
        if not paused:
            if self.scream_cooldown > 0:
                self.scream_cooldown -= 1
            if self.has_shield:
                if self.shield_cooldown > 0:
                    self.shield_cooldown -= 1

        if self.bullets <= 0:
            if self.reload_cooldown > 0:
                if not paused:
                    self.reload_cooldown -= 1
                    self.reload_bar.set_percent_full(self.reload_cooldown / self.reload_speed)
                    self.reload_bar.location = (self.rect.centerx - 1, self.rect.centery - 44)
                self.reload_bar.load(SCREEN)
            elif not paused:
                self.reload()
                self.reload_cooldown = self.reload_speed
        if self.has_shield:
            if self.shield_up_timer > 0:
                self.set_shield(SCREEN)
                if not paused:
                    self.shield_up_timer -= 1
            else:
                self.remove_shield()

        SCREEN.blit(self.image, self.rect)

    def move_up(self):
        self.rect.centery -= self.speed

    def move_down(self):
        self.rect.centery += self.speed

    def move_left(self):
        self.rect.centerx -= self.speed

    def move_right(self):
        self.rect.centerx += self.speed

    def scream(self, screams):
        if self.scream_cooldown <= 0 and self.bullets > 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rel_x = mouse_x - self.rect.x
            rel_y = mouse_y - self.rect.y
            angle = math.atan2(rel_y, rel_x)
            new_scream = scream.Scream(self.attack_power, self.projectile_speed, self.pierce, self.has_heat_seeking, (32, 32))
            new_scream.angle = angle
            new_scream.rect.center = self.rect.center
            screams.append(new_scream)
            self.scream_cooldown = self.scream_delay
            self.bullets -= 1

    def take_damage(self, amount):
        if not self.shield:
            self.hp -= amount
            if self.hp <= 0:
                self.hp = 0

    def increase_score(self, amount):
        self.score += amount

    def is_alive(self):
        return self.hp > 0

    def set_shield(self, SCREEN):
        self.shield = True
        self.shield_rect.center = self.rect.center
        SCREEN.blit(self.shield_image, self.shield_rect)

    def remove_shield(self):
        self.shield = False

    def stay_on_screen(self, screen_width, screen_height):
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y + self.rect.h > screen_height:
            self.rect.y = screen_height-self.rect.h
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x + self.rect.w > screen_width:
            self.rect.x = screen_width-self.rect.w

    def reload(self):
        self.bullets = self.max_bullets

    def try_level_up(self):
        if self.score >= self.level_up_cost:
            self.level += 1
            self.upgrade_points += self.level
            self.score -= self.level_up_cost
            self.level_up_cost *= 1.25

    def burst_scream(self, screams):
        for i in range(20):
            new_scream = scream.Scream(self.attack_power * 2, self.projectile_speed, self.pierce * 2, self.has_heat_seeking, (32, 32))
            new_scream.angle = i * 18
            new_scream.rect.center = self.rect.center
            screams.append(new_scream)
