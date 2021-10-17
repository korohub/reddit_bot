import json
import praw
import requests
from pymongo import MongoClient
from random import choice
import markdownify
import html2text

client = MongoClient('mongodb://USER:PWD@IP:PORT')
db = client.database

list_tables = ["python", "javascript", "reactjs", "flask", "django" ]

# Shake the collections
param = choice(list_tables)
print(param)

def get_question(table):

    try:
        
        question = list(db[table].find({"reddit": None, "publishext": 1}).limit(1))
        
    except Exception as e:
        print(f'Error  : {e}')

    for q in question:
        dataset = q
    
    return dataset

# recup question on database

q_t = param+"_question"

g_question = get_question(q_t)


subr = 'xxxxxxxxxxxxx'
credentials = 'cred.json'
 
with open(credentials) as f:
    creds = json.load(f)
 
reddit = praw.Reddit(client_id=creds['client_id'],
                     client_secret=creds['client_secret'],
                     user_agent=creds['user_agent'],
                     redirect_uri=creds['redirect_uri'],
                     refresh_token=creds['refresh_token'])
 
subreddit = reddit.subreddit(subr)


question  = g_question["question"]
m_question = markdownify.markdownify(question, heading_style="ATX")

# you can use Html2text instead markdownify
#print(m_question)
#print(html2text.html2text(question))
 
title = f'{g_question["title"]}'
selftext = f'''
{g_question["language"].capitalize()} \n
{m_question} \n
Answer link : https://xxxxx.xx/a/{g_question["language"]}/{g_question["slug"]}
'''
 
subreddit.submit(title,selftext=selftext)

# If necessary update the collection
#db[q_t].update_one({"id": g_question["id"]},{"$set": {"reddit": 1 }})