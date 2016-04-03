import json
import datetime, time
import matplotlib.pyplot as plt
import numpy as np
from sets import Set
import statsmodels.api as sm
import random

def cross_validation(X,Y,period):
		onelen =  len(X)/10
		cross_err = []
		cross_avg = []
		print "period: "+str(period)
		for i in range(10):
			trainSet = np.delete(X,np.s_[onelen*i:onelen*(i+1)],0)
			targetSet = np.delete(Y,np.s_[onelen*i:onelen*(i+1)],0)

			test_input = X[onelen*i:onelen*(i+1)] 
			test_real = Y[onelen*i:onelen*(i+1)]

			model = sm.OLS(targetSet, trainSet)
			results = model.fit()

			pred_err1=0
			for i in range(len(targetSet)):
				pred_err1 +=  abs(targetSet[i]-sum(results.params*trainSet[i]))
			print len(targetSet),pred_err1/len(targetSet)
			
			pred_err=0
			for i in range(onelen):
				pred_err +=  abs(test_real[i]-sum(results.params*test_input[i]))
			cross_err.append(round(pred_err/onelen,2))
			cross_avg.append(round(np.mean(test_real),2))
		avg_err=np.mean(cross_err)

		
		f = open("cross_validation_err.txt",'a')
		print>>f,"cross_error of period "+str(period)+" :"
		print>>f, cross_err
		print>>f,"cross_avg of period "+str(period)+" :"
		print>>f, cross_avg
		print>>f,"cross_error_avg of period "+str(period)+" :"
		print>>f, avg_err
		print>>f,""
		f.close()



def validation(filename):
	tweets = []
	postTime = []
	
	i = 0

	with open(filename,'r') as fp:
		for line in fp.readlines():
			try:
				tmp = json.loads(line)

				tweets.append({})
				tweets[i]['tweet'] = {}
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
	
	time1 = int(time.mktime(datetime.datetime(2015,02,01, 8,00,0).timetuple()))
	time2 = int(time.mktime(datetime.datetime(2015,02,01, 20,00,0).timetuple()))

	for i in range(len(tweets)):
		postTime.append(tweets[i]['firstpost_date'])
		
	beginTime = min(postTime)
	endTime = max(postTime)
	interval = (endTime-beginTime)/3600
	time_window = [[0 for i in range(6)] for j in range(interval+2)]
	interval1=0
	interval2=0

	for i in range(len(tweets)):
		cur_time = tweets[i]['firstpost_date']
		index = (cur_time-beginTime)/3600

		if cur_time<time1:
			interval1=index
			interval2=interval1
		elif cur_time<time2:
			interval2=index

		time_window[index][0] += 1
		time_window[index][1] += tweets[i]['tweet']['retweet_count']
		time_window[index][2] += tweets[i]['author']['followers']
		time_window[index][3] += tweets[i]['tweet']['user']['friends_count']
		time_window[index][4] = max(time_window[index][5],tweets[i]['tweet']['user']['followers_count'])
		time_window[index-1][5] = time_window[index][0]

	time_window_random = random.sample(time_window, len(time_window))

	y=[]
	for i in range(interval+1):
		y.append(time_window_random[i][5])
	x=[]
	for i in range(interval+1):
		x.append(time_window_random[i][0:5])

	X = np.array(x)
	Y = np.array(y)

	X1 = X[0:interval1+1]
	Y1 = Y[0:interval1+1]
	cross_validation(X1,Y1,0)

	X2 = X[interval1+1:interval2+1]
	Y2 = Y[interval1+1:interval2+1]
	cross_validation(X2,Y2,1)

	X3 = X[interval2:]
	Y3 = Y[interval2:]
	cross_validation(X3,Y3,2)



############################         problem4       #########################
validation('tweets_#superbowl.txt')


