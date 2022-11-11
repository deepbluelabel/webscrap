import sys
sys.path.append('/Library/Python/local-packages')
import requests
import time
from selenium import webdriver
from golfpro import GolfProScrap
from golf import GolfScrap
from asiana import AsianaScrap
from star import StarScrap
from kowanas_util_python import Config
import chromedriver_autoinstaller as chromedriver
chromedriver.install()

class ScrapFactory:
    @classmethod
    def create(self, argv):
        option = webdriver.ChromeOptions()
        option.add_argument('--no-sandbox')
        option.add_argument("disable-gpu")
        option.add_argument("--lang=ko_KR")
        option.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.87 Safari/537.36')
        option.add_argument('--disable-blink-features=AutomationControlled')
        option.add_argument("--disable-extensions")
        option.add_experimental_option('useAutomationExtension', False)
        option.add_experimental_option("excludeSwitches", ["enable-automation"])
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
        if site == AsianaScrap.name: return AsianaScrap(webdriver.Chrome(options=option))
        if site == StarScrap.name: return StarScrap(webdriver.Chrome(options=option))

if __name__ == '__main__':
    config = Config('.config')
    scrap = ScrapFactory.create(sys.argv)
    if scrap == None: sys.exit()
#    while True:
#    if scrap.found == False:
    scrap.run()
    time.sleep(10)
