from selenium import webdriver
import time

class Proxy:
    def __init__(self, site):
        options = webdriver.FirefoxOptions()
        options.headless = True
        self.auth = False
        self.driver = webdriver.Firefox(options=options)
        self.site = site

    def login(self, uname, pwd):
        if not self.auth:
            # Login logic here
            self.driver.get(self.site['LOGIN'])
            self.driver.find_element_by_name('username').send_keys(uname)
            self.driver.find_element_by_name('password').send_keys(pwd)
            try:
                self.driver.find_element_by_id('loginbtn').click()
            except:
                self.driver.find_element_by_class_name('btn btn-block btn-blue-alt').click()

            self.auth = self.driver.current_url != self.site['LOGIN']

    def logout(self):
        if self.auth:
            # Logout logic here
            self.auth = False

    def openPageOnAuth(self, url):
        # Open a page only if authenticated
        if self.auth:
            self.driver.get(url)

    def openPage(self, url):
        # Open a page regardless logged in or not
        self.driver.get(url)

    def close(self):
        if self.auth:
            self.logout()
        self.driver.close()