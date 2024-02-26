class Bank:
    def __init__(self) -> None:
        self.food = 0.0
        self.lux = 0.0
        self.land = 0.0
    
    def getFoodCap(self):
        return self.food
    
    def getLuxCap(self):
        return self.lux
    
    def addFood(self, food):
        self.food += food
        
    def addLux(self, lux):
        self.lux += lux
        
    def deductFood(self, food):
        if self.food < food:
            # error message
            print("woah woah mr.mayor you don't have enough food to give out! ")
            return False
        self.food -= food
        
    def deductLux(self, lux):
        if self.lux < lux:
            # error message
            print("woah woah mr.mayor you don't have enough lux good to give out! ")
            return False
        self.lux -= lux
