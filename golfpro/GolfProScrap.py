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

    def _waitTime(self):
        today = dt.now()
        scheduledTime = dt(today.year, today.month, today.day, hour=13, minute=0, second=0)
        while True:
            currentTime = dt.now()
            print (currentTime.strftime('%H:%M:%S'), scheduledTime.strftime('%H:%M:%S'))
            if currentTime >= scheduledTime:
                break
            time.sleep(1)

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
            self._waitTime()
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

    def _parseList(self, data):
        data = data.split('|')
        return data[1], data[2]

    def _compareDate(self, a, b):
        a = int(a.replace('-', ''))
        b = int(b.replace('-', ''))
        if a > b: return -1
        if a < b: return 1
        return 0

    def _process(self):
        updates = self._session.find_elements(By.TAG_NAME, 'a')
        updateList = []
        for update in updates:
            day = update.get_attribute('href')
            if 'Update' in str(day) and 'LIST' in str(day):
                print (day)
                startDate, endDate = self._parseList(str(day))
                compareStart = self._compareDate(startDate, self._wantDay)
                compareEnd = self._compareDate(endDate, self._wantDay)
                if compareStart >= 0 and compareEnd <= 0:
                    updateList.append(day)
            
        if len(updateList) > 0:
            update = str(updateList[0])
            listdata = update.split('\'')[1]
            print (listdata)
            self._session.execute_script(f'Update(\'{listdata}\')')
        else: 
            print (f'no day to select you want {self._wantDay} day')
            return
        return

        time.sleep(1)
        reserves = self._session.find_elements(By.TAG_NAME, 'a')
        reserveList = []
        for reserve in reserves:
            slot = reserve.get_attribute('href')
            if 'Reserve' in str(slot):
                print(slot)
                reserveTime = self._getTimeFromReserve(slot)
                reserveDate = self._getDateFromReserve(slot)
                if int(reserveTime) >= self._wantTime*100 and int(reserveTime) <= (self._wantTime+1)*100 and reserveDate == self._wantDay:
                    reserveList.append(slot)
        pick = None
        for reserve in reserveList:
            course = self._getCourceFromReserve(reserve)
            if course == '22':
                pick = reserve
                break
        
        if len(reserveList) > 0:
            if pick == None:
                count = len(reserveList)
                pick = reserveList[int(count / 2)]
            reserve = str(pick)
            data = reserve.split(':')[1][:-1]
            print (data)
            self._session.execute_script(data)
        else: 
            print (f'no time to select you want {self._wantTime} oclock at {self._wantDay}')
            return

    def _getDateFromReserve(self, reserve):
        data = str(reserve)
        timestr = data.split('(')[1].split(',')[0]
        return timestr.split('\'')[1]

    def _getTimeFromReserve(self, reserve):
        data = str(reserve)
        timestr = data.split('(')[1].split(',')[1]
        return timestr.split('\'')[1]

    def _getCourceFromReserve(self, reserve):
        data = str(reserve)
        timestr = data.split('(')[1].split(',')[2]
        return timestr.split('\'')[1]

    def _dispose(self):
#        self._session.quit()
        pass