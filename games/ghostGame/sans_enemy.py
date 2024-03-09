import pygame
import math


class Sans(pygame.sprite.Sprite):
    def __init__(self, attack_power, speed, attack_speed, max_hp, hp_bar, movement_delay, size=(74, 74)):
        #stats
        self.speed = speed
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack_speed = attack_speed
        self.attack_power = attack_power
        self.hp_bar = hp_bar

        #misc
        self.movement_delay = movement_delay
        self.rect = pygame.Rect((0, 0), size)
        self.image = pygame.image.load("Sprites/sans.png")
        self.image = pygame.transform.scale(self.image, size)
        self.angle = 0

        #timers
        self.attack_cooldown = 0

    def load(self, SCREEN):
        SCREEN.blit(self.image, self.rect)
        self.hp_bar.location = (self.rect.centerx - 1, self.rect.centery - 44)
        self.hp_bar.set_percent_full(self.hp/self.max_hp)
        self.hp_bar.load(SCREEN)

    def move(self, character, screams_list):
        if not self.rect.colliderect(character.rect):
            position = character.positions[self.movement_delay]
            d_y = self.rect.centery - character.rect.centery
            d_x = self.rect.centerx - character.rect.centerx
            distance = math.sqrt((self.rect.centerx - character.rect.centerx) ** 2 + (
                        self.rect.centery - character.rect.centery) ** 2)
            wanted_angle = self.angle
            if d_y > 0 and d_x == 0:
                wanted_angle = -math.pi
            elif d_y < 0 and d_x == 0:
                wanted_angle = math.pi
            elif d_x != 0:
                wanted_angle = math.atan(d_y / d_x)
                if d_y > 0 and d_x > 0:
                    wanted_angle += math.pi
                elif d_y < 0 and d_x > 0:
                    wanted_angle += math.pi
            if wanted_angle > math.pi:
                wanted_angle = -(2 * math.pi - wanted_angle)
            elif wanted_angle < -math.pi:
                wanted_angle = 2 * math.pi + wanted_angle
            angle_error = wanted_angle - self.angle
            while angle_error > math.pi:
                angle_error -= 2 * math.pi
            while angle_error < -math.pi:
                angle_error += 2 * math.pi
            self.angle += angle_error
            self.rect.centerx += math.cos(self.angle) * self.speed
            self.rect.centery += math.sin(self.angle) * self.speed
        self.attack(character)
        self.get_hit(screams_list)

    def attack(self, character):
        if self.is_overlapping(character) and self.attack_cooldown <= 0:
            character.take_damage(self.attack_power)
            self.attack_cooldown = self.attack_speed
        else:
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1

    def get_hit(self, screams_list):
        pop_iterable = 0
        #iterate over all screams
        for i in range(len(screams_list)):
            #check if overlapping with scream, pop_iterable is used to correct the index after a scream is popped
            if self.is_overlapping(screams_list[i - pop_iterable]):
                #if the scream has pierce left, check if the sans has already been hit by the scream
                #needed because otherwise the scream would hit the sans multiple times
                if screams_list[i - pop_iterable].pierce > 0:
                    already_hit = False
                    for x in screams_list[i - pop_iterable].damaged:
                        if self == x:
                            already_hit = True
                            break
                    #if not hit deal damage to self, subtract one pierce, and add sans to damaged list
                    if not already_hit:
                        self.hp -= screams_list[i - pop_iterable].power
                        screams_list[i - pop_iterable].pierce -= 1
                        if screams_list[i - pop_iterable].pierce <= 0:
                            screams_list.pop(i - pop_iterable)
                            pop_iterable += 1
                        else:
                            screams_list[i - pop_iterable].damaged.append(self)
                else:
                    screams_list.pop(i - pop_iterable)
                    pop_iterable += 1

    def is_overlapping(self, character):
        return self.rect.colliderect(character.rect)
