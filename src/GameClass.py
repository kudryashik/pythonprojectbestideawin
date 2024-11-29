import pygame
import random

from TargetClass import Target
from StatsClass import Stats
from constants import LABEL_FONT, WIDTH, TOP_BAR_HEIGHT, HEIGHT, TARGET_EVENT, TARGET_PADDING, LIVES, TARGET_INCREMENT

def format_time(secs):
    minutes = int(secs // 60)
    seconds = int(secs % 60)
    milliseconds = int((secs - minutes * 60 - seconds) * 100)
    return f"{minutes:02}:{seconds:02}.{milliseconds:02}"


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
        self.target_color = target_color
        self.target_type = target_type
        self.target_size = target_size
        global BG_COLOR
        BG_COLOR = bg_color

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
                        self.running = False
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

