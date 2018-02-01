# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 10:28:29 2017

@author: Hp
"""
import pandas as pd
import datetime
import matplotlib
import ggplot
from plotly.offline import download_plotlyjs, init_notebook_mode, plot
import plotly.graph_objs as go
from manipulate_data import *
#from ggplot import *

#from ggplot import *

#install outdside repositories
#conda install -c conda-forge ggplot

def clean_carriage(df,colnames):
    
    df[colnames] = df[colnames].replace(to_replace='\r\n', value=' ', regex=True)
    df[colnames] = df[colnames].replace(to_replace='\r', value=' ', regex=True)
    df[colnames] = df[colnames].replace(to_replace='\n', value=' ', regex=True)
    df[colnames] = df[colnames].replace(to_replace='`', value=' ', regex=True)
    df[colnames] = df[colnames].replace(to_replace='\s+', value=' ', regex=True)
    
    return df



#make table summary :

dayslist = {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}

outfileurl = "E:/RM/besoklibur/database_twitter.csv"  
outfileurl = "E:/RM/besoklibur/database_03122017_new.csv"
database1 = pd.read_csv(outfileurl, sep="`")

database = clean_carriage(database, 'description')
outfileurl = "E:/RM/besoklibur/database_03122017_new.csv" 
database1 = pd.read_csv(outfileurl, sep="`")
database.to_csv(outfileurl, sep='`', encoding='utf-8', index=False)
database['posttimestamp'] = pd.to_datetime(database['posttimestamp'])

database['hour'] = database['posttimestamp'].dt.hour
database['minute'] = database['posttimestamp'].dt.minute
database['second'] = database['posttimestamp'].dt.second
database['days'] = database['posttimestamp'].dt.dayofweek
database['days'].replace(dayslist, inplace=True)

database_promo = database[database['keyword'] == 'promo']
database_opentrip = database[database['keyword'] == 'opentrip']

time = database.groupby('hour').agg({'userid':'count', 'countcomments': 'sum', 'countlikes':'sum'}).rename(columns={'userid':'count','countcomments': 'sumcomments', 'countlikes':'sumlikes'}).reset_index()
day = database.groupby('days').agg({'userid':'count', 'countcomments': 'sum', 'countlikes':'sum'}).rename(columns={'userid':'count','countcomments': 'sumcomments', 'countlikes':'sumlikes'}).reset_index()

time_promo = database_promo.groupby('hour').agg({'userid':'count', 'countcomments': 'sum', 'countlikes':'sum'}).rename(columns={'userid':'count','countcomments': 'sumcomments', 'countlikes':'sumlikes'}).reset_index()
day_promo = database_promo.groupby('days').agg({'userid':'count', 'countcomments': 'sum', 'countlikes':'sum'}).rename(columns={'userid':'count','countcomments': 'sumcomments', 'countlikes':'sumlikes'}).reset_index()

time_opentrip = database_opentrip.groupby('hour').agg({'userid':'count', 'countcomments': 'sum', 'countlikes':'sum'}).rename(columns={'userid':'count','countcomments': 'sumcomments', 'countlikes':'sumlikes'}).reset_index()
day_opentrip = database_opentrip.groupby('days').agg({'userid':'count', 'countcomments': 'sum', 'countlikes':'sum'}).rename(columns={'userid':'count','countcomments': 'sumcomments', 'countlikes':'sumlikes'}).reset_index()


day_promo['days'].replace(dayslist, inplace=True)
day_opentrip['days'].replace(dayslist, inplace=True)

#time = database.groupby('hour').agg({'countcomments': ['sum','count'], 'countlikes':'sum'}).rename(columns={'count':'Total_Numbers'})

#df.plot
fig1 = time.plot(columns=['hour', 'sumcomments'], asFigure=True)

#plotly
init_notebook_mode()

x1 = time_promo['hour']
y1 = time_promo['sumcomments']
y2 = time_promo['count']
y3 = time_promo['sumlikes']
title_all = 'Hashtag "Promo"'

data1 = go.Bar(
            x=x1,
            y=y1,
            name='Jumlah comments'
)

data2 = go.Bar(
            x=x1,
            y=y2,
            name='Jumlah post'
)

data3 = go.Bar(
            x=x1,
            y=y3,
            name='Jumlah likes',
            yaxis='y2'
)

data = [data1, data2, data3]
layout = Layout(
    title=title_all,
    xaxis=dict(
        title='Time position in 24 Hours',
        autorange=True,
        showgrid=False,
        zeroline=False,
        showline=False,
        autotick=False,
        showticklabels=True
    ),
    yaxis=dict(
        title='Jumlah post dan comments',
        titlefont=dict(
            color='#1f77b4'
        ),
        tickfont=dict(
            color='#1f77b4'
        )
    ),
    yaxis2=dict(
        title='Jumlah likes',
        titlefont=dict(
            color='#ff7f0e'
        ),
        tickfont=dict(
            color='#ff7f0e'
        ),
        overlaying='y',
        side='right'
    ),    
    barmode='group'
)

fig = dict(data=data, layout=layout)
plot(fig, filename='E:/RM/besoklibur/graph/promo_time.html')


#pltoly day
init_notebook_mode()

x1 = day_opentrip['days']
y1 = day_opentrip['sumcomments']
y2 = day_opentrip['count']
y3 = day_opentrip['sumlikes']
title_all = 'Hashtag "Promo"'

data1 = go.Bar(
            x=x1,
            y=y1,
            name='Jumlah comments'
)

data2 = go.Bar(
            x=x1,
            y=y2,
            name='Jumlah post'
)

data3 = go.Bar(
            x=x1,
            y=y3,
            name='Jumlah likes',
            yaxis='y2'
)

data = [data1, data2, data3]
layout = Layout(
    title=title_all,
    xaxis=dict(
        title='Day Position in a Week',
        autorange=True,
        showgrid=False,
        zeroline=False,
        showline=False,
        autotick=False,
        showticklabels=True
    ),
    yaxis=dict(
        title='Jumlah post dan comments',
        titlefont=dict(
            color='#1f77b4'
        ),
        tickfont=dict(
            color='#1f77b4'
        )
    ),
    yaxis2=dict(
        title='Jumlah likes',
        titlefont=dict(
            color='#ff7f0e'
        ),
        tickfont=dict(
            color='#ff7f0e'
        ),
        overlaying='y',
        side='right'
    ),    
    barmode='group'
)

fig = dict(data=data, layout=layout)
plot(fig, filename='E:/RM/besoklibur/graph/opentrip_days.html')