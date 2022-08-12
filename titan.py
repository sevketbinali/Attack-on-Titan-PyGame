import pygame
from pygame import mixer
import math
import random
import sys
from pygame.locals import*

# surface(yüzey) için W = Weight(genişlik) H = Height(yükseklik)
W, H = 700, 514

# başlangıç
pygame.init()
# surface (yüzey)
CLOCK = pygame.time.Clock()
surface = pygame.display.set_mode((W, H))
pygame.display.set_caption("Attack on Titan")
icon = pygame.image.load("Graphics/aoticon.png")
pygame.display.set_icon(icon)
FPS = 200

# player
playerIMG = pygame.image.load("Graphics/erenbehind.png")
playerX = 300
playerY = 600
playerX_change = 0
playerY_change = 0
# player'ın sağa ve sola hareket ederken görüntünün değişmesi
walkRight = pygame.image.load("Graphics/erenright.png")
walkLeft = pygame.image.load("Graphics/erenleft.png")

# music
mixer.music.set_volume(0.05)
mixer.music.load("Sounds/titanmusic.wav")
mixer.music.play(-1)

# fontlar ve Skor yazısı
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 15
# Oyun Sonu
over_font = pygame.font.Font('freesansbold.ttf', 64)



# Düşman
enemyIMG = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 9


for i in range(num_of_enemies):
    enemyIMG.append(pygame.image.load('Graphics/titann.png'))
    enemyX.append(random.randint(2, 718))
    enemyY.append(random.randint(2, 40))
    enemyY_change.append(45)
    enemyX_change.append(2)


# Hook atışı
hookIMG = pygame.image.load('Graphics/new21.png')
hookX = 0
hookY = 480
hookX_change = 1
hookY_change = 3
hook_state = "ready"

# arkaplan
background = pygame.image.load("Graphics/backgrrnd.png").convert()


# game loop
def show_score(x, y):
    score = font.render("Skor : " + str(score_value), True, (255, 255, 255))
    surface.blit(score, (x, y))



def game_over_text():
    over_text = over_font.render("OYUN BİTTİ", True, (255, 255, 255))
    surface.blit(over_text, (150, 250))


def player(x, y):
    surface.blit(playerIMG, (x, y))

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
          surface.blit(walkLeft,(x,y))
        if event.key == pygame.K_RIGHT:
          surface.blit(walkRight, (x, y))



def enemy(x, y, i):
    surface.blit(enemyIMG[i], (x, y))


def fire_hook(x, y):
    global hook_state
    hook_state = "fire"
    surface.blit(hookIMG, (x + 17, y + 2))



def isCollision(enemyX, enemyY, hookX, hookY):
    distance = math.sqrt(math.pow(enemyX - hookX, 2) + (math.pow(enemyY - hookY, 2)))
    if distance < 30:
        return True
    else:
        return False


running = True
while running:

    # RGB = Red, Green, Blue
    surface.fill((0, 0, 0))
    # Background Image
    surface.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            sys.exit()

        # karakterin yön tuşlarına göre vereceği reaksiyon ve reaksiyonun hızı (yön tuşları basılı iken)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.55
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.55
            if event.key == pygame.K_SPACE:
                if hook_state == "ready":
                    hookSound = mixer.Sound("Sounds/3dManeuverGearEffect2x.mp3")
                    hookSound.set_volume(0.05)
                    hookSound.play()

                    hookX = playerX
                    fire_hook(hookX, hookY)
        #yön tuşlarına basılı değilken; haraket 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                playerY_change = 0
    playerX += playerX_change
    playerY -= playerY_change

    playerY = 430

    if playerX <= 0:
        playerX = 0
    elif playerX >= 620:
        playerX = 620

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] >400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        if score_value >=100:
                pygame.image.load("Graphics/blackscreen.png")
                over_text = font.render("100 SKORA ULAŞTIN", True, (255, 0, 0))
                surface.blit(over_text, (170, 100))
                over_text = font.render("TEBRİKLER!", True, (255, 0, 0))
                surface.blit(over_text, (244, 160))
                break
        #düşmanın hareket hızı ve konum değişikliği
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.53
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 720:
            enemyX_change[i] = -0.53
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], hookX, hookY)
        if collision:
            slashSound = mixer.Sound("Sounds/slash2x.mp3")
            slashSound.set_volume(0.5)
            slashSound.play()
            hookY = playerY
            hook_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 700)
            enemyY[i] = random.randint(5, 60)

        enemy(enemyX[i], enemyY[i], i)

    # Hook Hareketi
    if hookY <= 0:
        hookY = playerY
        hook_state = "ready"

    if hook_state == "fire":

        fire_hook(hookX, hookY)
        hookY -= hookY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()



