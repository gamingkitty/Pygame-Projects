import random
import time
import pygame
import math


class Sword(pygame.sprite.Sprite):
    def __init__(self, image_path, power, hitbox_offset_x=0, hitbox_offset_y=0):
        super().__init__()
        self.original_image = pygame.image.load(image_path)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.power = power
        self.hitbox_offset_x = hitbox_offset_x
        self.hitbox_offset_y = hitbox_offset_y

    def attack(self, target):
        # Perform the sword attack action here
        # For example, you can check for collision between the sword and the target
        if self.rect.colliderect(target.rect):
            target.take_damage(self.power)
            return True
        else:
            return False

    def load(self, screen, boss_rect, boss_angle, player_rect):
        boss_center = boss_rect.center
        player_center = player_rect.center

        angle_to_player = math.atan2(player_center[1] - boss_center[1], player_center[0] - boss_center[0])
        rotated_image = pygame.transform.rotate(self.original_image, -math.degrees(angle_to_player) - 45)

        handle_offset_x = -rotated_image.get_width() / 2
        handle_offset_y = -rotated_image.get_height() / 2

        self.image = rotated_image
        self.rect = self.image.get_rect(center=boss_center)

        # Draw the sword at the boss center
        screen.blit(self.image, self.rect)

        # Draw a point indicating the rotation center
        rotation_center = boss_center[0] + handle_offset_x, boss_center[1] + handle_offset_y
        pygame.draw.circle(screen, (255, 0, 0), rotation_center, 3)

        # Draw the hit box around the sword
        hit_box = self.rect.inflate(10, 10)  # Adjust the hit box size as needed
        pygame.draw.rect(screen, (255, 0, 0), hit_box, 2)  # Draw the hit box with a red color and a border width of 2


class Boss(pygame.sprite.Sprite):
    def __init__(self, speed, max_hp, hp_bar, power, size=(74, 74)):
        super().__init__()
        # stats
        self.power = power
        self.speed = speed
        self.true_speed = speed
        self.max_hp = max_hp
        self.hp = max_hp
        self.stage = "ranged"
        self.attack_delay = 130
        self.attack_timer = self.attack_delay
        self.hp_bar = hp_bar
        self.sword = Sword("Sprites/sword.png", 10, hitbox_offset_x=-10, hitbox_offset_y=20)
        self.melee_delay = 100
        self.melee_timer = self.melee_delay
        self.enraged_timer = 0
        self.enraged_delay = 150
        self.enraged_speed = 7


        #misc
        self.rect = pygame.Rect((0, 0), size)
        self.image = pygame.image.load("Sprites/Mech.png")
        self.image = pygame.transform.scale(self.image, size)
        self.angle = 0
        self.rotated_image = self.image
        self.rotated_rect = self.rect

    def rotate_towards_point(self, player):
        angle = math.atan2(player.rect.centery - self.rect.centery,
                           player.rect.centerx - self.rect.centerx)
        angle_degrees = math.degrees(angle)
        self.rotated_image = pygame.transform.rotate(self.image, -angle_degrees)
        self.rotated_rect = self.rotated_image.get_rect(center=self.rect.center)

    def ranged_attack(self, character, missiles):
        if self.attack_timer <= 0:
            num_missiles = random.randint(int(self.power/30), int(self.power/12))  # Number of missiles in the barrage
            angle_increment = 1/2 * math.pi / num_missiles  # Angle increment between each missile

            player_x, player_y = character.rect.centerx, character.rect.centery
            boss_x, boss_y = self.rect.centerx, self.rect.centery

            angle_to_player = math.atan2(player_y - boss_y, player_x - boss_x)

            start_angle = angle_to_player - (angle_increment * (num_missiles // 2))

            for _ in range(num_missiles):
                new_missile = Missile(self.power, 10, (32, 32))
                new_missile.rect.centerx = self.rect.centerx
                new_missile.rect.centery = self.rect.centery
                new_missile.angle = start_angle
                new_missile.rect.center = self.rect.center
                missiles.append(new_missile)

                start_angle += angle_increment

            self.attack_timer = self.attack_delay

    def melee_attack(self, character):
        if self.melee_timer <= 0:
            if self.sword.attack(character):
                self.melee_timer = self.melee_delay
        else:
            self.melee_timer -= 1


    def load(self, SCREEN):
        self.hp_bar.update_size()
        self.hp_bar.update_bar()
        SCREEN.blit(self.rotated_image, self.rotated_rect)
        self.hp_bar.location = (self.rect.centerx - 1, self.rect.centery - 44)
        self.hp_bar.set_percent_full(self.hp / self.max_hp)
        self.hp_bar.load(SCREEN)


    def move(self, character, screams_list, missles, boss_array, SCREEN):
        self.enraged_timer -= 1
        if self.enraged_timer <= 0:
            self.enraged_timer = self.enraged_delay
        if self.stage == "enraged" and self.enraged_timer <= 50:
            self.speed = self.enraged_speed
        else:
            self.speed = self.true_speed
        if character.rect.centerx < self.rect.centerx:
            self.rect.centerx -= self.speed
        elif character.rect.centerx > self.rect.centerx:
            self.rect.centerx += self.speed
        if character.rect.centery < self.rect.centery:
            self.rect.centery -= self.speed
        elif character.rect.centery > self.rect.centery:
            self.rect.centery += self.speed

        self.attack_timer -= 1
        self.attack(character, missles, SCREEN)
        self.rotate_towards_point(character)
        if self.get_hit(screams_list, boss_array):
            return True
        return False
    def attack(self, character, missiles, SCREEN):
        #get hp then set stage
        if self.hp >= 2*self.max_hp/3:
            self.stage = "ranged"
            self.ranged_attack(character, missiles)
        elif self.hp >= self.max_hp/3 < 2*self.max_hp/3:
            self.stage = "melee"
            self.melee_attack(character)
            self.sword.load(SCREEN, self.rotated_rect, self.angle, character.rect)
        elif self.hp < self.max_hp/3 > 0:
            self.stage = "enraged"
            self.melee_attack(character)
            self.sword.load(SCREEN, self.rotated_rect, self.angle, character.rect)

    def get_hit(self, screams_list, boss_array):
        pop_iterable = 0
        # iterate over all screams
        for i in range(len(screams_list)):
            # check if overlapping with scream, pop_iterable is used to correct the index after a scream is popped
            if self.rect.colliderect(screams_list[i - pop_iterable]):
                # if the scream has pierce left, check if the sans has already been hit by the scream
                # needed because otherwise the scream would hit the sans multiple times
                if screams_list[i - pop_iterable].pierce > 0:
                    already_hit = False
                    for x in screams_list[i - pop_iterable].damaged:
                        if self == x:
                            already_hit = True
                            break
                    # if not hit deal damage to self, subtract one pierce, and add sans to damaged list
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
        if self.hp <= 0:
            boss_array.remove(self)
            return True
        return False

class Missile(pygame.sprite.Sprite):
    def __init__(self, power, speed, size=(157, 34)):
        super(Missile, self).__init__()
        # stats
        self.power = power
        self.speed = speed

        # misc
        self.rect = pygame.Rect((0, 0), size)
        self.image = pygame.image.load("Sprites/Missle.png")
        self.angle = 0
        self.damaged = []

    def load(self, SCREEN):
        rotated_image = pygame.transform.rotate(self.image, -int(self.angle * 180 / math.pi) + 180)
        image_rect = rotated_image.get_rect(center=self.rect.center)
        SCREEN.blit(rotated_image, image_rect)

    def is_overlapping(self, character):
        return self.rect.colliderect(character.rect)

    def move(self, character, missiles):
        self.rect.centerx += math.cos(self.angle) * self.speed
        self.rect.centery += math.sin(self.angle) * self.speed
        if self.speed < 10:
            self.speed = self.speed + random.randint(0, 1)
        if self.is_overlapping(character):
            character.take_damage(self.power/5)
            missiles.remove(self)





