from all_colors import *
import pygame
pygame.init()

# shot_sound = pygame.mixer.Sound('')
size = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
BACKGROUND = (255, 255, 255)
screen.fill(BACKGROUND)

screen_rect = screen.get_rect()

ship = pygame.Rect(300, 200,  50, 100)
ship.right = screen_rect.right
ship.centery = screen_rect.centery

missile = pygame.Rect(50, 50, 10, 10)
missile.left = screen_rect.left
missile.centery = screen_rect.centery

missile_speed_x = 0
missile_speed_y = 0

ship_speed_y = 1

ship_alive = True
missile_alive = True  # Пуля всегда видна на экране

missile_launched = False
hp_ship = 10
ammo = 11  # Количество патронов

FPS = 120
clock = pygame.time.Clock()
running = True
game_over = False  # Флаг для завершения игры
result_text = ""  # Текст результата игры

while running:
    # Обработка событий игры
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not missile_launched and ammo > 0:
                missile_launched = True
                missile_speed_x = 3  # Пуля летит вправо
                ammo -= 1  # Тратим один патрон

    # Движение пули вверх и вниз перед запуском
    keys = pygame.key.get_pressed()
    if not missile_launched:
        if keys[pygame.K_w]:
            missile.y -= 2  # Движение вверх
        if keys[pygame.K_s]:
            missile.y += 2  # Движение вниз

    # Основная логика игры
    if not game_over:
        if missile_launched:
            missile.move_ip(missile_speed_x, missile_speed_y)
            if not missile.colliderect(screen_rect):
                missile_launched = False
                # Сбрасываем пулю в начальное положение
                missile.left = screen_rect.left
                missile.centery = screen_rect.centery
            if ship_alive and missile.colliderect(ship):
                missile_launched = False
                hp_ship -= 1  # Теряем одну жизнь
                if hp_ship <= 0:
                    ship_alive = False
                # Сбрасываем пулю в начальное положение
                missile.left = screen_rect.left
                missile.centery = screen_rect.centery

        if ship_alive:
            ship.move_ip(0, ship_speed_y)
        if ship.bottom > screen_rect.bottom or ship.top < screen_rect.top:
            ship_speed_y = -ship_speed_y

        # Проверка условий победы и поражения
        if ammo <= 0 and hp_ship > 0:
            game_over = True
            result_text = "ПРОИГРЫШ"
        elif ammo <= 0 and hp_ship <= 0:
            game_over = True
            result_text = "ПОБЕДА"

    # Отрисовка объектов
    screen.fill(BACKGROUND)  # очистка экрана
    if ship_alive:
        pygame.draw.rect(screen, BLUE, ship)
    pygame.draw.rect(screen, RED, missile)  # Пуля всегда отрисовывается

    # Отображение количества патронов и жизней
    font = pygame.font.Font(None, 36)
    ammo_text = font.render(f'Ammo: {ammo}', True, BLACK)
    hp_text = font.render(f'HP: {hp_ship}', True, BLACK)
    screen.blit(ammo_text, (10, 10))
    screen.blit(hp_text, (10, 50))

    # Отображение результата игры
    if game_over:
        result_font = pygame.font.Font(None, 74)
        result_surface = result_font.render(result_text, True, RED)
        result_rect = result_surface.get_rect(center=(screen_rect.centerx, screen_rect.centery))
        screen.blit(result_surface, result_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()