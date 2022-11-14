import requests

import time
from kowanas_util_python import Scrap, Config, KowanasTime, Action
from kowanas_util_python.notification import TelegramNotification
from datetime import datetime as dt

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup as bs

class AsianaScrap(Scrap):
    name = 'asiana'
    def __init__(self, session):
        super().__init__(session)
        session.maximize_window()
        config = Config()
        self._url = config.get('url', group=self.name)
        self._id = config.get('id', group=self.name)
        self._password = config.get('password', group=self.name)
        self.__first = False
        self.__months = ['2023.02', '2022.12']
        self.__days = ['2023-2-6', '2022-12-6']
        self.__rmonths = ['2023.02', '2022.12']
        self.__rdays = ['2023-2-21', '2022-12-21']
        self.__seat = 'business'
        self.__number = '4'
        self._action = Action(TelegramNotification())

    def _load(self):
        self.__getPage(self._url, By.LINK_TEXT, '로그인').send_keys(Keys.RETURN)
        self._session.find_element(By.ID, 'txtID').send_keys(self._id)
        self._session.find_element(By.ID, 'txtPW').send_keys(self._password)
        self._session.find_element(By.ID, 'btnLogin').send_keys(Keys.RETURN)
        time.sleep(3)
        reservation_url = 'https://www.flyasiana.com/I/KR/KO/RedemptionRegistTravel.do'
        self.__getPage(reservation_url, By.LINK_TEXT, '편도').send_keys(Keys.RETURN)
        count = self.__lookup('ICN', 'BKK', self.__months[0], self.__days[0], self.__seat)

    def __changeDestination(self, src, dest, month, day, seat):
        self._session.find_element(By.ID, 'txtDepartureAirport1').send_keys(src)
        time.sleep(3)
        self._session.find_element(By.ID, 'txtDepartureAirport1').send_keys(Keys.RETURN)
        time.sleep(3)
        self._session.find_element(By.ID, 'txtArrivalAirport1').send_keys(dest)
        time.sleep(3)
        self._session.find_element(By.ID, 'txtArrivalAirport1').send_keys(Keys.RETURN)
        time.sleep(3)
        selectedDay = self._session.find_element(By.ID, 'departureDate1').get_attribute('value')
        dates = day.split('-')
        dayDate = dt(int(dates[0]), int(dates[1]), int(dates[2]))
        dayDateString = dayDate.strftime('%Y%m%d')

#        print (selectedDay, dayDateString)
        if selectedDay != dayDateString:
            self._session.find_element(By.ID, 'sCalendar1').send_keys(Keys.RETURN)
            time.sleep(3)
            calendar = self._session.find_element(By.XPATH, '//*[@title="탑승연도 및 월"]')
            calendar.click()
            time.sleep(3)
            calendar = Select(calendar)
            calendar.select_by_visible_text(month) #'2023.02'
            time.sleep(3)

            self._session.find_element(By.XPATH, f'//*[@title="{day}"]').click()
        time.sleep(3)
        button = self._session.find_element(By.CLASS_NAME, 'btn_trv_edit')
        self._session.execute_script("javascript:changeBookcondition();", button)
        time.sleep(5)
        page = self._session.page_source
        seatTitle, seatIcon = self.__getSeatResource(seat)
        return page.count(seatIcon)

    def __getSeatResource(self, seat):
        if seat == 'business': 
            seatTitle = '비즈니스'
            seatIcon = 'ico_cal_business'
        else:
            seatTitle = '이코노미'
            seatIcon = 'ico_cal_economy'
        return seatTitle, seatIcon

    def __lookup(self, src, dest, month, day, seat):
        self._session.find_element(By.ID, 'txtDepartureAirport1').send_keys(src)
        time.sleep(3)
        self._session.find_element(By.ID, 'txtDepartureAirport1').send_keys(Keys.RETURN)
        time.sleep(3)
        self._session.find_element(By.ID, 'txtArrivalAirport1').send_keys(dest)
        time.sleep(3)
        self._session.find_element(By.ID, 'txtArrivalAirport1').send_keys(Keys.RETURN)
        time.sleep(3)
        self._session.find_element(By.ID, 'sCalendar').send_keys(Keys.RETURN)
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
        adultCount.send_keys(Keys.DELETE)
        adultCount.send_keys(self.__number)
        time.sleep(3)
#        plusButton = self._session.find_element(By.CLASS_NAME, 'btn_number plus')
#        for i in range(0, self.__number-1):
#            plusButton.click()
#            time.sleep(2)
        self._session.find_element(By.ID, 'btn_coupon_layer').send_keys(Keys.RETURN)
        time.sleep(5)
        button = self._session.find_element(By.CLASS_NAME, 'btn_wrap_ceType2')
        self._session.execute_script("javascript:$(this).prev().trigger('click');toFlightsSelect();", button)
        time.sleep(5)
        page = self._session.page_source
        return page.count(seatIcon)

    def __getPage(self, url, element, title):
        try:
            wait = WebDriverWait(self._session, timeout=10)
            self._session.get(url)
            return wait.until(lambda d: d.find_element(element, title))
        except Exception as e:
            print (e)
            self._session.quit()

    def _parse(self):
        destinations = ['BKK', 'SFO', 'LAX', 'CDG', 'SIN', 'JFK', 'ORD', 'SEA', 'HNL', 'LHR', 'FCO', 'BCN', 'frank', 'SYD']
        for month, day in zip(self.__months, self.__days):
            print (day)
            for destination in destinations:
                count = self.__changeDestination('ICN', destination, month, day, 'business')
                message = f'{day} ICN => {destination} : {count}' 
                print (message)
                if count > 0:
                    self._action.sendMessage(message)

        for month, day in zip(self.__rmonths, self.__rdays):
            print (day)
            for destination in destinations:
                count = self.__changeDestination(destination, 'ICN', month, day, 'business')
                message = f'{day} ICN <= {destination} : {count}' 
                print (message)
                if count > 0:
                    self._action.sendMessage(message)

    def _process(self):
        pass

    def _dispose(self):
        pass