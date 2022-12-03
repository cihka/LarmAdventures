import math
import random
import time

import pygame
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

abc = 1 # Я не знаю зачем я єто сделал я тогда на солях был


pygame.display.set_caption("StarPool") 
icon = pygame.image.load('daunZ.png') 
pygame.display.set_icon(icon) 

playerImg = pygame.image.load('test1.png') 
playerX = 370 
playerY = 480 
playerX_change = 0 


putinImg = [] 
putinX = [] 
putinY = []
putinX_change = [] 
putinY_change = []
num_of_putin = 1 

enemyImg = [] 
enemyX = [] 
enemyY = [] 
enemyX_change = [] 
enemyY_change = [] 
num_of_enemies = 6 

lvlValue = 0 

health_putin = 5 
health_img = pygame.image.load('heart.png') #
health_img2 = pygame.transform.scale(health_img, (40, 40)) #

tryhard = 0 

def pause(): 
    global tryhard 
    paused = True 
    while paused: 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit() 
                quit() 
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_RETURN]: 
            paused = False 
        pygame.display.update() 
        clock.tick(90) 
        tryhard = 1 


for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('test.png')) 
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)
#
for p in range(num_of_putin):
    putinImg.append(pygame.image.load('boss.png'))
    putinX.append(400)
    putinY.append(100) 
    putinX_change.append(4) 
    putinY_change.append(40)

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

putinbulletImg = pygame.image.load('rocket.png')
putinbulletX = 0
putinbulletY = 100
putinbulletX_change = 0
putinbulletY_change = 10
putinbullet_state = "ready"


# Score

lvlValue = 0    
score_value = -1
font = pygame.font.Font('freesansbold.ttf', 32)


textX = 10
testY = 10
lvlX = 10
lvlY = 50

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)
over_font1 = pygame.font.Font('freesansbold.ttf', 20)
over_font2 = pygame.font.Font('freesansbold.ttf', 15)
over_fontLarm = pygame.font.Font('freesansbold.ttf', 25)

class Button():
    def __init__(self, width, height, inactive_color, active_color):
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
    def draw(self, x, y, message, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
            if click[0] == 1 and action is not None: # if button was pressed
                if action == quit:
                    pygame.quit()
                    quit()
                else:
                    action()
        else:
            pygame.draw.rect(screen , self.inactive_color, (x, y, self.width, self.height))
        print_text(message=message, x=x+10, y=y+10, font_size=font_size)

def print_text(message, x, y, font_color=(0, 0, 0), font_type='freesansbold.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))

def menu():
    global lvlValue, score_value, damn
    menu_background = pygame.image.load('menu0.png')

    start_btn = Button(200, 70, (255, 255, 255), (91, 94, 96))
    quit_btn = Button(200, 70, (255, 255, 255), (91, 94, 96))

    show = True

    damn = 1

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.blit(menu_background, (0, 0))

        if damn == 1:
            keys = pygame.key.get_pressed()
            pygame.draw.rect(screen, (0, 0, 0), (0, 400, 800, 200))
            print_text('Ларм: ', 10, 420, (255,255,255), 'freesansbold.ttf', 25)
            print_text('Привет, друг. Меня создали чтобы я тебе помог освоится на этом корабле.', 10, 460, (255,255,255), 'freesansbold.ttf', 20)
            print_text('Чтобы продолжить нажмите [SPACE]', 510, 560, (255,255,255), 'freesansbold.ttf', 15)
            larm_exit = pygame.image.load('larm_pause.png')
            screen.blit(larm_exit, (0,0))
            if keys[pygame.K_SPACE]:
                damn = 0


        if damn == 0:
            start_btn.draw(200, 200, 'START', start_game, 35)
            quit_btn.draw(200, 300, 'EXIT', quit, 35)

        if lvlValue >= 2 or score_value >= 1:
            pygame.draw.rect(screen, (0, 0, 0), (0, 400, 800, 200))
            print_text('Ларм: ', 10, 420, (255,255,255), 'freesansbold.ttf', 25)
            print_text('Жаль заканчивать игру на такой ноте...', 10, 460, (255,255,255), 'freesansbold.ttf', 20)
            larm_exit = pygame.image.load('larm_pause.png')
            screen.blit(larm_exit, (0,0))

        pygame.display.update()
        clock.tick(90)

def show_score(x, y):
    score = font.render("Счёт : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
def show_lvl(x, y):
    global lvlValue
    if lvlValue == 0:
        lvlValue = 1
    if lvlValue < 5:
        lvl = font.render("Уровень : " + str(lvlValue), True, (255, 255, 255))
        screen.blit(lvl, (x, y))
    else:
        lvl = font.render("Уровень : " + str('BOSS'), True, (255, 255, 255))
        screen.blit(lvl, (x, y))

def nextLvl(lvl):
    lvl += 1

def game_over_text():
    over_text = over_font.render("ПРОИГРАЛ ДОДИК!", True, (255, 255, 255))
    screen.blit(over_text, (120, 250))

scripts_dialog = [
    "Салага мы уже половину врагов уничтожили. Хахаха.", "Они стали злыми. Их осталось мало добей их.", "Выживи друг мой.",
    "Чтобы продолжить нажми [ENTER]"
]
def pause_helper(script):
    larm = pygame.image.load('larm_pause.png')
    pygame.draw.rect(screen, (0, 0, 0), (0, 400, 800, 200))
    script_textLarm = over_fontLarm.render("Ларм:", True, (255, 255, 255))
    script_text = over_font1.render(scripts_dialog[0], True, (255, 255, 255))
    script_text2 = over_font1.render(scripts_dialog[1], True, (255, 255, 255))
    script_text3 = over_font1.render(scripts_dialog[2], True, (255, 255, 255))
    script_text4 = over_font2.render(scripts_dialog[3], True, (255, 255, 255))
    screen.blit(script_textLarm, (10, 420))
    screen.blit(script_text, (10, 460))
    screen.blit(script_text2, (10, 490))
    screen.blit(script_text3, (10, 560))
    screen.blit(script_text4, (520, 560))
    screen.blit(larm, (0, 0))

def pause_helper1():
    global background, score_value, script1, tryhard
    background = pygame.image.load('herson.png')
    pygame.draw.rect(screen, (0, 0, 0), (0, 400, 800, 200))
    print_text('Ларм: ', 10, 420, (255,255,255), 'freesansbold.ttf', 25)
    print_text('Осторожно. Мы уже почти выйграли.', 10, 460, (255,255,255), 'freesansbold.ttf', 20)
    print_text('После этой победы мы спасём миллионы жизней', 10, 490, (255,255,255), 'freesansbold.ttf', 20)
    print_text('Выживи друг мой.', 10, 520, (255,255,255), 'freesansbold.ttf', 20)
    print_text('Чтобы продолжить нажмите [ENTER]', 510, 560, (255,255,255), 'freesansbold.ttf', 15)
    larm_exit = pygame.image.load('larm_pause.png')
    screen.blit(larm_exit, (0,0))
    score_value = 0 
    keys0 = pygame.key.get_pressed()
    score_value = 0 
    pause()

def player(x, y):
    global lvlValue
    if lvlValue >= 2:
        screen.blit(pygame.image.load('playerUA.png'), (x, y))
    else:
        screen.blit(playerImg, (x, y))

def pause_script1():
    global background, score_value, script1, tryhard
    background = pygame.image.load('herson.png')
    pygame.draw.rect(screen, (0, 0, 0), (0, 400, 800, 200))
    print_text('Ларм: ', 10, 420, (255,255,255), 'freesansbold.ttf', 25)
    print_text('ОУ ДА. Молодец парень. Это была только разминка', 10, 460, (255,255,255), 'freesansbold.ttf', 20)
    print_text('Сейчас мы полетим на планету Земля', 10, 490, (255,255,255), 'freesansbold.ttf', 20)
    print_text('Нам надо спасти народ Украины', 10, 520, (255,255,255), 'freesansbold.ttf', 20)
    print_text('Чтобы продолжить нажмите [ENTER]', 510, 560, (255,255,255), 'freesansbold.ttf', 15)
    larm_exit = pygame.image.load('larm_pause.png')
    screen.blit(larm_exit, (0,0))
    score_value = 0 
    keys0 = pygame.key.get_pressed()
    score_value = 0 
    pause()

def pause_script2():
    global background, score_value, script1, tryhard
    background = pygame.image.load('donezk.png')
    pygame.draw.rect(screen, (0, 0, 0), (0, 400, 800, 200))
    print_text('Ларм: ', 10, 420, (255,255,255), 'freesansbold.ttf', 25)
    print_text('ОУ ДА. Молодец парень. Мы освободили Херсон', 10, 460, (255,255,255), 'freesansbold.ttf', 20)
    print_text('Мы направляемся в Донецк', 10, 490, (255,255,255), 'freesansbold.ttf', 20)
    print_text('Спасём Украину от псевдо освободителей', 10, 520, (255,255,255), 'freesansbold.ttf', 20)
    print_text('Чтобы продолжить нажмите [ENTER]', 510, 560, (255,255,255), 'freesansbold.ttf', 15)
    larm_exit = pygame.image.load('larm_pause.png')
    screen.blit(larm_exit, (0,0))
    score_value = 0 
    keys0 = pygame.key.get_pressed()
    score_value = 0 
    pause()

def pause_script3():
    global background, score_value, script1, tryhard
    background = pygame.image.load('kreml.png')
    pygame.draw.rect(screen, (0, 0, 0), (0, 400, 800, 200))
    print_text('Ларм: ', 10, 420, (255,255,255), 'freesansbold.ttf', 25)
    print_text('ОУ ДА. Молодец парень. Мы освободили Донецк', 10, 460, (255,255,255), 'freesansbold.ttf', 20)
    print_text('Мы направляемся в Кремль', 10, 490, (255,255,255), 'freesansbold.ttf', 20)
    print_text('Сожжём кремль!!!', 10, 520, (255,255,255), 'freesansbold.ttf', 20)
    print_text('Чтобы продолжить нажмите [ENTER]', 510, 560, (255,255,255), 'freesansbold.ttf', 15)
    larm_exit = pygame.image.load('larm_pause.png')
    screen.blit(larm_exit, (0,0))
    score_value = 0 
    keys0 = pygame.key.get_pressed()
    score_value = 0 
    pause()

def pause_script4():
    global background, score_value, script1, tryhard
    background = pygame.image.load('kreml.png')
    pygame.draw.rect(screen, (0, 0, 0), (0, 400, 800, 200))
    print_text('Ларм: ', 10, 420, (255,255,255), 'freesansbold.ttf', 25)
    print_text('Ой ой ой. Появился главный.', 10, 460, (255,255,255), 'freesansbold.ttf', 20)
    print_text('Говорят он ест детей. И что он вообще не человек', 10, 490, (255,255,255), 'freesansbold.ttf', 20)
    print_text('Давай изгоним зло из мира!!!', 10, 520, (255,255,255), 'freesansbold.ttf', 20)
    print_text('Чтобы продолжить нажмите [ENTER]', 510, 560, (255,255,255), 'freesansbold.ttf', 15)
    larm_exit = pygame.image.load('larm_pause.png')
    screen.blit(larm_exit, (0,0))
    keys0 = pygame.key.get_pressed()
    score_value += 1
    pause()

def win_script():
    global background, score_value, script1, tryhard
    background = pygame.image.load('kreml.png')
    pygame.draw.rect(screen, (0, 0, 0), (0, 400, 800, 200))
    print_text('Ларм: ', 10, 420, (255,255,255), 'freesansbold.ttf', 25)
    print_text('ДАААА! Молодец капитан. Я в тебе не сомневался', 10, 460, (255,255,255), 'freesansbold.ttf', 20)
    print_text('Мы сделали великое и доброе дело', 10, 490, (255,255,255), 'freesansbold.ttf', 20)
    print_text('После которого мы можем отправится в новое путешевствие', 10, 520, (255,255,255), 'freesansbold.ttf', 20)
    print_text('Чтобы выйти нажмите [ENTER]', 510, 560, (255,255,255), 'freesansbold.ttf', 15)
    larm_exit = pygame.image.load('larm_pause.png')
    screen.blit(larm_exit, (0,0))
    score_value = 0 
    keys0 = pygame.key.get_pressed()
    score_value = 0 
    pause()

def end_script():
    global background, score_value, script1, tryhard
    background = pygame.image.load('kreml.png')
    pygame.draw.rect(screen, (0, 0, 0), (0, 400, 800, 200))
    print_text('Ларм: ', 10, 420, (255,255,255), 'freesansbold.ttf', 25)
    print_text('Как так...', 10, 460, (255,255,255), 'freesansbold.ttf', 20)
    print_text('Когда же я найду великого хозяина????', 10, 490, (255,255,255), 'freesansbold.ttf', 20)
    print_text('Чтобы выйти нажмите [ENTER]', 510, 560, (255,255,255), 'freesansbold.ttf', 15)
    larm_exit = pygame.image.load('larm_pause.png')
    screen.blit(larm_exit, (0,0))
    score_value = 0 
    keys0 = pygame.key.get_pressed()
    score_value = 0 
    pause()



def enemy(x, y, i, hard):
    if hard >= 2:
        screen.blit(pygame.image.load('enemyZ1.png'), (x, y))
    if hard >= 4:
        screen.blit(pygame.image.load('daunZ.png'), (x, y))
    if hard == 1:       
        screen.blit(enemyImg[i], (x, y))

def putin(x, y, i, hard):
    screen.blit(putinImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def putinfire_bullet(x, y):
    global putinbullet_state
    putinbullet_state = "fire"
    screen.blit(putinbulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def welcome():
    pygame.draw.rect(screen, (0, 0, 0), (0, 400, 800, 200))
    print_text('Ларм: ', 10, 420, (255,255,255), 'freesansbold.ttf', 25)
    print_text('Снова привет, парень. Меня зовут Ларм. Я роботттт', 10, 460, (255,255,255), 'freesansbold.ttf', 20)
    print_text('Который отвечает за этот корабль', 10, 490, (255,255,255), 'freesansbold.ttf', 20)
    print_text('Давай убьём их всех!!!', 10, 520, (255,255,255), 'freesansbold.ttf', 20)
    print_text('Чтобы продолжить нажмите [ENTER]', 510, 560, (255,255,255), 'freesansbold.ttf', 15)
    larm_exit = pygame.image.load('larm_pause.png')
    screen.blit(larm_exit, (0,0))

clock = pygame.time.Clock()
background = pygame.image.load('1619113741_13-phonoteka_org-p-chyornii-fon-bez-nichego-13.jpg')

def show_health():
    global health_putin
    show = 0
    x = 300
    while show != health_putin:
        screen.blit(health_img2, (x, 20) )
        x += 40
        show += 1

def check_health():
    global health_putin, running
    health_putin -= 1
    if health_putin == 0:
        win_script()
        quit()

def start_game():

    global background, playerX, playerX_change, playerY, bulletX, bulletY, lvlValue, bullet_state, score_value, tryhard, script1, abc, i

    running = True

    while running == True:

        screen.fill((0, 0, 0))

        screen.blit(background, (0, 0))

        chlen = 1

        if chlen == 1:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        playerX_change = -5
                    if event.key == pygame.K_RIGHT:
                        playerX_change = 5
                    if event.key == pygame.K_SPACE:
                        if bullet_state == "ready":
                            bulletSound = mixer.Sound("laser.wav")
                            bulletSound.play()
                            bulletX = playerX
                            fire_bullet(bulletX, bulletY)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        playerX_change = 0


            playerX += playerX_change
            if playerX <= 0:
                playerX = 0
            elif playerX >= 736:
                playerX = 736

            for i in range(num_of_enemies):

                if enemyY[i] > 440:
                    for j in range(num_of_enemies):
                        enemyY[j] = 2000
                    end_script()
                    quit()
                    break
                enemyX[i] += enemyX_change[i]
                if enemyX[i] <= 0:
                    enemyX_change[i] = 4
                    enemyY[i] += enemyY_change[i]
                elif enemyX[i] >= 736:
                    enemyX_change[i] = -4
                    enemyY[i] += enemyY_change[i]

                collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
                if collision:
                    explosionSound = mixer.Sound("explosion.wav")
                    explosionSound.play()
                    bulletY = 480
                    bullet_state = "ready"
                    score_value += 1
                    if score_value == 20:
                        lvlValue += 1
                        score_value = 0
                        if lvlValue == 2:
                            pause_script1()
                        if lvlValue == 3:
                            pause_script2()
                        if lvlValue == 4:
                            pause_script3()
                        if lvlValue == 5:
                            game_boss()
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(50, 150)

                enemy(enemyX[i], enemyY[i], i, lvlValue)

            if bulletY <= 0:
                bulletY = 480
                bullet_state = "ready"

            if bullet_state == "fire":
                fire_bullet(bulletX, bulletY)
                bulletY -= bulletY_change

            player(playerX, playerY)
            show_score(textX, testY)
            show_lvl(lvlX, lvlY)
            if lvlValue == 1 and score_value == -1:
                welcome()
                pause()
                score_value += 1
            if score_value == 10:
                pause_helper(lvlX)
                pause()
                score_value += 1
                print(tryhard)
            pygame.display.update()
            clock.tick(90)


def game_boss():        

    global background, playerX, playerX_change, playerY, bulletX, putinbulletX, putinbulletY, bulletY, lvlValue, putinbullet_state, bullet_state, score_value, tryhard, script1, abc, health_putin, playerImg

    playerImg = pygame.image.load('playerUA.png')

    playerX = 100

    score_value = -1

    running = True

    while running == True:
        
        background = pygame.image.load('kreml.png')
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        chlen = 1


        if score_value == -1:
            pause_script4() 

        show_health()
          
        if chlen == 1:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        playerX_change = -5
                    if event.key == pygame.K_RIGHT:
                        playerX_change = 5
                    if event.key == pygame.K_SPACE:
                        if bullet_state == "ready":
                            bulletSound = mixer.Sound("laser.wav")
                            bulletSound.play()
                            bulletX = playerX
                            fire_bullet(bulletX, bulletY)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        playerX_change = 0

        if abc == 1:
            if putinbullet_state == "ready":
                bulletSound = mixer.Sound("laser.wav")
                bulletSound.play()
                putinbulletX = putinX[p]
                putinfire_bullet(putinbulletX, putinbulletY)

            playerX += playerX_change
            if playerX <= 0:
                playerX = 0
            elif playerX >= 736:
                playerX = 736

            for i in range(num_of_putin):

                if putinY[p] > 440:
                    for j in range(num_of_putin):
                        putinY[j] = 2000
                    game_over_text()
                    break
                putinX[p] += putinX_change[p]
                if putinX[p] <= 0:
                    putinX_change[p] = 4
                elif putinX[p] >= 736:
                    putinX_change[p] = -4

                collision = isCollision(putinX[p], putinY[p], bulletX, bulletY)
                if collision:
                    explosionSound = mixer.Sound("explosion.wav")
                    explosionSound.play()
                    bulletY = 480
                    bullet_state = "ready"
                    putinbulletY = 100
                    putinbullet_state = "ready"
                    score_value += 1
                    if not check_health():
                        a = 0
                chlencollision = isCollision(playerX, playerY, putinbulletX, putinbulletY)
                if chlencollision:
                    end_script()
                    quit()
                putin(putinX[p], putinY[p], i, lvlValue)
                
            if putinbulletY >= 600:
                putinbulletY = 100
                putinbullet_state = "ready"

            if putinbullet_state == "fire":
                putinfire_bullet(putinbulletX, putinbulletY)
                putinbulletY += putinbulletY_change

            if bulletY <= 0:
                bulletY = 480
                bullet_state = "ready"

            if bullet_state == "fire":
                fire_bullet(bulletX, bulletY)
                bulletY -= bulletY_change

            player(playerX, playerY)
            show_score(textX, testY)
            show_lvl(lvlX, lvlY)
            if score_value == 3:
                pause_helper1()
            pygame.display.update()
            clock.tick(90)

menu()