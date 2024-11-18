import pygame
import random
class Spin:
    def __init__(self, Balance, Lines, Bet):
        self.screen = pygame.display.set_mode((800, 700))
        pygame.mixer.init()
        self.Balance = Balance
        self.Lines = Lines
        self.Bet = Bet
        self.amount = 0

        self.idxM = 0

        self.message = ["Welcome, Press handle to Play",
                        f"You Lose {Bet} coins, Balance from {Balance + Bet} to Balance {Balance}",
                        f"You Win {self.amount} coins on {Lines} lines"]

        self.selected_rows = []

        self.ROWS = 3
        self.COLS = 3

        self.lemon = pygame.image.load("objects/lemon.png").convert_alpha() # lowest value
        self.red_apple = pygame.image.load("objects/redApple.png").convert_alpha() # second-highest value
        self.green_apple = pygame.image.load("objects/greenApple.png").convert_alpha() # highest value
        self.peach = pygame.image.load("objects/peach.png").convert_alpha() # second lowest value

        self.spinning = False

        self.slotLine = {
            self.red_apple: 4,
            self.green_apple: 3,
            self.peach: 6,
            self.lemon: 8
        }

        self.multipliers = {self.lemon: 2,
                            self.peach: 3,
                            self.red_apple: 4,
                            self.green_apple: 5}

    def update_condition(self):
        bet = self.Bet
        balance = self.Balance
        amount = self.amount
        lines = self.Lines

        self.message = ["Welcome, Press handle to Play",
                        f"You Lose {bet * lines} coins, Balance from {balance + bet * lines} to Balance {balance}",
                        f"You Win {amount} coins on {lines} lines"]

    def slot_spin(self):
        slot_items = []
        for item, count in self.slotLine.items():
            slot_items.extend([item] * count)
        self.selected_rows = [
            [(random.choice(slot_items)) for _ in range(self.COLS)],
            [(random.choice(slot_items)) for _ in range(self.COLS)],
            [(random.choice(slot_items)) for _ in range(self.COLS)]
        ]
        return self.selected_rows

    def check_winnings(self):
        winnings = 0
        condition = False
        for idx, row in enumerate(self.slot_spin()):

            if row[0] == row[1] == row[2]:
                winnings += self.multipliers.get(row[0])

                condition = True

                if self.Lines == 1 and idx == 0:
                    break
                elif self.Lines == 2 and idx == 1:
                    break

            if winnings == 4.5 or winnings == 6 or winnings == 9 or winnings == 15:
                pygame.mixer.Sound("sounds/jackpot3X.mp3").play()

        if condition:
            pygame.mixer.Sound("sounds/slotWin.mp3").play()
            self.idxM = 2
            self.amount = self.Bet * winnings
            self.Balance += self.amount
            self.update_condition()
        else:
            pygame.mixer.Sound("sounds/slotLose.mp3").play()
            self.idxM = 1
            self.Balance -= self.Bet * self.Lines
            self.update_condition()
            return self.Balance

        return self.Balance

    def start(self):
        return self.check_winnings(), self.selected_rows
