import random
import pygame
class Slot:
    def __init__(self, x_position, y_position):
        self.screen = pygame.display.set_mode((800, 700))
        self.lemon = pygame.image.load("objects/lemon.png").convert_alpha()
        self.red_apple = pygame.image.load("objects/redApple.png").convert_alpha()
        self.green_apple = pygame.image.load("objects/greenApple.png").convert_alpha()
        self.peach = pygame.image.load("objects/peach.png").convert_alpha()

        self.image_width = self.red_apple.get_width()
        self.image_height = self.red_apple.get_height()

        self.spinning = False
        self.counter = 0

        # Displaying random image for slot spinning
        self.index = [self.lemon, self.red_apple, self.green_apple, self.peach]

        self.x = x_position
        self.y = y_position
        self.y_change = 40
        self.current_image = random.choice(self.index)

    def update_position1(self):
        if self.spinning:
            self.y -= self.y_change
            if self.y <= 55:
                self.current_image = random.choice(self.index)
                self.y = 200
                self.counter += 1
            elif self.counter == 25:
                self.y_change = 20
            elif self.counter == 38:
                self.y = (700 // 2 - 117) - (self.image_height // 2)
                self.y_change = 0
                self.counter = 0
                self.spinning = False

    def update_position2(self):
        if self.spinning:
            self.y -= self.y_change
            if self.y <= 250:
                self.current_image = random.choice(self.index)
                self.y = 400
                self.counter += 1
            elif self.counter == 25:
                self.y_change = 20
            elif self.counter == 38:
                self.y = (700 // 2 - 117) - (self.image_height // 2) + (3 // 3) * 117
                self.y_change = 0
                self.counter = 0
                self.spinning = False

    def update_position3(self):
        if self.spinning:
            self.y -= self.y_change
            if self.y <= 350:
                self.current_image = random.choice(self.index)
                self.y = 500
                self.counter += 1
            elif self.counter == 25:
                self.y_change = 20
            elif self.counter == 38:
                self.y = (700 // 2 - 117) - (self.image_height // 2) + (6 // 3) * 117
                self.y_change = 0
                self.counter = 0
                self.spinning = False


    def draw(self, screen, slot):
        original_clip = screen.get_clip()
        screen.set_clip(slot)
        screen.blit(self.current_image, (self.x, self.y))
        screen.set_clip(original_clip)

    def update_draw(self, screen, selected_rows, slot, row, col): # for updating the images based on the selected row in spin.py
        self.current_image = selected_rows[row][col]
        self.draw(screen, slot)

    def default(self):
        self.y_change = 40

