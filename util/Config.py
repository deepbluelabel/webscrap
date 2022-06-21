from .Singleton import Singleton

class Config(metaclass=Singleton):
    defaultGroup = 'base'
    def __init__(self, file):
        self.__configs = {}
        with open(file) as f:
            self.__configs = self.__parse(f.read())

    def __parse(self, data):
        configs = {}
        lines = data.split('\n')
        name = self.defaultGroup
        configs[name] = {}
        for line in lines:
            line = line.replace(' ', '')
            try:
                if '[' in line and ']' in line:
                    left = line.find('[')
                    right = line.find(']')
                    name = line[left+1:right]
                    configs[name] = {}
                else:
                    keyValue = line.split('=')
                    key = keyValue[0]
                    value = keyValue[1]
                    configs[name][key] = value
            except Exception as e:
                continue
        return configs

    def get(self, key, group=defaultGroup):
        return self.__configs[group][key]

    def isExistGroup(self, group):
        return group in self.getGroups()

    def getGroups(self):
        return list(self.__configs.keys())
