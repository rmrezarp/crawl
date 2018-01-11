# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 15:36:53 2017

@author: Hp
"""

import sys
import os
import os.path
import re
import pandas as pd
sys.path.append(os.path.abspath("E:/RM/besoklibur/python/crawl/source/social media/"))
from manipulate_data import *
from get_instagram import *
from get_twitter import *

#database = pd.read_csv("E:/RM/besoklibur/database_03122017.csv", sep="`")

# define the function blocks
def zero():
    print("You typed zero.\n")
    filename = input('Enter a file name: ')
    options[filename]()


def crawl():
    keyword = input('Enter a keyword: ')
    outfileurl = "E:/RM/besoklibur/database_03122017_new.csv"  
    database = df_open(outfileurl)
    old = len(database)
    print(old)
    database = instacrawl(database,keyword)
    new = len(database)
    diff = new - old
    if diff > 0:
        print("there are new {} crawled data".format(diff))
        outfileurlsample = "E:/RM/besoklibur/sample.csv"  
    
        database.to_csv(outfileurl, sep='`', encoding='utf-8', index=False)
        database.to_csv(outfileurlsample, sep='`', encoding='utf-8', index=False)
    
    else:
        print("There are no new crawled data")

    print("Done for crawling")
    start_menu()

def crawl_twitter():
    browser = "chrome"
    keyword = input('Enter a keyword: ')   
    outfileurl = "E:/RM/besoklibur/database_twitter.csv"
    database = df_open(outfileurl)
    old = len(database)
    database = tweetcrawl(browser,outfileurl,keyword)
    new = len(database)
    diff = new - old
    if diff > 0:
        print("there are new {} crawled data".format(diff))  
        outfileurlsample = "E:/RM/besoklibur/sample_twitter.csv"  
        database.to_csv(outfileurl, sep='`', encoding='utf-8', index=False)
        database.to_csv(outfileurlsample, sep='`', encoding='utf-8', index=False)
    
    else:
        print("There are no new crawled data")

    print("Done for crawling")
    start_menu()

def twitter():    
    browser = "chrome"
    keyword = input('Enter a keyword: ')
    outfileurl = "E:/RM/besoklibur/database_twitter.csv"
    dataf = myPage(browser,outfileurl)
    if not dataf.dffinal.empty:
        dataf.dfpause = get_last_row(dataf.dffinal,keyword)
        print(dataf.dfpause)
    
    dffinal = dataf.dffinal
    dataf.search('twitter',keyword)
    
#    counter = 0
    while(True):
        print(dataf.flagdone)
        if not dataf.flagdone:
            datafin = dataf.scrape_2()
            dataf.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(10) 
            test = dataf.execute_script("if($(window).scrollTop() + $(window).height() == $(document).height()) {return true;} else {return false;}")
            print("hei {}".format(test))
            if test:
                print("already on bottom page")
                break;
        else:
            print("nothing to crawl")
            break;
#        counter = counter + 1
#        if counter == 2:
            break
    dffinal.userid = pd.to_numeric(dffinal.userid, errors='coerce').fillna(0).astype(np.int64)    
    dffinal.tweetid = pd.to_numeric(dffinal.tweetid, errors='coerce').fillna(0).astype(np.int64)    
    dffinal = dffinal.append(datafin, ignore_index=True)
        
    print('Done crawling')
    outfileurl = "E:/RM/besoklibur/database_twitter.csv"  
    dffinal.to_csv(outfileurl, sep='`', encoding='utf-8', index=False)
    start_menu()


def twitter_x():    
    browser = input(
"""Type browser from list: 
a. Chrome
b. Phantom

Type its name : """)
    keyword = input('Enter a keyword: ')
    outfileurl = "E:/RM/besoklibur/database_twitter.csv"
    dataf = myPage(browser,outfileurl)
    if not dataf.dffinal.empty:
        dataf.dfpause = get_last_row(dataf.dffinal,keyword)
    
    dffinal = dataf.dffinal
    dataf.search('twitter',keyword)
    
#    counter = 0
    while(True):
        print(dataf.flagdone)
        if not dataf.flagdone:
            datafin = dataf.scrape_2()
            dataf.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(10) 
            test = dataf.execute_script("if($(window).scrollTop() + $(window).height() == $(document).height()) {return true;} else {return false;}")
            print("hei {}".format(test))
            if test:
                print("already on bottom page")
                break;
        else:
            print("nothing to crawl")
            break;
#        counter = counter + 1
#        if counter == 2:
            break
    dffinal.userid = pd.to_numeric(dffinal.userid, errors='coerce').fillna(0).astype(np.int64)    
    dffinal.tweetid = pd.to_numeric(dffinal.tweetid, errors='coerce').fillna(0).astype(np.int64)    
    dffinal = dffinal.append(datafin, ignore_index=True)
        
    print('Done crawling')
    outfileurl = "E:/RM/besoklibur/database_twitter.csv"  
    dffinal.to_csv(outfileurl, sep='`', encoding='utf-8', index=False)
    start_menu()

    
    
def even():
    print("n is an even number\n")

def prime():
    print("n is a prime number\n")

def start_menu():
    filename = input('Enter a file name: ')
    options[filename]()

def quits():
    sys.exit()

# map the inputs to the function blocks
options = {'crawl' : crawl,
           'back' : start_menu,
           'quit' : quits,
           'twitter' : crawl_twitter,
           1 : zero,
           2 : even,
           3 : prime,
           5 : prime,
           7 : prime,
}
if __name__ == '__main__':
    start_menu()
