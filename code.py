import pygame
import random

# Константы
WIDTH, HEIGHT = 800, 600
TARGET_INCREMENT = 1000  # миллисекунд
TARGET_PADDING = 50
TOP_BAR_HEIGHT = 50
LABEL_FONT = pygame.font.SysFont('Arial', 24)
TARGET_EVENT = pygame.USEREVENT + 1
LIVES = 3

# Цвета для выбора
COLORS = {
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
    "Purple": (128, 0, 128)
}

# Цвета фона
BACKGROUND_COLORS = {
    "Light Gray": (211, 211, 211),
    "Light Blue": (173, 216, 230),
    "Light Purple": (230, 230, 250),
    "Light Pink": (255, 182, 193)
}

# Типы мишеней
TARGET_TYPES = {
    "Circle": "circle",
    "Oval": "oval",
    "Cross": "cross",
    "Triangle": "triangle"
}

# Размеры мишеней
TARGET_SIZES = [20, 30, 40, 50]  # Возможные размеры


class Target:
    MAX_SIZE = 50
    GROWTH_RATE = 1

    def __init__(self, x, y, color, target_type):
        self.size = 20
        self.x = x
        self.y = y
        self.color = color
        self.target_type = target_type

    def update(self):
        self.size += self.GROWTH_RATE
        if self.size > self.MAX_SIZE or self.size < 20:
            self.GROWTH_RATE = -self.GROWTH_RATE

    def draw(self, win):
        if self.target_type == "circle":
            pygame.draw.circle(win, self.color, (self.x, self.y), self.size)
        elif self.target_type == "oval":
            pygame.draw.ellipse(win, self.color,
                                (self.x - self.size // 2, self.y - self.size // 4, self.size, self.size // 2))
        elif self.target_type == "cross":
            pygame.draw.line(win, self.color, (self.x - self.size // 2, self.y), (self.x + self.size // 2, self.y),
                             5)  # Горизонтальная линия
            pygame.draw.line(win, self.color, (self.x, self.y - self.size // 2), (self.x, self.y + self.size // 2),
                             5)  # Вертикальная линия
        elif self.target_type == "triangle":
            points = [
                (self.x, self.y - self.size // 2),  # Верх
                (self.x - self.size // 2, self.y + self.size // 2),  # Левый нижний
                (self.x + self.size // 2, self.y + self.size // 2)  # Правый нижний
            ]
            pygame.draw.polygon(win, self.color, points)

    def collide(self, x, y):
        return (x - self.x) ** 2 + (y - self.y) ** 2 < self.size ** 2


class Display:
    @staticmethod
    def draw(win, targets):
        win.fill(BG_COLOR)
        for target in targets:
            target.draw(win)
        pygame.display.update()

    @staticmethod
    def draw_top_bar(win, elapsed_time, targets_pressed, misses):
        pygame.draw.rect(win, (50, 50, 50), (0, 0, WIDTH, TOP_BAR_HEIGHT))
        time_str = format_time(elapsed_time)
        score_text = LABEL_FONT.render(f'Score: {targets_pressed} Misses: {misses} Time: {time_str}', True,
                                       (255, 255, 255))
        win.blit(score_text, (10, 10))

    @staticmethod
    def end_screen(win, elapsed_time, targets_pressed, misses, lives):
        win.fill(BG_COLOR)
        end_text = f'Game Over! Hits: {targets_pressed} Misses: {misses} ' \
                   f'Time: {format_time(elapsed_time)} Lives Lost: {lives}'
        accuracy = (targets_pressed / (targets_pressed + misses) * 100) if (targets_pressed + misses) > 0 else 0
        stats_text = f'Accuracy: {accuracy:.2f}%'
        end_surface = LABEL_FONT.render(end_text, True, (255, 255, 255))
        stats_surface = LABEL_FONT.render(stats_text, True, (255, 255, 255))

        win.blit(end_surface, (WIDTH // 2 - end_surface.get_width() // 2, HEIGHT // 2 - 40))
        win.blit(stats_surface, (WIDTH // 2 - stats_surface.get_width() // 2, HEIGHT // 2 + 10))
        pygame.display.update()
        pygame.time.delay(2000)


class Stats:
    def __init__(self):
        self.hits = 0
        self.misses = 0

    def record_hit(self):
        self.hits += 1

    def record_miss(self):
        self.misses += 1


class Game:
    def __init__(self, target_color, target_type, target_size, bg_color):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)
        self.targets = []
        self.stats = Stats()
        self.elapsed_time = 0
        self.lives = LIVES
        self.clock = pygame.time.Clock()
        self.running = True
        self.target_color = target_color  # Цвет мишеней
        self.target_type = target_type  # Тип мишени
        self.target_size = target_size  # Размер мишени
        global BG_COLOR
        BG_COLOR = bg_color  # Цвет фона

    def run_game(self):
        start_ticks = pygame.time.get_ticks()
        while self.running:
            elapsed_seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            self.elapsed_time = elapsed_seconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == TARGET_EVENT:
                    if self.lives > 0:
                        x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                        y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                        self.targets.append(Target(x, y, self.target_color, self.target_type))
                    else:
                        self.running = False  # Завершить игру, если осталось 0 жизней
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for target in self.targets:
                        if target.collide(x, y):
                            self.stats.record_hit()
                            self.targets.remove(target)
                            break
                    else:
                        self.stats.record_miss()
                        self.lives -= 1

            Display.draw_top_bar(self.win, self.elapsed_time, self.stats.hits, self.stats.misses)
            Display.draw(self.win, self.targets)
            self.clock.tick(60)

        Display.end_screen(self.win, self.elapsed_time, self.stats.hits, self.stats.misses, LIVES - self.lives)
        pygame.quit()


def format_time(secs):
    minutes = int(secs // 60)
    seconds = int(secs % 60)
    milliseconds = int((secs - minutes * 60 - seconds) * 100)
    return f"{minutes:02}:{seconds:02}.{milliseconds:02}"


def main_menu():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Aim Trainer - Choose Options")
    clock = pygame.time.Clock()

    selected_color = (255, 0, 0)  # Цвет по умолчанию (красный)
    selected_type = "circle"  # Тип по умолчанию (круг)
    selected_size = 20  # Размер по умолчанию
    bg_color_keys = list(BACKGROUND_COLORS.keys())
    current_bg_index = 0  # Индекс текущего цвета фона
    target_color_keys = list(COLORS.keys())
    current_color_index = 0  # Индекс текущего цвета мишеней
    target_type_keys = list(TARGET_TYPES.keys())
    current_type_index = 0  # Индекс текущего типа мишени
    current_size_index = 0  # Индекс текущего размера мишени

    while True:
        win.fill((255, 255, 255))  # Белый фон для меню
        y_offset = 100

        # Выбор цвета мишеней
        win.blit(LABEL_FONT.render("Select Target Color:", True, (0, 0, 0)), (WIDTH // 2 - 100, y_offset))
        for i, color_name in enumerate(target_color_keys):
            color_value = COLORS[color_name]
            pygame.draw.rect(win, color_value, (WIDTH // 2 - 50, y_offset + i * 30 + 30, 100, 20))
            if i == current_color_index:
                pygame.draw.rect(win, (255, 0, 0), (WIDTH // 2 - 50, y_offset + i * 30 + 30, 100, 20), 3)
        y_offset += len(target_color_keys) * 30 + 50

        # Выбор типа мишени
        win.blit(LABEL_FONT.render("Select Target Type:", True, (0, 0, 0)), (WIDTH // 2 - 100, y_offset))
        for i, type_name in enumerate(target_type_keys):
            if i == current_type_index:
                pygame.draw.rect(win, (255, 0, 0), (WIDTH // 2 - 50, y_offset + i * 30 + 30, 100, 20), 3)
            win.blit(LABEL_FONT.render(type_name, True, (0, 0, 0)), (WIDTH // 2 - 80, y_offset + i * 30 + 30))
        y_offset += len(target_type_keys) * 30 + 50

        # Выбор размера мишени
        win.blit(LABEL_FONT.render("Select Target Size:", True, (0, 0, 0)), (WIDTH // 2 - 100, y_offset))
        for i, size in enumerate(TARGET_SIZES):
            size_text = LABEL_FONT.render(f"{size}", True, (0, 0, 0))
            if i == current_size_index:
                pygame.draw.rect(win, (255, 0, 0), (WIDTH // 2 - 50, y_offset + i * 30 + 30, 100, 20), 3)
            win.blit(size_text, (WIDTH // 2 - size_text.get_width() // 2, y_offset + i * 30 + 30))
        y_offset += len(TARGET_SIZES) * 30 + 50

        # Выбор цвета фона
        win.blit(LABEL_FONT.render("Select Background Color:", True, (0, 0, 0)), (WIDTH // 2 - 140, y_offset))
        for i, bg_color_name in enumerate(bg_color_keys):
            bg_color_value = BACKGROUND_COLORS[bg_color_name]
            pygame.draw.rect(win, bg_color_value, (WIDTH // 2 - 50, y_offset + i * 30 + 30, 100, 20))
            if i == current_bg_index:
                pygame.draw.rect(win, (255, 0, 0), (WIDTH // 2 - 50, y_offset + i * 30 + 30, 100, 20), 3)

        # Инструкции для выбора цвета фона
        instruction_text = LABEL_FONT.render("Use Left/Right arrows to select background color", True, (0, 0, 0))
        win.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT - 50))

        # Обработка нажатий клавиш для выбора
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            current_color_index = (current_color_index - 1) % len(target_color_keys)  # Переключение вверх
        if keys[pygame.K_DOWN]:
            current_color_index = (current_color_index + 1) % len(target_color_keys)  # Переключение вниз
        if keys[pygame.K_LEFT]:
            current_bg_index = (current_bg_index - 1) % len(bg_color_keys)  # Переключение влево
        if keys[pygame.K_RIGHT]:
            current_bg_index = (current_bg_index + 1) % len(bg_color_keys)  # Переключение вправо
        if keys[pygame.K_a]:
            current_type_index = (current_type_index - 1) % len(target_type_keys)  # Переключение через 'A'
        if keys[pygame.K_d]:
            current_type_index = (current_type_index + 1) % len(target_type_keys)  # Переключение через 'D'
        if keys[pygame.K_w]:
            current_size_index = (current_size_index - 1) % len(TARGET_SIZES)  # Переключение через 'W'
        if keys[pygame.K_s]:
            current_size_index = (current_size_index + 1) % len(TARGET_SIZES)  # Переключение через 'S'

        # Начать игру
        y_offset += 20  # Отступ от выбора цвета фона
        start_game_text = LABEL_FONT.render("Start Game", True, (0, 0, 0))
        win.blit(start_game_text, (WIDTH // 2 - start_game_text.get_width() // 2, y_offset))
        if y_offset <= pygame.mouse.get_pos()[1] <= y_offset + 30 and pygame.mouse.get_pressed()[0]:
            selected_color = COLORS[target_color_keys[current_color_index]]
            selected_type = TARGET_TYPES[target_type_keys[current_type_index]]
            selected_size = TARGET_SIZES[current_size_index]
            selected_bg_color = BACKGROUND_COLORS[bg_color_keys[current_bg_index]]
            return selected_color, selected_type, selected_size, selected_bg_color

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    chosen_color, chosen_type, chosen_size, chosen_bg_color = main_menu()
    game = Game(chosen_color, chosen_type, chosen_size, chosen_bg_color)
    game.run_game()