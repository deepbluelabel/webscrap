from abc import *

class Notification(metaclass=ABCMeta):
    def sendMessage(self, message):
        pass