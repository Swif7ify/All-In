import pygame
import os
import sys
from handle import Handle
from spin import Spin
from slots import Slot
from data import Data

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("sounds/bgm.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)
        pygame.display.set_caption("All In")
        icon = pygame.image.load("objects/icon.png")
        pygame.display.set_icon(icon)
        self.titleFont = pygame.font.Font("fonts/Quinquefive-ALoRM.ttf", 32)
        self.font = pygame.font.Font("fonts/GamestationCond.otf", 32)
        self.bgColor = (246, 223, 207)
        # Handle
        self.handle_sprite = Handle()
        self.all_sprites = pygame.sprite.Group(self.handle_sprite)
        # money amount
        self.balance = 0
        # lines to bet
        self.amountLines = 0
        # amount to bet
        self.amountBet = 0
        self.protect = ""
        # spin logic
        self.spin = Spin(self.balance, self.amountLines, self.amountBet)
        self.selected_rows = []
        self.idxM = 0
        # slot image
        self.slot = [Slot(195 + (i % 3) * 160, (700 // 2 - 117) - (96 // 2) + (i // 3) * 117) for i in range(9)]
        self.first_slot = self.slot[0]
        # input boxes in information
        self.active_color = (22, 190, 128)
        self.inactive_color = (201, 186, 167)
        self.width, self.height = 800, 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.data = Data(self.balance, self.amountLines, self.amountBet, self.protect)
        self.running = True
        self.delay_active = False
        self.delay_start_time = 0
        self.delay_duration = 3100
        self.clock = pygame.time.Clock()

    def main_screen(self):
        cursor_over_button = False
        resumeActive = False
        folder = 'gameData'
        file_path = os.path.join(folder, 'game_state')
        if os.path.exists(file_path + '.dat'):
            resumeActive = True

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

        startText = self.font.render("New Game", True, (0, 0, 0))
        startHitBox = startText.get_rect(center=(self.width // 2, self.height // 2 + 90))

        resumeColor = (0, 0, 0) if resumeActive else (154, 152, 152)
        resumeText = self.font.render("Resume", True, resumeColor)
        resumeHitBox = resumeText.get_rect(center=(self.width // 2, self.height // 2 + 210))

        deleteColor = (255, 0, 0) if resumeActive else (154, 152, 152)
        deleteText = self.font.render("Delete Game Save", True, deleteColor)
        deleteHitBox = deleteText.get_rect(center=(self.width // 2, self.height // 2 + 150))

        quitText = self.font.render("Quit", True, (0, 0, 0))
        quitHitBox = quitText.get_rect(center=(self.width // 2, self.height // 2 + 270))

        # How to play
        howToPlay = pygame.transform.scale(pygame.image.load("objects/howtoplay.png"), (27, 40)).convert_alpha()
        howToPlayHitBox = howToPlay.get_rect(topleft=(750, 20))

        # creator font and text
        creatorFont = pygame.font.Font("fonts/Quinquefive-ALoRM.ttf", 16)
        creatorText = creatorFont.render("Created by: Earl Ordovez", True, (0, 0, 0))
        creatorText_rect = creatorText.get_rect(center=(self.width // 2, self.height - 30))

        arrow_offset = 50
        arrow_color = (0, 0, 0)
        arrow_size = 10

        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    if startHitBox.collidepoint(event.pos) or quitHitBox.collidepoint(event.pos) or resumeActive and resumeHitBox.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        if not cursor_over_button:
                            pygame.mixer.Sound("sounds/buttonHover.mp3").play()
                            cursor_over_button = True
                    elif howToPlayHitBox.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif deleteHitBox.collidepoint(event.pos) and resumeActive:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        if not cursor_over_button:
                            pygame.mixer.Sound("sounds/warning.mp3").play()
                            cursor_over_button = True
                    else:
                        cursor_over_button = False
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if startHitBox.collidepoint(event.pos):
                        pygame.mixer.Sound("sounds/buttonClick.mp3").play()
                        self.information()
                        return
                    elif deleteHitBox.collidepoint(event.pos) and resumeActive:
                        self.confirm_delete()
                        return
                    elif howToPlayHitBox.collidepoint(event.pos):
                        pygame.mixer.Sound("sounds/buttonClick.mp3").play()
                        self.how_to_play()
                        return
                    elif resumeHitBox.collidepoint(event.pos):
                        if resumeActive:
                            self.data.load_game()
                            pygame.mixer.Sound("sounds/transition.mp3").play()
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("sounds/bgm2.mp3")
                            self.balance = self.data.Balance
                            self.amountLines = self.data.amountLines
                            self.amountBet = self.data.amountBet
                            self.protect = self.data.protect
                            pygame.time.delay(2000)
                            pygame.mixer.music.play(-1)
                            return
                    elif quitHitBox.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            # drawing object and fonts
            self.screen.fill(self.bgColor)
            self.screen.blit(howToPlay, (750, 20))
            self.screen.blit(subTitleText, subTitleText_rect)
            self.screen.blit(titleText, titleText_rect)
            self.screen.blit(gameIcon, (self.width // 2 - 50, self.height // 2 - 100))
            self.screen.blit(startText, startHitBox)
            self.screen.blit(resumeText, resumeHitBox)
            self.screen.blit(deleteText, deleteHitBox)
            self.screen.blit(quitText, quitHitBox)
            self.screen.blit(creatorText, creatorText_rect)

            if startHitBox.collidepoint(mouse_pos):
                pygame.draw.polygon(self.screen, arrow_color, [
                    (startHitBox.left - arrow_offset + arrow_size, startHitBox.centery),
                    (startHitBox.left - arrow_offset, startHitBox.centery - arrow_size),
                    (startHitBox.left - arrow_offset, startHitBox.centery + arrow_size)
                ])
            elif resumeHitBox.collidepoint(mouse_pos) and resumeActive:
                pygame.draw.polygon(self.screen, arrow_color, [
                    (resumeHitBox.left - arrow_offset + arrow_size, resumeHitBox.centery),
                    (resumeHitBox.left - arrow_offset, resumeHitBox.centery - arrow_size),
                    (resumeHitBox.left - arrow_offset, resumeHitBox.centery + arrow_size)
                ])
            elif deleteHitBox.collidepoint(mouse_pos) and resumeActive:
                pygame.draw.polygon(self.screen, arrow_color, [
                    (deleteHitBox.left - arrow_offset + arrow_size, deleteHitBox.centery),
                    (deleteHitBox.left - arrow_offset, deleteHitBox.centery - arrow_size),
                    (deleteHitBox.left - arrow_offset, deleteHitBox.centery + arrow_size)
                ])
            elif quitHitBox.collidepoint(mouse_pos):
                pygame.draw.polygon(self.screen, arrow_color, [
                    (quitHitBox.left - arrow_offset + arrow_size, quitHitBox.centery),
                    (quitHitBox.left - arrow_offset, quitHitBox.centery - arrow_size),
                    (quitHitBox.left - arrow_offset, quitHitBox.centery + arrow_size)
                ])

            pygame.display.update()

    def confirm_delete(self):
        self.screen.fill((0, 0, 0))
        # close button
        closeButton = pygame.transform.scale(pygame.image.load("objects/close.png"), (44, 44)).convert_alpha()
        closeButtonHitBox = closeButton.get_rect(topleft=(30, 30))

        # delete button
        deleteButton = pygame.transform.scale(pygame.image.load("objects/redButton.png"), (185, 185)).convert_alpha()
        deleteButtonHitBox = deleteButton.get_rect(center=(self.width // 2, self.height // 2 + 100))

        # delete text
        deleteFont = pygame.font.Font("fonts/Quinquefive-ALoRM.ttf", 36)
        deleteText = deleteFont.render("ARE YOU SURE?", True, (255, 255, 255))
        deleteText_rect = deleteText.get_rect(center=(self.width // 2, self.height // 2 - 100))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    if closeButtonHitBox.collidepoint(event.pos) or deleteButtonHitBox.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if closeButtonHitBox.collidepoint(event.pos):
                        pygame.mixer.Sound("sounds/buttonClick.mp3").play()
                        self.main_screen()
                        return
                    elif deleteButtonHitBox.collidepoint(event.pos):
                        pygame.mixer.Sound("sounds/delete.mp3").play()
                        self.data.delete_game()
                        self.main_screen()
                        return

            self.screen.fill((0, 0, 0))
            self.screen.blit(closeButton, (30, 30))
            self.screen.blit(deleteButton, deleteButtonHitBox)
            self.screen.blit(deleteText, deleteText_rect)
            pygame.display.update()

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
                    sys.exit()

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

        # amount > 500
        amountWarning = Font.render("Amount must be greater than 500", True, (255, 0, 0))
        amountWarning_rect = amountWarning.get_rect(center=(self.width // 2, self.height // 2 + 50))

        # back button
        backButton = pygame.transform.scale(pygame.image.load("objects/playButton.png"), (50, 50)).convert_alpha()
        backButtonHitBox = backButton.get_rect(topleft=(720, 20))

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
            amount = int(text2) if text2 != "" else 0
            self.screen.fill((246, 223, 207))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEMOTION:
                    if submitButtonHitBox.collidepoint(event.pos) or creditCardInput.collidepoint(event.pos) or amountInput.collidepoint(event.pos) or backButtonHitBox.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if submitButtonHitBox.collidepoint(event.pos) and text1 != "" and text2 != "" and amount >= 500:
                        pygame.mixer.Sound("sounds/transition.mp3").play()
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("sounds/bgm2.mp3")
                        pygame.time.delay(2000)
                        pygame.mixer.music.play(-1)
                        self.protect = text1
                        self.balance = int(text2)
                        return
                    elif backButtonHitBox.collidepoint(event.pos):
                        pygame.mixer.Sound("sounds/buttonClick.mp3").play()
                        self.run()
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
                    pygame.mixer.Sound("sounds/keySound.mp3").play()
                    if event.key == pygame.K_RETURN:
                        if text1 != "" and text2 != "":
                            pygame.mixer.Sound("sounds/transition.mp3").play()
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("sounds/bgm2.mp3")
                            pygame.time.delay(2000)
                            pygame.mixer.music.play(-1)
                            self.protect = text1
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
            if submitButtonHitBox.collidepoint(pygame.mouse.get_pos()) and amount < 500:
                self.screen.blit(amountWarning, amountWarning_rect)
            self.screen.blit(backButton, backButtonHitBox)
            self.screen.blit(submitButton, submitButtonHitBox)
            pygame.draw.rect(self.screen, color2, amountInput, 4)
            pygame.draw.rect(self.screen, color1, creditCardInput, 4)
            self.screen.blit(txt_surface1, (creditCardInput.x + 5, creditCardInput.y + 5))
            self.screen.blit(txt_surface2, (amountInput.x + 5, amountInput.y + 5))
            pygame.display.update()

    def show_balance(self):
        coins = pygame.transform.scale(pygame.image.load("objects/coins.png"), (50, 47)).convert_alpha()
        coins_rect = coins.get_rect(center=(50, 50))
        balanceFont = pygame.font.Font("fonts/Quinquefive-ALoRM.ttf", 24)
        balanceText = balanceFont.render(f"{self.balance:,}", True, (0, 0, 0))
        self.screen.blit(balanceText, (100, 35))
        self.screen.blit(coins, coins_rect)

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
        resumeTextHitBox = resumeText.get_rect(center=(self.width // 2, self.height // 2 - 70))
        restartText = font.render("Restart Your Pathetic Life", True, (0, 0, 0))
        restartTextHitBox = restartText.get_rect(center=(self.width // 2, self.height // 2))
        quitText = font.render("You Gay Why You Quittin'", True, (0, 0, 0))
        quitTextHitBox = quitText.get_rect(center=(self.width // 2, self.height // 2 + 70))
        multiplierText = font.render("Fruit Multiplier", True, (0, 0, 0))
        multiplierTextHitBox = multiplierText.get_rect(center=(self.width // 2, self.height // 2 + 140))

        saveText = font.render("Save Game", True, (0, 0, 0))
        saveTextHitBox = saveText.get_rect(center=(self.width // 2, self.height // 2 + 210))

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
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    if resumeTextHitBox.collidepoint(event.pos) or restartTextHitBox.collidepoint(
                            event.pos) or quitTextHitBox.collidepoint(event.pos) or multiplierTextHitBox.collidepoint(event.pos) or saveTextHitBox.collidepoint(event.pos):
                        if not cursor_over_button:
                            pygame.mixer.Sound("sounds/buttonHover.mp3").play()
                            cursor_over_button = True
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        cursor_over_button = False
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if resumeTextHitBox.collidepoint(event.pos) or restartTextHitBox.collidepoint(
                        event.pos) or quitTextHitBox.collidepoint(event.pos) or multiplierTextHitBox.collidepoint(event.pos) or saveTextHitBox.collidepoint(event.pos):
                        pygame.mixer.Sound("sounds/buttonClick.mp3").play()

                    if resumeTextHitBox.collidepoint(event.pos):
                        paused = False
                    elif restartTextHitBox.collidepoint(event.pos):
                        pygame.mixer.music.stop()
                        pygame.time.delay(2000)
                        pygame.mixer.music.load("sounds/bgm.mp3")
                        pygame.mixer.music.play(-1)
                        self.restart()
                        return
                    elif quitTextHitBox.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    elif multiplierTextHitBox.collidepoint(event.pos):
                        paused = False
                        self.fruit_multiplier()

                    elif saveTextHitBox.collidepoint(event.pos):
                        self.data.Balance = self.balance
                        self.data.amountLines = self.amountLines
                        self.data.amountBet = self.amountBet
                        self.data.protect = self.protect
                        self.data.save_game()
                        paused = False

            self.screen.fill(self.bgColor)
            self.screen.blit(titleText, titleText_rect)
            self.screen.blit(subText, subText_rect)
            self.screen.blit(resumeText, resumeTextHitBox)
            self.screen.blit(restartText, restartTextHitBox)
            self.screen.blit(quitText, quitTextHitBox)
            self.screen.blit(multiplierText, multiplierTextHitBox)
            self.screen.blit(saveText, saveTextHitBox)
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
            elif multiplierTextHitBox.collidepoint(mouse_pos):
                pygame.draw.polygon(self.screen, arrow_color, [
                    (multiplierTextHitBox.left - arrow_offset + arrow_size, multiplierTextHitBox.centery),
                    (multiplierTextHitBox.left - arrow_offset, multiplierTextHitBox.centery - arrow_size),
                    (multiplierTextHitBox.left - arrow_offset, multiplierTextHitBox.centery + arrow_size)
                ])
            elif saveTextHitBox.collidepoint(mouse_pos):
                pygame.draw.polygon(self.screen, arrow_color, [
                    (saveTextHitBox.left - arrow_offset + arrow_size, saveTextHitBox.centery),
                    (saveTextHitBox.left - arrow_offset, saveTextHitBox.centery - arrow_size),
                    (saveTextHitBox.left - arrow_offset, saveTextHitBox.centery + arrow_size)
                ])

            pygame.display.update()

    def fruit_multiplier(self):
        titleFont = pygame.font.Font("fonts/Quinquefive-ALoRM.ttf", 24)
        subTitleFont = pygame.font.Font("fonts/GamestationCond.otf", 32)
        titleText = titleFont.render("Fruit Multiplier", True, (0, 0, 0))
        titleText_rect = titleText.get_rect(center=(self.width // 2, self.height // 2 - 250))
        backButton = pygame.transform.scale(pygame.image.load("objects/playButton.png"), (50, 50)).convert_alpha()
        backButtonHitBox = backButton.get_rect(topleft=(720, 20))
        creatorFont = pygame.font.Font("fonts/Quinquefive-ALoRM.ttf", 16)
        creatorText = creatorFont.render("Created by: Earl Ordovez", True, (0, 0, 0))
        creatorText_rect = creatorText.get_rect(center=(self.width // 2, self.height - 30))

        # fruit images
        lemon = pygame.image.load("objects/lemon.png").convert_alpha()
        lemonText = subTitleFont.render("Lemon: 2x", True, (0, 0, 0))
        redApple = pygame.image.load("objects/redApple.png").convert_alpha()
        redAppleText = subTitleFont.render("Red Apple: 4x", True, (0, 0, 0))
        greenApple = pygame.image.load("objects/greenApple.png").convert_alpha()
        greenAppleText = subTitleFont.render("Green Apple: 5x", True, (0, 0, 0))
        peach = pygame.image.load("objects/peach.png").convert_alpha()
        peachText = subTitleFont.render("Peach: 3x", True, (0, 0, 0))

        paused = True
        while paused:
            self.screen.fill(self.bgColor)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEMOTION:
                    if backButtonHitBox.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if backButtonHitBox.collidepoint(event.pos):
                        pygame.mixer.Sound("sounds/buttonClick.mp3").play()
                        paused = False

            self.screen.blit(titleText, titleText_rect)
            self.screen.blit(backButton, backButtonHitBox)
            gap = 20  # Define the gap between images
            self.screen.blit(lemon, (self.width // 2 - 140, self.height // 2 - 200))
            self.screen.blit(redApple, (self.width // 2 - 140, self.height // 2 - 100 + gap))
            self.screen.blit(greenApple, (self.width // 2 - 140, self.height // 2 + gap * 2))
            self.screen.blit(peach, (self.width // 2 - 140, self.height // 2 + 100 + gap * 3))

            self.screen.blit(lemonText, (self.width // 2 - 30, self.height // 2 - 160))
            self.screen.blit(redAppleText, (self.width // 2 - 30, self.height // 2 - 60 + gap))
            self.screen.blit(greenAppleText, (self.width // 2 - 30, self.height // 2 + 40 + gap * 2))
            self.screen.blit(peachText, (self.width // 2 - 30, self.height // 2 + 140 + gap * 3))
            self.screen.blit(creatorText, creatorText_rect)
            pygame.display.update()

    def restart(self):
        self.balance = 0
        self.run()

    def game_over(self):
        titleFont = pygame.font.Font("fonts/Quinquefive-ALoRM.ttf", 32)
        titleText = titleFont.render("GAME OVER", True, (0, 0, 0))
        titleText_rect = titleText.get_rect(center=(self.width // 2, self.height // 2 - 150))

        restartText = self.font.render("Restart?", True, (0, 0, 0))
        restartText_rect = restartText.get_rect(center=(self.width // 2, self.height // 2 - 70))

        restartButton = pygame.transform.scale(pygame.image.load("objects/redButton.png"), (185, 185)).convert_alpha()
        restartButtonHitBox = restartButton.get_rect(center=(self.width // 2, self.height // 2 + 80))

        while True:
            self.screen.fill(self.bgColor)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEMOTION:
                    if restartButtonHitBox.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if restartButtonHitBox.collidepoint(event.pos):
                        folder = 'gameData'
                        file_path = os.path.join(folder, 'game_state')
                        if os.path.exists(file_path + '.dat'):
                            self.data.delete_game()
                        
                        pygame.mixer.Sound("sounds/transition.mp3").play()
                        pygame.mixer.music.stop()
                        pygame.time.delay(2000)
                        pygame.mixer.music.load("sounds/bgm.mp3")
                        pygame.mixer.music.play(-1)
                        self.restart()
                        return

            self.screen.blit(titleText, titleText_rect)
            self.screen.blit(restartText, restartText_rect)
            self.screen.blit(restartButton, restartButtonHitBox)
            pygame.display.update()

    def add_bet(self):
        titleFont = pygame.font.Font("fonts/Quinquefive-ALoRM.ttf", 32)
        font = pygame.font.Font("fonts/GamestationCond.otf", 32)
        titleText = titleFont.render("ADD BET", True, (0, 0, 0))
        titleText_rect = titleText.get_rect(center=(self.width // 2, self.height // 2 - 100))
        input_rect = pygame.Rect(73, 320, self.width // 2 + 245, 50)

        backButton = pygame.transform.scale(pygame.image.load("objects/playButton.png"), (50, 50)).convert_alpha()
        backButtonHitBox = backButton.get_rect(topleft=(720, 20))

        submitButton = pygame.transform.scale(pygame.image.load("objects/submitButton.png"), (191.36, 63.18)).convert_alpha()
        submitButtonHitBox = submitButton.get_rect(center=(self.width // 2, self.height // 2 + 80))

        color = self.inactive_color
        active = False
        text = ""

        while True:
            self.screen.fill(self.bgColor)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEMOTION:
                    if submitButtonHitBox.collidepoint(event.pos) or input_rect.collidepoint(event.pos) or backButtonHitBox.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if submitButtonHitBox.collidepoint(event.pos) and text != "":
                        pygame.mixer.Sound("sounds/transition.mp3").play()
                        self.amountBet = int(text)
                        return
                    if backButtonHitBox.collidepoint(event.pos):
                        pygame.mixer.Sound("sounds/buttonClick.mp3").play()
                        return
                    elif input_rect.collidepoint(event.pos):
                        active = True
                    else:
                        active = False

                    color = self.active_color if active else self.inactive_color

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if text != "":
                            pygame.mixer.Sound("sounds/transition.mp3").play()
                            self.amountBet = int(text)
                            return
                    elif active:
                        pygame.mixer.Sound("sounds/keySound.mp3").play()
                        if event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        elif event.unicode.isdigit():
                            text += event.unicode

            self.screen.blit(backButton, backButtonHitBox)
            self.screen.blit(titleText, titleText_rect)
            txt_surface = font.render(text, True, (0, 0, 0))
            pygame.draw.rect(self.screen, color, input_rect, 4)
            self.screen.blit(txt_surface, (input_rect.x + 5, input_rect.y + 5))
            self.screen.blit(submitButton, submitButtonHitBox)
            self.show_balance()
            pygame.display.update()

    def add_lines(self):
        titleText = self.titleFont.render("HOW MANY LINES", True, (0, 0, 0))
        titleText_rect = titleText.get_rect(center=(self.width // 2, self.height // 2 - 100))
        backButton = pygame.transform.scale(pygame.image.load("objects/playButton.png"), (50, 50)).convert_alpha()
        backButtonHitBox = backButton.get_rect(topleft=(720, 20))

        # line button
        oneLineButton = pygame.transform.scale(pygame.image.load("objects/oneButton.png"), (118, 130)).convert_alpha()
        oneLineButtonHitBox = oneLineButton.get_rect(center=(self.width // 2 - 154, self.height // 2 + 50))
        twoLineButton = pygame.transform.scale(pygame.image.load("objects/twoButton.png"), (118, 130)).convert_alpha()
        twoLineButtonHitBox = twoLineButton.get_rect(center=(self.width // 2, self.height // 2 + 50))
        threeLineButton = pygame.transform.scale(pygame.image.load("objects/threeButton.png"), (118, 130)).convert_alpha()
        threeLineButtonHitBox = threeLineButton.get_rect(center=(self.width // 2 + 154, self.height // 2 + 50))


        while True:
            self.screen.fill(self.bgColor)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEMOTION:
                    if oneLineButtonHitBox.collidepoint(event.pos) or twoLineButtonHitBox.collidepoint(event.pos) or threeLineButtonHitBox.collidepoint(event.pos) or backButtonHitBox.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if oneLineButtonHitBox.collidepoint(event.pos):
                        pygame.mixer.Sound("sounds/transition.mp3").play()
                        self.amountLines = 1
                        return
                    elif twoLineButtonHitBox.collidepoint(event.pos):
                        pygame.mixer.Sound("sounds/transition.mp3").play()
                        self.amountLines = 2
                        return
                    elif threeLineButtonHitBox.collidepoint(event.pos):
                        pygame.mixer.Sound("sounds/transition.mp3").play()
                        self.amountLines = 3
                        return
                    elif backButtonHitBox.collidepoint(event.pos):
                        pygame.mixer.Sound("sounds/buttonClick.mp3").play()
                        return

            self.screen.blit(titleText, titleText_rect)
            self.screen.blit(backButton, backButtonHitBox)
            self.screen.blit(oneLineButton, oneLineButtonHitBox)
            self.screen.blit(twoLineButton, twoLineButtonHitBox)
            self.screen.blit(threeLineButton, threeLineButtonHitBox)
            self.show_balance()
            pygame.display.update()

    def update_information(self):
        bettingInfo = pygame.font.Font("fonts/Quinquefive-ALoRM.ttf", 15)

        bettingText = bettingInfo.render(f"Betting {self.amountBet:,} on {self.amountLines} Lines", True, (0, 0, 0))
        bettingText_rect = bettingText.get_rect(center=(self.width // 2, self.height // 2 - 220))
        self.screen.blit(bettingText, bettingText_rect)
        pygame.display.update()

    def update_spin(self):
        self.spin.Balance = self.balance
        self.spin.Lines = self.amountLines
        self.spin.Bet = self.amountBet
        amount, self.selected_rows = self.spin.start()
        self.balance = amount
        for i, slot in enumerate(self.slot):
            row = i // 3
            col = i % 3
            slot.current_image = self.selected_rows[row][col]

    def take_spin(self):
        # Check if the delay is active and the delay duration has passed
        if self.delay_active:
            current_time = pygame.time.get_ticks()
            if current_time - self.delay_start_time >= self.delay_duration:
                self.update_spin()  # Call the spin logic after delay
                self.delay_active = False

    def run(self): # Game loop
        self.main_screen()
        if self.protect == "":
            pygame.quit()
            sys.exit()
        pauseButton = pygame.transform.scale(pygame.image.load("objects/pauseButton.png"), (50, 50)).convert_alpha()
        pauseButtonHitbox = pauseButton.get_rect(topleft=(720, 20))

        # slot machine Body
        slotMachine = pygame.transform.scale(pygame.image.load("objects/slotMachine.png"), (501.2, 373.8)).convert_alpha()
        slotMachine_rect = slotMachine.get_rect(center=(self.width // 2, self.height // 2))
        slotLine1 = pygame.Rect((145, self.height // 2 - 175), (slotMachine.get_width(), slotMachine.get_height() / 3.3))
        slotLine2 = pygame.Rect((145, self.height // 2 - 175 + 120), (slotMachine.get_width(), slotMachine.get_height() / 3.3))
        slotLine3 = pygame.Rect((145, self.height // 2 - 175 + 240), (slotMachine.get_width(), slotMachine.get_height() / 3.3))

        # buttons for slot machine
        betButton = pygame.transform.scale(pygame.image.load("objects/buttonBet.png"), (191.36, 63.18)).convert_alpha()
        betButtonHitBox = betButton.get_rect(center=(self.width // 2 - 110, self.height // 2 + 230))

        lineButton = pygame.transform.scale(pygame.image.load("objects/buttonLines.png"), (191.36, 63.18)).convert_alpha()
        lineButtonHitBox = lineButton.get_rect(center=(self.width // 2 + 110, self.height // 2 + 230))

        while self.running:
            messageText = self.font.render(self.spin.message[self.idxM], True, (0, 0, 0))
            messageText_rect = messageText.get_rect(center=(self.width // 2, self.height - 50))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEMOTION:
                    if pauseButtonHitbox.collidepoint(event.pos) or betButtonHitBox.collidepoint(event.pos) or lineButtonHitBox.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif self.handle_sprite.rect.collidepoint(event.pos) and not self.handle_sprite.animating:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pauseButtonHitbox.collidepoint(event.pos):
                        pygame.mixer.Sound("sounds/buttonClick.mp3").play()
                        self.pause()
                    if betButtonHitBox.collidepoint(event.pos):
                        pygame.mixer.Sound("sounds/linesAmount.mp3").play()
                        self.add_bet()
                    if lineButtonHitBox.collidepoint(event.pos):
                        pygame.mixer.Sound("sounds/linesAmount.mp3").play()
                        self.add_lines()
                    elif self.handle_sprite.rect.collidepoint(event.pos) and self.amountBet != 0 and self.amountLines != 0 and self.amountBet * self.amountLines <= self.balance:
                        self.handle_sprite.handle_click(event.pos)
                        if self.handle_sprite.index == 0:
                            pygame.mixer.Sound("sounds/handleSound.mp3").play()
                            pygame.mixer.Sound("sounds/slotSpin.mp3").play()
                            for slot in self.slot:
                                slot.spinning = True
                                slot.default()
                            self.delay_active = True
                            self.delay_start_time = pygame.time.get_ticks()

            self.screen.fill(self.bgColor)
            self.screen.blit(pauseButton, (720, 20))
            self.screen.blit(slotMachine, slotMachine_rect)
            self.screen.blit(messageText, messageText_rect)
            for i, slot in enumerate(self.slot):
                row = i // 3
                col = i % 3
                if i < 3:
                    slot.draw(self.screen, slotLine1)
                    if slot.spinning:
                        slot.update_position1()
                        if not slot.spinning:
                            self.idxM = self.spin.idxM
                            slot.update_draw(self.screen, self.selected_rows, slotLine1, row, col)
                elif i < 6:
                    slot.draw(self.screen, slotLine2)
                    if slot.spinning:
                        slot.update_position2()
                        if not slot.spinning:
                            slot.update_draw(self.screen, self.selected_rows, slotLine2, row, col)
                elif i < 9:
                    slot.draw(self.screen, slotLine3)
                    if slot.spinning:
                        slot.update_position3()
                        if not slot.spinning:
                            slot.update_draw(self.screen, self.selected_rows, slotLine3, row, col)

            self.take_spin()
            self.screen.blit(betButton, betButtonHitBox)
            self.screen.blit(lineButton, lineButtonHitBox)
            self.all_sprites.update()
            self.all_sprites.draw(self.screen)
            self.show_balance()
            self.update_information()
            if self.balance <= 0:
                pygame.mixer.music.stop()
                pygame.mixer.stop()
                pygame.mixer.Sound("sounds/gameOver.mp3").play()
                pygame.time.delay(2000)
                self.game_over()
            self.clock.tick(120)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()

# Donate to stonk my career https://paypal.me/EarlOrdovez
