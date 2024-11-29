import pygame

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
            pygame.draw.line(win, self.color, (self.x - self.size // 2, self.y), (self.x + self.size // 2, self.y), 5)
            pygame.draw.line(win, self.color, (self.x, self.y - self.size // 2), (self.x, self.y + self.size // 2), 5)
        elif self.target_type == "triangle":
            points = [
                (self.x, self.y - self.size // 2),
                (self.x - self.size // 2, self.y + self.size // 2),
                (self.x + self.size // 2, self.y + self.size // 2)
            ]
            pygame.draw.polygon(win, self.color, points)

    def collide(self, x, y):
        return (x - self.x) ** 2 + (y - self.y) ** 2 < self.size ** 2
