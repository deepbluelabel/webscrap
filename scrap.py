import sys
from golf import GolfScrap
from util import Config

class ScrapFactory:
    @classmethod
    def create(self, argv):
        if len(argv) != 2:
            print('Wrong command, Please refer the usage as following')
            print('scrap [site name]')
            return None

        site = argv[1]
        config = Config()

        if config.isExistGroup(site) == False:
            print('Wrong site, Please refer site names in .config file as following')
            groups = config.getGroups()
            print (groups)
            return None

        if site == GolfScrap.name: return GolfScrap()

if __name__ == '__main__':
    config = Config('.config')
    scrap = ScrapFactory.create(sys.argv)
    if scrap == None: sys.exit()
    scrap.run()
