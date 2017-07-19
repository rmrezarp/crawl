# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 13:15:17 2017

@author: Hp
"""

import urllib
import html
import datetime
import facebook
import json
import pandas as pd
import psycopg2
import locale
import numpy as np
from bs4 import BeautifulSoup
locale.setlocale(locale.LC_TIME, "id")

id_fetchpost = '17880160963012870'
id_fetchcomment = '17852405266163336'

def visit_profile(userid):
    url = 'https://www.youtube.com/user/' + userid
    response =  urllib.request.urlopen(url).read().decode('utf8') 
    return json.loads(response)



def get_post(json_prof,id_fetchpost):    
    count_posts = json_prof['user']['media']['count']
    id_user = json_prof['user']['id']

    url = 'https://www.instagram.com/graphql/query/?query_id=' + id_fetchpost + '&id=' + id_user + '&first=' + str(count_posts)
    response =  urllib.request.urlopen(url).read().decode('utf8') 
    json_posts = json.loads(response)
    return json_posts



def iterate_post(json_posts):
    i = 1
    df = pd.DataFrame()
    for row in json_posts['data']['user']['edge_owner_to_timeline_media']['edges']:
        print('no ke : ', i)
        id_owner = row['node']['owner']['id']
        count_likes = row['node']['edge_liked_by']['count']
        type_post = row['node']['__typename']
        count_comments = row['node']['edge_media_to_comment']['count']
        id_post = row['node']['id']
        code_post = row['node']['shortcode']
        timestamp_post = row['node']['taken_at_timestamp']
        if len(row['node']['edge_media_to_caption']['edges']) != 0:
            desc_post = row['node']['edge_media_to_caption']['edges'][0]['node']['text']
        else:
            desc_post = np.NaN
        print(desc_post)
        
        df_comments = get_comments(id_owner, code_post, count_comments, id_fetchcomment)
        df = df.append(df_comments)
#        if i == 1:
#            df.append({'id_owner': id_owner,'id_post': id_post, 'link_post' : code_post, 'type_post': type_post, 'count_comments': count_comments, 'count_likes': count_likes, 'timestamp_post': timestamp_post, 'desc_post' : desc_post })
#            break;
#        print('yes')
#        i = i + 1
        i = i + 1
    df = df.reset_index(drop=True)
    return df

def get_comments(id_owner, code_post,count_comments,id_fetchcomment):
    print(count_comments)
    url = 'https://www.instagram.com/graphql/query/?query_id=' + id_fetchcomment + '&shortcode=' + code_post + '&first=' + str(count_comments)
    response =  urllib.request.urlopen(url).read().decode('utf8') 
    df = []
    json_comments = json.loads(response)
    for row in json_comments['data']['shortcode_media']['edge_media_to_comment']['edges']:
        comment_text = row['node']['text']
        timestamp_text = row['node']['created_at']
        idcomment_text = row['node']['id']
        user_text = row['node']['owner']['username'] 
        iduser_text = row['node']['owner']['id']
        df.append({'idowner' : str(id_owner), 'idpost' : str(code_post), 'iduser': str(iduser_text), 'username': str(user_text), 'idcomment' : str(idcomment_text), 'timestamp': str(timestamp_text), 'comment': str(comment_text) })

#        datetime.datetime.fromtimestamp(int(fbdatepost)).strftime('%d-%m-%Y)
    dframe = pd.DataFrame(df)
    return dframe

def main_crawl():
    prof = visit_profile('FWDLifeIndonesia')
    posts = get_post(prof,id_fetchpost)
    dffinal = iterate_post(posts)
    outfileurl = "E:\IDXP\FWD\instagram_delim.csv"    

    dffinal.to_csv(outfileurl, sep='`', encoding='utf-8', index=False)
    df2 = pd.read_csv("E:\IDXP\FWD\instagram.csv", sep="`")
    
#    x = x.reset_index(drop=True)
#    Y = get_comments('2138069033','BV9hEqwnpVA',5,id_fetchcomment)