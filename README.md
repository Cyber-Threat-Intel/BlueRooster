# **BlueRooster**
I would like to thank Aleprada for their script "ioc_tweets", as this was the main idea/template for the BlueRooster project to extract IOCs from Twitter.
* [ioc_tweets](https://github.com/aleprada/ioc_tweets)


### **Status Information**
* Twitter Access Level
  * This scpipt is built to use an account's access level of "Essential".
    * See further details on [Twitter's Dev Portal](https://developer.twitter.com/en/docs/twitter-api/getting-started/about-twitter-api)
* PyMISP Utilization - _Currently Not Available_
  * The additional implimentation of aggregating IOCs into a MISP instance is not currently available but will be in the near future.
    * See further details about on [PyMISP's GitHub page](https://github.com/MISP/PyMISP)
    * For more infomation about using as an IOC aggregator/threat intel platform see their main webiste [MISP](https://www.misp-project.org/)


### **Script Details**
1. This script works by using [Tweepy](https://docs.tweepy.org) which will look up a Twitter's "account_id" and grab their recent tweets/re-tweets.
  * . _Currently built to look over the past 24-25 hours. It will search from the bottom of the hour_ 
2. After, the tweets from each account has been pulled from Twitter, it will then perform a regex "findall" for any IPv4 strings and hash values.
  * _Currently MD5, SHA-1, & SHA-256_
  * _Future patch will include domains, URLs and emails_
3. Finally, it will print a sorted list by string length, and then alphabetically.
  * _Future patch will include sortting by IOC type_


### **How it Works**
1. You will need to add in your bearer token
  * See further details about the different authentication methods on Twitter's dev page [Twitter Authentication](https://developer.twitter.com/en/docs/authentication/overview)
 * [EDITING] 2. You will need to add every Twitter Account username/handle within the "TwitterAccounts.txt" file.

'''
bearer_token = "your_bearer_token"
'''

