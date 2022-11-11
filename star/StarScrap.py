import requests

import time
from kowanas_util_python import Scrap, Config, KowanasTime, Action
from kowanas_util_python.notification import TelegramNotification
from datetime import datetime as dt
from datetime import timedelta as td

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup as bs

class StarScrap(Scrap):
    name = 'star'
    def __init__(self, session):
        super().__init__(session)
        session.maximize_window()
        config = Config()
        self._url = config.get('url', group=self.name)
        self._id = config.get('id', group=self.name)
        self._password = config.get('password', group=self.name)
        self.__first = False
        self.__targets = [
#          ['SFO', 'BKK', dt(2023, 2, 13), 7],
#          ['LAX', 'BKK', dt(2023, 2, 13), 7],
#          ['SFO', 'SIN', dt(2023, 2, 13), 7],
#          ['LAX', 'SIN', dt(2023, 2, 13), 7],
#          ['SFO', 'ICN', dt(2023, 2, 21), 7],
#          ['LAX', 'ICN', dt(2023, 2, 21), 7],
#          ['ICN', 'BKK', dt(2023, 2, 3), 7],
#          ['ICN', 'SIN', dt(2023, 2, 3), 7],
          ['BKK', 'ICN', dt(2023, 2, 21), 7],
          ['SIN', 'ICN', dt(2023, 2, 21), 7],
#          ['ICN', 'DPS', dt(2023, 2, 3), 7],
#          ['ICN', 'MLE', dt(2023, 2, 3), 7],
#          ['ICN', 'SFO', dt(2023, 2, 3), 7],
#          ['ICN', 'LAX', dt(2023, 2, 3), 7],
#          ['HND', 'SFO', dt(2023, 2, 5), 7],
#          ['HND', 'LAX', dt(2023, 2, 5), 7],
#          ['NRT', 'SFO', dt(2023, 2, 5), 7],
#          ['NRT', 'LAX', dt(2023, 2, 5), 7],
#          ['ICN', 'BKK', dt(2022, 11, 25), 7],
#          ['ICN', 'SIN', dt(2022, 11, 25), 7],
#          ['ICN', 'DPS', dt(2022, 11, 25), 7],
#          ['ICN', 'MLE', dt(2022, 11, 25), 7],
#          ['ICN', 'SFO', dt(2022, 11, 25), 7],
#          ['ICN', 'LAX', dt(2022, 11, 25), 7],
#          ['HND', 'SFO', dt(2022, 11, 27), 7],
#          ['HND', 'LAX', dt(2022, 11, 27), 7],
#          ['NRT', 'SFO', dt(2022, 11, 27), 7],
#          ['NRT', 'LAX', dt(2022, 11, 27), 7],
#          ['SFO', 'BKK', dt(2022, 12, 5), 7],
#          ['LAX', 'BKK', dt(2022, 12, 5), 7],
#          ['SFO', 'SIN', dt(2022, 12, 5), 7],
#          ['LAX', 'SIN', dt(2022, 12, 5), 7],
#          ['SFO', 'ICN', dt(2022, 12, 13), 7],
#          ['LAX', 'ICN', dt(2022, 12, 13), 7],
        ]
        self.__seat = 'business'
        self.__number = '2'
        self._action = Action(TelegramNotification())

    def _load(self):
        self.__getPage(self._url, By.LINK_TEXT, '로그인').send_keys(Keys.RETURN)
        self._session.find_element(By.ID, 'txtID').send_keys(self._id)
        self._session.find_element(By.ID, 'txtPW').send_keys(self._password)
        self._session.find_element(By.ID, 'btnLogin').send_keys(Keys.RETURN)
        time.sleep(3)
        reservation_url = 'https://www.flyasiana.com/I/KR/KO/RedemptionStarAllianceRegistTravel.do'
        self.__getPage(reservation_url, By.ID, 'txtDepartureAirport1')
        count = self.__lookup('ICN', 'BKK', '2023.02', '2023-2-6', self.__seat)

    def __changeDestination(self, src, dest, month, day, seat):
#        print (src, dest, month, day, seat)
        selectedSrc = self._session.find_element(By.ID, 'departureAirport1').get_attribute('value')
        if selectedSrc != src:
            self._session.find_element(By.XPATH, f'//a[@id="txtDepartureAirport1"]').click()
            time.sleep(3)
            self._session.find_element(By.ID, 'txtStarAirport').send_keys(src)
            self._session.find_element(By.ID, 'txtStarAirport').send_keys(Keys.RETURN)
            time.sleep(3)
            self._session.find_element(By.XPATH, f'//li[@airport="{src}"]').click()
            time.sleep(3)

        selectedDest = self._session.find_element(By.ID, 'arrivalAirport1').get_attribute('value')
        if selectedDest != dest:
            self._session.find_element(By.XPATH, f'//a[@id="txtArrivalAirport1"]').click()
            time.sleep(3)
            self._session.find_element(By.ID, 'txtStarAirport').send_keys(dest)
            self._session.find_element(By.ID, 'txtStarAirport').send_keys(Keys.RETURN)
            time.sleep(3)
            self._session.find_element(By.XPATH, f'//li[@airport="{dest}"]').click()
            time.sleep(3)

        selectedDay = self._session.find_element(By.ID, 'departureDate1').get_attribute('value')
        dates = day.split('-')
        dayDate = dt(int(dates[0]), int(dates[1]), int(dates[2]))
        dayDateString = dayDate.strftime('%Y%m%d')

#        print (selectedDay, dayDateString)
        if selectedDay != dayDateString:
            self._session.find_element(By.ID, 'sCalendar').send_keys(Keys.RETURN)
            time.sleep(5)
#            if selectedDay[4:6] != dayDateString[4:6]:
            calendar = self._session.find_element(By.XPATH, '//*[@title="탑승연도 및 월"]')
            calendar.click()
            time.sleep(3)
            calendar = Select(calendar)
            selectedMonth = selectedDay[:4]+'.'+selectedDay[4:6]
            calendar.select_by_visible_text(selectedMonth) #'2023.02'
            time.sleep(2)
            print (selectedMonth, month)
            calendar.select_by_visible_text(month) #'2023.02'
            time.sleep(3)

            self._session.find_element(By.XPATH, f'//*[@title="{day}"]').click()
        time.sleep(3)
        button = self._session.find_element(By.CLASS_NAME, 'btn_trv_edit')
        self._session.execute_script("javascript:changeBook();", button)
        time.sleep(3)
        button = self._session.find_element(By.NAME, 're').click()
        time.sleep(1)
        self._session.execute_script("javascript:_weblog = true;flightChange(this);", button)
        time.sleep(10)
        page = self._session.page_source
        seatTitle, seatIcon = self.__getSeatResource(seat)
        return page.count(seatIcon)

    def __getSeatResource(self, seat):
        if seat == 'business': 
            seatTitle = '비즈니스'
            seatIcon = 'business_area'
        elif seat == 'first':
            seatTitle = '퍼스트'
            seatIcon = 'first_area'
        else:
            seatTitle = '이코노미'
            seatIcon = 'economy_area'
        return seatTitle, seatIcon

    def __getPage(self, url, element, title):
        try:
            wait = WebDriverWait(self._session, timeout=10)
            self._session.get(url)
            return wait.until(lambda d: d.find_element(element, title))
        except Exception as e:
            print (e)
            self._session.quit()

    def _parse(self):
        for target in self.__targets:
            src = target[0]
            dest = target[1]
            startDay = target[2]
            numdays = target[3]
            days = [startDay + td(days=x) for x in range(0, numdays)]
            for day in days:
                month = day.strftime('%Y.%m')
                dayDate = f'{day.year}-{day.month}-{day.day}'
                count = self.__changeDestination(src, dest, month, dayDate, self.__seat)
                message = f'{dayDate} {src} => {dest} : {count}' 
                print (message)
                if count > 0:
                    self._action.sendMessage(message)

    def __lookup(self, src, dest, month, day, seat):
        self._session.find_element(By.ID, 'txtDepartureAirport1').click()
        time.sleep(3)
        self._session.find_element(By.ID, 'txtStarAirport').send_keys(src)
        self._session.find_element(By.ID, 'txtStarAirport').send_keys(Keys.RETURN)
        time.sleep(3)
        self._session.find_element(By.XPATH, f'//li[@airport="{src}"]').click()
        time.sleep(3)

        self._session.find_element(By.ID, 'txtArrivalAirport1').click()
        time.sleep(3)
        self._session.find_element(By.ID, 'txtStarAirport').send_keys(dest)
        self._session.find_element(By.ID, 'txtStarAirport').send_keys(Keys.RETURN)
        time.sleep(3)
        self._session.find_element(By.XPATH, f'//li[@airport="{dest}"]').click()
        time.sleep(3)

        self._session.find_element(By.ID, 'sCalendar1').send_keys(Keys.RETURN)
        time.sleep(3)
        calendar = self._session.find_element(By.XPATH, '//*[@title="탑승연도 및 월"]')
        calendar.click()
        calendar = Select(calendar)
        time.sleep(3)
        calendar.select_by_visible_text(month) #'2023.02'
        time.sleep(3)

        self._session.find_element(By.XPATH, f'//*[@title="{day}"]').click()
        time.sleep(3)

        seatTitle, seatIcon = self.__getSeatResource(seat)

        self._session.find_element(By.LINK_TEXT, seatTitle).send_keys(Keys.RETURN)
        time.sleep(3)
        adultCount = self._session.find_element(By.ID, 'adultCount')
        adultCount.click()
        time.sleep(2)
        adultCount.send_keys(Keys.BACKSPACE)
        adultCount.send_keys(self.__number)
        time.sleep(3)
#        plusButton = self._session.find_element(By.CLASS_NAME, 'btn_number plus')
#        for i in range(0, self.__number-1):
#            plusButton.click()
#            time.sleep(2)
#        self._session.find_element(By.ID, 'btnExpCase').send_keys(Keys.RETURN)
#        self._session.execute_script("javascript:showMileageRule();", button)
        self._session.find_element(By.ID, 'btn_coupon_layer').send_keys(Keys.RETURN)
        time.sleep(5)
        button = self._session.find_element(By.CLASS_NAME, 'btn_wrap_ceType2')
        self._session.execute_script("javascript:sendNext(this);", button)
        time.sleep(10)
        page = self._session.page_source
        return page.count(seatIcon)

    def _process(self):
        pass

    def _dispose(self):
        pass