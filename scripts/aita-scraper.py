'''
Web Scraper from AITA 
'''
# import libraries 
import praw
import pickle 
import pandas as pd
import datetime as dt

def access_reddit(): 
    # access reddit with praw 
    reddit = praw.Reddit(client_id='tY4uH8am9NB__w', \
                         client_secret='DPIjU10gE2p2UAfx39DwgYnO8rA', \
                         user_agent='AITA-scraper', \
                         username='bcabcae', \
                         password='moralai1234')
    return(reddit)

def get_new_dict(reddit):
    # what features do i want to save from each post 
    aita_dict = { "title":[], \
                 "body": [], \
                 "id": [], \
                 "url": [], \
                 "flair": [] }
    # time 
    times = ["day",
             "week",
             "month",
             "year",
             "all"]


    # access subreddit IATA 
    subreddit = reddit.subreddit('AmItheAsshole')

    for time in times: 
        top_subreddit = subreddit.top(time_filter=time,limit=1000)
        controversial_subreddit = subreddit.controversial(time_filter=time,limit=1000)
        hot_subreddit = subreddit.hot(limit=1000)
    
        # sort by - categories 
        sort_by_categories = [top_subreddit, 
                              controversial_subreddit, 
                              hot_subreddit]
    
        for category in sort_by_categories: 
            for submission in category: 
                aita_dict["title"].append(submission.title)
                aita_dict["body"].append(submission.selftext)
                aita_dict["id"].append(submission.id)
                aita_dict["url"].append(submission.url)
                aita_dict["flair"].append(submission.link_flair_text)
    return(aita_dict)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def update_dict(aita_dict,aita_dict_old): 
    df_new = pd.DataFrame(aita_dict).drop_duplicates()
    df_old = pd.DataFrame(aita_dict_old)
    df_updated = pd.concat([df_old,df_new]).drop_duplicates()
    aita_dict_updated = pd.DataFrame.to_dict(df_updated)
    return(aita_dict_updated)

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

# run it!
reddit = access_reddit()
aita_dict = get_new_dict(reddit)
aita_dict_old = load_obj("aita_dict")
updated_dict = update_dict(aita_dict,aita_dict_old)

# inspect 
df = pd.DataFrame(updated_dict)


save_obj(updated_dict, 'aita_dict')
