import pygame
from pygame import mixer
import random
import math



# initialize the pygame
pygame.init()

#create a screen with defined shape ans size
height, width = 700, 700
window = pygame.display.set_mode(size=(height,width),)

color_map=(50,50,50)
# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('./resources/rocket.png')
pygame.display.set_icon(icon)

# Quit events
Playing = False

# PLayer and Its coordinates
playerImage = pygame.image.load("./resources/player.png")
pCoordX = (width/2)-playerImage.get_width()/2 - 1
pCoordY =  height -playerImage.get_height()
Delta = 0.5
pMoveX  = 0
pMoveY = 0

# Enemy and Its coordinates

nbEnemies = 6
enemyImage = [pygame.image.load("./resources/enemy.png")]*nbEnemies
eCoordX = [random.randint(0, width  - enemyImage[i].get_width() - enemyImage[i].get_width()/2) for i in range(nbEnemies)]
eCoordY = [random.randint(0, 150) for _ in range(nbEnemies)]
eDelta = [random.randint(1,4) for _ in range(nbEnemies)]
eMoveX  = [random.randint(1,3) for _ in range(nbEnemies)]*nbEnemies
eMoveY  = [random.randint(1,3) for _ in range(nbEnemies)]

# Backgroud
bulletImage  = pygame.transform.rotate(surface=pygame.image.load("./resources/bullet.png"),angle=90)
bullet_state = "ready"
bDelta = 5
bMoveX = 0
bMoveY = bDelta
bCoordX = (width/2)-playerImage.get_width()/2 - 1
bCoordY = height + playerImage.get_height()
 
# Backgroud
BackgroundImage = pygame.image.load("./resources/background.png")
BackgroundImage = pygame.transform.scale(BackgroundImage, (width, height))

# backgroud sound
mixer.music.load("./resources/background.wav")
mixer.music.play(-1)


def fire(x,y) :
    global bullet_state
    bullet_state = "fire"
    window.blit(bulletImage, (x+bulletImage.get_width()/2,y-bulletImage.get_width()))

def enemy(x,y, enemyImage) :
    window.blit(source=enemyImage, dest=(x,y))

def player(x,y) :
    # Draw in the screen display
    window.blit(source=playerImage,dest = (x, y))
    
def boundaries(x,y) :

    if x >= width-1-playerImage.get_width() :
        x = width-1-playerImage.get_width()
    elif x <= 0 :
        x = 0
    if y >= height-1-playerImage.get_height() :
        y = height-1-playerImage.get_height()
    elif y <= 0 :
        y = 0

    return x,y

def enemyMovement(x,y) :
    
    if eCoordX <= 0 :
        eMoveX = eDelta
        eCoordY += 10
    if eCoordX >= width - enemyImage.get_width() - 1 :
        x = -eDelta
        y += 10
    
    return x, y


def isCollision(eCoordX, eCoordY, bCoordX, bCoordY) :
   distance = math.sqrt( (eCoordX-bCoordX)**2 + (eCoordY-bCoordY)**2 )
   if distance <= 32 :
       return True
   return False

#Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 24)
textX = 16
textY  = 16

GameOver = pygame.font.Font("freesansbold.ttf", 64)
def game_over() :
    go = GameOver.render("GAME OVER", True, (255,50,255))
    window.blit(go, ((width-64*6)/2, (height-1)/2))
    
def show_score(x,y) :
    score = font.render("Score :" +str(score_value), True, (255, 255, 0))
    window.blit(score, (x,y))

# Clock 
clock = pygame.time.Clock()
fps = 120

# The Game Loop
while not Playing :

    # ticking 
    clock.tick(fps)

    #  Paint the surface(Screen) with RGB Color
    window.fill(color=color_map) # not needed anymore

    # background
    window.blit(BackgroundImage, (0,0))
    # player movement and boundary check
    
    # Check for events
    for event in pygame.event.get() :
        # The Quit Event
        if event.type == pygame.QUIT :
            Playing = True
        
        if event.type == pygame.KEYDOWN : # Keyboard Events
            if event.key == pygame.K_UP :
                pMoveY -= Delta
            if event.key == pygame.K_DOWN :
                pMoveY += Delta
            if event.key == pygame.K_RIGHT :
                pMoveX  += Delta
            if event.key == pygame.K_LEFT :
                pMoveX -= Delta

            if event.key == pygame.K_SPACE :
                if bullet_state is "ready" :
                    bullet_sound = mixer.Sound("./resources/laser.wav")
                    bullet_sound.play()
                    bCoordX = pCoordX
                    bCoordY = pCoordY
                    fire(bCoordX, bCoordY)
            if event.key == pygame.K_ESCAPE : # wink
                Playing = True
                
        if pygame.event == pygame.KEYUP :
            pCoordX =  0
            pCoordY =  0
    
    pCoordX += pMoveX
    pCoordY += pMoveY
    pCoordX, pCoordY = boundaries(pCoordX, pCoordY)

    # enemy movement  and boundary check
    for i in range(nbEnemies) :

        # Game Over
        if eCoordY[i] >= height-enemyImage[i].get_height()*2 :
            for j in range(nbEnemies) :
                eCoordY[j] = height*2
            game_over()
            break
        # Call the enemy function adn draw it in the screen
        enemy(eCoordX[i],eCoordY[i],enemyImage[i])

        eCoordX[i] += eMoveX[i]
        if eCoordX[i] <= 0 :
            eMoveX[i] = eDelta[i]
            eCoordY[i] += 10
        elif eCoordX[i] >= width - enemyImage[i].get_width() - 1 :
            eMoveX[i] = -eDelta[i]
            eCoordY[i] += random.randint(0,100)

        eCoordX[i], eCoordY[i] = boundaries(eCoordX[i], eCoordY[i])

        #Collision
        collision = isCollision(eCoordX[i], eCoordY[i], bCoordX, bCoordY)
        if collision :

            explosion_sound = mixer.Sound("./resources/explosion.wav")
            explosion_sound.play()
            bCoordY = height + playerImage.get_height()
            bullet_state = "ready"
            score_value += 1 
            
            eCoordX[i] = random.randint(0, width  - enemyImage[i].get_width() - 1)
            eCoordY[i] = random.randint(0, 150)

    # Bullet Movement
    if bCoordY <=0 :
        bCoordY = height -playerImage.get_height()
        bullet_state = "ready"
    if bullet_state is "fire" :
        fire(bCoordX, bCoordY)
        bCoordY -= bMoveY

    # Call the player function and draw the characters in the screen
    player(pCoordX, pCoordY)

    #Text
    show_score(textX,textY)
    
    #update the changes made
    pygame.display.update()
