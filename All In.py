import pygame

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("sounds/bgm.mp3")
        pygame.mixer.music.play(-1)
        pygame.display.set_caption("All In")
        icon = pygame.image.load("objects/icon.png")
        pygame.display.set_icon(icon)
        self.bgColor = (246, 223, 207)
        # money amount
        self.balance = 0
        # input boxes in information
        self.active_color = (22, 190, 128)
        self.inactive_color = (201, 186, 167)
        self.width, self.height = 800, 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True
        self.clock = pygame.time.Clock()

    def main_screen(self):
        self.screen.fill(self.bgColor)
        # title Font and Text
        titleFont = pygame.font.Font("fonts/Quinquefive-ALoRM.ttf", 38)
        titleText = titleFont.render('"ALL IN"', True, (0, 0, 0))
        titleText_rect = titleText.get_rect(center=(self.width // 2, self.height // 2 - 250))

        # subTitle Font and Text
        subTitleFont = pygame.font.Font("fonts/GamestationCond.otf", 42)
        subTitleText = subTitleFont.render("HIGH RISK, HIGH REWARD", True, (0, 0, 0))
        subTitleText_rect = subTitleText.get_rect(center=(self.width // 2, self.height // 2 - 170))

        # game icon and start button
        gameIcon = pygame.transform.scale(pygame.image.load("objects/icon.png"), (90, 140)).convert_alpha()
        startButton = pygame.transform.scale(pygame.image.load("objects/buttonStart.png"), (275, 100)).convert_alpha()
        startButtonHitBox = startButton.get_rect(center=(self.width // 2, self.height // 2 + 150))

        # How to play
        howToPlay = pygame.transform.scale(pygame.image.load("objects/howtoplay.png"), (27, 40)).convert_alpha()
        howToPlayHitBox = howToPlay.get_rect(topleft=(750, 20))

        # creator font and text
        creatorFont = pygame.font.Font("fonts/Quinquefive-ALoRM.ttf", 16)
        creatorText = creatorFont.render("Created by: Earl Ordovez", True, (0, 0, 0))
        creatorText_rect = creatorText.get_rect(center=(self.width // 2, self.height - 30))

        # drawing object and fonts
        self.screen.blit(howToPlay, (750, 20))
        self.screen.blit(subTitleText, subTitleText_rect)
        self.screen.blit(titleText, titleText_rect)
        self.screen.blit(gameIcon, (self.width // 2 - 50, self.height // 2 - 100))
        self.screen.blit(startButton, startButtonHitBox)
        self.screen.blit(creatorText, creatorText_rect)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEMOTION:
                    if startButtonHitBox.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif howToPlayHitBox.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if startButtonHitBox.collidepoint(event.pos):
                        pygame.mixer.Sound("sounds/buttonClick.mp3").play()
                        self.information()
                        return
                    elif howToPlayHitBox.collidepoint(event.pos):
                        pygame.mixer.Sound("sounds/buttonClick.mp3").play()
                        self.how_to_play()
                        return

    def how_to_play(self):
        self.screen.fill((0, 0, 0))
        # close button
        closeButton = pygame.transform.scale(pygame.image.load("objects/close.png"), (44, 44)).convert_alpha()
        closeButtonHitBox = closeButton.get_rect(topleft=(30, 30))

        # how play text
        howToPlayFont = pygame.font.Font("fonts/Quinquefive-ALoRM.ttf", 36)
        howToPlayText = howToPlayFont.render("HOW TO PLAY", True, (255, 255, 255))
        howToPlayText_rect = howToPlayText.get_rect(center=(self.width // 2, self.height // 2 - 250))

        # Money object
        dollarIcon = pygame.transform.scale(pygame.image.load("objects/dollar.png"), (160, 101)).convert_alpha()
        dollarIcon_rect = dollarIcon.get_rect(center=(self.width // 2, self.height // 2 - 100))

        # Arrow down object
        arrowDown = pygame.transform.scale(pygame.image.load("objects/arrowToEqual.png"), (71, 120)).convert_alpha()
        arrowDown_rect = arrowDown.get_rect(center=(self.width // 2, self.height // 2 + 40))

        # money chest object
        moneyChest = pygame.transform.scale(pygame.image.load("objects/chestMoney.png"), (160, 130)).convert_alpha()
        moneyChest_rect = moneyChest.get_rect(center=(self.width // 2, self.height // 2 + 200))

        # drawing object and fonts
        self.screen.blit(closeButton, (30, 30))
        self.screen.blit(howToPlayText, howToPlayText_rect)
        self.screen.blit(dollarIcon, dollarIcon_rect)
        self.screen.blit(arrowDown, arrowDown_rect)
        self.screen.blit(moneyChest, moneyChest_rect)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEMOTION:
                    if closeButtonHitBox.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if closeButtonHitBox.collidepoint(event.pos):
                        pygame.mixer.Sound("sounds/buttonClick.mp3").play()
                        self.run()

            pygame.display.update()

    def information(self):
        # title Font and Text
        titleFont = pygame.font.Font("fonts/Quinquefive-ALoRM.ttf", 24)
        titleText = titleFont.render("ENTER YOUR INFORMATION", True, (0, 0, 0))
        titleText_rect = titleText.get_rect(center=(self.width // 2, self.height // 2 - 250))

        # Credit Card Number
        Font = pygame.font.Font("fonts/GamestationCond.otf", 32)
        creditCardText = Font.render("Credit Card Number", True, (0, 0, 0))
        creditCardText_rect = creditCardText.get_rect(center=(self.width // 2 - 220, self.height // 2 - 100))
        creditCardInput = pygame.Rect(73, 280, self.width // 2 + 245, 50)

        # Amount
        amountText = Font.render("Amount", True, (0, 0, 0))
        amountText_rect = amountText.get_rect(center=(self.width // 2 - 277, self.height // 2 + 50))
        amountInput = pygame.Rect(73, 430, self.width // 2 + 245, 50)

        # submit button
        submitButton = pygame.transform.scale(pygame.image.load("objects/buttonSubmit.png"), (275, 100)).convert_alpha()
        submitButtonHitBox = submitButton.get_rect(center=(self.width // 2, self.height // 2 + 250))

        # for input boxes
        color1 = self.inactive_color
        color2 = self.inactive_color
        active1 = False
        active2 = False
        text1 = ""
        text2 = ""

        while True:
            self.screen.fill((246, 223, 207))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.MOUSEMOTION:
                    if submitButtonHitBox.collidepoint(event.pos) or creditCardInput.collidepoint(event.pos) or amountInput.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if submitButtonHitBox.collidepoint(event.pos) and text1 != "" and text2 != "":
                        pygame.mixer.Sound("sounds/transition.mp3").play()
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("sounds/bgm2.mp3")
                        pygame.time.delay(2000)
                        pygame.mixer.music.play(-1)
                        self.balance = int(text2)
                        return

                    elif creditCardInput.collidepoint(event.pos):
                        active1 = True
                        active2 = False
                    elif amountInput.collidepoint(event.pos):
                        active1 = False
                        active2 = True
                    else:
                        active1 = False
                        active2 = False

                    color1 = self.active_color if active1 else self.inactive_color
                    color2 = self.active_color if active2 else self.inactive_color

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if text1 != "" and text2 != "":
                            pygame.mixer.Sound("sounds/transition.mp3").play()
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("sounds/bgm2.mp3")
                            pygame.time.delay(2000)
                            pygame.mixer.music.play(-1)
                            self.balance = int(text2)
                            return
                    elif active1:
                        if event.key == pygame.K_BACKSPACE:
                            text1 = text1[:-1]
                        else:
                            text1 += event.unicode
                    elif active2:
                        if event.key == pygame.K_BACKSPACE:
                            text2 = text2[:-1]
                        elif event.unicode.isdigit():
                            text2 += event.unicode


            self.screen.fill(self.bgColor)
            # rendering the text in the input box
            txt_surface1 = Font.render(text1, True, (0, 0, 0))
            txt_surface2 = Font.render(text2, True, (0, 0, 0))
            self.screen.blit(titleText, titleText_rect)
            self.screen.blit(creditCardText, creditCardText_rect)
            self.screen.blit(amountText, amountText_rect)
            self.screen.blit(submitButton, submitButtonHitBox)
            pygame.draw.rect(self.screen, color2, amountInput, 4)
            pygame.draw.rect(self.screen, color1, creditCardInput, 4)
            self.screen.blit(txt_surface1, (creditCardInput.x + 5, creditCardInput.y + 5))
            self.screen.blit(txt_surface2, (amountInput.x + 5, amountInput.y + 5))
            pygame.display.update()

    def show_balance(self):
        balanceFont = pygame.font.Font("fonts/Quinquefive-ALoRM.ttf", 24)
        balanceText = balanceFont.render(f"{self.balance}", True, (0, 0, 0))
        self.screen.blit(balanceText, (100, 35))

    def pause(self):
        cursor_over_button = False

        titleFont = pygame.font.Font("fonts/Quinquefive-ALoRM.ttf", 32)
        titleText = titleFont.render("Paused", True, (0, 0, 0))
        titleText_rect = titleText.get_rect(center=(self.width // 2, self.height // 2 - 250))
        subFont = pygame.font.Font("fonts/GamestationCond.otf", 32)
        subText = subFont.render("ARE YOU WINNING SON?", True, (0, 0, 0))
        subText_rect = subText.get_rect(center=(self.width // 2, self.height // 2 - 180))

        # options
        font = pygame.font.Font("fonts/GamestationCond.otf", 32)
        resumeText = font.render("Resume Your Wealth", True, (0, 0, 0))
        resumeTextHitBox = resumeText.get_rect(center=(self.width // 2, self.height // 2 - 50))
        restartText = font.render("Restart Your Pathetic Life", True, (0, 0, 0))
        restartTextHitBox = restartText.get_rect(center=(self.width // 2, self.height // 2 + 20))
        quitText = font.render("You Gay Why You Quittin'", True, (0, 0, 0))
        quitTextHitBox = quitText.get_rect(center=(self.width // 2, self.height // 2 + 90))

        creatorFont = pygame.font.Font("fonts/Quinquefive-ALoRM.ttf", 16)
        creatorText = creatorFont.render("Created by: Earl Ordovez", True, (0, 0, 0))
        creatorText_rect = creatorText.get_rect(center=(self.width // 2, self.height - 30))

        arrow_offset = 50
        arrow_color = (0, 0, 0)
        arrow_size = 10

        paused = True
        while paused:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEMOTION:
                    if resumeTextHitBox.collidepoint(event.pos) or restartTextHitBox.collidepoint(
                            event.pos) or quitTextHitBox.collidepoint(event.pos):
                        if not cursor_over_button:
                            pygame.mixer.Sound("sounds/buttonHover.mp3").play()
                            cursor_over_button = True
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        cursor_over_button = False
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if resumeTextHitBox.collidepoint(event.pos) or restartTextHitBox.collidepoint(
                        event.pos) or quitTextHitBox.collidepoint(event.pos):
                        pygame.mixer.Sound("sounds/buttonClick.mp3").play()

                    if resumeTextHitBox.collidepoint(event.pos):
                        paused = False
                    elif restartTextHitBox.collidepoint(event.pos):
                        pygame.mixer.music.stop()
                        pygame.time.delay(2000)
                        pygame.mixer.music.load("sounds/bgm.mp3")
                        pygame.mixer.music.play(-1)
                        self.restart()
                    elif quitTextHitBox.collidepoint(event.pos):
                        pygame.quit()
                        exit()

            self.screen.fill(self.bgColor)
            self.screen.blit(titleText, titleText_rect)
            self.screen.blit(subText, subText_rect)
            self.screen.blit(resumeText, resumeTextHitBox)
            self.screen.blit(restartText, restartTextHitBox)
            self.screen.blit(quitText, quitTextHitBox)
            self.screen.blit(creatorText, creatorText_rect)

            if resumeTextHitBox.collidepoint(mouse_pos):
                pygame.draw.polygon(self.screen, arrow_color, [
                    (resumeTextHitBox.left - arrow_offset + arrow_size, resumeTextHitBox.centery),
                    (resumeTextHitBox.left - arrow_offset, resumeTextHitBox.centery - arrow_size),
                    (resumeTextHitBox.left - arrow_offset, resumeTextHitBox.centery + arrow_size)
                ])
            elif restartTextHitBox.collidepoint(mouse_pos):
                pygame.draw.polygon(self.screen, arrow_color, [
                    (restartTextHitBox.left - arrow_offset + arrow_size, restartTextHitBox.centery),
                    (restartTextHitBox.left - arrow_offset, restartTextHitBox.centery - arrow_size),
                    (restartTextHitBox.left - arrow_offset, restartTextHitBox.centery + arrow_size)
                ])
            elif quitTextHitBox.collidepoint(mouse_pos):
                pygame.draw.polygon(self.screen, arrow_color, [
                    (quitTextHitBox.left - arrow_offset + arrow_size, quitTextHitBox.centery),
                    (quitTextHitBox.left - arrow_offset, quitTextHitBox.centery - arrow_size),
                    (quitTextHitBox.left - arrow_offset, quitTextHitBox.centery + arrow_size)
                ])

            pygame.display.update()

    def restart(self):
        self.balance = 0
        self.run()

    def run(self): # Game loop
        self.main_screen()
        self.screen.fill(self.bgColor)

        coins = pygame.transform.scale(pygame.image.load("objects/coins.png"), (50, 47)).convert_alpha()
        coins_rect = coins.get_rect(center=(50, 50))

        pauseButton = pygame.transform.scale(pygame.image.load("objects/pauseButton.png"), (50, 50)).convert_alpha()
        pauseButtonHitbox = pauseButton.get_rect(topleft=(720, 20))

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEMOTION:
                    if pauseButtonHitbox.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pauseButtonHitbox.collidepoint(event.pos):
                        pygame.mixer.Sound("sounds/buttonClick.mp3").play()
                        self.pause()

            self.screen.blit(coins, coins_rect)
            self.screen.blit(pauseButton, (720, 20))
            self.show_balance()
            self.clock.tick(120)
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()