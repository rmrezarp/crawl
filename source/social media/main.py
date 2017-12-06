# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 15:36:53 2017

@author: Hp
"""

import sys
import os
import re
import pandas as pd
sys.path.append(os.path.abspath("E:/RM/besoklibur/python/code/"))
from manipulate_data import *
from get_instagram_base import *

#database = pd.read_csv("E:/RM/besoklibur/database_03122017.csv", sep="`")

# define the function blocks
def zero():
    print("You typed zero.\n")
    filename = input('Enter a file name: ')
    options[filename]()


def crawl():
    keyword = input('Enter a keyword: ')
    
    database = pd.read_csv("E:/RM/besoklibur/database_03122017_new.csv", sep="`")
    old = len(database)
    database = instacrawl(database,keyword)
    new = len(database)
    diff = new - old
    if diff > 0:
        print("there are new {} crawled data".format(diff))
        outfileurl = "E:/RM/besoklibur/database_03122017_new.csv"  
        outfileurlsample = "E:/RM/besoklibur/sample.csv"  
    
        database.to_csv(outfileurl, sep='`', encoding='utf-8', index=False)
        database.to_csv(outfileurlsample, sep='`', encoding='utf-8', index=False)
    
    else:
        print("There are no new crawled data")

    print("Done for crawling")
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
           1 : zero,
           2 : even,
           3 : prime,
           5 : prime,
           7 : prime,
}
if __name__ == '__main__':
    start_menu()
