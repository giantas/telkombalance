#! /usr/bin/env python3

import os
import sys
import time
import notify2
from datetime import datetime
from pprint import pprint
from daterelate.daterelate import relate
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as conditions
from selenium.webdriver.support import ui
from configreader import ConfigReader

os.environ['DISPLAY'] = ':0'  # Set the display if set to run as cronjob

HOMEPAGE = 'http://myaccount.telkom.co.ke'
TODAY = datetime.now()

config = ConfigReader('defaults.ini')
TITLE = config.get('notificationtitle', default='Telkom Balance')
NUMBER = config.get('number', section='credentials', default='')
PASSWD = config.get('pass', section='credentials', default='')
s = os.path.join(os.path.expanduser('~'), 'bin')
driver_path = config.get('driverspath', default=s)
chrome_driver_name = config.get('chromedrivername',
                                section='Chrome',
                                default='chromedriver')
firefox_driver_name = config.get('firefoxdrivername',
                                 section='Firefox',
                                 default='geckodriver')
headless = config.get('headless', default=True)

chrome_options = ChromeOptions()
firefox_options = FirefoxOptions()
if headless:
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    firefox_options.add_argument('--headless')
    os.environ['MOZ_HEADLESS'] = '1'

browsers = {
    'chrome': {
        'filename': chrome_driver_name,
        'class': webdriver.Chrome,
        'kwargs': {
            'chrome_options': chrome_options
        }
    },
    'firefox': {
        'filename': firefox_driver_name,
        'class': webdriver.Firefox,
        'kwargs': {
            'firefox_options': firefox_options,
            'log_path': os.path.join(
                driver_path, 'geckodriver.log')
        }
    }
}

choice_browser = browsers[config.get('Browser', default='chrome')]

driver_full_path = os.path.join(
    driver_path, choice_browser['filename'])
choice_browser['kwargs']['executable_path'] = driver_full_path

read = notify2.init(TITLE)
notifier = notify2.Notification(TITLE, 'Querying')
notifier.show()


def alert(message, title=TITLE):
    notifier.update(title, message)
    notifier.show()


kwargs = choice_browser.get('kwargs', {})


def login(browser):
    """Log in to the website using the provided credentials"""
    number_input = browser.find_element_by_xpath(
        "//div[@class='login_form']/div[@id='divInputNumber']/input")
    pwd_input = browser.find_element_by_xpath(
        "//div[@class='login_form']/div[@id='divInputPwd']/input")
    login_btn = browser.find_element_by_id('userLoginBtn')

    number_input.clear()
    number_input.send_keys(NUMBER)

    pwd_input.clear()
    pwd_input.send_keys(PASSWD)

    login_btn.click()


def query():
    """Load selenium and scrape"""
    browser = choice_browser.get(
        'class', webdriver.Chrome)(**kwargs)
    browser.get(HOMEPAGE)

    try:
        # Wait until logout button is visible
        ui.WebDriverWait(browser, 3).until(
            conditions.visibility_of_element_located(
                (By.ID, 'userLogoutBtn')))
        # browser.find_element_by_id('userLogoutBtn').click()
    except TimeoutException:
        # Login if logout button not visible
        login(browser)

    try:
        # Locate details table
        ui.WebDriverWait(browser, 15).until(
            conditions.visibility_of_element_located(
                (By.CLASS_NAME, 'table_main')))
    except TimeoutException:
        browser.close()
        sys.exit(1)
    else:
        table = browser.find_element_by_class_name('table_main')

    rows = table.find_elements_by_tag_name('tr')

    messages = []

    for row in rows[1:6]:
        message = ''
        tds = row.find_elements_by_tag_name('td')
        for td in tds:
            try:
                input = td.find_element_by_tag_name('input')
            except NoSuchElementException:
                text = td.text.strip()
                message += '{}'.format(text)
            else:
                text = input.get_attribute('value')
                message += ': {}\n'.format(text)
                try:
                    date = datetime.strptime(text, '%d-%m-%Y')
                except ValueError:
                    pass
                else:
                    message += relate(date, TODAY, future='to expiry', past='ago')

        messages.append(message)

    browser.close()

    pprint(messages)

    for message in messages:
        # Display notification
        alert(message)
        time.sleep(3)


if __name__ == "__main__":
    query()
