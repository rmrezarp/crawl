# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 19:11:16 2018

@author: Hp
"""

import re
import os
import pandas as pd
import sys
import dateutil.relativedelta as relativedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.common.exceptions import NoSuchElementException        

#from Crypto.Cipher import AES
import base64
import time
import datetime
import itertools
from nltk.tokenize import TweetTokenizer
from selenium.webdriver.common.keys import Keys



class myPage(webdriver.Firefox, webdriver.Chrome, webdriver.Ie):
    def __check_exists_by_xpath(self, xpath):
        try:
            self.find_element_by_xpath(xpath)
        except NoSuchElementException as e:
            print(e)
            return False
        return True

    def __send_keys(self, xpath, command, text):
        if command == "input":
            if self.__check_exists_by_xpath(xpath):            
                objectn = self.find_element_by_xpath(xpath)
                objectn.send_keys(text)
                print('success input {} with {} element'.format(command,xpath))
            else:
                print('failed input {} with {} element'.format(command,xpath))
        elif command == "click":
            if self.__check_exists_by_xpath(xpath):            
                objectn = self.find_element_by_xpath(xpath)
                objectn.click()
                print('success click {} element'.format(xpath))
            else:
                print('failed click {} element'.format(xpath))            

    def __access_menu(self, menu):
        menulist = {"profile":0,"inbox":1,"myshop":2,"pesanan":3,"logout":4}
        block = self.find_element_by_xpath('//*[@id="login-dp"]')
        alllist = block.find_elements_by_class_name('menu-icon-dropdown')
        return alllist[menulist[menu]]

###login and logout method
    def login_page(self, username, password): 
        print('masuk')
        
        WebDriverWait(self, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/ul[1]/li/a/i')))
        men_menu = self.find_element_by_xpath('/html/body/div[1]/div[2]/div/ul[2]')
        ActionChains(self).move_to_element(men_menu).perform()
        
        self.__send_keys('//*[@id="usernameU"]', "input", username)
        self.__send_keys('//*[@id="passwordU"]', "input", password)
        self.__send_keys('//*[@id="btn-login"]', "click", "")
        print('success login')
    
    def login_page_account(self, username, password):
        self.get_page(self, 'https://besoklibur.com/p/account/masuk')
        WebDriverWait(self, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]')))

        self.__send_keys('//*[@id="usernameU"]', "input", username)
        self.__send_keys('//*[@id="passwordU"]', "input", password)
        self.__send_keys('//*[@id="btn-login"]', "click", "")
        print('success login')
        
    def logout_page(self):
        WebDriverWait(self, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/ul[1]/li/a/i')))
        men_menu = self.find_element_by_xpath('/html/body/div[1]/div[2]/div/ul[2]')
        ActionChains(self).move_to_element(men_menu).perform()
        objectn = self.__access_menu("logout")     
        objectn.click()
        print('success logout')        
###login and logout method

    def profile_page(self):
        objectn = self.__access_menu("profile")     
        objectn.click()
        

    def get_page(self, url):
        self.get(url)
    
    def __init__(self, browser,outfileurl):
        if browser.lower() == "ie":
            print('ie selected')
            webdriver.Ie.__init__(self)
        elif browser.lower() == "chrome":
            print('chrome selected')
        #    webdriver.Chrome.__init__(self)
            chromedriver = "E:/RM/python/chromedriver_win32/chromedriver.exe"
            os.environ["webdriver.chrome.driver"] = chromedriver
            prefs = {"profile.managed_default_content_settings.images":2}
            options = Options()
#            options.add_argument("--disable-extensions")
#            options.add_argument("--disable-notifications")
#            options.add_argument("--headless")
#            options.add_argument("--disable-gpu")            
            options.add_argument("--start-maximized");
            options.add_experimental_option("prefs",prefs)
            webdriver.Chrome.__init__(self,executable_path=chromedriver, chrome_options=options)
            self.get_page(outfileurl)

        elif browser.lower() == "phantom":
            print('phantom selected')
            phantomjs_path = "C:/PhantomJS/bin/phantomjs.exe"
            desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
            desired_capabilities['phantomjs.page.customHeaders.User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) ' \
                                                                          'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                                                          'Chrome/39.0.2171.95 Safari/537.36'
            webdriver.PhantomJS.__init__(self,executable_path=phantomjs_path,desired_capabilities=desired_capabilities, service_args=['--ignore-ssl-errors=true'], service_log_path=os.path.devnull)
           
        else:
            webdriver.Firefox.__init__(self)
            print('firefox selected')

if __name__ == '__main__':
    browser = "chrome"
    outfileurl = "https://besoklibur.com"
    data = myPage(browser,outfileurl)
    data.login_page('kessya2','apaankek')
    time.sleep(5)
    data.logout_page()


