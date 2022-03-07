#!/usr/bin/env python3
#================================================================
from datetime import datetime
from time import sleep
import configparser
import tweepy
import os
import re
#================================================================

ioc_list = []

#----------------------------------------------------------------

def config_parser(section, key):
    config = configparser.ConfigParser(interpolation=None)
    try:
        config.read(os.path.join(os.path.dirname(__file__) + "/config/config.ini"))
        result = config.get(section, key)
        return result
    except config.NoOptionError:
        raise Exception("There was a problem with configuration file. The key does not exist.")
    except config.NoSectionError:
        raise Exception("There was a problem with configuration file. The key does not exist.")

#----------------------------------------------------------------

def init_twitter_config():
    bearer_token = config_parser('twitter_api', 'bearer_token')
    auth = tweepy.Client(bearer_token)
    return auth

#----------------------------------------------------------------

def load_accounts_file(accounts_filename):
    with open(os.path.dirname(__file__) + "/config/" + accounts_filename, "r") as account_list:
        array = []
        for line in account_list:
            handle = line.replace('@', '')
            array.append(handle.strip())
        account_list.close()
    return array

#----------------------------------------------------------------

def ioc_union(ioc_list):
    sleep(1)
    union_iocs = list(set().union(*ioc_list))
    union_iocs = [brack.replace('[', '') for brack in union_iocs]
    union_iocs = [brack.replace(']', '') for brack in union_iocs]
    union_iocs.sort(key=lambda item: (len(item), item))
    with open(os.path.dirname(__file__) + "/config/" + "Aggregated_IOCs.txt", "r+") as ioc_file:
        ioc_file.write(str(union_iocs))
    print(union_iocs)

#----------------------------------------------------------------

def grab_iocs(tweet):
    single_tweet = str(tweet)
    hash_iocs = re.findall(r'([0-9a-fA-F]{32}|[0-9a-fA-F]{40}|[0-9a-fA-F]{64})', single_tweet)
    ipv4_iocs = re.findall(r'(\d{1,3}[\[\]\.]+\d{1,3}[\[\]\.]+\d{1,3}[\[\]\.]+\d{1,3})', single_tweet)
    ioc_list.append(hash_iocs)
    ioc_list.append(ipv4_iocs)

#----------------------------------------------------------------

def search_on_twitter(client):
    n = 0
    sleep(1)
    tweets_list = []
    twitter_accounts_list = load_accounts_file("TwitterAccounts.txt")
    twitter_accounts_details = client.get_users(usernames=twitter_accounts_list)
    twitter_accounts = str(twitter_accounts_details[0])
    today = datetime.today()
    past_hour = (today.hour - 1)
    past_day = (today.day - 1)
    daily_search_period = str((datetime(year=today.year, month=today.month, day=past_day, hour=past_hour, second=0)).isoformat() + "Z")
    sleep(1)
    print("\t[+] Gathering Tweets Starting From: " + daily_search_period)
    account_names = re.findall(r'(?: username=)(\w+)', twitter_accounts)
    account_ids = re.findall(r'(?:User id=)(\d+)', twitter_accounts)
    for account_id in account_ids:
        sleep(1)
        print("\t\t[+] Twitter Account Handle: @" + account_names[n])
        n += 1
        tweets = tweepy.Paginator(client.get_users_tweets, id=account_id, start_time=daily_search_period, max_results=100).flatten()
        for tweet in tweets:
            grab_iocs(tweet)

#----------------------------------------------------------------

def start_listen_twitter():
    client = init_twitter_config()
    print("[*] ____ Starting Script ____")
    search_on_twitter(client)
    ioc_union(ioc_list)

#----------------------------------------------------------------

if __name__ == '__main__':
    start_listen_twitter()

#----------------------------------------------------------------
