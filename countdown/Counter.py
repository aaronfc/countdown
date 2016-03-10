import time
import math

class Counter():
    def __init__(self, initialValue, warningLimit, dangerLimit):
        self.initialValue = initialValue
        self.running = False
        self.currentValue = initialValue
        self.dangerLimit = dangerLimit
        self.warningLimit = warningLimit
        self.lastTick = None
        self.text = ""
        self.color = (255, 255, 255)

    def start(self):
        if self.currentValue == 0:
            self.currentValue = self.initialValue
        self.lastTick = time.time()
        if not self.running:
            self.running = True

    def reset(self):
        self.lastTick = time.time()
        self.currentValue = self.initialValue

    def stop(self):
        self.running = False

    def update(self):
        if self.running:
            newTick = time.time()
            self.currentValue -= newTick - self.lastTick
            self.lastTick = newTick
        if self.currentValue > 0:
            usefulValue = math.ceil(self.currentValue)
            if usefulValue <= self.dangerLimit:
                self.color = (255,50,50)
            elif usefulValue <= self.warningLimit:
                self.color = (255,255,100)
            else:
                self.color = (255, 255, 255)
            self.text = time.strftime("%Mm%Ss", time.gmtime(usefulValue))
        else:
            self.currentValue = 0
            self.running = False
            self.text = "TIME'S UP!"
            self.color = (148, 190, 0) # Tuenti Green

    def isRunning(self):
        return self.running

    def getValue(self):
        return self.currentValue