import pygame
import math


class Scream(pygame.sprite.Sprite):
    def __init__(self, power, speed, pierce, is_heat_seeking=False, size=(32, 32)):
        super(Scream, self).__init__()
        #stats
        self.power = power
        self.speed = speed
        self.pierce = pierce

        #misc
        self.rect = pygame.Rect((0, 0), size)
        self.image = pygame.image.load("Sprites/screem.png")
        self.image = pygame.transform.scale(self.image, size)
        self.angle = 0
        self.damaged = []
        self.is_heat_seeking = is_heat_seeking

    def load(self, SCREEN):
        rotated_image = pygame.transform.rotate(self.image, -int(self.angle * 180 / math.pi) + 180)
        image_rect = rotated_image.get_rect(center=self.rect.center)
        SCREEN.blit(rotated_image, image_rect)

    def move(self, enemies):
        if self.is_heat_seeking and len(enemies) > 0:
            least_error = math.pi
            closest_enemy = None
            for enemy_type in enemies:
                for enemy in enemy_type:
                    if enemy not in self.damaged:
                        d_y = self.rect.centery - enemy.rect.centery
                        d_x = self.rect.centerx - enemy.rect.centerx
                        distance = math.sqrt((self.rect.centerx - enemy.rect.centerx) ** 2 + (
                                    self.rect.centery - enemy.rect.centery) ** 2)
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
                        if abs(angle_error) < abs(least_error):
                            least_error = angle_error
                            closest_enemy = enemy
            if closest_enemy is not None:
                d_y = self.rect.centery - closest_enemy.rect.centery
                d_x = self.rect.centerx - closest_enemy.rect.centerx
                distance = math.sqrt((self.rect.centerx - closest_enemy.rect.centerx) ** 2 + (self.rect.centery - closest_enemy.rect.centery) ** 2)
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
                    wanted_angle = -(2*math.pi - wanted_angle)
                elif wanted_angle < -math.pi:
                    wanted_angle = 2*math.pi + wanted_angle
                angle_error = wanted_angle - self.angle
                while angle_error > math.pi:
                    angle_error -= 2 * math.pi
                while angle_error < -math.pi:
                    angle_error += 2 * math.pi
                self.angle += angle_error/50
        self.rect.centerx += math.cos(self.angle) * self.speed
        self.rect.centery += math.sin(self.angle) * self.speed
