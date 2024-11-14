import pygame
import random
class Spin:
    def __init__(self, Balance, Lines, Bet):
        self.screen = pygame.display.set_mode((800, 700))
        self.Balance = Balance
        self.Lines = Lines
        self.Bet = Bet

        self.selected_rows = []

        self.ROWS = 3
        self.COLS = 3

        self.winnings = 0
        self.lemon = pygame.image.load("objects/lemon.png").convert_alpha() # lowest value
        self.red_apple = pygame.image.load("objects/redApple.png").convert_alpha() # second-highest value
        self.green_apple = pygame.image.load("objects/greenApple.png").convert_alpha() # highest value
        self.peach = pygame.image.load("objects/peach.png").convert_alpha() # second lowest value

        self.spinning = False

        self.a_line = [self.red_apple,
                  self.green_apple,
                  self.green_apple,
                  self.red_apple,
                  self.red_apple,
                  self.peach,
                  self.peach,
                  self.peach,
                  self.peach]

        self.b_line = [self.red_apple,
                  self.green_apple,
                  self.green_apple,
                  self.red_apple,
                  self.red_apple,
                  self.peach,
                  self.peach,
                  self.peach,
                  self.peach]

        self.c_line = [self.red_apple,
                  self.green_apple,
                  self.green_apple,
                  self.red_apple,
                  self.red_apple,
                  self.peach,
                  self.peach,
                  self.peach,
                  self.peach]

        self.multipliers = {self.lemon: 1.5,
                            self.peach: 2,
                            self.red_apple: 3,
                            self.green_apple: 5}

    def slot_spin(self):
        self.selected_rows = [
            [(random.choice(self.a_line)) for _ in range(self.COLS)],
            [(random.choice(self.b_line)) for _ in range(self.COLS)],
            [(random.choice(self.c_line)) for _ in range(self.COLS)]
        ]

        return self.selected_rows

    def check_winnings(self):
        condition = False
        for row in self.slot_spin():
            if row[0] == row[1] == row[2]:
                if self.Lines == 1:
                    self.winnings += self.multipliers.get(row[0])
                    condition = True
                    break
                elif self.Lines == 2:
                    self.winnings += self.multipliers.get(row[0])
                    if row == 1:
                        break
                else:
                    self.winnings += self.multipliers.get(row[0])

                condition = True

        if condition:
            amount = self.Bet * self.winnings
            self.Balance += amount
        else:
            self.Balance -= self.Bet
            return self.Balance

        return self.Balance

    def start(self):
        return self.check_winnings()
