import os
import pygame

class Handle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        handle1 = pygame.transform.scale(pygame.image.load(os.path.join("sprite", "handle1.png")), (135.3, 115.5))
        handle2 = pygame.transform.scale(pygame.image.load(os.path.join("sprite", "handle2.png")), (135.3, 115.5))
        self.images = [handle1, handle2]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(800 // 2 + 318, 700 //2))
        self.animating = False
        self.delay_counter = 0
        self.delay_duration = 400  # Number of frames to hold on handle2

    def update(self):
        # If animating, switch to handle2 then back to handle1 with delay
        if self.animating:
            if self.index == 0:  # Switch to handle2
                self.index = 1
                self.image = self.images[self.index]
                self.delay_counter = 0  # Reset delay counter

            elif self.index == 1:  # Hold on handle2 for delay duration
                self.delay_counter += 1
                if self.delay_counter >= self.delay_duration:
                    # Switch back to handle1 after the delay
                    self.index = 0
                    self.image = self.images[self.index]
                    self.animating = False

    def handle_click(self, pos):
        # Start animation if handle is clicked
        if self.rect.collidepoint(pos):
            self.animating = True