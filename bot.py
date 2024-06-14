import praw
import os
from psaw import PushshiftAPI
from replit import db
import pandas as pd
from pymongo import MongoClient
from time import sleep

# Reddit connection
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
reddit_username = os.environ['REDDIT_USERNAME']
reddit_password = os.environ['REDDIT_PASSWORD']

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     username=reddit_username,
                     password=reddit_password,
                     user_agent="BeginnerHelperBot 1.0 by Autotelico")

print(str(reddit.user.me()) + ' is now active')


# Decides whether to reply to the submission or not
def find_words(title_array, selftext_array):
  includesLearn = False
  includesPython = False

  for word in title_array:
    if (word.casefold() == 'learn'):
      includesLearn = True
    if (word.casefold() == 'python'):
      includesPython = True
  for word in selftext_array:
    if (word.casefold() == 'learn'):
      includesLearn = True
    if (word.casefold() == 'python'):
      includesPython = True

  return includesLearn and includesPython


# Avoids replying to the same submission
replied_posts = []

while True:
  for post in reddit.subreddit('learnpython').stream.submissions():
    print(f"NEW POST -> {post.title}")
    print(post.selftext)

    title_words = post.title.split()
    selftext_words = post.selftext.split()

    if find_words(title_words,
                  selftext_words) and post.id not in replied_posts:
      post.reply(
          "Hi there! 🫡 I see you're interested in learning Python. I'm a bot built in Python 😄 Pretty cool, right?\n\nHere are some of the best resources out there to learn Python from:\n\n- [Free Code Camp's Python Tutorial](https://www.youtube.com/watch?v=rfscVS0vtbw)\n- [Python Wiki's suggestions](https://wiki.python.org/moin/BeginnersGuide/Programmers)\n- [CS50](https://cs50.harvard.edu/python/2022/)\n\nPython can be a lot of fun. Good luck on your Python journey! 💜\n\n^(If I missed the point of this post, kindly downvote my reply)"
      )
      replied_posts.append(post.id)
      print(f'REPLY SENT TO POST "{post.title}"')
      # Reddit requires a 10-minute cooldown between each reply
      sleep(600)
      break
