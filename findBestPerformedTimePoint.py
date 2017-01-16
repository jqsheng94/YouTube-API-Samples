import requests
import pymysql
import pymysql.cursors
from datetime import timedelta
from datetime import datetime
import dateutil.parser
from urllib.request import urlopen
import simplejson as json
import matplotlib.pyplot as plt
from pylab import plot, show, bar
import matplotlib.pyplot as plt
import pandas as pd, numpy as np, matplotlib.pyplot as plt
import matplotlib.cm as cm, matplotlib.font_manager
from statistics import mean
import numpy as np
from scipy.signal import find_peaks_cwt
import peakutils



class getChannelRefreshTokenLanguage():    
    def __init__(self, noChannels):
        self.noChannels = str(noChannels)
    
    def main(self):
        hostname = 'XXX'
        username = 'XXXX'
        password = 'XXXXX'
        database = 'XXXXXX'
        myConnection = pymysql.connect(host=hostname, user=username, password=password, db=database)
        cursor = myConnection.cursor()
        
        sql = "SELECT channelYid, refreshToken FROM ytChannel Where refreshToken <> '' ORDER by crawlTime DESC LIMIT " + self.noChannels + ";"
        cursor.execute(sql)
        fetchedData = cursor.fetchall()
        cursor.close()
        myConnection.close()
        
        refreshToeknList = []
        channelIDList = []
        for fetchedDataItem in fetchedData:
            channelIDList.append(fetchedDataItem[0])    
            refreshToeknList.append(fetchedDataItem[1])
        return channelIDList, refreshToeknList
 
class getVideos():   
    def __init__(self, channelID, noVideos):
        self.channelID = channelID
        self.noVideos = str(noVideos)
        self.DeveloperKey = "XXXXXXXXXXXXXXXXXXXXX"
        
    def main(self):   
        videoIDs = []
        startDates = []
        channelUrl = "https://www.googleapis.com/youtube/v3/search?key=" + self.DeveloperKey + "&channelId=" + self.channelID + "&part=snippet,id&order=date&maxResults=" + self.noVideos
        videoResults = urlopen(channelUrl)
        videoResults = json.load(videoResults)  
        for searchResult in videoResults.get("items", []):
            if 'videoId' in searchResult['id']:
                videoIDs.append(searchResult['id']['videoId'])
            if 'publishedAt' in searchResult['snippet']:
                startDates.append(searchResult['snippet']['publishedAt'])
        return videoIDs, startDates        
        

class getAnalytics():
    def __init__(self, refreshToekn, channelID, videoID, videoStartDate, videoNumberOfDays):
        self.refreshToekn = refreshToekn
        self.videoNumberOfDays = videoNumberOfDays
        self.channelID = channelID
        self.videoID = videoID
        self.videoStartDate = videoStartDate
        
    def refreshAccessToken(self):
        url = 'https://accounts.google.com/o/oauth2/token'
        payload = {
                   "client_id": "XXX",
                   "client_secret": "XXX",
                   "refresh_token": self.refreshToekn,
                   "grant_type": "refresh_token"
                  }
                  
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        r = requests.post(url, data=(payload), headers=headers)
        r = r.json()
        if 'access_token' in r:
           print('Access Token:')
           print(r['access_token'])
           accessToken = r['access_token']
        else:
           print('No Valid Token')
           accessToken = []                
        return accessToken
        
    def fetchAnalytics(self, videoID, startDate, endDate, metrics, dimension,DetailType, accesstoken):
        if videoID == '':        
            fetchUrl = "https://www.googleapis.com/youtube/analytics/v1/reports?ids=" + \
                       "channel==" + self.channelID + "&start-date=" + startDate + "&end-date=" + endDate + "&metrics=" + metrics + \
                       "&dimensions=" + dimension + "&access_token=" + accesstoken
        else:
            fetchUrl = "https://www.googleapis.com/youtube/analytics/v1/reports?ids=" + \
                       "channel==" + self.channelID + "&start-date=" + startDate + "&end-date=" + endDate + "&metrics=" + metrics + \
                       "&dimensions=" + dimension + "&filters=video=="  + videoID + "&access_token=" + accesstoken
        results = urlopen(fetchUrl)
        results = json.load(results)
        return results



    def retrieveVideoLevelResults(self):
        startDateTD = dateutil.parser.parse(self.videoStartDate)
        startDate = startDateTD.strftime('%Y-%m-%d')
        endDateTD = startDateTD + timedelta(days = self.videoNumberOfDays)
        endDate = endDateTD.strftime('%Y-%m-%d')
        metrics = "audienceWatchRatio"
        dimension = "elapsedVideoTimeRatio"
        audienceRetention = []
        if getAnalytics.accessToken:
           videoID = self.videoID
           print(videoID)
           analyticsResults = self.fetchAnalytics(videoID, startDate, endDate, metrics, dimension, '', getAnalytics.accessToken)
           if analyticsResults:
              for analyticsResult in analyticsResults['rows']:
                  audienceRetention.append(analyticsResult)
        getAnalytics.videoAnalytics = {}
        getAnalytics.videoAnalytics['AudienceRetention'] = audienceRetention
        return audienceRetention

        
    def main(self):
        getAnalytics.accessToken = self.refreshAccessToken()
        self.retrieveVideoLevelResults()
        return getAnalytics.accessToken


noChannels = 60
getChannel = getChannelRefreshTokenLanguage(noChannels)
channelIDList, refreshToeknList = getChannel.main()

channelIndex = 12
channelID = channelIDList[channelIndex]
noVideos = 50
getvideos =getVideos(channelID, noVideos)
videoIDs, startDates = getvideos.main()

videoIndex = 18
videoID = videoIDs[videoIndex]
videoStartDate = startDates[videoIndex]
videoNumberOfDays = 365
refreshToekn = refreshToeknList[channelIndex]
retrieveAnalytics = getAnalytics(refreshToekn, channelID, videoID, videoStartDate, videoNumberOfDays)
accessToken = retrieveAnalytics.main()

AudienceRetention = getAnalytics.videoAnalytics['AudienceRetention']
X = [i[0] for i in AudienceRetention]
Y = [i[1] for i in AudienceRetention]
max20to40 = max([i for i in AudienceRetention if i[0] <= 0.4 and i[0] >= 0.2], key = lambda x: float(x[1]))
max40to60 = max([i for i in AudienceRetention if i[0] <= 0.6 and i[0] > 0.4], key = lambda x: float(x[1]))
max60to80 = max([i for i in AudienceRetention if i[0] <= 0.8 and i[0] > 0.6], key = lambda x: float(x[1]))
max80to100 = max([i for i in AudienceRetention if i[0] <= 1 and i[0] > 0.8], key = lambda x: float(x[1]))
localMax = [max20to40, max40to60, max60to80, max80to100]
for i in localMax:
    rangeBefore = [t for t in AudienceRetention if t[0] >= i[0]- 0.1 and t[0] < i[0]]
    rangeAfter = [t for t in AudienceRetention if t[0] <= i[0] + 0.1 and t[0] > i[0]]
    averageBefore = mean(i[1] for i in rangeBefore)
    averageAfter = mean(i[1] for i in rangeAfter)
    if i[1] > averageAfter and i[1] > averageBefore:
        if float(i[1]/averageBefore -1) > 0.04 and float(i[1]/averageAfter -1) > 0.07:
            Xpoint = i[0]
            print (str(i[0]) + ' is the best time point with ' + str(i[1])+ " percentage of views")
        else:
            Xpoint = 0
plot(X, Y)
if Xpoint != 0:
   plt.axvline(Xpoint)
show()
