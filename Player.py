class Player:
    def __init__(self, bases):
        self.money = 100
        self.basesLeft = len(bases)

    def getBases(self):
        return self.basesLeft