from Units import *
from Constants import BROWN
from Constants import WHITE
from Constants import RIGHT
from Constants import LEFT
from Constants import RATE
from Constants import MELEECOST
from Constants import RANGECOST
from Constants import TANKCOST
from Constants import RECONCOST
from Player import Player


class RTSGame:
    def __init__(self):
        global player1, player2
        entities = []

        self.basesP1 = []
        self.basesP1.append(Base(WHITE,(100,100,100,100)))
        self.basesP1.append(Base(WHITE,(100,350,100,100)))
        self.basesP1.append(Base(WHITE,(100,600,100,100)))

        self.basesP2 = []
        self.basesP2.append(Base(WHITE,(1200,100,100,100)))
        self.basesP2.append(Base(WHITE,(1200,350,100,100)))
        self.basesP2.append(Base(WHITE,(1200,600,100,100)))
        entities.append(self.basesP1)
        entities.append(self.basesP2)

        paths = []
        paths.append(Box(BROWN,((200,112.5,1000,75))))
        paths.append(Box(BROWN,((200,362.5,1000,75))))
        paths.append(Box(BROWN,((200,612.5,1000,75))))
        entities.append(paths)

        player1 = Player(self.basesP1, "player1")
        player2 = Player(self.basesP2, "player2")

        self.units = []
        entities.append(self.units)

        self.buttons = []
        self.buttons.append(Button(WHITE, (300,25,50,40), self.spawn_unit))
        self.buttons.append(Button(WHITE, (500,25,50,40), self.spawn_unit))
        self.buttons.append(Button(WHITE, (700,25,50,40), self.spawn_unit))
        self.buttons.append(Button(WHITE, (900,25,50,40), self.spawn_unit))
        entities.append(self.buttons)

        self.screen = pygame.display.set_mode((1366,768))
        clock = pygame.time.Clock()

        running = True
        while running:
            dt = clock.tick(50)

            player1.addMoney(dt*RATE)
            player2.addMoney(dt*RATE)
            print(player1.getMoney())

            events = pygame.event.get()
            self.screen.fill((144, 245, 0))

            for entity in entities:
                for item in entity:
                    item.drawon(self.screen, dt)

            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.checkBounds(pos)

            self.checkCollision()

            pygame.display.flip()

    def spawn_unit(self):
        player = player1
        unit = "Melee"
        for base in self.basesP1:
            if base.active:
                coords = base.getcoords()
                if unit == "Melee":
                    cost = MELEECOST
                    if player.getName() == "player1":
                        unit = Melee(GREY, (coords[0] + coords[2], coords[1] + coords[3]/2, 25, 25), RIGHT)
                    else:
                        unit = Melee(GREY, (coords[0] + coords[2] + 975, coords[1] + coords[3] / 2, 25, 25), LEFT)
                elif unit == "Ranged":
                    cost = RANGECOST
                    if player.getName() == "player1":
                        unit = Ranged(GREY, (coords[0] + coords[2], coords[1] + coords[3]/2, 25, 25), RIGHT)
                    else:
                        unit = Ranged(GREY, (coords[0] + coords[2] + 975, coords[1] + coords[3] / 2, 25, 25), LEFT)
                elif unit == "Tank":
                    cost = TANKCOST
                    if player.getName() == "player1":
                        unit = Tank(GREY, (coords[0] + coords[2], coords[1] + coords[3]/2, 25, 25), RIGHT)
                    else:
                        unit = Tank(GREY, (coords[0] + coords[2] + 975, coords[1] + coords[3] / 2, 25, 25), LEFT)
                elif unit == "Recon":
                    cost = RECONCOST
                    if player.getName() == "player1":
                        unit = Recon(GREY, (coords[0] + coords[2], coords[1] + coords[3]/2, 25, 25), RIGHT)
                    else:
                        unit = Recon(GREY, (coords[0] + coords[2] + 975, coords[1] + coords[3] / 2, 25, 25), LEFT)
                if player.getMoney() > cost:
                    player.removeMoney(cost)
                    self.units.append(unit)

    def checkCollision(self):
        for unit in self.units:
            ounits = [u for u in self.units if unit.intersects(u.getpos()) and not unit == u]
            if ounits:  # list is not empty
                for u in ounits:
                    self.units.remove(u)
                    self.units.remove(unit)

    def checkBounds(self, pos):
        for base in self.basesP1:
            if base.intersects(pos):
                for b in self.basesP1:
                    b.setUnactive()  # Sets all bases to unactive
                base.setActive()  # Sets the active base to active
                break

        for button in self.buttons:
            if button.intersects(pos):
                button.clicked()
                break

        return