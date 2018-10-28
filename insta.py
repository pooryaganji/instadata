#url structure for profile page:
#base+query_hash+variables(user_ID(user id of user's profile)
#+first(number of objects to extract at first request+after)
import bs4
import requests
import urllib
import json
import time
import pandas as pd
import os
import csv
from IPython.display import display

#post_file for saving posts

location="C:\\Users\\ASUS\\Documents\\doyle-twitter\\"
profile="shahrzadseries"
post_file=location+profile+".csv"
comment_file=location+'commenters_{}'.format(profile)
"""initialize main parameters"""
def main_parameters(profile):
    url_extraction="https://www.instagram.com"+"/{}/".format(profile)
    cooki=dict(cookie=r'csrftoken=9FxPdAIhDmmOC9fWAcxelVkEWoZqUuyO; ds_user_id=3671346645; mid=W2BiCwALAAHV0SCzkbwgg9zjgv_1; ig_cb=1; mcd=3; csrftoken=9FxPdAIhDmmOC9fWAcxelVkEWoZqUuyO; shbid=14728; sessionid=IGSC26ba3437a61f01e788dcccfa9d2bce0b3d810179bfac525a618c0df61ce510e5%3APa3Ucm3vYyBjSJpEhz3mDvbP44GmiASz%3A%7B%22_auth_user_id%22%3A3671346645%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_auth_user_hash%22%3A%22%22%2C%22_platform%22%3A4%2C%22_token_ver%22%3A2%2C%22_token%22%3A%223671346645%3Amj2EEv3HAJYp0RIdAI0d6XpOF3rp92gN%3A3d28e1f4ffad39ad621b67c1b8c8db93f36f27dc7347475d5ba69de14009713f%22%2C%22last_refreshed%22%3A1540475985.7600660324%7D; rur=ATN; shbts=1540558534.2105925; urlgen="{\"46.224.55.223\": 56402}:1gG1rW:BWG8AOo5YEv5eybpnUK2vtPJzwE"')
    #useragent={"user-agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    #cookie_notlog={"cookie":'mid=WxU4JwALAAFLcHrIW4M8jss-HqNw; mcd=3; shbid=14728; rur=FRC; csrftoken=Es8C8xSSUhrIfhPxqz9ih8JahyyzRY4o; urlgen="{\"time\": 1531896776\054 \"46.224.108.197\": 56402}:1ffosN:GxIvwVRDE7MFwYpn6LhxV6UiSqQ"'}
    #query_hash for different things
    q_followers="149bef52a3b2af88c0fec37913fe1cbc"
    q_more_post="bd0d6d184eefd4d0ce7036c11ae58ed9"
    #base url
    base_url=r"https://www.instagram.com/graphql/query/?"

    init=requests.get(url_extraction)
    #user_id extraction from initial request
    content=bs4.BeautifulSoup(init.text,'html.parser')
    script = content.find('body').find("script").text

    jsonValue = '{%s}' % (script.split('{', 1)[1].rsplit('}', 1)[0])
    value = json.loads(jsonValue)
    id_value=value['entry_data']['ProfilePage'][0]['graphql']['user']['id']
    user_id={'id': '{}'.format(id_value)}
    secondpart=user_id.copy()
    secondpart.update({"first":"50"})
    return secondpart,cooki,q_followers,q_more_post,base_url

secondpart,cooki,q_followers,q_more_post,base_url=main_parameters(profile)

def writer(*variables,file):
    try:
        file.write(str(variables).strip(r"'").strip("(").strip(")")+"\n")
    except:
        pass


"""loading all posts"""
def posts(secondpart=secondpart,cooki=cooki,q_followers=q_followers,q_more_post=q_more_post,base_url=base_url):
    try:
        os.remove(post_file)
    except:
        pass
    file=open(post_file,'a',encoding='utf-8')
    params={"query_hash":q_more_post,"variables":secondpart}
    semi_url=urllib.parse.urlencode(params)
    f_url=semi_url.replace("%27","%22").replace("+","")
    posts=requests.get(base_url+f_url,headers=cooki).json()
    writer('links','img_url','timestamp','num_comments','num_likes','caption',file=file)
    for i in posts["data"]["user"]["edge_owner_to_timeline_media"]['edges']:
        try:
            caption=i['node']['edge_media_to_caption']['edges'][0]['node']['text'].replace("\n"," ").replace("\r"," ").replace("\r"," ")
        except:
            caption=""
        num_likes,num_comments,links,timestamp,img_url=i['node']['edge_media_preview_like']['count'],i['node']['edge_media_to_comment']['count'],r"https://www.instagram.com/p/"+i['node']['shortcode']+r"/?taken-by=shahrzadseries",i['node']['taken_at_timestamp'],i['node']["display_url"]
        writer(links,img_url,timestamp,num_comments,num_likes,caption,file=file)

    while posts["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]['has_next_page']:
        time.sleep(2)
        after=posts["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]['end_cursor']
        secondpart.update({"after":after})
        params.update({"variables":secondpart})
        semi_url=urllib.parse.urlencode(params)
        f_url=semi_url.replace("%27","%22").replace("+","")
        posts=requests.get(base_url+f_url,headers=cooki).json()
        for i in posts["data"]["user"]["edge_owner_to_timeline_media"]['edges']:
            try:
                caption=i['node']['edge_media_to_caption']['edges'][0]['node']['text'].replace("\n"," ").replace("\r"," ").replace("\r"," ")
            except:
                caption=""
            num_likes,num_comments,links,timestamp,img_url=i['node']['edge_media_preview_like']['count'],i['node']['edge_media_to_comment']['count'],r"https://www.instagram.com/p/"+i['node']['shortcode']+r"/?taken-by=shahrzadseries",i['node']['taken_at_timestamp'],i['node']["display_url"]
            writer(links,img_url,timestamp,num_comments,num_likes,caption,file=file)
    file.close()
posts()

"""loading all followers"""
"""
secondpart.update({"first":"5000"})
params={"query_hash":q_followers,"variables":secondpart}
semi_url=urllib.parse.urlencode(params)
follow_url=semi_url.replace("%27","%22").replace("+","")
print(base_url+follow_url)
followers=requests.get(base_url+follow_url,headers=cooki)
with open("follwers1.csv","w",encoding='utf-16') as file:
    for i in followers.json()['data']['user']['edge_followed_by']['edges']:
        file.write("{},{}\n".format(i['node']['id'],i['node']['full_name']))


while followers.json()['data']['user']['edge_followed_by']['page_info']['has_next_page']:
    time.sleep(2)
    after=followers.json()['data']['user']['edge_followed_by']['page_info']['end_cursor']
    secondpart.update({"after":after})
    params.update({"variables":secondpart})
    semi_url=urllib.parse.urlencode(params)
    f_url=semi_url.replace("%27","%22").replace("+","")
    print(base_url+f_url)
    followers=requests.get(base_url+f_url,headers=cooki)
    j=followers.json()
    with open("follwers.csv","a",encoding='utf-16') as file:
        for i in j['data']['user']['edge_followed_by']['edges']:
            file.write("{},{}\n".format(i['node']['id'],i['node']['full_name']))

"""

a=2

def comments():
    """if file exists:
        #open the file......
    """
    if a==3:
        return a    
    else:
        file=open(comment_file,'a',encoding='utf-8')
        posts=pd.read_csv(post_file,quoting=csv.QUOTE_NONE,lineterminator='\n',sep='delimiter',usecols=[0],squeeze=True)
        generator=posts.iteritems()
        for index,link in generator:
            shortcode=link[28:39]
            params={"query_hash":"a3b895bdcb9606d5b1ee9926d885b924","variables":{"shortcode":shortcode,"first":5000}}
            semi_url=urllib.parse.urlencode(params)
            f_url=base_url+semi_url.replace("%27","%22").replace("+","")
            commenters=requests.get(f_url,headers=cooki)
            for i in commenters.json()['data']['shortcode_media']['edge_media_to_comment']['edges']:
                timestamp=i['node']['created_at']
                user_id=i['node']['owner']['id']
                username=i['node']['owner']['username']
                text=i['node']['text'].replace("\n"," ")
                comm_id=i['node']['id']
                shortcode=shortcode
                writer(comm_id,timestamp,user_id,username,shortcode,text,comment_file,file=file)
            while commenters.json()['data']['shortcode_media']['edge_media_to_comment']['page_info']['has_next_page']:
            time.sleep(3)
            after=commenters.json()['data']['shortcode_media']['edge_media_to_comment']['page_info']['end_cursor']
            params['variables'].update({'after':after})
            semi_url=urllib.parse.urlencode(params)
            f_url=base_url+semi_url.replace("%27","%22").replace("+","")
            commenters=requests.get(f_url,headers=cooki)
            for i in commenters.json()['data']['shortcode_media']['edge_media_to_comment']['edges']:
                timestamp=i['node']['created_at']
                user_id=i['node']['owner']['id']
                username=i['node']['owner']['username']
                text=i['node']['text'].replace("\n"," ")
                comm_id=i['node']['id']
                shortcode=shortcode
                writer(comm_id,timestamp,user_id,username,shortcode,text,file=file)
    file.close()



    
    commenters=requests.get(urlcommf,headers=cooki)
        with open('C:\\Users\\ASUS\\Documents\\doyle-twitter\\commenters_{}.csv'.format(link),'a',encoding='utf-8') as file:
            for i in commenters.json()['data']['shortcode_media']['edge_media_to_comment']['edges']:
                
                time_comm=commenters.json()['data']['shortcode_media']['edge_media_to_comment']['edges'][0]['node']['created_at']
                userid=commenters.json()['data']['shortcode_media']['edge_media_to_comment']['edges'][0]['node']['owner']['id']
                username=commenters.json()['data']['shortcode_media']['edge_media_to_comment']['edges'][0]['node']['owner']['username']
                text=commenters.json()['data']['shortcode_media']['edge_media_to_comment']['edges'][0]['node']['text']
                commenters.text

                file.write("{},{},{},{}\n".format(i['node']['created_at'],i['node']['owner']['id'],i['node']['owner']['username'],i['node']['text'].replace("\n"," "))) 


        while commenters.json()['data']['shortcode_media']['edge_media_to_comment']['page_info']['has_next_page']:
            time.sleep(2)
            after=commenters.json()['data']['shortcode_media']['edge_media_to_comment']['page_info']['end_cursor']
            comm['variables'].update({'after':after})
            urlcomm=urllib.parse.urlencode(comm)
            urlcommf=base_url+urlcomm.replace("%27","%22").replace("+","")
            commenters=requests.get(urlcommf,headers=cooki)
            with open('F:\\shahrzadpage\\commenters_{}.csv'.format(link),'a',encoding='utf-8') as file:
                for i in commenters.json()['data']['shortcode_media']['edge_media_to_comment']['edges']:
                    file.write("{},{},{},{}\n".format(i['node']['created_at'],i['node']['owner']['id'],i['node']['owner']['username'],i['node']['text'].replace("\n"," ")))      
    else:
        continue

likers={"query_hash":"1cb6ec562846122743b61e492c85999f","variables":{"shortcode":"BbFFM8uhHv5","first":10000}}
urllike=urllib.parse.urlencode(likers)
urllikef=base_url+urllike.replace("%27","%22").replace("+","")
like=requests.get(urllikef,headers=cooki)
with open('likers.csv','a',encoding='utf-16') as file:
    for i in like.json()['data']['shortcode_media']['edge_liked_by']['edges']:
        file.write("{},{}\n".format(i['node']['id'],i['node']['username']))

like.json()['data']['shortcode_media']['edge_liked_by']['edges'][0]['node']['id']
like.json()['data']['shortcode_media']['edge_liked_by']['edges'][0]['node']['username']

while like.json()['data']['shortcode_media']['edge_liked_by']['page_info']['has_next_page']:  
    likers["variables"].update({"after":after})
    urllike=urllib.parse.urlencode(likers)
    urllikef=base_url+urllike.replace("%27","%22").replace("+","")
    print(urllikef)
    like=requests.get(urllikef,headers=cooki)
    with open('likers.csv','a',encoding='utf-16') as file:
        for i in like.json()['data']['shortcode_media']['edge_liked_by']['edges']:
            file.write("{},{}\n".format(i['node']['id'],i['node']['username']))

like.json()
    

if like.json()['data']['shortcode_media']['edge_liked_by']['page_info']['has_next_page']==True:
   
    while True:
        
        after=like.json()['data']['shortcode_media']['edge_liked_by']['page_info']['end_cursor']
        print(after)
        likers["variables"].update({"after":after})
        print(likers)
        urllike=urllib.parse.urlencode(likers)
        urllikef=base_url+urllike.replace("%27","%22").replace("+","")
        print(urllikef)
        like=requests.get(urllikef)
        print("first is","\n",like.json()['data']['shortcode_media']['edge_liked_by']['edges'][0]['node']['full_name'])
        print("last is","\n",like.json()['data']['shortcode_media']['edge_liked_by']['edges'][-2]['node']['full_name'] )    
        like.json()['data']['shortcode_media']['edge_liked_by']['page_info']['has_next_page']==True
"""
#extract persons who liked
like.json()['data']['shortcode_media']['edge_liked_by']['edges'][0]['node']['full_name']

##database
import psycopg2
conn = psycopg2.connect(database='dvdrents' ,user='postgres',password=1)

cur = conn.cursor()

user_list=q.json()['data']['user']['edge_followed_by']['edges']

cur.execute("CREATE TABLE followers (username varchar PRIMARY KEY, user_id bigint);")

for i in user_list:
    
    #print(i['node']['username'], i['node']['id'])
    cur.execute("INSERT INTO followers (username, user_id) VALUES (%s, %s)",(i['node']['username'], i['node']['id']))
cur.execute("SELECT * FROM followers;")

conn.commit()
cur.close()
conn.close()

a={"ali":12}
b={"emad":"z"}
a.update(b)
print(a)
"""