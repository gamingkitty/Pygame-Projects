import math
import pygame


# def get_obj_from_save(save_list):
#     obj = SpriteSheet(save_list[0], save_list[1], save_list[2], save_list[3])
#     obj.current_frame = save_list[4]
#     obj.increment_timer = save_list[4]
#     return obj


class SpriteSheet:
    def __init__(self, sheet, sprite_size, scale, increment_cooldown, sheet_image=None):
        self.sprites = []
        self.sheet = sheet
        self.sprite_size = sprite_size
        self.scale = scale
        if sheet_image is None:
            sheet_image = pygame.image.load(sheet)

        sheet_size = sheet_image.get_size()
        for i in range(sheet_size[1] // sprite_size[1]):
            for j in range(sheet_size[0] // sprite_size[0]):
                clip_rect = pygame.rect.Rect(((j * sprite_size[0]), (i * sprite_size[1])), sprite_size)
                frame = sheet_image.subsurface(clip_rect)
                frame = pygame.transform.scale(frame, (sprite_size[0] * scale, sprite_size[1] * scale))
                self.sprites.append(frame)
        self.current_frame = 0
        self.increment_cooldown = increment_cooldown
        self.increment_timer = increment_cooldown

    # def get_save_data(self):
    #     return [self.sheet, self.sprite_size, self.scale, self.increment_cooldown, self.current_frame, self.increment_timer]

    def get_sprite(self, index):
        return self.sprites[index]

    def get_current_frame(self):
        return self.sprites[self.current_frame]

    def set_current_frame(self, frame):
        self.current_frame = frame

    def increment_frame(self, delta_time):
        if self.increment_timer > self.increment_cooldown:
            self.current_frame += 1
            if self.current_frame >= len(self.sprites):
                self.current_frame = 0
            self.increment_timer = 0
        else:
            self.increment_timer += 60 * delta_time
