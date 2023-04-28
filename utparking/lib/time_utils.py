from utparking.lib.log import get_logger
class Ticker:
    def __init__(self):
        self.log = get_logger()
        self.log.debug("Initializing ticker")
        self.__ticks = 0
        

    def tick(self):
        self.__ticks += 1

    def __call__(self):
        return self.__ticks
    
    def reset(self):
        self.log.warning("Resetting tick counter")
        self.__ticks = 0
