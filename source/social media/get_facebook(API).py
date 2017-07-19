# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 14:31:28 2017

@author: Hp
"""

import urllib
import datetime
import facebook
import json
import pandas as pd
import psycopg2
import locale
import html
import requests
import time
from bs4 import BeautifulSoup
locale.setlocale(locale.LC_TIME, "id")

APP_ID = "181560758911664"
APP_SECRET = "5b0874a270777180de4089788624ca97"
graph = facebook.GraphAPI("EAAClIOiKQrABAMZChRbfkAhsXcZA8qkCdpTPkhaWV9B6NFPcmYxlCDazP4MFXoBuxXUIUnWE8gsI3sz5xQopuPZBhTCbPmQ6b7tv0ZBGV3jShCQbgpbFVrQIzaaZCHFgmrQYaCoseq18MtsjxrqMs")

#https://graph.facebook.com/search?q=fwdlife&type=page&limit=100&access_token=181560758911664|5b0874a270777180de4089788624ca97
pageid = "1383470468578286"

#get_all = 1383470468578286/tagged?fields=picture,likes,message,created_time,link,target,name,id,feed_targeting,object_id,parent_id,from,description,type,comments{message,id,from,comments{message,id,from}}&pretty=0&limit=100&before=Cg8Ic3RvcnlfaWQPEzg3MDM1MzYyNjMxNDE0MDo1OjAPB3Bvc3RfaWQIAAMXlP65tZAwPCG93bmVyX2lkCAAAzKSTRZAuZBDwR0aW1lBlNzM2QB"
#def get_shares(postid):
#    fburl = "http://www.facebook.com/ajax/shares/view/?target_fbid=10154612868272801&__a=1"

def get_review(pageid):
    fburl = 'https://www.facebook.com/ajax/pages/review/spotlight_reviews_tab_pager/?fetch_on_scroll=1&max_fetch_count=1000&page_id=' + pageid +'&sort_order=most_helpful&dpr=1&__user=0&__a=1&__af=iw&__req=1g&__be=-1&__pc=PHASED%3ADEFAULT&__rev=2923756'

    jsons = (requests.get(fburl).text).replace("for (;;);",'')
    jsons = json.loads(jsons) 
    
    page = jsons['domops'][0][3]['__html']
    page = html.unescape(page)
    posts2 = jsons['jsmods']['require']
    soup = BeautifulSoup(page, 'html.parser')
    posts = soup.findAll("div",{"class" : "_4-u2"})
    
    df = []
    print(len(posts))
    for post in posts:
        post_id = post.find("input", {"name" : "ft_ent_identifier"})
        post_id = post_id['value']
        
        review_star = str(post.find("i", {"class" : "_51mq"}).text).split(' ')[0]
        date = post.find("abbr", {"class" : "_5ptz"})['data-utime']
        date =  time.strftime("%d-%m-%Y", time.localtime(int(date)))
        message = post.find("div", {"class" : "_5pbx"})
        if message != None:
            message = str(post.find("div", {"class" : "_5pbx"}).text)
        else:
            message = ""

        

        df.append({'post_id' : post_id, 'review_star' : review_star, 'date' : date, 'message' : message})

    dffinal1 = pd.DataFrame(df)    
    
    df = []
    for post in posts2:
        if post[0] == "UFIController":
            data = post[3][2]['feedbacktarget']
            user_name = data['actorname']
            user_id = data['actorid']
            count_comment = data['commentcount']
            post_id = data['entidentifier']
            count_like = data['likecount']
            df.append({'post_id' : post_id, 'user_name' : user_name, 'user_id' : user_id, 'count_comment' : count_comment , "count_like" : count_like})
    
    dffinal2 = pd.DataFrame(df)        
    dffinal = pd.merge(dffinal1, dffinal2, left_on='post_id', right_on='post_id')    

        
    return dffinal



def get_visitor_post(pageid):
    fburl = "https://graph.facebook.com/" + pageid + "/feed?fields=shares,picture,comments.limit(0).summary(1),likes.limit(0).summary(1),message,created_time,link,target,name,id,feed_targeting,object_id,parent_id,from,description,type&limit=100&access_token=181560758911664|5b0874a270777180de4089788624ca97"
    fburln = fburl    
    df1 = []
    while True:
        getfb =  urllib.request.urlopen(fburln).read().decode('utf8')
        json_post = json.loads(getfb)
        i = 1
        for data in json_post['data']:
           if data.get('target'):           
               print(i)
               i = i + 1
               targetid = data['target']['id']
               targetname = data['target']['name']
               postid = data['id']
               if data.get('link'):
                   postlink = data['link']        
               else:
                   postlink = ""  
               posttype = data['type'] 
               if data.get('name'):
                   postname = data['name']        
               else:
                   postname = ""           
                   
               if data.get('comments'):
                   count_comments = data['comments']['summary']['total_count']       
               else:
                   count_comments = 0      
                   
               if data.get('likes'):
                   count_likes = data['likes']['summary']['total_count']      
               else:
                   count_likes = 0  
               
               if data.get('shares'):
                   count_shares = data['shares']['count']       
               else:
                   count_shares = 0  

                
               userid = data['from']['id']
               username = data['from']['name']
               if data.get('message'):
                   message = data['message']        
                   message = str(message).replace('\n','')
               else:
                   message = ""
               date = data['created_time']
               date = date.split('T')
               date = date[0]
               date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')
               df1.append({'target_id' : targetid, 'target_name' : targetname, 'post_id' : postid, 'post_link' : postlink, 'post_type' : posttype, 'post_name' : postname, 'user_id' : userid, 'user_name' : username, 'message' : message, 'date' : date, 'count_likes' : count_likes, 'count_shares' : count_shares, 'count_comments' : count_comments})

        if json_post.get('paging'):
            fburln = str(json_post['paging']['next'])
        else:
            break
    dffinal = pd.DataFrame(df1)
    return dffinal

def get_tagged_post(pageid):
    #get tagged post
    fburl1 = "https://graph.facebook.com/" + pageid + "/tagged?fields=shares,from,comments.limit(0).summary(1),likes.limit(0).summary(1),message,tagged_time,id,link,type&limit=100&access_token=181560758911664|5b0874a270777180de4089788624ca97"
    fburltag = fburl1

    print('masuk tagged')
    df2 = []
    while True:
        getfb =  urllib.request.urlopen(fburltag).read().decode('utf8')
        json_post = json.loads(getfb)
        i = 1
        for data in json_post['data']:
            postid = data['id']
            print(i)
            i = i + 1
            if data.get('message'):
                message = data['message']
                message = str(message).replace('\n','')
            else:
                message = ""
            

            if data.get('likes'):
                count_likes = data['likes']['summary']['total_count']      
            else:
                count_likes = 0  

            if data.get('shares'):
                count_shares = data['shares']['count']       
            else:
                count_shares = 0  

            if data.get('comments'):
                count_comments = data['comments']['summary']['total_count']       
            else:
                count_comments = 0    

            if data.get('link'):
                postlink = data['link']        
            else:
                postlink = ""  
            posttype = data['type'] 
            userid = data['from']['id']
            username = data['from']['name']
            date = data['tagged_time']
            date = date.split('T')
            date = date[0]
            date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')
            df2.append({'post_id' : postid, 'post_link' : postlink , 'post_type' : posttype , 'user_id' : userid, 'user_name' : username, 'message' : message, 'date' : date, 'count_likes' : count_likes, 'count_shares' : count_shares, 'count_comments' : count_comments})
        if json_post.get('paging'):
            fburltag = str(json_post['paging']['next'])
        else:
            break
    dffinal = pd.DataFrame(df2)
    return dffinal




def get_page_post(pageid):
    fburl = "https://graph.facebook.com/" + pageid + "/feed?fields=shares,picture,comments.limit(0).summary(1),likes.limit(0).summary(1),message,created_time,link,target,name,id,feed_targeting,object_id,parent_id,from,description,type&limit=100&access_token=181560758911664|5b0874a270777180de4089788624ca97"
    fburln = fburl    
    df = []
    while True:
        getfb =  urllib.request.urlopen(fburln).read().decode('utf8')
        json_post = json.loads(getfb)
        i = 1
        for data in json_post['data']:
#get post by page
            if not data.get('target'):
                print(i)
                i = i + 1
                postid = data['id']

                if data.get('likes'):
                    count_likes = data['likes']['summary']['total_count']      
                else:
                    count_likes = 0  

                if data.get('comments'):
                    count_comments = data['comments']['summary']['total_count']       
                else:
                    count_comments = 0  
                
                if data.get('shares'):
                    count_shares = data['shares']['count']       
                else:
                    count_shares = 0  
                
                if data.get('link'):
                    postlink = data['link']        
                else:
                    postlink = ""  
                posttype = data['type'] 
                if data.get('name'):
                    postname = data['name']        
                else:
                    postname = ""                 
                userid = data['from']['id']
                username = data['from']['name']
                if data.get('message'):
                    message = data['message']        
                    message = str(message).replace('\n','')

                else:
                    message = ""
                date = data['created_time']
                date = date.split('T')
                date = date[0]
                date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')
                df.append({'post_id' : postid, 'post_link' : postlink, 'post_type' : posttype, 'post_name' : postname, 'user_id' : userid, 'user_name' : username, 'message' : message, 'date' : date, 'count_likes' : count_likes, 'count_shares' : count_shares, 'count_comments' : count_comments})

                
        if json_post.get('paging'):
            fburln = str(json_post['paging']['next'])
        else:
            break
    dffinal = pd.DataFrame(df)
    return dffinal

def get_replies(commentid):
    fburl = "https://graph.facebook.com/" + commentid +  "/comments?limit=10000&access_token=181560758911664|5b0874a270777180de4089788624ca97"
    fburln = fburl
    df = []
    post_id = str(commentid).split('_')[0]
    while True:
        getfb =  urllib.request.urlopen(fburln, timeout=2000).read().decode('utf8')
        json_replies = json.loads(getfb)
        for data in json_replies['data']:
            
            repliesid = data['id']
            userid = data['from']['id']
            username = data['from']['name']
            if data.get('message'):
                replies = data['message']        
                replies = str(replies).replace('\n','')

            else:
                replies = ""

            date = data['created_time']
            date = date.split('T')
            date = date[0]
            date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')
            df.append({'post_id' : post_id, 'comment_id' : commentid, 'repliesid' : repliesid, 'userid' : userid, 'username' : username, 'replies' : replies, 'date' : date})
        
        if json_replies.get('paging'):
            fburln = fburl + "&after=" + str(json_replies['paging']['cursors']['after'])
        else:
            break
    dffinal = pd.DataFrame(df)
    dffinal['count_replies'] = dffinal.groupby(['post_id'])['post_id'].transform('count')
    return dffinal
        
    

def get_comments(postid):
    fburl = "https://graph.facebook.com/" + postid +  "/comments?limit=10000&access_token=181560758911664|5b0874a270777180de4089788624ca97"
    fburln = fburl
    df = []
    while True:
        getfb =  urllib.request.urlopen(fburln, timeout=2000).read().decode('utf8')
        json_comments = json.loads(getfb)
        for data in json_comments['data']:
            commentid = data['id']
            userid = data['from']['id']
            username = data['from']['name']
            if data.get('message'):
                comment = data['message']        
                comment = str(comment).replace('\n','')

            else:
                comment = ""

            date = data['created_time']
            date = date.split('T')
            date = date[0]
            date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')
            df.append({'post_id' : postid, 'comment_id' : commentid, 'userid' : userid, 'username' : username, 'comment' : comment, 'date' : date})
        if json_comments.get('paging'):
            fburln = fburl + "&after=" + str(json_comments['paging']['cursors']['after'])
        else:
            break
    dffinal = pd.DataFrame(df)
    dffinal['count_comments'] = dffinal.groupby(['post_id'])['post_id'].transform('count')

    return dffinal

def get_likes(postid, types):

    fburl = "https://graph.facebook.com/" + postid +  "/reactions?limit=10000&access_token=181560758911664|5b0874a270777180de4089788624ca97"
    fburln = fburl

    df = []
    
    if types == 1:
        getfb =  urllib.request.urlopen(fburl, timeout=2000).read().decode('utf8')
        json_likes = json.loads(getfb)
        return len(json_likes['data'])
        
    elif types == 2:
        O = 1
        while True:
            print('masuk :', O)
            getfb =  urllib.request.urlopen(fburln, timeout=2000).read().decode('utf8')
            json_likes = json.loads(getfb)
            print(len(json_likes['data']))
            n = 1
            for data in json_likes['data']:
                n = n + 1
                userid = data['id']
                username = data['name']
                typelike = data['type']
                df.append({'post_id' : postid, 'userid' : userid, 'username' : username, 'typelike' : typelike})
            if json_likes.get('paging'):
                print('ada lagi')
                fburln = fburl + "&after=" + str(json_likes['paging']['cursors']['after'])
                print(fburln)
                O = O + 1
            else:
                break
        dffinal = pd.DataFrame(df)
        dffinal['count_likes'] = dffinal.groupby(['post_id'])['post_id'].transform('count')
        return dffinal



def iterate_post(postid_list):
    i = 1
    df_comments = pd.DataFrame()
    df_likes = pd.DataFrame()
    df_replies = pd.DataFrame()

    for posts in postid_list:
        print('comment :',i)
        i = i + 1
        df1 = get_comments(str(posts))
#        df2 = get_likes(str(posts), 2)
        df_comments = df_comments.append(df1)
#        df_likes = df_likes.append(df2)
    
    i = 1
    for posts in df_comments['comment_id']:
        print('replies :',i)
        i = i + 1
        df = get_replies(str(posts))
        df_replies = df_replies.append(df)
    return df_comments, df_replies


#############

df_page_post = get_page_post(pageid)
df_visitor_post = get_visitor_post(pageid)
df_tagged_post = get_tagged_post(pageid)
df_review_post = get_review(pageid)


df_page_post.to_csv('E:\IDXP\FWD\Facebook_FWD_page_post.csv', sep='`', encoding='utf-8', index=False)
df_visitor_post.to_csv('E:\IDXP\FWD\Facebook_FWD_visitor_post.csv', sep='`', encoding='utf-8', index=False)
df_tagged_post.to_csv('E:\IDXP\FWD\Facebook_FWD_tagged_post.csv', sep='`', encoding='utf-8', index=False)
df_review_post.to_csv('E:\IDXP\FWD\Facebook_FWD_review_post.csv', sep='`', encoding='utf-8', index=False)

df_tagged_post_comments, df_tagged_post_replies = iterate_post(df_tagged_post['post_id'])
df_tagged_post_comments.to_csv('E:\IDXP\FWD\Facebook_FWD_tagged_post(comments).csv', sep='`', encoding='utf-8', index=False)
#df_tagged_post_likes.to_csv('E:\IDXP\FWD\Facebook_FWD_tagged_post(likes).csv', sep='`', encoding='utf-8', index=False)
df_tagged_post_replies.to_csv('E:\IDXP\FWD\Facebook_FWD_tagged_post(replies).csv', sep='`', encoding='utf-8', index=False)

df_page_post_comments, df_page_post_replies = iterate_post(df_page_post['post_id'])
df_page_post_comments.to_csv('E:\IDXP\FWD\Facebook_FWD_page_post(comments).csv', sep='`', encoding='utf-8', index=False)
#df_page_post_likes.to_csv('E:\IDXP\FWD\Facebook_FWD_page_post(likes).csv', sep='`', encoding='utf-8', index=False)
df_page_post_replies.to_csv('E:\IDXP\FWD\Facebook_FWD_page_post(replies).csv', sep='`', encoding='utf-8', index=False)


df_visitor_post_comments, df_visitor_post_replies = iterate_post(df_visitor_post['post_id'])
df_visitor_post_comments.to_csv('E:\IDXP\FWD\Facebook_FWD_visitor_post(comments).csv', sep='`', encoding='utf-8', index=False)
#df_visitor_post_likes.to_csv('E:\IDXP\FWD\Facebook_FWD_visitor_post(likes).csv', sep='`', encoding='utf-8', index=False)
df_visitor_post_replies.to_csv('E:\IDXP\FWD\Facebook_FWD_visitor_post(replies).csv', sep='`', encoding='utf-8', index=False)


df = pd.read_csv('E:\IDXP\FWD\Facebook_FWD_visitor_post.csv', sep='`')


import codecs
df2s = codecs.open('E:\\IDXP\\FWD\\page_post(comments).csv', "r",encoding='utf-8', errors='ignore')

df2 = pd.read_csv('E:\\IDXP\\FWD\\page_post(comments).csv', sep='`')
df1['count_comments'] = df1.groupby(['post_id'])['post_id'].transform('count')
df1s = df1.groupby('post_id').size()
df1s['post_id'] = df1s.index
#############
