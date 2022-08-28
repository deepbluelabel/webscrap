import sys
sys.path.append('/Library/Python/local-packages')
import requests
import time
from selenium import webdriver
from golfpro import GolfProScrap
from golf import GolfScrap
from kowanas_util_python import Config
import chromedriver_autoinstaller as chromedriver
chromedriver.install()

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

        if site == GolfScrap.name: return GolfScrap(requests.Session())
        if site == GolfProScrap.name: 
            return GolfProScrap(webdriver.Chrome())

if __name__ == '__main__':
    config = Config('.config')
    scrap = ScrapFactory.create(sys.argv)
    if scrap == None: sys.exit()
    while True:
        if scrap.found == False:
            scrap.run()
        time.sleep(10)
