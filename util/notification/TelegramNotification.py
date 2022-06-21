import telegram
from .Notification import Notification
from util.Config import  Config

class TelegramNotification(Notification):
    def __init__(self):
        config = Config()
        token = config.get('accesstoken', group='telegram')
        self.__users = config.get('users', group='telegram').split(',')
        self.__bot = telegram.Bot(token=token)

    def sendMessage(self, message):
        for user in self.__users:
            self.__bot.sendMessage(chat_id=user, text=message)
            print (f'{self.__users.index(user)+1}. sent message')