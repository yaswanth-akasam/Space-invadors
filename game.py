import pygame
import random
import math
import time
from pygame import mixer
import os



pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))


# title and icon for the project
pygame.display.set_caption("Space game")
icon = pygame.image.load(os.path.join("Assets","icon.png"))
pygame.display.set_icon(icon)





# screen background
background = pygame.image.load(os.path.join("Assets","bg.png"))
# background music
# pygame.mixer.music.load(os.path.join("Assets","pubgbgm.wav"))
# pygame.mixer.music.play(-1)


rightedge = 800
leftedge = 0
playersize = 64

# playerImg
playerImg = pygame.image.load(os.path.join(os.path.join("Assets","player.png")))
playerX = 370
playerY = 480
playerX_change = 0

# enemyImg
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
enemyImg=[]
nums_of_enemy=6



for i in range(nums_of_enemy):
    enemyImg.append(pygame.image.load(os.path.join("Assets","swag.png")))
    enemyX.append(random.randint(0, rightedge-playersize))
    enemyY.append(random.randint(50, 200))

    enemyX_change.append(10.0)
    enemyY_change.append(40)


#bullet
bulletImg = pygame.image.load(os.path.join("Assets","bullet.png")) 
bulletX = 370
bulletY = 480
bulletY_change = 20
bullet_state = "ready"

# score value
score_value = 0
textX = 10
textY = 10
font = pygame.font.Font("freesansbold.ttf",30)
overtext = pygame.font.Font("freesansbold.ttf",100)

# game over 
def gameover():
    gameovertext = overtext.render("GAME OVER",True,(0,255,0))
    screen.blit(gameovertext,(100,280))





# def stopwatch():
#     start_time = 60
#     frame_count = 0
#     frame_rate = 60
#     total_seconds = 0
#     total_seconds = start_time - (frame_count // frame_rate)
#     if total_seconds < 0:
#         total_seconds = 0
#     seconds = total_seconds % 60
#     timeout = font.render(f"Timer:{seconds}",True,(0,255,0))
#     screen.blit(timeout,(600,10))
#     frame_count += 1

 
   
   

    
score = 0
def show_score(x,y):
    score = font.render("Score :"+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def kills():
    finalscore = font.render("FINALSCORE :"+str(score_value),True,(0,255,0))
    screen.blit(finalscore,(330,400))







def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y,i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10))

#collision happens
def iscollision(enemyX,enemyY,playerX,playerY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance <= 45.2:
        return True
    else:
        return False
FPS = 60
    


press =None
# display game loop
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(FPS)
    screen.fill((0,0,0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        # quit event
        if event.type == pygame.QUIT:
            running = False
        
        # keydown event

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -10.0
            if event.key == pygame.K_RIGHT:
                playerX_change = 10.0
            if event.key == pygame.K_SPACE:
               if bullet_state == "ready":
                    bullet_Sound = mixer.Sound(os.path.join("Assets","laser.wav"))
                    bullet_Sound.play()
                
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
            
            
                

        # key realse event
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    # player movement 
    playerX += playerX_change

    # restrict the player
    if playerX <= 0:
        playerX = leftedge
    elif playerX >= rightedge-playersize:
        playerX = rightedge-playersize

    
    for i in range(nums_of_enemy):

        if enemyY[i]>420:
            for j in range(nums_of_enemy):
                enemyY[j]=2000
            gameover()
            kills()

            break
        if pygame.time.Clock().get_time() == 6000:
            for j in range(nums_of_enemy):
                enemyY[j]=2000
            gameover()

            break



        enemyX[i] += enemyX_change[i]
        # enemy movement
        if enemyX[i] <= 0:
            enemyX_change[i] = 7.0
            enemyY_change[i] = 40
            enemyY[i] += enemyY_change[i]
        if enemyX[i]>= rightedge-playersize:
            enemyX_change[i] = -7.0
            enemyY_change[i] = 40
            enemyY[i]+= enemyY_change[i]
        
        # enemy collision detection

        collision = iscollision(enemyX[i], enemyY[i],bulletX, bulletY)
        if collision:
            explosion_Sound=mixer.Sound(os.path.join("Assets", "explosion.wav")) 
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            enemyX[i] = random.randint(0, rightedge-playersize)
            enemyY[i] = random.randint(50, 200)
            score_value += 1
        
        enemy(enemyX[i], enemyY[i],i)

    # bullet restrict
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if collision:
        bulletY = 480
        bullet_state = "ready"
    

    

    # player calling
    player(playerX, playerY)
    show_score(textX,textY)
    # stopwatch()
    
    # bullet fire bullet_state
    if bullet_state == "fire":
       fire_bullet(bulletX, bulletY)
       bulletY -= bulletY_change
    
    

       

    pygame.display.update()
