# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:55:21 2017

@author: Hp
"""

import urllib
import sys
import html
import datetime
import json
import os
import pandas as pd
#import psycopg2
import locale
import numpy as np
import time
import requests
from requests.exceptions import ConnectionError
import bs4
sys.path.append(os.path.abspath("E:/RM/besoklibur/python/crawl/source/social media/"))
from manipulate_data import *

locale.setlocale(locale.LC_TIME, "id")

id_fetchpost = '17880160963012870'
id_fetchcomment = '17852405266163336'
id_fetchexplore = '17875800862117404'

#options = {0 : zero,
#           1 : sqr,
#           4 : sqr,
#           9 : sqr,
#           2 : even,
#           3 : prime,
#           5 : prime,
#           7 : prime,
#}


def visit_profile(userid):
    url = 'https://www.instagram.com/' + userid + '/?__a=1'
    dftemp = pd.DataFrame()
    column = ['userid','username','followedby','following','mediacount','biography','url']
    dfrow = make_temp_df(column)
    response = get_json(url,'user')
    if check_json("values",response,""):
        dfrow['userid']      = response['user']['id']
        dfrow['username']    = response['user']['username']
        dfrow['followedby']  = response['user']["followed_by"]['count']
        dfrow['following']   = response['user']["follows"]['count']
        dfrow['mediacount']  = response['user']['media']['count']
        dfrow['biography']   = response['user']['biography']
        dfrow['url']         = response['user']['external_url']
    #dataframe
    dftemp = append_list_df(dftemp, dfrow)
    return dftemp

def visit_explore(tags):
    url = 'https://www.instagram.com/explore/tags/' + tags + '/?__a=1'
    try:
        r = requests.get("http://example.com", timeout=0.001)
    except ConnectionError as e:    # This is the correct syntax
        r = "No response"
    
    response =  urllib.request.urlopen(url).read().decode('utf8') 
    return json.loads(response)    


def count_profile(df):
    count = 0
    users = []

    dffinal = pd.DataFrame()
    for row in df.itertuples():
        users.append(row.username)
#        print(row.description)
#        print(type(row.description))
        count +=1
#        print(len(words))
#        print(words)
#        if len(words) > 0:
#            dffinal = append_list_df(dffinal,words)
#        else:
#            continue
    dffinal = append_list_df(dffinal,users)
    dffinal = dffinal.rename(columns={0: 'users'})
    dffinal = count_tags(dffinal,"users")
    return dffinal

def get_profile(df):
    dffinal1 = pd.DataFrame()
    dffinal2 = pd.DataFrame()
    dffinal = pd.DataFrame()
    count = 1
    for row in df.itertuples():
        print("No. of profile : {}".format(count))
        dftemp1 = visit_profile(row.users)
        dftemp2 = fetch_bio(dftemp1.biography[0])
        dffinal1 = append_list_df(dffinal1,dftemp1)
        dffinal2 = append_list_df(dffinal2,dftemp2)
        count+=1

    dffinal = pd.concat([dffinal1, dffinal2], axis=1)
    return dffinal


def get_explore_post(dfpause,tag,id_fetch,hastoken,countpost):
    hasnext = True
    dffinal = pd.DataFrame()  
    i = 1
    while hasnext:
        print("No of Iteration : {} and has next = {} ".format(i,hasnext) )
        if hastoken:
            url = 'https://www.instagram.com/graphql/query/?query_id=' + id_fetch + '&tag_name=' + tag + '&first=' + str(countpost) + '&after=' + token
        else:
            url = 'https://www.instagram.com/graphql/query/?query_id=' + id_fetch + '&tag_name=' + tag + '&first=' + str(countpost)
        
        response = get_json(url,"data")    
 
        print('done get json')
        print(url)

        dffinal, token, hastoken = iterate_explore_post(response, dffinal,dfpause,tag)
        dffinal['keyword'] = tag
        hasnext = hastoken
        i+=1
        print(token)
        if token == "DONE":
            return dffinal
        else:
            continue
    return dffinal

def get_profile_post(json_prof,id_fetchpost,type_fetch):            
    count_posts = json_prof['user']['media']['count']
    id_user = json_prof['user']['id']
    url = 'https://www.instagram.com/graphql/query/?query_id=' + id_fetchpost + '&id=' + id_user + '&first=' + str(count_posts)
    response = get_json(url)
    return response

def get_data_from_post(link):
    url = "https://www.instagram.com/p/" + link + "/?__a=1"
    column = ['postid','username','userfullname','userid','description','countlikes','countcomments','posttimestamp','postlink']
    dfrow = make_temp_df(column)
    load = get_json(url,"graphql")
    row = load['graphql']['shortcode_media']
#    return row
#    print(row['shortcode'])
    dfrow['username']        = row['owner']['username']
    dfrow['userfullname']       = row['owner']['full_name']
    dfrow['userid']       = row['owner']['id']
    dfrow['description']      = row['edge_media_to_caption']['edges'][0]['node']['text'] if check_json("values",row['edge_media_to_caption']['edges'],"") else np.NaN
    
    dfrow['countlikes']      = row['edge_media_preview_like']['count']
    dfrow['countcomments']   = row['edge_media_to_comment']['count']
    dfrow['posttimestamp']   = time.strftime("%D %H:%M:%S", time.localtime(int(row['taken_at_timestamp'])))
    dfrow['postlink']        = row['shortcode']
    dfrow['postid']          = row['id']
    return dfrow

#n = get_data_from_post("Bb_-ZnaHDF_")
#n1 = get_data_from_post("BcNAnIFHhmE")

#o = n['edge_media_to_caption']['edges'][0]


#check_json("values",n['edge_media_to_caption']['edges'],"node")

def iterate_explore_post(jsonposts, dffinal,dfpause,keyword):
    dftemp = pd.DataFrame()
    rows = jsonposts['data']['hashtag']['edge_hashtag_to_media']
    flagdone = False
    for row in rows['edges']:
        postlink = row['node']['shortcode']
        dfrow =  get_data_from_post(postlink)
        
#        postid = row['node']['id']
#        postlink = row['node']['shortcode']
#        ownerid = row['node']['owner']['id']
#        ownername = get_username_from_post(postlink)
#        posttimestamp = row['node']['taken_at_timestamp']
#        posttimestamp = time.strftime("%D %H:%M:%S", time.localtime(int(posttimestamp)))
#        countlikes = row['node']['edge_liked_by']['count']
#        countcomments = row['node']['edge_media_to_comment']['count']
#
#        dfrow = []
#        dfrow.append({'idowner' : str(ownerid), 'nameowner' : str(ownername),'idpost' : str(postid), 'linkpost': str(postlink), 'timestamp': str(posttimestamp), 'likescount' : str(countlikes), 'commentscount' : str(countcomments) })
        if crawl_stop(dfrow,dfpause,"postid",keyword):
            flagdone = True
            break
        else: 
            dftemp = append_list_df(dftemp, dfrow)
#            print("panjang dftemp = {}".format(len(dftemp)))
            continue

    dffinal = dffinal.append(dftemp)
#    print("panjang df = {}".format(len(dffinal)))
    if not flagdone:
        nexttoken = rows['page_info']['end_cursor']
    else:
        nexttoken = "DONE"
    hasnext = rows['page_info']['has_next_page']
    return dffinal, nexttoken, hasnext
  
def iterate_post(json_posts,command):
    i = 1
    if command == 0:
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

    elif command == 1:
        dflist = []
        for row in json_posts['data']['user']['edge_owner_to_timeline_media']['edges']:
            print('no ke : ', i)
            id_owner = row['node']['owner']['id']
            count_likes = row['node']['edge_liked_by']['count']
            type_post = row['node']['__typename']
            count_comments = row['node']['edge_media_to_comment']['count']
            id_post = row['node']['id']
            code_post = row['node']['shortcode']
            timestamp_post = row['node']['taken_at_timestamp']
            timestamp_post =  time.strftime("%D %H:%M:%S", time.localtime(int(timestamp_post)))
            if len(row['node']['edge_media_to_caption']['edges']) != 0:
                desc_post = row['node']['edge_media_to_caption']['edges'][0]['node']['text']
            else:
                desc_post = np.NaN
            print(desc_post)
            dflist.append({'idowner' : str(id_owner), 'count_comments' : count_comments, 'count_likes' : count_likes, 'idpost' : str(id_post), 'linkpost' : str(code_post), 'timestamp': str(timestamp_post), 'type_post' : str(type_post), 'desc_post' : str(desc_post)   })
            
    #        if i == 1:
    #            df.append({'id_owner': id_owner,'id_post': id_post, 'link_post' : code_post, 'type_post': type_post, 'count_comments': count_comments, 'count_likes': count_likes, 'timestamp_post': timestamp_post, 'desc_post' : desc_post })
    #            break;
    #        print('yes')
    #        i = i + 1
            i = i + 1
        df = pd.DataFrame(dflist)
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
        timestamp_text =  time.strftime("%D %H:%M:%S", time.localtime(int(timestamp_text)))
        idcomment_text = row['node']['id']
        user_text = row['node']['owner']['username'] 
        iduser_text = row['node']['owner']['id']
        df.append({'idowner' : str(id_owner), 'idpost' : str(code_post), 'iduser': str(iduser_text), 'username': str(user_text), 'idcomment' : str(idcomment_text), 'timestamp': str(timestamp_text), 'comment': str(comment_text) })

#        datetime.datetime.fromtimestamp(int(fbdatepost)).strftime('%d-%m-%Y)
    dframe = pd.DataFrame(df)
    return dframe


def instacrawl(dffinal,tag):
    dfpause = get_last_row(dffinal)
#    print(dfpause)
    dftemp = get_explore_post(dfpause,tag,id_fetchexplore,False,10)
    dftemp = dftemp.sort_values(by='posttimestamp', ascending=True)
    dffinal = dffinal.append(dftemp)
    return dffinal

#opentrip5[opentrip5['linkpost']=="BcCgwzTDuqO"]
#
#post = visit_explore('opentrip')
#prof = visit_profile('fwdlife_id')
#posts = get_post(prof,id_fetchpost)
#dffinal = iterate_post(posts,1)
#  
#
#
#    
##    x = x.reset_index(drop=True)
##    Y = get_comments('2138069033','BV9hEqwnpVA',5,id_fetchcomment)
#
#
#

#opentrip = get_explore_post('opentrip',id_fetchexplore,False,10)
#outfileurl = "E:/RM/besoklibur/database_03122017_new.csv"  
#opentrip.to_csv(outfileurl, sep='`', encoding='utf-8', index=False)

#opentrip6 = get_explore_post('opentrip',id_fetchexplore,False,10)
#

