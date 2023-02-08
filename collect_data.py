'''
# Collect Twitter data by hashtag (or other string) within time period using snscrape package

# CLI test
snscrape --max-results 100 --jsonl --with-entity twitter-hashtag groomer > hashtag_groomer

# References
https://github.com/JustAnotherArchivist/snscrape/blob/master/snscrape/modules/twitter.py
https://betterprogramming.pub/how-to-scrape-tweets-with-snscrape-90124ed006af
https://www.freecodecamp.org/news/python-web-scraping-tutorial/
'''

import snscrape.modules.twitter as sntwitter
import pandas as pd
import os

# Inputs
maxTweets = 100 # for testing
hashtag = '#groomer'
startdate = '2023-01-01'
enddate = '2023-02-09' # day after to get full day
outpath = ''
excludeattrs = ['json', 'source', 'description', 'username', 'content']
# TODO - parse link attributes correctly and exclude these depreciated attributes
# 'descriptionUrls', 'linkUrl', 'linkTcourl', 'outlinks', 'outlinksss', 'tcooutlinks', 'tcooutlinksss'

# Creating list to append tweets to
tweets_list = []

# Using TwitterSearchScraper to scrape data, create dict for each tweet
for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{hashtag} since:{startdate} until:{enddate}').get_items()):
    if i>maxTweets:
        break
    # Initialize tweet dict
    tdict = {}
    # Append all Tweet class attributes to tweet dict
    for a in dir(tweet):
    	if ("__" not in a) & (a not in excludeattrs):
    		# Add User attibutes seperately
    		if a == 'user':
    			for ua in dir(tweet.user):
    				if ("__" not in ua) & (ua not in excludeattrs):
    					key = 'user_' + ua
    					tdict[key] = getattr(tweet.user, ua)
    		
    		# Add other attributes
    		tdict[a] = getattr(tweet, a)

    # Append to tweets list
    tweets_list.append(tdict)

# Convert to df
df = pd.DataFrame.from_dict(tweets_list)

# Save df
df.to_csv(os.path.join(outpath, f'tweets_{hashtag}_{startdate}_{enddate}.csv'), index=False, encoding='utf-8-sig')