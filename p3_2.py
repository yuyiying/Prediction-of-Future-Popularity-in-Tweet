import json
import datetime, time
from sets import Set
import statsmodels.api as sm

def resultSummary(filename):
	tweets = []
	postTime = []
	
	i = 0
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
	time_window = [[0 for i in range(5)] for j in range(interval+2)]

	for i in range(len(tweets)):
		cur_time = tweets[i]['firstpost_date']
		index = (cur_time-beginTime)/3600
		time_window[index][0] += 1
		time_window[index][1] += tweets[i]['tweet']['retweet_count']
		time_window[index][2] += tweets[i]['author']['followers']
		time_window[index][3] = max(time_window[index][3],tweets[i]['tweet']['user']['followers_count'])
		cur_time = time.strftime('%H:%M:%S', time.gmtime(cur_time))
		time_window[index][4] = int(cur_time[0])

	nextHour=[]
	for i in range(interval+1):
		nextHour.append(time_window[i+1][0])
	del time_window[-1]
	X = np.array(time_window)
	Y = np.array(nextHour)
	ols_model = sm.OLS(Y, X)
	ols_results = ols_model.fit()

	hashtag=filename[7:-4]

	Time_Windows = open('Time_Windows', 'a')
	print>>Time_Windows, hashtag
	print>>Time_Windows, time_window
	Time_Windows.close()

	Linear_Regression_Model = open('Linear_Regression_Model', 'a')
	print>>Linear_Regression_Model, hashtag
	print>>Linear_Regression_Model, ols_results.summary()
	Linear_Regression_Model.close()


############################         problem2       #########################
hashFilename = ['tweets_#gohawks.txt', 'tweets_#gopatriots.txt', 'tweets_#nfl.txt', 'tweets_#patriots.txt', 'tweets_#sb49.txt', 'tweets_#superbowl.txt']
for i in range(6):
	resultSummary(hashFilename[i])
