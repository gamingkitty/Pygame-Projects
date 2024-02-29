import button


class Relic:
    def __init__(self, image, size, location, type):
        self.button = button.Button(image, size, location)
        self.type = type
        self.bought_count = 0

    def load(self, SCREEN):
        self.button.load(SCREEN)

    def buy(self, character, relics, upgrades):
        self.bought_count += 1
        if self.type == "medpack":
            character.medpack_chance += 5
            if self.bought_count >= 3:
                relics.remove(self)
        elif self.type == "heal":
            character.hp = character.max_hp
        elif self.type == "upgradepoint":
            character.upgrade_points += 20
        elif self.type == "reload":
            character.reload_speed -= 60
            character.reload_cooldown -= 60
            relics.remove(self)
        elif self.type == "lifesteal":
            character.lifesteal += 1
            if self.bought_count >= 3:
                relics.remove(self)
        elif self.type == "screamshield":
            character.has_scream_shield = True
            relics.remove(self)
        elif self.type == "maxupgrade":
            for upgrade in upgrades:
                upgrade.max_amount += 1
                upgrade.size = upgrade.original_size
                upgrade.set_text(upgrade.original_text)
                upgrade.maxed = False

            if self.bought_count >= 5:
                relics.remove(self)
        elif self.type == "heatseeking":
            character.has_heat_seeking = True
            relics.remove(self)
