# Filename p3_1.py
# for each hashtag, calculate:
# average number of tweets per hour
# average number of followers of users posting the tweets
# average number of retweets
# Plot:
# number of tweets in hour for #SuperBowl & #NFL

import json
import datetime, time
import matplotlib.pyplot as plt
import numpy as np
from sets import Set

def tweetsResult(filename):
	tweets = []
	followers = []
	retweets = []
	postTime = []
	uniqueTweets = []
	
	i = 0
	#tweets = {}
	uniqueTweets = Set([])

	with open(filename,'r') as fp:
		for line in fp.readlines():
			try:
				tmp = json.loads(line)

				tweets.append({})
				tweets[i]['tweet'] = {}
				tweets[i]['tweet']['retweet_count'] = tmp['tweet']['retweet_count']
				tweets[i]['firstpost_date'] = tmp['firstpost_date']
				tweets[i]['tweet']['user'] = {}
				tweets[i]['tweet']['user']['id'] = tmp['tweet']['user']['id']
				tweets[i]['tweet']['user']['followers_count'] = tmp['tweet']['user']['followers_count']
				i += 1
				
			except:
				pass


	print len(tweets),i,tweets[0]
	
	for i in range(len(tweets)):

		retweets.append(tweets[i]['tweet']['retweet_count'])
		postTime.append(tweets[i]['firstpost_date'])
		if tweets[i]['tweet']['user']['id'] in uniqueTweets:
			continue
		else:
			uniqueTweets.add(tweets[i]['tweet']['user']['id'])
			followers.append(tweets[i]['tweet']['user']['followers_count'])
	

	beginTime = min(postTime)
	endTime = max(postTime)
	numOfTweets = len(tweets)
	numOfFollowers = len(followers)
	numOfRetweets = len(retweets)
	avgTweets = numOfTweets * 3600 / (endTime - beginTime)
	avgFollowers = sum(followers) / float(numOfFollowers) 
	avgRetweets = sum(retweets) / float(numOfRetweets)
	hashtag = filename[7:-4]

	if (filename == 'tweets_#nfl.txt') or (filename == 'tweets_#superbowl.txt'):
		numofHour = (endTime - beginTime) / 3600 + 1
		seperateSum = [0] * numofHour

		for k in range(len(tweets)):
			for j in range(numofHour):
				if (tweets[k]['firstpost_date'] > (beginTime + 3600*j)) and (tweets[k]['firstpost_date'] < (beginTime + 3600*(j+1))): 
					seperateSum[j] = seperateSum[j] + 1
		plot(filename, seperateSum, numofHour)

	statisticalResult = file('statisticalResult.txt','a')

	statisticalResult.write('{hfn}\n  average number of tweets per hour: {nt}\n   average number of followers: {nf}\n    average number of retweets: {nr}\n\n'.format(hfn = hashtag, nt = avgTweets, nf = avgFollowers, nr = avgRetweets))

	statisticalResult.close()

def plot(filename, seperateSum, numofHour):
	index = np.arange(numofHour)   
	plt.plot(index, seperateSum)
	plt.xlabel('Time Interval')  
	plt.ylabel('Number of Tweets')  
	plt.title('Average Number of Tweets Per Hour of ' + filename)
	plt.show()

############################         problem1        #########################
hashFilename = ['tweets_#gohawks.txt', 'tweets_#gopatriots.txt', 'tweets_#nfl.txt', 'tweets_#patriots.txt', 'tweets_#sb49.txt', 'tweets_#superbowl.txt']
for i in range(6):
	tweetsResult(hashFilename[i])


