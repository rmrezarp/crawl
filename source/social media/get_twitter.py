# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 14:51:43 2017

@author: Hp
"""
import re
import os
import pandas as pd
import sys
import dateutil.relativedelta as relativedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
#from Crypto.Cipher import AES
import base64
import time
import datetime
import itertools
from nltk.tokenize import TweetTokenizer
from selenium.webdriver.common.keys import Keys
sys.path.append(os.path.abspath("E:/RM/besoklibur/python/crawl/source/social media/"))
from pathlib import Path
from manipulate_data import *

#https://twitter.com/intent/user?user_id=629100599S

#class DriverCrawl:    
def start_chrome():
    chromedriver = "E:/RM/python/chromedriver_win32/chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    prefs = {"profile.managed_default_content_settings.images":2}
    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized");    
    options.add_experimental_option("prefs",prefs)
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

def init_df(outfile,column):
    if outfile != "" and os.path.exists(outfile):
        dffinal = pd.read_csv(outfile, sep="`")
    else:
        dffinal = pd.DataFrame(columns=column)
    return dffinal

#def extract_hashtag(texts):


#def hashtag_insert(df):
#    column = ['tweetid', 'userid','datetimetweets','tweetdatetext','tweetdatetime','keyword','hashtag']
#    dfrow = make_temp_df(column)
#    for test 
#    dfrow['hashtag'] = [ht for ht in df['hashtag']]
#        
        
        

class myPage(webdriver.Firefox, webdriver.Chrome, webdriver.Ie):
    html = None
    webhtml = None
    keys = None
    tweets = ""
    keyword = ""
    column = ['tweetid', 'userid', 'twitterscreenname', 'twitterfullname', 'tweets', 'datetimetweets', 'tweetdatetext', 'tweetdatetime','keyword','outfilelink','hashtag']
    dftemp = pd.DataFrame()
    first = 1
    last = 1
    flagdone = False
    dfpause = pd.DataFrame()

        
    def get_page(self, url):
        self.get(url)
        return BeautifulSoup(self.page_source,'html.parser')     
    
    def search(self, website, words):
        self.keys = website
        self.keyword = words
        if self.keys.lower() == "twitter":
            words = words.replace('#','%23')
            url = 'https://twitter.com'
            #https://twitter.com/search?f=tweets&vertical=default&q=%22dota%202%22%20OR%20%22dota2%22&src=typd
            urlsearch = url + '/search?f=tweets&vertical=default&q=' + words
            self.html = self.get_page(urlsearch)
            
    def scrape(self):
       
        tweets = self.find_elements_by_xpath('//li[@data-item-type="tweet"]')
#        print("awal first : {}, last : {}".format(self.first,self.last))
        if not self.dfpause.empty:            
            for tweet in tweets:
#                print("iterasi ke {}".format(counter))
                dfrow = self.get_tweets(tweet)
#                print(dfrow['tweetid'][0])
#                print("type = {}, dfpause = {}".format(type(dfpause['tweetid']),dfpause['tweetid']))
#                print("type = {}, dfrow = {}".format(type(dfrow['tweetid']),dfrow['tweetid']))
                if crawl_stop(dfrow.iloc[0],self.dfpause,"tweetid",self.keyword):
                    self.flagdone = True
                    break
                else: 
                    self.dftemp = append_list_df(self.dftemp,dfrow)
                self.first = self.first + 1
                print("data number : {}".format(self.first))
                self.dftemp.userid = pd.to_numeric(self.dftemp.userid, errors='coerce').fillna(0).astype(np.int64)    
                self.dftemp.tweetid = pd.to_numeric(self.dftemp.tweetid, errors='coerce').fillna(0).astype(np.int64)    
                self.dftemp = self.dftemp.sort_values(by='tweetid', ascending=True)
                    

        else:
            for tweet in tweets:
    #            print("iterasi ke {}".format(counter))
                dfrow = self.get_tweets(tweet)
    #            print(dfrow['tweetid'][0])
    #            print("dfpause = {}".format(dfpause['tweetid']))
    #            print("dfrow = {}".format(dfrow['tweetid']))
                self.dftemp = append_list_df(self.dftemp,dfrow)
            
                self.first = self.first + 1
                print("data number : {}".format(self.first))
                self.dftemp.userid = pd.to_numeric(self.dftemp.userid, errors='coerce').fillna(0).astype(np.int64)    
                self.dftemp.tweetid = pd.to_numeric(self.dftemp.tweetid, errors='coerce').fillna(0).astype(np.int64)    
                self.dftemp = self.dftemp.sort_values(by='tweetid', ascending=True)

                
#        print("first : {}, last : {}".format(self.first,self.last))
#        print(self.dftemp)
        return self.dftemp
            
    def get_tweets(self,items):
        dftemp = pd.DataFrame()
        dfrow = make_temp_df(self.column)

        items = items.get_attribute('innerHTML')
        items = BeautifulSoup(items,'html.parser')  
        datauser = items.find("div", {"class": "tweet"})
        tweet = items.find("p", {"class":"TweetTextSize"})
        tweet = BeautifulSoup(str(tweet),'html.parser')
        dfrow['tweetid'] = datauser['data-item-id']
        dfrow['userid'] = int(datauser['data-user-id'])  
        dfrow['twitterscreenname'] = str(datauser['data-screen-name'])
        dfrow['twitterfullname'] = str(datauser['data-name'])
        
        links = []
        for link in tweet.find_all('a'):
            test = link.extract().get_text()
            test = test.replace(u'\xa0', '')
            links.append(test)
        links = ' '.join(links)
        tweets = tweet.get_text()
        dfrow['tweets'] = clean_carriage(tweets)
        hashtagobj = fetch_hashtags(links)
        outlinkobj = fetch_website(links)
        dfrow['outfilelink'] = outlinkobj
        dfrow['hashtag'] = hashtagobj

#        tweet = tweet.get_text(separator=" ")
#        tweet = tweet.replace('@ ',"@")
#        tweet = tweet.replace('# ',"#")
#        tweet = tweet.replace('\n',' ')
#        tweet = ' '.join(tweet.split())
#        dfrow['tweets'] = str(tweet)
        
        datatweet = items.find("span", {"class": "_timestamp"})
        tweetdatepost = datetime.datetime.fromtimestamp(int(datatweet['data-time'])).strftime('%d-%m-%Y %H:%M:%S')
        dfrow['datetimetweets'] = tweetdatepost    
        #print('Tanggal Tweet = \n', datetweets)
        tweetdatetext = datetime.datetime.strptime(tweetdatepost, '%d-%m-%Y %H:%M:%S').strftime('%Y-%m-%d')
        tweetdatetime = datetime.datetime.strptime(tweetdatepost, '%d-%m-%Y %H:%M:%S').strftime('%H:%M:%S')
        dfrow['tweetdatetext'] = tweetdatetext
        dfrow['tweetdatetime'] = tweetdatetime
        dfrow['keyword'] = self.keyword
        dftemp = append_list_df(dftemp, dfrow)
        
        return dftemp
    
    def login_account(self,username, password):
        #looking for login box
        
        #twitter         
#        if self.keys.lower() == "twitter":
            usern = self.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[1]/input')
            usern.send_keys(username)
        
            passw = self.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[2]/input')
            passw.send_keys(password)
    
            login = self.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/div[2]/button')
            login.click()
        
    #        usern = self.driver.find_element_by_xpath('//input[@id="session_key-login"]')
    #        usern.send_keys(username)
    
    
    
    #        passw = self.driver.find_element_by_xpath('//input[@id="session_password-login"]')
    #        passw.send_keys(password)
    
    def delete_element(self):
        self.execute_script("""
        var element = document.querySelector(".classname");
        if (element)
            element.parentNode.removeChild(element);
        """)
    
    
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
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-notifications")
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")            
            options.add_argument("--start-maximized");
            options.add_experimental_option("prefs",prefs)
            self.dffinal = init_df(outfileurl,self.column)

            webdriver.Chrome.__init__(self,executable_path=chromedriver, chrome_options=options)
        elif browser.lower() == "phantom":
            print('phantom selected')
            phantomjs_path = "C:/PhantomJS/bin/phantomjs.exe"
            desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
            desired_capabilities['phantomjs.page.customHeaders.User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) ' \
                                                                          'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                                                          'Chrome/39.0.2171.95 Safari/537.36'
            self.dffinal = init_df(outfileurl,self.column)        
            webdriver.PhantomJS.__init__(self,executable_path=phantomjs_path,desired_capabilities=desired_capabilities, service_args=['--ignore-ssl-errors=true'], service_log_path=os.path.devnull)
           
        else:
            webdriver.Firefox.__init__(self)
            print('firefox selected')
   

def tweetcrawl(browser,outfileurl,tag):
    dataf = myPage(browser,outfileurl)
    if not dataf.dffinal.empty:
        dataf.dfpause = get_last_row(dataf.dffinal,tag)    
    
    dffinal = dataf.dffinal
    dataf.search('twitter',tag)
    
    while(True):
#        print(dataf.flagdone)
        if not dataf.flagdone:
            datafin = dataf.scrape()

            dataf.execute_script("window.scrollTo(0,0);")
            dataf.execute_script("""
                                    var list = document.getElementById("stream-items-id");

                                    while (list.firstChild) {
                                        //The list is LIVE so it will re-index each call
                                        list.removeChild(list.firstChild);
                                    }                     
                                 """
                                 )
            dataf.execute_script("window.scrollTo(0,document.body.scrollHeight/2);")
            dataf.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(5)
            try:
                WebDriverWait(dataf, 100).until(EC.presence_of_element_located((By.XPATH, '//li[@data-item-type="tweet"]')))
            except:
                print('Nothing to crawl')
                break
        else:
            print("Done from last crawling")
            break;
    #        counter = counter + 1
    #        if counter == 2:
    dffinal.userid = pd.to_numeric(dffinal.userid, errors='coerce').fillna(0).astype(np.int64)    
    dffinal.tweetid = pd.to_numeric(dffinal.tweetid, errors='coerce').fillna(0).astype(np.int64)    
    dffinal = dffinal.append(datafin, ignore_index=True)
    
    return dffinal

    
#def tweetcrawl(dffinal,tag):
#    dfpause = get_first_row(dffinal)
#    dftemp = get_explore_post(dfpause,tag,id_fetchexplore,False,10)
#    dffinal = dffinal.append(dftemp)
#    dffinal = dffinal.sort_values(by='posttimestamp', ascending=False)
#    return dffinal
#  

     



#dffinal2.iloc[2]
#na = dffinal2['tweets'][2]
#ho = fetch_website(dffinal2['tweets'][2])
#lista = TweetTokenizer().tokenize(dffinal2['tweets'][2])
#
#lista = TweetTokenizer().tokenize(self.dftemp['tweet'])
#
#
#
#
#
#
##class HTMLWeb(object):
##    
##    
##    def __init__(self,driver):
##    
##    def visit_link(self,link):
##        self.get(link)
##
##    def login_account(self, username, password):
##        #looking for login box
##        
##        #twitter 
##        usern = self.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[1]/input')
##        usern.send_keys(username)
##
##        
###        usern = self.driver.find_element_by_xpath('//input[@id="session_key-login"]')
###        usern.send_keys(username)
##    
##        passw = self.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[2]/input')
##        passw.send_keys(password)
##
##
###        passw = self.driver.find_element_by_xpath('//input[@id="session_password-login"]')
###        passw.send_keys(password)
##
##
##
##        login = self.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/div[2]/button')
##        login.click()
##
###        login = self.driver.find_element_by_xpath('//input[@id="btn-primary"]')
###        login.click()
#
#driver = select_driver('chrome')
#driver = start_chrome()
#driver.session_id
#driver.get('https://google.com')
#x = driver.page_source
#
#chromes = HTMLWeb('chrome')
#chromes.visit_link
#chromes.visit_link("https://twitter.com/login")
#chromes.page_source
#chromes.session_id
#driver.get("https://twitter.com/login")
#chromes.visit_link("https://google.com")
#x = driver.start()    
#x.get('http://python.org')
#
#
#html = x.page_source
#
#y = HTMLWeb(x,"https://twitter.com/login")
#x.p
#y = startchrome()
#driver = start_phantomjs()
