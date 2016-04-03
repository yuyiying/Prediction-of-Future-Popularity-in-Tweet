import json
import datetime, time
import matplotlib.pyplot as plt
import numpy as np
from sets import Set
import statsmodels.api as sm

def ourmodel(filename):
	tweets = []
	postTime = []
	
	i = 0
	#tweets = {}
	uniqueTweets = Set([])

	with open(filename,'r') as fp:
		for line in fp.readlines():
			try:
				tmp = json.loads(line)

				tweets.append({})
				tweets[i]['tweet'] = {}
				tweets[i]['tweet']['favorite_count'] = tmp['tweet']['favorite_count']
				tweets[i]['tweet']['retweet_count'] = tmp['tweet']['retweet_count']
				tweets[i]['firstpost_date'] = tmp['firstpost_date']
				tweets[i]['tweet']['user'] = {}
				tweets[i]['tweet']['user']['friends_count'] = tmp['tweet']['user']['friends_count']
				tweets[i]['tweet']['user']['id'] = tmp['tweet']['user']['id']
				tweets[i]['tweet']['user']['followers_count'] = tmp['tweet']['user']['followers_count']
				tweets[i]['author'] = {}
				tweets[i]['author']['followers'] = tmp['author']['followers']
				

				i += 1
				if i % 10000 == 0:
					print i

			except:
				pass


	print len(tweets),i,tweets[0]
	
	for i in range(len(tweets)):
		postTime.append(tweets[i]['firstpost_date'])
		

	beginTime = min(postTime)
	endTime = max(postTime)
	interval = (endTime-beginTime)/3600
	time_window = [[0 for i in range(7)] for j in range(interval+2)]

	for i in range(len(tweets)):
		cur_time = tweets[i]['firstpost_date']
		index = (cur_time-beginTime)/3600
		time_window[index][0] += 1
		time_window[index][1] += tweets[i]['tweet']['retweet_count']
		time_window[index][2] += tweets[i]['author']['followers']
		time_window[index][3] += tweets[i]['tweet']['favorite_count']
		time_window[index][4] += tweets[i]['tweet']['user']['friends_count']
		time_window[index][5] = max(time_window[index][5],tweets[i]['tweet']['user']['followers_count'])

	nextHour=[]
	for i in range(interval+1):
		nextHour.append(time_window[i+1][0])
		time_window[i][6] = time_window[i][0]-time_window[i-1][0]
	del time_window[-1]
	X = np.array(time_window)
	Y = np.array(nextHour)
	ols_model = sm.OLS(Y, X)
	ols_results = ols_model.fit()


	hashtag=filename[7:-4]

	ourTime_Windows = open('ourTime_Windows', 'a')
	print>>ourTime_Windows, hashtag
	print>>ourTime_Windows, time_window
	ourTime_Windows.close()

	ourLinear_Regression_Model = open('ourLinear_Regression_Model', 'a')
	print>>ourLinear_Regression_Model, hashtag
	print>>ourLinear_Regression_Model, ols_results.summary()
	ourLinear_Regression_Model.close()




############################         problem3       #########################
hashFilename = ['tweets_#gohawks.txt', 'tweets_#gopatriots.txt', 'tweets_#nfl.txt', 'tweets_#patriots.txt', 'tweets_#sb49.txt', 'tweets_#superbowl.txt']
Xall = []
Yall = []
for i in range(6):
	ourmodel(hashFilename[i])
	Xall.append(X)
	Yall.append(Y)

plt.scatter(Xall[:,0],Yall) #top3 feature: number of tweets, sum of number of followers posintg the hash, number of friends of all users
plt.show()
plt.scatter(Xall[:,5],Yall)
plt.show()
plt.scatter(Xall[:,4],Yall)
plt.show()


