from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs

import logging
import time

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s [%(module)s][%(funcName)s] %(levelname)s : %(message)s',
    datefmt='(%d/%m/%Y) %H:%M:%S'
)


class Proxy:
    def __init__(self, website, credentials=None, headless=True):        
        self.website = website
        self.credentials = credentials
        self.auth = False

        try:
            logging.debug('Trying Chrome webdriver')
            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.headless = headless
            self.driver = webdriver.Chrome(options=chromeOptions)
            logging.debug('Chrome webdriver initiated')
        except Exception as e:
            logging.debug('Chrome webdriver failed')
            try:
                logging.debug('Trying Firefox webdriver')
                firefoxOptions = webdriver.FirefoxOptions()
                firefoxOptions.headless = headless
                firefoxProfile = webdriver.FirefoxProfile()
                self.driver = webdriver.Firefox(options=firefoxOptions, firefox_profile=firefoxProfile)
                logging.debug('Firefox webdriver initiated')
            except Exception as e:
                logging.debug('Firefox webdriver failed')
                logging.critical('No available webdriver')

        logging.info('Proxy initialized')

    def login(self):
        self.driver.get(self.website['LOGIN'])
        self.driver.find_element_by_name('username').send_keys(self.credentials['username'])
        self.driver.find_element_by_name('password').send_keys(self.credentials['password'])

        try:
            self.driver.find_element_by_id('loginbtn').click()
        except:
            self.driver.find_element_by_class_name('btn btn-block btn-blue-alt').click()
        
        self.auth = self.driver.current_url != self.website['LOGIN']

        if not self.auth:
            logging.error('Log in failed')
        else:
            logging.info('Successfully logged in into %s', self.website['MAIN'])

    def openPage(self, url):
        if self.credentials:
            if self.auth:
                self.driver.get(url)
            else:
                self.login()
        else:
            self.driver.get(url)
        
        if self.driver.current_url == url:
            logging.info('Proxy successfully opened %s', url)
        else:
            logging.error('Proxy failed to open %s', url)

    def waitForElement(self, partialLinkText):
        try:
            element_present = EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, partialLinkText))
            WebDriverWait(self.driver, 3).until(element_present)
        except TimeoutException:
            pass
    
    def clickLink(self, buttonName):
        try:
            element_present = EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, buttonName))
            WebDriverWait(self.driver, 3).until(element_present)
        except TimeoutException:
            logging.error('Proxy timeout while trying to click %s', buttonName)
        
        self.driver.find_element_by_link_text(buttonName).click()

        logging.info('Proxy clicked "%s" link', buttonName)
        logging.info('Proxy url now at %s', self.driver.current_url)
    
    def getSauce(self, expectedClassName=None, expectedId=None, expectedXpath=None, expectedTagName=None):
        if expectedClassName:
            try:
                element_present = EC.presence_of_element_located((By.CLASS_NAME, expectedClassName))
                WebDriverWait(self.driver, 5).until(element_present)
            except TimeoutException:
                logging.warning('Proxy timeout while trying to find element by Class Name: "%s"', expectedClassName)
        if expectedId:
            try:
                element_present = EC.presence_of_element_located((By.ID, expectedId))
                WebDriverWait(self.driver, 5).until(element_present)
            except TimeoutException:
                logging.warning('Proxy timeout while trying to find element by ID: "%s"', expectedId)
        if expectedXpath:
            try:
                element_present = EC.presence_of_element_located((By.XPATH, expectedXpath))
                WebDriverWait(self.driver, 5).until(element_present)
            except TimeoutException:
                logging.warning('Proxy timeout while trying to find element by ID: "%s"', expectedXpath)
        if expectedTagName:
            try:
                element_present = EC.presence_of_element_located((By.TAG_NAME, expectedTagName))
                WebDriverWait(self.driver, 3).until(element_present)
            except TimeoutException:
                logging.warning('Proxy timeout while trying to find element by ID: "%s"', expectedXpath)


        return bs(self.driver.page_source, 'html.parser')

    def logout(self):
        pass

    def close(self):
        if self.auth:
            self.logout()
        self.driver.close()
        logging.info('Proxy closed')

class OpenWeb:
    def __init__(self, website, credentials=None, headless=True):
        self.proxy = Proxy(website, credentials, headless)

    def __enter__(self):
        self.proxy.openPage(self.proxy.website['MAIN'])
        return self.proxy

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.proxy.close()      

# with ProxyContext(
#     website={'MAIN': 'https://sap.gunadarma.ac.id/'}
# ) as ProxyFakultas:
#     ProxyFakultas.clickLink('Daftar SAP')