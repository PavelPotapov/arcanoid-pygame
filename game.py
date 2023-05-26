import pygame
pygame.init()

#фоновая музыка
volume = 0.1
pygame.mixer.music.load("sounds/fon.mp3") #загрузили
pygame.mixer.music.play(-1) #зациклили (-1)
pygame.mixer.music.set_volume(volume) #устанвоили громкость

hit = pygame.mixer.Sound("sounds/hit.wav") #звук удара
lose = pygame.mixer.Sound("sounds/lose.wav") #звук проигрыша
win = pygame.mixer.Sound("sounds/win.wav") #звук победы

window = pygame.display.set_mode([500,500])
back_color = (114,225,237)
clock = pygame.time.Clock()
run = True

class Picture():
    def __init__(self, x, y, w, h, image_name):
        self.rect = pygame.Rect(x,y,w,h)
        self.image = pygame.image.load(image_name)
        self.image = pygame.transform.scale(self.image, (w,h))
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

platform = Picture(210, 430, 100, 20, 'images/platform.png')
ball = Picture(230, 250, 40,40, 'images/ball.png')

enemies = []

#1 ряд врагов
x_start = 0
for i in range(9):
    enemy1 = Picture(x_start,0,50,50, 'images/enemy.png')
    x_start += 55
    enemies.append(enemy1)
#2 ряд врагов
x_start = 0
for i in range(9):
    enemy1 = Picture(x_start,50,50,50, 'images/enemy.png')
    x_start += 55
    enemies.append(enemy1)

#3 ряд врагов
x_start = 0
for i in range(9):
    enemy1 = Picture(x_start,100,50,50, 'images/enemy.png')
    x_start += 55
    enemies.append(enemy1)

dx = 1
dy = 1 

def restart():
    enemies.clear()
    x_start = 0
    for i in range(9):
        enemy1 = Picture(x_start,0,50,50, 'images/enemy.png')
        x_start += 55
        enemies.append(enemy1)
    #2 ряд врагов
    x_start = 0
    for i in range(9):
        enemy1 = Picture(x_start,50,50,50, 'images/enemy.png')
        x_start += 55
        enemies.append(enemy1)

    #3 ряд врагов
    x_start = 0
    for i in range(9):
        enemy1 = Picture(x_start,100,50,50, 'images/enemy.png')
        x_start += 55
        enemies.append(enemy1)
    

win_text = pygame.font.Font(None, 70).render('ПОБЕДА!', True, (0,255,0))
lose_text = pygame.font.Font(None, 70).render('ПОРАЖЕНИЕ!', True, (255,0,0))
finish = False 

while run:
    if finish == False:
        window.fill(back_color)
        platform.draw()
    
        for enemy in enemies:
            enemy.draw()
        ball.draw()
        #движение платформы
        keys = pygame.key.get_pressed() #получаем список состояния всех клавиш клавиатуры
        if keys[pygame.K_RIGHT] and platform.rect.x < 400: #если нажали на стрелку вправо
            platform.rect.x += 3
        elif keys[pygame.K_LEFT] and platform.rect.x > 0: #если нажали на стрелку влево
            platform.rect.x -= 3

        #движение шарика
        ball.rect.x += dx*3
        ball.rect.y += dy*3
        #проверка столкновения шарика и левой и правой стенки (изменения его dx в случае столкновения)
        if ball.rect.x > 450 or ball.rect.x < 0:
            dx *= -1
            hit.play()
        #проверка столкновения шарика и нижней и верхней стенки (изменения его dy в случае столкновения)
        if ball.rect.y < 0 or ball.rect.y > 450:                  
            dy *= -1
            hit.play()

        #проверка на столкновение шарика и платформы
        if platform.rect.colliderect(ball.rect):
            dy *= -1
            hit.play()

        #проверка на столкновение шарика с врагами
        for enemy in enemies: #перебираем список всех врагов
            if ball.rect.colliderect(enemy.rect): #для каждого врана делаем проверку на столкновение
                dy *= -1
                hit.play()
                enemies.remove(enemy) #удаляем врага из списка, потому что его выбили!
            
        if ball.rect.y > platform.rect.y:
            lose.play()
            window.blit(lose_text, (100,200))
            finish = True
        
        if len(enemies) == 0:
            win.play()
            window.blit(win_text, (100,200))
            finish = True
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and finish == True:
            finish = False
            platform = Picture(210, 430, 100, 20, 'images/platform.png')
            ball = Picture(230, 250, 40,40, 'images/ball.png')
            dx = 1
            dy = 1 
            restart()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                volume += 0.05
                pygame.mixer.music.set_volume(volume)
                win.set_volume(volume)
                hit.set_volume(volume)
                lose.set_volume(volume)
            if event.key == pygame.K_DOWN:
                volume -= 0.05
                pygame.mixer.music.set_volume(volume)
                win.set_volume(volume)
                hit.set_volume(volume)
                lose.set_volume(volume)

    clock.tick(60)
    pygame.display.update()