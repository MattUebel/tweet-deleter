import tweepy
import os
import sys
import dotenv
import json
import time
import argparse

# import base exception class


SLEEP_TIME = 20


def load_tweets_from_js(js_file):
    with open(js_file, "r") as f:
        data = f.read()
        data = data.replace("window.YTD.tweets.part0 = ", "")
        tweets = json.loads(data)
        print("Loaded %d tweets" % len(tweets))
        return tweets


def load_likes_from_js(js_file):
    with open(js_file, "r") as f:
        data = f.read()
        data = data.replace("window.YTD.like.part0 = ", "")
        likes = json.loads(data)
        print("Loaded %d likes" % len(likes))
        return likes


if __name__ == "__main__":
    # take parameter to determine if tweets or likes should be deleted
    parser = argparse.ArgumentParser(
        prog="TwitterCleanup",
        description="Delete all tweets or likes from a Twitter account given that accounts archive",
        epilog="This script is provided as is, use at your own risk",
    )
    # add flags for tweets and likes, i.e --tweets or --likes
    parser.add_argument("-t", "--tweets", help="Delete all tweets", action="store_true")
    parser.add_argument("-l", "--likes", help="Delete all likes", action="store_true")
    args = parser.parse_args()

    # load environment variables
    dotenv.load_dotenv()

    client = tweepy.Client(
        consumer_key=os.environ["CONSUMER_KEY"],
        consumer_secret=os.environ["CONSUMER_SECRET"],
        access_token=os.environ["ACCESS_TOKEN"],
        access_token_secret=os.environ["ACCESS_TOKEN_SECRET"],
    )

    # check if tweets or likes should be deleted

    if args.tweets:
        tweets = load_tweets_from_js("archive/data/tweets.js")
        tweet_ids = [tweet["tweet"]["id_str"] for tweet in tweets]
        # find the last line in deleted_tweets.txt  so we can resume
        # if the script is interrupted
        if os.path.exists("deleted_tweets.txt"):
            with open("deleted_tweets.txt", "r") as f:
                last_line = f.readlines()[-1]
                # strip the newline
                last_line = last_line[:-1]
                last_id = last_line.split(" ")[0]
                print("Last deleted tweet: %s" % last_id)
                last_index = tweet_ids.index(last_id) + 1
                tweet_ids = tweet_ids[last_index:]

        # open a file to write the deleted tweet ids to
        for tweet_id in tweet_ids:
            try:
                client.delete_tweet(tweet_id, user_auth=True)
            except tweepy.errors.BadRequest as e:
                print("Error deleting tweet %s" % tweet_id)
                print(e)
            with open("deleted_tweets.txt", "a") as f:
                # write the tweet id and a newline to the file so we can resume
                f.write(tweet_id + "\n")
            time.sleep(SLEEP_TIME)
    elif args.likes:
        likes = load_likes_from_js("archive/data/like.js")
        like_ids = [like["like"]["tweetId"] for like in likes]
        # find the last line in deleted_likes.txt  so we can resume
        # if the script is interrupted
        if os.path.exists("deleted_likes.txt"):
            with open("deleted_likes.txt", "r") as f:
                last_line = f.readlines()[-1]
                # strip the newline
                last_line = last_line[:-1]
                last_id = last_line.split(" ")[0]
                print("Last deleted like: %s" % last_id)
                last_index = like_ids.index(last_id) + 1
                like_ids = like_ids[last_index:]

        # open a file to write the deleted like ids to
        for like_id in like_ids:
            try:
                client.unlike(like_id, user_auth=True)
            except tweepy.errors.BadRequest as e:
                print("Error deleting like %s: %s" % (like_id, e))
            with open("deleted_likes.txt", "a") as f:
                # write the like id and a newline to the file so we can resume
                f.write(like_id + "\n")
            time.sleep(SLEEP_TIME)
