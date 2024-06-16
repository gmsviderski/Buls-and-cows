import pygame
import json
from random import sample

# Инициализация Pygame
pygame.init()

# Параметры экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Быки и коровы")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Шрифты
font = pygame.font.Font(None, 36)

# Загрузка настроек
try:
    with open('settings.json', 'r') as f:
        settings = json.load(f)
except FileNotFoundError:
    settings = {"num_digits": 4}
    with open('settings.json', 'w') as f:
        json.dump(settings, f)

num_digits = settings["num_digits"]


# Функция для генерации случайного числа
def generate_number(num_digits):
    return ''.join(map(str, sample(range(10), num_digits)))


# Функция для подсчёта быков и коров
def calculate_bulls_and_cows(secret, guess):
    bulls = cows = 0
    for i in range(len(guess)):
        if guess[i] == secret[i]:
            bulls += 1
        elif guess[i] in secret:
            cows += 1
    return bulls, cows


# Основные переменные игры
secret_number = generate_number(num_digits)
attempts = []
input_number = ''
max_attempts = 10

# Основной игровой цикл
running = True
while running:
    screen.fill(WHITE)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if len(input_number) == num_digits:
                    bulls, cows = calculate_bulls_and_cows(secret_number, input_number)
                    attempts.append((input_number, bulls, cows))
                    input_number = ''
                    if bulls == num_digits or len(attempts) >= max_attempts:
                        running = False
            elif event.key == pygame.K_BACKSPACE:
                input_number = input_number[:-1]
            elif event.unicode.isdigit() and len(input_number) < num_digits:
                input_number += event.unicode

    # Отображение текущего ввода
    input_text = font.render(f'Введите ваше число: {input_number}', True, BLACK)
    screen.blit(input_text, (20, 20))

    # Отображение попыток
    for i, (guess, bulls, cows) in enumerate(attempts):
        attempt_text = font.render(f'{i + 1}. {guess} - Быков: {bulls}, Коров: {cows}', True, BLACK)
        screen.blit(attempt_text, (20, 60 + i * 30))
    pygame.display.flip()
# Вывод результата игры
screen.fill(WHITE)
result_text = font.render(f'Загаданное число: {secret_number}', True, BLACK)
screen.blit(result_text, (20, 20))
if len(attempts) >= max_attempts and attempts[-1][1] != num_digits:
    end_text = font.render('Вы проиграли!', True, BLACK)
else:
    end_text = font.render('Поздравляю! Вы угадали число!!', True, BLACK)
screen.blit(end_text, (20, 60))
pygame.display.flip()
pygame.time.wait(4000)

# Завершение Pygame
pygame.quit()