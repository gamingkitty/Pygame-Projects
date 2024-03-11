import pygame
import math
import rock


class RockLobber(pygame.sprite.Sprite):
    def __init__(self, attack_power, speed, attack_speed, rock_attack_speed , max_hp, hp_bar, rock_time, size=(32, 43)):
        #stats
        self.speed = speed
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack_speed = attack_speed
        self.attack_power = attack_power
        self.hp_bar = hp_bar
        self.rock_attack_speed = rock_attack_speed
        self.rock_time = rock_time

        #misc
        self.rect = pygame.Rect((0, 0), size)
        self.image = pygame.image.load("Sprites/rock_thrower.png")
        self.image = pygame.transform.scale(self.image, size)
        self.angle = 0

        #timers
        self.attack_cooldown = 0

    def load(self, SCREEN):
        SCREEN.blit(self.image, self.rect)
        self.hp_bar.location = (self.rect.centerx, self.rect.centery - 44)
        self.hp_bar.set_percent_full(self.hp/self.max_hp)
        self.hp_bar.load(SCREEN)

    def move(self, character, screams_list, rocks):
        if abs(character.rect.centery - self.rect.centery) + abs(character.rect.centerx - self.rect.centerx) > 500:
            if character.rect.centerx < self.rect.centerx - 5:
                self.rect.centerx -= self.speed
            elif character.rect.centerx > self.rect.centerx + 5:
                self.rect.centerx += self.speed
            if character.rect.centery < self.rect.centery - 5:
                self.rect.centery -= self.speed
            elif character.rect.centery > self.rect.centery + 5:
                self.rect.centery += self.speed
        elif abs(character.rect.centery - self.rect.centery) + abs(character.rect.centerx - self.rect.centerx) < 400:
            if character.rect.centerx < self.rect.centerx - 5:
                self.rect.centerx += self.speed
            elif character.rect.centerx > self.rect.centerx + 5:
                self.rect.centerx -= self.speed
            if character.rect.centery < self.rect.centery - 5:
                self.rect.centery += self.speed
            elif character.rect.centery > self.rect.centery + 5:
                self.rect.centery -= self.speed

        self.attack(character, rocks)
        self.get_hit(screams_list)

    def attack(self, character, rocks):
        if self.attack_cooldown <= 0:
            thrown_rock = rock.Rock(self.attack_power, self.rock_attack_speed, self.rock_time)
            thrown_rock.rect.center = self.rect.center
            rocks.append(thrown_rock)
            total_dist_from_target = math.sqrt(((character.rect.centerx - self.rect.centerx)**2 + (character.rect.centery - self.rect.centery)**2))
            thrown_rock.velocity_x = 10 * (character.rect.centerx - self.rect.centerx)/total_dist_from_target
            thrown_rock.velocity_y = 10 * (character.rect.centery - self.rect.centery)/total_dist_from_target
            self.attack_cooldown = self.attack_speed
        else:
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
