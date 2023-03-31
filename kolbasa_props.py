from pygame import *
from time import sleep as sl

font.init()

WND_SIZE = (700, 500)
PLR_SIZE = (250, 300)#(70, 90)
GRAY = (125, 125, 125)
wnd = display.set_mode(WND_SIZE)
clock = time.Clock()
display.set_caption('Where is my Kolbasa?!')
game = True
gamemode = 'basic'
shotgun_reload_time = 0

### Очень специфичные 
tutorial_missed_shots = 0

plr_walk_props_left = [transform.scale(image.load('walk1_left.png'), PLR_SIZE), 
transform.scale(image.load('walk2_left.png'), PLR_SIZE), 
transform.scale(image.load('walk3_left.png'), PLR_SIZE)]

plr_walk_props_right = [transform.scale(image.load('walk1_right.png'), PLR_SIZE), 
transform.scale(image.load('walk2_right.png'), PLR_SIZE), 
transform.scale(image.load('walk3_right.png'), PLR_SIZE)]

shotguns_anims = [transform.scale(image.load('shotgun_first_person.png'), (300, 150)), 
transform.scale(image.load('shotgun_first_person_recoil.png'), (300, 150))]

plr_stand = transform.scale(image.load('mc_stand.png'), PLR_SIZE)
plr_stand_back = transform.scale(image.load('mc_stand_back.png'), PLR_SIZE)


class basicsprite(sprite.Sprite):
    def __init__(self, image_name, pos_x, pos_y, size):
        super().__init__()
        self.image = transform.scale(image.load(image_name), size)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        ### В основном только для ентера
        self.is_on_screen = False
    def render(self):
        wnd.blit(self.image, (self.rect.x, self.rect.y))
    def collpoint(self, x, y):
        return self.rect.collidepoint(x,y)

class player(basicsprite):
    def __init__(self, image_name, pos_x, pos_y, size):
        super().__init__(image_name, pos_x, pos_y, size)
        self.was_anim = None
        self.speed = 5
        self.cd_change_walk = 0
        self.moved = False
        self.talk = 1
        self.level_on = 0
    def control(self):
        keys = key.get_pressed()

        if keys[K_LEFT]:
            self.rect.x -= self.speed
            if self.cd_change_walk == 0:
                if self.image == plr_walk_props_left[1] or self.image == plr_walk_props_left[2]:
                    self.image = plr_walk_props_left[0]
                    self.cd_change_walk = 5
                elif self.was_anim == 'walk3_left':
                    self.image = plr_walk_props_left[1]
                    self.was_anim = 'walk2_left'
                    self.cd_change_walk = 5
                elif self.was_anim == 'walk2_left':
                    self.image = plr_walk_props_left[2]
                    self.was_anim = 'walk3_left'
                    self.cd_change_walk = 5

                else:
                    self.image = plr_walk_props_left[1]
                    self.was_anim = 'walk2_left'
                    self.cd_change_walk = 5
            else:
                self.cd_change_walk -= 1
            self.moved = True
        if keys[K_RIGHT]:
            self.rect.x += self.speed
            if self.cd_change_walk == 0:
                if self.image == plr_walk_props_right[1] or self.image == plr_walk_props_right[2]:
                    self.image = plr_walk_props_right[0]
                    self.cd_change_walk = 5
                elif self.was_anim == 'walk3_right':
                    self.image = plr_walk_props_right[1]
                    self.was_anim = 'walk2_right'
                    self.cd_change_walk = 5
                elif self.was_anim == 'walk2_right':
                    self.image = plr_walk_props_right[2]
                    self.was_anim = 'walk3_right'
                    self.cd_change_walk = 5

                else:
                    self.image = plr_walk_props_right[1]
                    self.was_anim = 'walk2_right'
                    self.cd_change_walk = 5
            else:
                self.cd_change_walk -= 1
            self.moved = True
        if not keys[K_RIGHT] and not keys[K_LEFT]:
            self.image = plr_stand