import requests

import crawler.helper.config as config

from bs4 import BeautifulSoup
from crawler.helper.singleton import Singleton
from crawler.poems.user import PoemsUser
from http import HTTPStatus

HOME_URL = 'https://www.poems.co.id'
USER_CONFIG = '.config'

class Poems(metaclass=Singleton):

  def init(self):
    print('Initiate POEMS data')

    # read user config
    userConfig = config.readUserConfig(USER_CONFIG)
    self.user = PoemsUser(
        userConfig['poemsUser'],
        userConfig['poemsPassword'],
        userConfig['poemsPin']
    )

    # create session
    self.session = requests.Session()

    # sending get request to POEMS home
    response = self.session.get(
        url = HOME_URL
    )

    if response.status_code != HTTPStatus.OK:
      raise RuntimeError('Response status ' + str(response.status_code))

    # save token
    htmlSoup = BeautifulSoup(response.text, 'lxml')
    htmlSoup = htmlSoup.find('div', attrs = { 'class': 'poems_login' })
    htmlSoup = htmlSoup.find('input', attrs = { 'name': '__RequestVerificationToken' })
    self.token = htmlSoup['value']

  def login(self):
    print('Login to POEMS')

    response = self.session.post(
      url = HOME_URL + '/PoemsApp/Login',
      data = {
        '__RequestVerificationToken' : self.token,
        'txtacctno' : self.user.username,
        'txtpwd' : self.user.password,
        'txtpin' : self.user.pin
      }
    )

    if response.status_code != HTTPStatus.OK:
      raise RuntimeError('Response status ' + str(response.status_code))

if __name__ == '__main__':
  Poems().init()
  Poems().login()
