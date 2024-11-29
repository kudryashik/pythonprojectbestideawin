import pygame
from src.constants import WIDTH, HEIGHT, COLORS, BACKGROUND_COLORS, LABEL_FONT

from src.GameClass import Game


# Инициализация Pygame
pygame.init()


def main_menu():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Aim Trainer - Choose Options")
    clock = pygame.time.Clock()

    target_color_keys = list(COLORS.keys())
    current_color_index = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_color_index = (current_color_index - 1) % len(target_color_keys)
                if event.key == pygame.K_DOWN:
                    current_color_index = (current_color_index + 1) % len(target_color_keys)
                if event.key == pygame.K_RETURN:
                    selected_color = COLORS[target_color_keys[current_color_index]]
                    return selected_color, "circle", 20, BACKGROUND_COLORS["Light Gray"]

        win.fill((255, 255, 255))
        y_offset = 100
        win.blit(LABEL_FONT.render("Select Target Color:", True, (0, 0, 0)), (WIDTH // 2 - 100, y_offset))

        for i, color_name in enumerate(target_color_keys):
            color_value = COLORS[color_name]
            pygame.draw.rect(win, color_value, (WIDTH // 2 - 50, y_offset + i * 30 + 30, 100, 20))
            if i == current_color_index:
                pygame.draw.rect(win, (0, 0, 0), (WIDTH // 2 - 50, y_offset + i * 30 + 30, 100, 20), 3)

        y_offset += len(target_color_keys) * 30 + 50
        start_game_text = LABEL_FONT.render("Start Game (Press Enter)", True, (0, 0, 0))
        win.blit(start_game_text, (WIDTH // 2 - start_game_text.get_width() // 2, y_offset))
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    chosen_color, chosen_type, chosen_size, chosen_bg_color = main_menu()
    game = Game(chosen_color, chosen_type, chosen_size, chosen_bg_color)
    game.run_game()
