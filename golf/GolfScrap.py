import requests

from util import Scrap, Config, KowanasTime, Action
from util.notification import TelegramNotification
from datetime import datetime as dt
from .GolfReservation import GolfReservation

class GolfScrap(Scrap):
    name = 'golf'
    def __init__(self):
        super().__init__(requests.Session())
        config = Config()
        self.__url = config.get('url', group=self.name)
        self.__loginUrl = config.get('login_url', group=self.name)
        self.__id = config.get('id', group=self.name)
        self.__password = config.get('password', group=self.name)
        self.__thePage = None
        self.__reservations = {}
        self.__action = Action(TelegramNotification())

    def _load(self):
        loginPage = self._getPage(self.__loginUrl)
#        inputTags = loginPage.findAll('input')
#        for tag in inputTags:
#            print(tag)

        credentialInfos = {}
        credentialInfos['ctl00$ContentPlaceHolder1$userID'] = self.__id
        credentialInfos['ctl00$ContentPlaceHolder1$userPass'] = self.__password
        credentialInfos['ctl00$ContentPlaceHolder1$SendLoginButton'] = 'click'
        credentialInfos['__VIEWSTATE'] = loginPage.find('input',
                                               {'id':'__VIEWSTATE'})['value']
        credentialInfos['__VIEWSTATEGENERATOR'] = loginPage.find('input',
                                      {'id':'__VIEWSTATEGENERATOR'})['value']
        credentialInfos['__EVENTVALIDATION'] = loginPage.find('input',
                                         {'id':'__EVENTVALIDATION'})['value']
        self._postPage(self.__loginUrl, credentialInfos)
        self.__thePage = self._getPage(self.__url)

    # <td class="" title="2022년 06월 01일 - 마감"
    def _parse(self):
        tds = self.__thePage.findAll('td')
        tds = [td['title'] for td in tds if 'title' in list(td.attrs.keys())]
        for td in tds:
            values = td.replace(' ', '').split('-')
            date = dt.strptime(values[0], '%Y년%m월%d일')
            if date <= dt.now(): continue         
            if values[1] == '일정없음': continue
            reservation = GolfReservation(date, values[1])
            self.__reservations[KowanasTime.dateToString(date)] = reservation

    def _process(self):
        for key, value in self.__reservations.items():
            if value.status != '마감':
                self.__action.sendMessage(key)
                self.__action.savePage(
                    KowanasTime.nowToString('%Y%m%d%H%M%S')+'.html',
                    self.__thePage)