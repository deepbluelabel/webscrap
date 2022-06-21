class Action:
    def __init__(self, notificdation):
        self.__notification = notificdation

    def sendMessage(self, message):
        try:
            self.__notification.sendMessage(message)
        except Exception as e:
            print (str(e))

    def savePage(self, filename, page):
        with open(filename, 'w') as f:
            f.write(str(page))