# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 09:55:39 2017

@author: Hp
"""
import re
import os
import pandas as pd
import dateutil.relativedelta as relativedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from Crypto.Cipher import AES
import base64
import time
import datetime
import itertools
from selenium.webdriver.common.keys import Keys


def init_df():
    mylisttemp = list(range(0,1))
    dffinal_temp = pd.DataFrame(index=mylisttemp)
    dffinal_temp = dffinal_temp.astype('object')
    return dffinal_temp    

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def start_chrome():
    chromedriver = "C:/Users/Hp/Downloads/chromedriver_win32/chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    options = Options()
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(chromedriver, chrome_options=options)
    return driver

def start_phantomjs():
    phantomjs_path = "C:/PhantomJS/bin/phantomjs.exe"
    desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
    desired_capabilities['phantomjs.page.customHeaders.User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) ' \
                                                                  'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                                                  'Chrome/39.0.2171.95 Safari/537.36'
    
    driver = webdriver.PhantomJS(executable_path=phantomjs_path,desired_capabilities=desired_capabilities, service_args=['--ignore-ssl-errors=true'], service_log_path=os.path.devnull)
    return driver
    
def encrypt(password):
    msg_text = password.rjust(32)
    secret_key = '1234567890123456' # create new & store somewhere safe
    cipher = AES.new(secret_key,AES.MODE_ECB) # never use ECB in strong systems obviously
    encoded = base64.b64encode(cipher.encrypt(msg_text))
    return encoded
    
def decrypt_es(encoded):
    secret_key = '1234567890123456' # create new & store somewhere safe
    cipher = AES.new(secret_key,AES.MODE_ECB) # never use ECB in strong systems obviously
    encoded = encoded.encode("utf-8")
    decoded = cipher.decrypt(base64.b64decode(encoded))
    decoded = decoded.decode("utf-8")
    decoded = decoded.strip()
    return decoded

def scroll_down(driver, no):
    if no > 0:
        lastHeight = driver.execute_script("return document.body.scrollHeight")
        while no > 0:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            newHeight = driver.execute_script("return document.body.scrollHeight")
            if newHeight == lastHeight:
                break
            lastHeight = newHeight
            no = no - 1
        return 0        
#        lastHeight = driver.execute_script("return document.body.scrollHeight")
#        while True:
#            driver.execute_script("window.scrollTo(0, (document.body.scrollHeight));")
#            time.sleep(5)

#            newHeight = driver.execute_script("return document.body.scrollHeight")
#            if newHeight == lastHeight:
#                break
#            lastHeight = newHeight

# ---for linkedin
    elif no == -1:
        bd = driver.find_element_by_tag_name("body")
        initialHeight = bd.size['height']
        currentHeight = 0;
#        print("0",initialHeight)
        while(True):
            initialHeight = bd.size['height']
#            print("na",initialHeight)
#  
#            print("ni",currentHeight)
#               
            time.sleep(0.5)
            driver.execute_script("scrollBy(0, "+ '500' +");")
#
#                System.out.println("Sleeping... wleepy");
#                Thread.sleep(2000);
#
            currentHeight = currentHeight + 500
#            print("na",currentHeight)
            if currentHeight >= initialHeight:
                break
#            currentHeight = driver.execute_script("return document.body.scrollTop;");

#                currentHeight = driver.find_element_by_tag_name("body").getSize().getHeight();
#}
# ---end for linkedin

# ---for twitter
    else:
        lastHeight = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, (document.body.scrollHeight));")
            time.sleep(2)
            newHeight = driver.execute_script("return document.body.scrollHeight")
            if newHeight == lastHeight:
                break
            lastHeight = newHeight        

        return 0
# ---end for twitter
def visit_link(driver,href):
    driver.get(href)
    scroll_down(driver,-1)
    html = driver.page_source
    
    return html

def check_exist(html, elem, attr, value):
    found = html.find(elem, { attr : value })
    if found != None:
        return True
    else:
        return False

def check_null_get_info(var,f,l):
#    print(var)
    if (var is not None) and (var != 'None') and (var != '') and (var !='nan'):
        var = var.text
        var = var.split()
        var = var[f:l]
        var = ' '.join(var)
        return var
    else:
        var = 'nan'
        return var

def clean_name(name):
    name = name.replace('.',' ')
    word = name.split(' ')
    y = [c for c in word if len(c) > 2] 
    y = ' '.join(y)
    y = y.lower()
    regex = re.compile(".*?\((.*?)\)")
    result = re.findall(regex, y)
    for resultrow in result:
        print('asas',resultrow)
    
        y = y.replace('('+resultrow+')', '')
    return y

def clean_str(df, name_field):
 #   df[name_field] = df[name_field].replace({".": ""}, regex=True)
    df[name_field] = df[name_field].str.replace("."," ")
    df[name_field] = df[name_field].str.replace("  ","")

    return df



def change_month_ind(word):
    word = word.replace('Januari','January')
    word = word.replace('Februari','February')
    word = word.replace('Maret','March')
    word = word.replace('Mei','May ')
    word = word.replace('Juni','June')
    word = word.replace('Juli','July')
    word = word.replace('Agustus','August')
    word = word.replace('Oktober','October')
    word = word.replace('Desember','December')
    word = word.replace('Pada','')    
    return word
    
def check_captcha_fb(driver, html):
    if check_exist(html, 'div','id','captcha'):
        print('masuk captcha')
        driver.execute_script("window.stop();")         
        return True
    else:
        return False

#        driver.find_element_by_tag_name("body").send_keys("Keys.ESCAPE")
#        driver.find_element_by_tag_name("body").send_keys("Keys.ESCAPE")
#
##img class img
#        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
#        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
#
#        driver.execute_script("window.stop()")
def check_captcha_li(driver, html):
    if check_exist(html, 'div', 'class', 'search-results-page'):
        print('hahahahah')
#        driver.findElement(By.linkText("Sign in")).click();                
#        login = driver.find_element_by_class_name("sign-in-link")
#        time.sleep(5)
#        login.click()    
        return True
    else:
        print('hohohoo')
        return False
    
