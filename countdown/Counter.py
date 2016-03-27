import time
import math
from enum import Enum
import argparse


class CounterEvents(Enum):
    STATUS_CHANGE_WARNING = "sc-warning"
    STATUS_CHANGE_DANGER = "sc-danger"
    STATUS_CHANGE_TIME_OUT = "sc-timeout"
    STATUS_CHANGE_NORMAL = "sc-normal"


class CounterOptions:
    def __init__(self):
        self.INITIAL_COUNTER = 300
        self.WARNING_LIMIT = 60
        self.DANGER_LIMIT = 30

    def load(self, args):
        parser = argparse.ArgumentParser(description='Start a countdown interactive interface.')
        parser.add_argument('--counter', '-c', type=int, default=self.INITIAL_COUNTER, help='Amount of seconds for the timer')
        parser.add_argument('--warning', '-w', type=int, default=self.WARNING_LIMIT, help='Time limit to start warning signal')
        parser.add_argument('--danger', '-d', type=int, default=self.DANGER_LIMIT, help='Time limit to start danger signal')
        parsed = parser.parse_args(args)
        self.INITIAL_COUNTER = parsed.counter
        self.WARNING_LIMIT = parsed.warning
        self.DANGER_LIMIT = parsed.danger
        return self


class Counter():
    def __init__(self, options):
        self.initialValue = options.INITIAL_COUNTER
        self.running = False
        self.currentValue = options.INITIAL_COUNTER
        self.dangerLimit = options.DANGER_LIMIT
        self.warningLimit = options.WARNING_LIMIT
        self.lastTick = None
        self.text = ""
        self.color = (255, 255, 255)
        self.status = "normal"

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
        events = []
        if self.running:
            newTick = time.time()
            self.currentValue -= newTick - self.lastTick
            self.lastTick = newTick
        if self.currentValue > 0:
            usefulValue = math.ceil(self.currentValue)
            if usefulValue <= self.dangerLimit:
                self.color = (255,50,50)
                if self.status != "danger":
                    self.status = "danger"
                    events.append(CounterEvents.STATUS_CHANGE_DANGER)
            elif usefulValue <= self.warningLimit:
                self.color = (255,255,100)
                if self.status != "warning":
                    self.status = "warning"
                    events.append(CounterEvents.STATUS_CHANGE_WARNING)
            else:
                self.color = (255, 255, 255)
                if self.status != "normal":
                    self.status = "normal"
                    events.append(CounterEvents.STATUS_CHANGE_NORMAL)
            self.text = time.strftime("%Mm%Ss", time.gmtime(usefulValue))
        else:
            self.currentValue = 0
            self.running = False
            self.text = "TIME'S UP!"
            self.color = (148, 190, 0) # Tuenti Green
            if self.status != "time-out":
                self.status = "time-out"
                events.append(CounterEvents.STATUS_CHANGE_TIME_OUT)
        return events


    def isRunning(self):
        return self.running

    def getValue(self):
        return self.currentValue