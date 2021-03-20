#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 14:59:59 2021

@author: yijingtan
"""
import time
from bs4 import BeautifulSoup
import re
import traceback
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/Users/yijingtan/Desktop/project/Earnings_call_NLP/chromedriver')
#from selenium.webdriver.support.wait import WebDriverWait

import datetime
today=datetime.date.today()  
now_time = datetime.datetime.now()  

#login in linkedin'''
driver.get('https://www.linkedin.com')
username = driver.find_element_by_class_name('input__input')
username.send_keys('yt333@scarletmail.rutgers.edu')
time.sleep(0.5)
pwd=driver.find_element_by_id('session_password')
pwd.send_keys('19930112Dks!')
time.sleep(0.5)
log_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')
log_in_button.click()
time.sleep(0.5)

#get company post page
company='https://www.linkedin.com/company/google/posts/?feedView=all'
driver.get(company)
time.sleep(3)

#scroll page
try:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    driver.execute_script("document.getElementsByTagName('span')[300].scrollIntoView(false);")
    time.sleep(3)
    #driver.execute_script("window.scrollBy (0,400);")
    #time.sleep(3)
#except Exception as e:
except Exception:
    print (traceback.print_exc())

#get page source
soup = BeautifulSoup(driver.page_source,'html.parser')
pret = soup.prettify() 
body = soup.html.body

posts=body.find_all('span',class_='break-words')
# print(len(posts)) 
time.sleep(5)

#record post time
posts_time=body.find_all('span',class_='feed-shared-actor__sub-description')
time.sleep(3)
def find_post_time(posts_time):
    res=[]
    num=[]
    for i in range(len(posts_time)):
        p=str(posts_time[i])
        date=p.split('<span aria-hidden="true">')[1].split('•')[0].replace(' ','')

        x=re.findall(r'[A-Za-z]',str(date))[0]
        n=int(re.findall(r'[1-7]',str(date))[0])
        print(n,x)
        if x=='h':
            delta=datetime.timedelta(days=0)
            num.append(i)
        elif x=='d':
            delta = datetime.timedelta(days=n)
            num.append(i)
        elif x=='w':
            delta = datetime.timedelta(weeks=n)  
            num.append(i)
        else: #at least more than 1 month
            #continue
            delta=today
        post_date=today-delta
        res.append(post_date)
        
    return res,num
        
posts_time,num=find_post_time(posts_time)

#post analysis
def post_inspector(post_link):
    search_page='https://www.linkedin.com/post-inspector/'
    driver.get(search_page)
    time.sleep(3)
    #
    post_url=post_link 
    enter=driver.find_element_by_id('js-url-input')
    enter.send_keys(post_url)
    time.sleep(0.5)
    search_button = driver.find_element_by_id('js-inspect-button')
    search_button.click()
    time.sleep(1) #then direcct to the search post page
   
    #locate to the current window
    driver.switch_to.window(driver.window_handles[0])
    return post_url

def post_link_pic(body):
    contents=body.find_all('a',class_='feed-shared-article__image-link')
    link=[]
    for i in range(len(contents)):
        link.append(contents[i]['href'])
        
    return link


def get_post_links(content,m):
    links=re.findall('(https?://[a-zA-Z0-9\.\?/%-_]*)',content)
    time.sleep(3)
    
    j = 0 
    if links!=[]: #links that contained in the post content
        for i in range(len(links)):
            if 'hashtag' in links[j]:  
                links.pop(j)
            else:
                j += 1   #check if mutipile links 
        post_link=links[0]
    else:        #links that attached on the pic 
        l=post_link_pic(body)
        post_link=l[m]
        m+=1
    #elif:post_link='None'
        
    return (post_link)  

def get_hash_tags(span):
    content=span.text
    #print ('content:',content)
    words=content.replace('\n','').split(' ')
    hashtags=[]
    for word in words:
        if word.startswith('#'):
            hashtag=word.split(',')[0]
            hashtags.append(hashtag)
            #print(hashtag)
        else:
            hashtag='None'
    #print(hashtags)
    if hashtags==[]:
        hashtags=''
    else:
        hashtags=','.join(hashtags)
    return content,hashtags

    
 
    
 
posts=body.find_all('span',class_='break-words')
time.sleep(10)
#l=post_link_pic(body)  #links that attached on the pic 
m=0
time.sleep(10)
co_post=[]
#value='hashtag'
for j in num:
    print(j)
    span=posts[j]
    content = str(span)   
    post_link=get_post_links(content,m)
    print('Processing for :',post_link)
    content,hashtags=get_hash_tags(span)
    scrape_time=today 
    post_time=posts_time[j]
    
    # save into df
    co_post.append({
        'scrape_time':scrape_time,
        'post_time':post_time,
        #'publish_time':publish_time,
        'description':content,
        'post_url':post_link,
        'hashtag':hashtags
        }) 
#print(co_post) 


import pandas as pd
from sqlalchemy import create_engine

df=pd.DataFrame(co_post, columns=['scrape_time', 'post_time','description','post_url','hashtag']) 
def save_to_db(df):
    engine = create_engine('mysql+mysqlconnector://foo:bar202012@localhost/Linkedin_post')
    df.to_sql(name='google', con=engine , schema='Linkedin_post',if_exists='replace', chunksize=1000, index=False)
    engine.dispose()

save_to_db(df)



def f():
    post_inspector(post_link)
    # post information
    soup = BeautifulSoup(driver.page_source,'html.parser')
    time.sleep(3)
    
    #try:
    #    scrape_time=soup.find_all('td',class_='urlInfoTable__value')[0].text.replace('\n','').replace(' ','') 
    #    time.sleep(3)
    #except:
    #    print (traceback.print_exc()) 
    #if scrape_time is None:
    #    scrape_time='None'
    #else:
    #    scrape_time=today 
    scrape_time=today 
    
    tdlist=soup.find_all('td',class_='metadataTable__propertyValue')
    time.sleep(3)
    #print(tdlist)
    try:
        publish_time=tdlist[len(tdlist)-1].text.replace('\n','').replace(' ','') 
        time.sleep(3)
    except:
        print (traceback.print_exc()) 
    if publish_time=='Nopublicationdatefound':
        publish_time='None'
    else:
        publish_time=tdlist[len(tdlist)-1].text.replace('\n','').replace(' ','').split(',')[0]
