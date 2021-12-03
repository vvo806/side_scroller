"""
Creating jungle game
"""

# imports
import pygame, sys
from pygame.locals import *
import random, time

# initalize pygame
pygame.init()

# assign FPS(frame per second)
FPS = 30
clock = pygame.time.Clock()

#setup colors
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)

# display dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0

#setting up fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 30)
game_over = font.render("Game Over", True, BLACK)

background = pygame.transform.scale(pygame.image.load("forest2.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))

# setup a 300x300 pixel display
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.transform.scale(pygame.image.load("snake.png"), (60,80))
        self.rect = self.image.get_rect()
        self.rect.center= (600, (random.randint(40, SCREEN_HEIGHT-40)))
 
      def move(self):
        global SCORE
        self.rect.move_ip(-10,0)
        if (self.rect.left < 0): #when snake leaves screen on the left
            SCORE += 1
            self.rect.left = 600
            self.rect.center = (600, (random.randint(40, SCREEN_HEIGHT-40)))

      def draw(self, surface):
        surface.blit(self.image, self.rect) 
 
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.transform.scale(pygame.image.load("mouse.png"), (60,80))
        self.rect = self.image.get_rect()
        self.rect.center = (140, 520)
 
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)
        if self.rect.bottom < 600:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0,5)
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.left > 0:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
 
    def draw(self, surface):
        surface.blit(self.image, self.rect)     
 
         
P1 = Player()
E1 = Enemy()
E2 = Enemy()

#creating Sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)
enemies.add(E2)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
 
#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)
 
#Game Loop
while True:
       
    #Cycles through all events occuring  
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 5
           
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
 
 
    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
 
    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

        if E1.rect.left < 100: #second snake comes in
            all_sprites.add(E2)

        if SCORE == 20:
            all_sprites.add(E2)


    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('eating_sound.wav').play()
        time.sleep(3)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (150, 150))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill() 
        time.sleep(2)
        pygame.quit()
        sys.exit()       
         
    pygame.display.update()
    clock.tick(FPS)
