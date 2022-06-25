import requests

from util import Scrap, Config, KowanasTime, Action
from util.notification import TelegramNotification
from datetime import datetime as dt
from .GolfReservation import GolfReservation

class GolfScrap(Scrap):
    name = 'golf'
    def __init__(self, session):
        super().__init__(session)
        config = Config()
        self._url = config.get('url', group=self.name)
        self._loginUrl = config.get('login_url', group=self.name)
        self._id = config.get('id', group=self.name)
        self._password = config.get('password', group=self.name)
        self._thePage = None
        self._reservations = {}
        self._action = Action(TelegramNotification())

    def _load(self):
        loginPage = self._getPage(self._loginUrl)
#        inputTags = loginPage.findAll('input')
#        for tag in inputTags:
#            print(tag)

        credentialInfos = {}
        credentialInfos['ctl00$ContentPlaceHolder1$userID'] = self._id
        credentialInfos['ctl00$ContentPlaceHolder1$userPass'] = self._password
        credentialInfos['ctl00$ContentPlaceHolder1$SendLoginButton'] = 'click'
        credentialInfos['__VIEWSTATE'] = loginPage.find('input',
                                               {'id':'__VIEWSTATE'})['value']
        credentialInfos['__VIEWSTATEGENERATOR'] = loginPage.find('input',
                                      {'id':'__VIEWSTATEGENERATOR'})['value']
        credentialInfos['__EVENTVALIDATION'] = loginPage.find('input',
                                         {'id':'__EVENTVALIDATION'})['value']
        self._postPage(self._loginUrl, credentialInfos)
        self._thePage = self._getPage(self._url)

    # <td class="" title="2022년 06월 01일 - 마감"
    def _parse(self):
        tds = self._thePage.findAll('td')
        tds = [td['title'] for td in tds if 'title' in list(td.attrs.keys())]
        for td in tds:
            values = td.replace(' ', '').split('-')
            date = dt.strptime(values[0], '%Y년%m월%d일')
            if date <= dt.now(): continue         
            if values[1] == '일정없음': continue
            reservation = GolfReservation(date, values[1])
            self._reservations[KowanasTime.dateToString(date)] = reservation

    def _process(self):
        for key, value in self._reservations.items():
            if value.status != '마감':
                self._action.sendMessage(key)
                self._action.savePage(
                    KowanasTime.nowToString('%Y%m%d%H%M%S')+'.html',
                    self._thePage)