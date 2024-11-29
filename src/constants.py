import pygame

# Константы
WIDTH, HEIGHT = 800, 600
TARGET_INCREMENT = 1000  # миллисекунд
TARGET_PADDING = 50
TOP_BAR_HEIGHT = 50
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

# Шрифт для надписей
LABEL_FONT = pygame.font.SysFont('Arial', 24)
