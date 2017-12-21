# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 15:36:53 2017

@author: Hp
"""

import sys
import os
import re
import pandas as pd
sys.path.append(os.path.abspath("E:/RM/besoklibur/python/crawl/source/social media/"))
from manipulate_data import *
from get_instagram_base import *

#database = pd.read_csv("E:/RM/besoklibur/database_03122017.csv", sep="`")
database = pd.read_csv("E:/RM/besoklibur/sample.csv", sep="`")
old = len(database)
database = instacrawl(database,'opentrip')
new = len(database)
diff = new - old
if diff > 0:
    print("there are new {} crawled data".format(diff))
    outfileurl = "E:/RM/besoklibur/sample.csv"  
    database.to_csv(outfileurl, sep='`', encoding='utf-8', index=False)
else:
    print("There are no new crawled data")

#database.iloc[1]['description']
#database.description
#n = database['description']
#n[1]
#first = database[database['postlink']=="BcQlTs5lcTW"]
#type(first)
#print(first['description'])
#first['postid'] #1661916831117599297

#dfs = clean_carriage(database,"description")
#dfs.iloc[0]['description']
#dfs.description

#    x = df['description'].to_string()
#    print(type(x))
#    print(x)
#    re.match(r'#([^\s]+)', x).groups()   
#    return x

#n = database.iloc[2]['description']

database[database.postlink == "Bb_-ZnaHDF_"]
database[database.postlink == "BcQ2ECqgFGa"]


database1 = get_hashtags(database)



database2 = count_profile(database)

#database[database.username == "panorama__trip"]


#database2[database2.users == "panorama__trip"]


def get_profile(df):
    dffinal1 = pd.DataFrame()
    dffinal2 = pd.DataFrame()
    dffinal = pd.DataFrame()
    count = 1
    for row in df.itertuples():
        print("No. of profile : {}".format(count))
        dftemp1 = visit_profile(row.users)
        dftemp2 = fetch_phones(dftemp1.biography[0])
        dffinal1 = append_list_df(dffinal1,dftemp1)
        dffinal2 = append_list_df(dffinal2,dftemp2)
        count+=1
    dffinal = pd.concat([dffinal1, dffinal2], axis=1)
    return dffinal
database2 = pd.read_csv("E:/RM/besoklibur/profilepostcount.csv", sep="`")
dffinal = get_profile(database2)
dffinal = clean_carriage(dffinal,"biography")
outfileurl = "E:/RM/besoklibur/users_with_data.csv"  
dffinal.to_csv(outfileurl, sep='`', encoding='utf-8', index=False)


len(dffinal[dffinal['website'].str.len()!=0])

outfileurl1 = "E:/RM/besoklibur/hashtagscount.csv"  
database1.to_csv(outfileurl1, sep='`', encoding='utf-8', index=False)

outfileurl2 = "E:/RM/besoklibur/profilepostcount.csv"  
database2.to_csv(outfileurl2, sep='`', encoding='utf-8', index=False)


#data user

datauser = pd.read_csv("E:/RM/besoklibur/users.csv", sep="`")


count = 1
dffinal = pd.DataFrame()
y = get_phones(datauser)
for row in datauser.itertuples():
    print("No {} : {}\n".format(count,row.biography))
    count +=1
#    dftemp = get_phones(row.biography)
#    dffinal = dffinal.append(dftemp)
    if count == 30:
        break
