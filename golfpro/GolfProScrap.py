import time
from golf import GolfScrap, GolfReservation

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime as dt
from kowanas_util_python import KowanasTime
from bs4 import BeautifulSoup as bs

class GolfProScrap(GolfScrap):
    name = 'golfpro'
    def __init__(self, session):
        super().__init__(session)
        session.maximize_window()
        self.__loggedin = False
        self.found = False

    def __getPage(self, url, element, title):
        try:
            wait = WebDriverWait(self._session, timeout=10)
            self._session.get(url)
            return wait.until(lambda d: d.find_element(element, title))
        except Exception as e:
            print (e)
            self._session.quit()

    def _load(self):
        try:
            if self.__loggedin == False:
                self.__getPage(self._loginUrl, By.NAME, 
                    'ctl00$ContentPlaceHolder1$userID').send_keys(self._id)
                self._session.find_element(By.NAME, 
                    'ctl00$ContentPlaceHolder1$userPass').send_keys(self._password)
                self._session.find_element(By.NAME, 
                    'ctl00$ContentPlaceHolder1$userPass').send_keys(Keys.RETURN)
                self.__loggedin = True
            self.__getPage(self._url, By.CLASS_NAME, 'home')
        except Exception as e:
            print(e)
            self._session.quit()

    def _parse(self):
        try:
            tds = self._session.find_elements(By.TAG_NAME, 'td')
            for td in tds:
                title = td.get_attribute('title')
                if title == '': continue 
                values = title.replace(' ', '').split('-')
                date = dt.strptime(values[0], '%Y년%m월%d일')
                if date <= dt.now(): continue 
                if values[1] == '일정없음': continue
                reservation = GolfReservation(date, values[1])
                self._reservations[KowanasTime.dateToString(date)] = reservation
        except Exception as e:
            print (e)
            self._session.quit()

    def _process(self):
        for key, value in self._reservations.items():
            if value.status != '마감':
                self._session.execute_script('Update(\'LIST|2022-08-19|2022-08-21|N|3|||\')')
                self.found = True
#                self._action.sendMessage(key)
                time.sleep(1)
                tables = self._session.find_elements(By.CLASS_NAME, 'tbl_01')
#                for table in tables:
#                    attrs = table.get_attribute('outerHTML')
#                    print (attrs)
                self._session.execute_script('Reserve(\'2022-08-21\',\'1430\',\'11\',\'3\',\'00042\',\'18\',\'\',\'True\',\'2\', \'190000\', \'0\')')
                time.sleep(1)
                
                self._action.savePage(
                    KowanasTime.nowToString('%Y%m%d%H%M%S')+'.html',
                    self._session.page_source)
                break

    def _dispose(self):
#        self._session.quit()
        pass