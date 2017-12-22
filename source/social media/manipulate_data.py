# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 19:13:51 2017

@author: Hp
"""

import sys
import os
import urllib
import html
import datetime
import json
import pandas as pd
import psycopg2
import locale
import numpy as np
import time
import requests
import re

sys.path.append(os.path.abspath("E:/RM/besoklibur/python/crawl/source/social media/"))
from requests.exceptions import ConnectionError
#from get_instagram_base import *

def check_json(case,json,strings):
    if case == "key":
        flag = True if strings in json else False        
    if case == "values":        
        flag = True if json != [] else False
    return flag

def get_json(url,setname):
    tries = 1  
    retries = 1
    jsontries = 1
    httptries = 1

    while True:
        try:
            response = requests.get(url).json()

        except requests.exceptions.Timeout:
            print("timeout, tries : {}".format(retries))
            retries+=1
            continue
        
        except requests.exceptions.RequestException as e:
            print("request exception, tries : {}".format(tries))
            tries+=1
            continue

        
        except requests.exceptions.HTTPError as x:
            if x.status_code == 404:
                print("HTTP Error ({}), tries : {}".format(x,httptries))
            httptries+=1
            continue
        
        except ValueError:
            print("json empty, tries : {}".format(jsontries))
            jsontries+=1
            if jsontries >= 5:
                response = []
                break
            else:
                continue
        
        try:
            if setname == "":
                break
            if response[setname]:
                break

        except KeyError:
            print("json not loaded, tries : {}".format(jsontries))
            jsontries+=1
            continue

        except ValueError:
            print("json empty, tries : {}".format(jsontries))
            jsontries+=1
            continue            

        break
    return response


def clean_carriage(df,colnames):
    df[colnames] = df[colnames].str.replace(r'\r\n', ' ')
    df[colnames] = df[colnames].str.replace(r'\r', ' ')
    df[colnames] = df[colnames].str.replace(r'\n', ' ')
    return df

def make_temp_df(lists):
    dfrow = dict.fromkeys(lists)
    return dfrow

def append_list_df(df, lists):
    df = df.append(lists, ignore_index=True)
    return df

def get_first_row(df):
    return df.iloc[0]

def get_last_row(df):
    return df.iloc[-1]

def crawl_stop(dfcrawl,dfpause,field,keyword):
    
#    print("{} {}".format(dfcrawl[field], type(dfcrawl[field])))
#    print("{} {}".format(dfpause[field], type(dfpause[field])))
#    print("{} & {}".format(dfpause['keyword'],keyword))
#    
    
    if str(dfcrawl[field]) <= str(dfpause[field]) and dfpause['keyword'] == keyword:
#        print('sama')
        return True
    else:
#        print('beda')
        return False


def fetch_hashtags(strings):
   hashtagsObject = re.findall(r'#([^#]+)', strings)
   hashtagsObject = ["#" + hashtags.lower() for hashtags in hashtagsObject]
   hashtagsObject = [re.findall(r'#([^\s]+)', words) for words in hashtagsObject]
#   hashtagsObject = [words.replace(' ', '') for words in hashtagsObject]
   return hashtagsObject

def count_tags(df,colname):
    df = df[colname].value_counts().reset_index().rename(columns={"index": colname, colname: "count"})
    return df

def get_hashtags(df):
    count = 0
    dffinal = pd.DataFrame()
    for row in df.itertuples():
        print(row.postlink)
        print(row.description)
        print(type(row.description))
        if pd.isnull(row.description):
            continue
        words = fetch_hashtags(row.description)
#        print(row.description)
#        print(type(row.description))
        count +=1
        print(len(words))
        print(words)
        if len(words) > 0:
            dffinal = append_list_df(dffinal,words)
        else:
            continue
    dffinal = dffinal.rename(columns={0: 'words'})
    dffinal = count_tags(dffinal,"words")
    return dffinal

def check_none(ob):
    if ob == None:
        return False
    else:
        return True

def fetch_website(strings):
    websiteObject = re.findall(r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))""", strings)
    return websiteObject

def fetch_email(strings):
    emailObject = re.findall(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', strings)
    return emailObject    

def fetch_phone(strings):
    phoneObject = re.findall(r'(8[\d\s\-]{10,25})', strings)
    phoneObject = [words.replace(' ', '') for words in phoneObject]
    phoneObject = [words.replace('\r', '') for words in phoneObject]
    phoneObject = [words.replace('-', '') for words in phoneObject]
    phoneObject = ['0'+ words.replace('\n', '') for words in phoneObject]
    return phoneObject

def fetch_bio(strings):
    column = ['phone','email','website']
    dfrow = make_temp_df(column)
    print(strings)
    if not strings:
        dfrow['phone'] = []
        dfrow['email'] = []
        dfrow['website'] = []        
        return dfrow  
    else:

        
    #    ((https?://|www.)+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)
    #    (www\.)[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)
    #    websiteObject   = re.findall(r"(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/|www.)[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?", strings)
    #    websiteObject   = re.findall(r"(www\.)[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)", strings)    
        phoneObject = fetch_phone(strings)
        emailObject = fetch_email(strings)
        websiteObject  = fetch_website(strings)
        dfrow['phone'] = phoneObject
        dfrow['email'] = emailObject
        dfrow['website'] = websiteObject        
        return dfrow
    
def get_phones(df):
    count = 0
    dffinal = pd.DataFrame()
    for row in df.itertuples():
        if pd.isnull(row.biography):
            continue
        dftemp = fetch_phones(row.biography)
#        print(row.description)
#        print(type(row.description))
        count +=1
        dffinal = append_list_df(dffinal,dftemp)
        if count == 30:
            break
#    dffinal = dffinal.rename(columns={0: 'words'})
#    dffinal = count_tags(dffinal,"words")
    return dffinal
