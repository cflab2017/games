import pygame
import random
import math

# 초기화
pygame.init()

# 화면 크기 설정
screen = pygame.display.set_mode((800, 600))

# 배경 이미지
background = pygame.image.load('background.png')

# 제목과 아이콘
pygame.display.set_caption("Galaga")
icon = pygame.image.load('spaceship.png')
icon = pygame.transform.scale(icon, (80, 80))
pygame.display.set_icon(icon)

# 플레이어
playerImg = pygame.image.load('player.png')
playerImg = pygame.transform.scale(playerImg, (80, 80))
playerX = 370
playerY = 480
playerX_change = 0

# 적
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    img = pygame.image.load('enemy.png')
    img = pygame.transform.scale(img, (80, 80))
    enemyImg.append(img)
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# 탄환
bulletImg = pygame.image.load('bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (40, 80))
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# 점수
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# 게임 오버 텍스트
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# 게임 루프
running = True
while running:
    screen.fill((0, 0, 0))  # 화면을 검은색으로 채우기
    screen.blit(background, (0, 0))  # 배경 이미지 그리기

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 키보드 입력 확인
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 플레이어 위치 업데이트
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # 적 위치 업데이트
    for i in range(num_of_enemies):

        # 게임 오버
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # 충돌 감지
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # 탄환 움직임
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
