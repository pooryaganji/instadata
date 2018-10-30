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
import datetime

#post_file for saving posts

#location="C:\\Users\\ASUS\\Documents\\doyle-twitter\\"
location="G:\\projects\\insta\\"
#profile="shahrzadseries"
profile="emadazimi"
post_file=location+profile+".csv"
comment_file=location+'commenters_{}.csv'.format(profile)
"""initialize main parameters"""
def main_parameters(profile):
    url_extraction="https://www.instagram.com"+"/{}/".format(profile)
    cooki=dict(cookie=r'csrftoken=9FxPdAIhDmmOC9fWAcxelVkEWoZqUuyO; ds_user_id=3671346645; mid=W2BiCwALAAHV0SCzkbwgg9zjgv_1; ig_cb=1; mcd=3; csrftoken=9FxPdAIhDmmOC9fWAcxelVkEWoZqUuyO; shbid=14728; sessionid=IGSC26ba3437a61f01e788dcccfa9d2bce0b3d810179bfac525a618c0df61ce510e5%3APa3Ucm3vYyBjSJpEhz3mDvbP44GmiASz%3A%7B%22_auth_user_id%22%3A3671346645%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_auth_user_hash%22%3A%22%22%2C%22_platform%22%3A4%2C%22_token_ver%22%3A2%2C%22_token%22%3A%223671346645%3Amj2EEv3HAJYp0RIdAI0d6XpOF3rp92gN%3A3d28e1f4ffad39ad621b67c1b8c8db93f36f27dc7347475d5ba69de14009713f%22%2C%22last_refreshed%22%3A1540475985.7600660324%7D; rur=ATN; shbts=1540558534.2105925; urlgen="{\"46.224.55.223\": 56402}:1gG1rW:BWG8AOo5YEv5eybpnUK2vtPJzwE"')
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
    file.write("{},{},{},{},{},{},{},{}\n".format('post_num','shortcode','links','img_url','timestamp','num_comments','num_likes','caption'))
    post_num=posts["data"]["user"]["edge_owner_to_timeline_media"]['count']
    for i in posts["data"]["user"]["edge_owner_to_timeline_media"]['edges']:
        try:
            caption=i['node']['edge_media_to_caption']['edges'][0]['node']['text'].replace("\n"," ").replace("\r"," ")
        except:
            caption=""
        num_likes,shortcode,num_comments,links,timestamp,img_url=i['node']['edge_media_preview_like']['count'],i['node']['shortcode'],i['node']['edge_media_to_comment']['count'],r"https://www.instagram.com/p/"+i['node']['shortcode']+r"/?taken-by={}".format(profile),i['node']['taken_at_timestamp'],i['node']["display_url"]
        file.write("{},{},{},{},{},{},{},{}\n".format(post_num,shortcode,links,img_url,timestamp,num_comments,num_likes,caption))
        post_num-=1

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
            num_likes,num_comments,links,timestamp,img_url=i['node']['edge_media_preview_like']['count'],i['node']['edge_media_to_comment']['count'],r"https://www.instagram.com/p/"+i['node']['shortcode']+r"/?taken-by={}".format(profile),i['node']['taken_at_timestamp'],i['node']["display_url"]
            file.write("{},{},{},{},{},{},{},{}\n".format(post_num,shortcode,links,img_url,timestamp,num_comments,num_likes,caption))
            post_num-=1
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

def comments():
    #blacklist for posts which dont contain comment
    blist=[]
    try:
        with open("blacklist_{}.txt".format(profile),'r') as blacklist:
            blist+=blacklist.read().split(",")

    except:
        pass
    """if file exists:
    open the file......"""
    if 'commenters_{}.csv'.format(profile) in os.listdir(location):
        print("file exists")
        file=open(comment_file,'a',encoding='utf-8')
        posts=pd.read_csv(post_file,usecols=["shortcode","post_num","timestamp"],sep='delimiter',delimiter=",",quoting=csv.QUOTE_NONE,lineterminator='\n')
        comments=pd.read_csv(comment_file,usecols=["timestamp","shortcode","post_num"],sep='delimiter',delimiter=",",quoting=csv.QUOTE_NONE,lineterminator='\n')
        #unique comments and their last comment time
        cmnt_checker=comments[["timestamp","shortcode"]].groupby("shortcode").max()
        unique_comments=cmnt_checker.index
        generator=posts.iterrows()
        
        for _ , others in generator:
            post_num=others[0]
            shortcode=others[1]
            timestamp=others[2]
            delta_time=datetime.date.today()-datetime.date.fromtimestamp(timestamp)
            #check if post is older than 3 days if yes ,so others are older
            if delta_time.days > 60:
                print("this is old post "+shortcode)
                break
            #check if post is new (not in blacklist and not in history of previuous comments)
            elif shortcode not in set(blist) and shortcode not in set(unique_comments):
                print("this is new post "+shortcode)
                params={"query_hash":"a3b895bdcb9606d5b1ee9926d885b924","variables":{"shortcode":shortcode,"first":5000}}
                semi_url=urllib.parse.urlencode(params)
                f_url=base_url+semi_url.replace("%27","%22").replace("+","")
                commenters=requests.get(f_url,headers=cooki)
                content=commenters.json()['data']['shortcode_media']['edge_media_to_comment']['edges']
                if len(content)>0:
                    #content=commenters.json()['data']['shortcode_media']['edge_media_to_comment']['edges']
                    for i in content:
                        timestamp=i['node']['created_at']
                        user_id=i['node']['owner']['id']
                        username=i['node']['owner']['username']
                        text=i['node']['text'].replace("\n"," ")
                        comm_id=i['node']['id']
                        shortcode=shortcode
                        file.write("{},{},{},{},{},{},{}\n".format(comm_id,timestamp,user_id,username,shortcode,post_num,text))
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
                            file.write("{},{},{},{},{},{},{}\n".format(comm_id,timestamp,user_id,username,shortcode,post_num,text))
                else:
                    print("except")
                    with open("blacklist_{}.txt".format(profile),'a') as blacklist:
                        blacklist.write(others[1]+",")
                    continue
            #if not in black list and its less than 3 days old, so we check for new comments
            elif shortcode not in set(blist):
                print("less than three days post"+shortcode)
                params={"query_hash":"a3b895bdcb9606d5b1ee9926d885b924","variables":{"shortcode":shortcode,"first":5000}}
                semi_url=urllib.parse.urlencode(params)
                f_url=base_url+semi_url.replace("%27","%22").replace("+","")
                commenters=requests.get(f_url,headers=cooki)
                content=commenters.json()['data']['shortcode_media']['edge_media_to_comment']['edges']
                if len(content)>0:
                    
                    for i in content:
                        timestamp=i['node']['created_at']
                        user_id=i['node']['owner']['id']
                        username=i['node']['owner']['username']
                        text=i['node']['text'].replace("\n"," ")
                        comm_id=i['node']['id']
                        shortcode=shortcode
                        #with this variable if we get to old comment we stop while loop
                        continues=True
                        #old and new comment problem
                        last_cmnt_time=cmnt_checker.loc[shortcode].values[0]
                        if timestamp <= last_cmnt_time:
                            continues=False
                            continue
                        file.write("{},{},{},{},{},{},{}\n".format(comm_id,timestamp,user_id,username,shortcode,post_num,text))
                    while continues and commenters.json()['data']['shortcode_media']['edge_media_to_comment']['page_info']['has_next_page']:
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
                            if timestamp >= cmnt_checker.loc[shortcode].values[0]:
                                break
                            file.write("{},{},{},{},{},{},{}\n".format(comm_id,timestamp,user_id,username,shortcode,post_num,text))
                else:
                    print("except")
                    with open("blacklist_{}.txt".format(profile),'a') as blacklist:
                        blacklist.write(others[1]+",")
                    continue  

        """
        new_posts=set(posts.shortcode.unique())-set(comments.shortcode.unique())-set(blist)
        print(new_posts)
        for shortcode in new_posts:
            params={"query_hash":"a3b895bdcb9606d5b1ee9926d885b924","variables":{"shortcode":shortcode,"first":5000}}
            semi_url=urllib.parse.urlencode(params)
            f_url=base_url+semi_url.replace("%27","%22").replace("+","")
            commenters=requests.get(f_url,headers=cooki)
            content=commenters.json()['data']['shortcode_media']['edge_media_to_comment']['edges']
            if len(content)>0:
                #content=commenters.json()['data']['shortcode_media']['edge_media_to_comment']['edges']
                for i in content:
                    timestamp=i['node']['created_at']
                    user_id=i['node']['owner']['id']
                    username=i['node']['owner']['username']
                    text=i['node']['text'].replace("\n"," ")
                    comm_id=i['node']['id']
                    shortcode=shortcode
                    file.write("{},{},{},{},{},{},{}\n".format(comm_id,timestamp,user_id,username,shortcode,post_num,text))
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
                        file.write("{},{},{},{},{},{},{}\n".format(comm_id,timestamp,user_id,username,shortcode,post_num,text))    
            else:
                print("except")
                with open("blacklist_{}.txt".format(profile),'a') as blacklist:
                    blacklist.write(others[1]+",")
                continue"""
    else:
        print("new file creating ...")
        file=open(comment_file,'a',encoding='utf-8')
        file.write("{},{},{},{},{},{},{}\n".format('comm_id','timestamp','user_id','username','shortcode','post_num','text'))
        #posts=pd.read_csv(post_file,quoting=csv.QUOTE_NONE,lineterminator='\n',sep='delimiter',usecols=[0,1])
        posts=pd.read_csv(post_file,usecols=["shortcode","post_num"],sep='delimiter',delimiter=",",quoting=csv.QUOTE_NONE,lineterminator='\n')
        generator=posts.iterrows()
        for _ , others in generator:
            
            shortcode=others[1]
            post_num=others[0]
            params={"query_hash":"a3b895bdcb9606d5b1ee9926d885b924","variables":{"shortcode":shortcode,"first":5000}}
            semi_url=urllib.parse.urlencode(params)
            f_url=base_url+semi_url.replace("%27","%22").replace("+","")
            commenters=requests.get(f_url,headers=cooki)
            content=commenters.json()['data']['shortcode_media']['edge_media_to_comment']['edges']
            if len(content)>0:
                #content=commenters.json()['data']['shortcode_media']['edge_media_to_comment']['edges']
                for i in content:
                    timestamp=i['node']['created_at']
                    user_id=i['node']['owner']['id']
                    username=i['node']['owner']['username']
                    text=i['node']['text'].replace("\n"," ")
                    comm_id=i['node']['id']
                    shortcode=shortcode
                    file.write("{},{},{},{},{},{},{}\n".format(comm_id,timestamp,user_id,username,shortcode,post_num,text))
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
                        file.write("{},{},{},{},{},{},{}\n".format(comm_id,timestamp,user_id,username,shortcode,post_num,text))
            else:
                print("except")
                with open("blacklist_{}.txt".format(profile),'a') as blacklist:
                    blacklist.write(others[1]+",")
                continue
    file.close()
comments()
