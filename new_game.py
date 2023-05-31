import pygame
import random
import os

WIDTH = 500
HEIGHT = 600
FPS = 60

# define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255,255,0)

#set up assets
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,"img")

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)



class Player(pygame.sprite.Sprite):
    # sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(game_folder,"enemyShip.png")).convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = 25
        #pygame.draw.circle(self.image , red, self.rect.center, self.radius)
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        
        if keystate[pygame.K_LEFT]:
            self.speedx = -5

        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        
        self.rect.x += self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        
        if self.rect.left < 0:
            self.rect.left = 0
        # self.rect.y += self.y_speed
        # if self.rect.bottom > HEIGHT - 200:
        #     self.y_speed = -5

        # if self.rect.top < 200:
        #     self.y_speed = 5

        # if self.rect.left > WIDTH:
        #     self.rect.right = 0
        
    def shoot(self):
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

class Mob(pygame.sprite.Sprite) :
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image_orig = pygame.image.load(os.path.join(game_folder,"meteorSmall.png")).convert()
       self.image_orig.set_colorkey(black)
       self.image = self.image_orig.copy()
       self.rect = self.image.get_rect()
       self.radius = int(self.rect.width *0.9/2 )
       pygame.draw.circle(self.image , red, self.rect.center, self.radius)
       self.rect.x  = random.randrange(WIDTH - self.rect.width)
       self.rect.y = random.randrange(-100, -40)
       self.speedy =random.randrange(1,8)
       self.speedx = random.randrange(-3,3)
       self.rot = 0
       self.rot_speed = random.randrange(-8, 8)
       self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()

        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed)%360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT - 10 or self.rect.left < -25 or self.rect.right > WIDTH:
           self.rect.x  = random.randrange(WIDTH - self.rect.width)
           self.rect.y = random.randrange(-100, -40)
           self.speedy =random.randrange(1,8)
           self.speedx = random.randrange(-3,3)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.image.load(os.path.join(game_folder,"laserRed.png")).convert()
       self.image.set_colorkey(black)
       self.rect = self.image.get_rect()
       self.rect.bottom = y
       self.rect.centerx = x
       self.speedy = -10

    def update(self):
        self.rect.y += self.speedy

        if self.rect.bottom <0 :
            self.kill()

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My game")
clock = pygame.time.Clock()

background=pygame.image.load(os.path.join(game_folder,"bg5.jpg")).convert()      
background_rect=background.get_rect() 


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group() 
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
score = 0

for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Game loop
running = True
while running:
    clock.tick(FPS)
    # Process input(events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

        # update
    all_sprites.update()

    #check if bullet hit mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True) 
    for hit in hits:
        score += hit.radius
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
 

    #check if a player hit a mob
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)

    if hits:
        running = False

    # Draw/render
    screen.fill(black )
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    pygame.display.flip()


pygame.quit()
