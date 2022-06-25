from golf import GolfScrap, GolfReservation

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime as dt

class GolfProScrap(GolfScrap):
    name = 'golfpro'
    def __init__(self, session):
        super().__init__(session)

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
            self.__getPage(self._loginUrl, By.NAME, 
                'ctl00$ContentPlaceHolder1$userID').send_keys(self._id)
            self._session.find_element(By.NAME, 
                'ctl00$ContentPlaceHolder1$userPass').send_keys(self._password)
            self._session.find_element(By.NAME, 
                'ctl00$ContentPlaceHolder1$userPass').send_keys(Keys.RETURN)
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
        except Exception as e:
            print (e)
            self._session.quit()

    def _dispose(self):
        self._session.quit()