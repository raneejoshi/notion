import os

import requests
from datetime import datetime
import praw


NOTION_API_KEY= os.environ['NOTION_API_KEY']
REDDIT_CLIENT_ID = os.environ['REDDIT_CLIENT_ID']
REDDIT_CLIENT_SECRET = os.environ['REDDIT_CLIENT_SECRET']
REDDIT_USER_AGENT = os.environ['REDDIT_USER_AGENT']

DATABASE_KEY = os.environ['DATABASE_KEY']
PAGE_KEY = os.environ['PAGE_KEY']


def create_notionpost(title, score, subreddit, contenturl, created_date, actualurl):

    headers = {
        'Authorization': f"Bearer {NOTION_API_KEY}",
        'Content-Type': 'application/json',
        'Notion-Version': '2021-08-16',
    }
    data = { "parent": { "database_id": DATABASE_KEY }, "properties": { 
        "Name": {"title": [ { "text": { "content": title } } ] },
        "Views": { "number": score },
        "Subreddit": { "select": { "name": subreddit } },
        # "subreddit": { "rich_text": [ { "text": { "content": subreddit } } ] },
        "contenturl": {"url": contenturl}, 
        "URL": {"url": actualurl}, 
        "Publish Date": {"date" : {"start": created_date}}, 
    },  }

    requests.post('https://api.notion.com/v1/pages', headers=headers, json=data)


## checks the notion block and retrieve subreddits in form of list of strings
def get_subreddits():
    headers = {
        'Notion-Version': '2021-08-16',
        'Authorization': f"Bearer {NOTION_API_KEY}",
    }
    response = requests.get(f'https://api.notion.com/v1/blocks/{PAGE_KEY}/children?page_size=10', headers=headers)
    mylist = response.json()['results'][1]['bulleted_list_item']['text'][0]['plain_text'].split()
    return mylist


def reddit_notion(subreddits):

    ## first: retrieve database and create searchable set 

    headers = {
        'Authorization': f"Bearer {NOTION_API_KEY}",
        'Notion-Version': '2021-08-16',
        'Content-Type': 'application/json',
    }
    response = requests.post(f'https://api.notion.com/v1/databases/{DATABASE_KEY}/query', headers=headers)
    myneeded = response.json()['results']
    myset = set()

    for i in myneeded:
        try:
            myurl = i['properties']['URL']['url']
            myset.add(myurl)
        except:
            pass
    
    reddit = praw.Reddit(client_id= REDDIT_CLIENT_ID,
                        client_secret= REDDIT_CLIENT_SECRET,
                        user_agent= REDDIT_USER_AGENT)
    for subreddit in subreddits:
        try:
            test_reddit = reddit.subreddit(subreddit).top("day", limit = 2)
            # test_reddit = reddit.subreddit(subreddit).top("month", limit = 10)
            # test_reddit = reddit.multireddit("reactjs", "programming").top("day")
            # ml_subreddit = reddit.subreddit(mysub)
            for post in test_reddit:
                if ("https://www.reddit.com" + post.permalink) not in myset:
                    create_notionpost(post.title, post.score, subreddit, post.url, datetime.fromtimestamp(post.created).strftime("%Y-%m-%d"), ("https://www.reddit.com" + post.permalink))
        except:
            pass

targetlist = get_subreddits()
reddit_notion(targetlist)
