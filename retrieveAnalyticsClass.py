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
        
        sql = "SELECT channelYid, refreshToken FROM XXX Where refreshToken <> '' ORDER by crawlTime DESC LIMIT " + self.noChannels + ";"
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
        self.DeveloperKey = "PUT YOUR KEY HERE"
        
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
                   "client_secret": "XXXX",
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
        
    def fetchAnalytics(self, videoID, startDate, endDate, metrics, dimension, accesstoken):
    
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
        metrics = "audienceWatchRatio"  #Could be changed to "relativeRetentionPerformance"
        dimension = "elapsedVideoTimeRatio"
        audienceRetention = []
        audienceRetention_X = []
        audienceRetention_Y = []
        if getAnalytics.accessToken:
           videoID = self.videoID
           analyticsResults = self.fetchAnalytics(videoID, startDate, endDate, metrics, dimension, getAnalytics.accessToken)
           if analyticsResults:
              for analyticsResult in analyticsResults['rows']:
                  audienceRetention.append(analyticsResult)
                  print(analyticsResult)
                  audienceRetention_X.append(analyticsResult[0])
                  audienceRetention_Y.append(analyticsResult[1])
        getAnalytics.videoAnalytics = {}
        getAnalytics.videoAnalytics['AudienceRetention'] = audienceRetention
        plot(audienceRetention_X, audienceRetention_Y)
        show()
        return audienceRetention
        
    def main(self):
        getAnalytics.accessToken = self.refreshAccessToken()
        self.retrieveVideoLevelResults()
        return getAnalytics.accessToken, getAnalytics.videoAnalytics

noChannels = 50
getChannel = getChannelRefreshTokenLanguage(noChannels)
channelIDList, refreshToeknList = getChannel.main()

channelIndex = 7
channelID = channelIDList[channelIndex]
noVideos = 8
getvideos =getVideos(channelID, noVideos)
videoIDs, startDates = getvideos.main()

videoIndex = 2
videoID = videoIDs[videoIndex]
videoStartDate = startDates[videoIndex]
videoNumberOfDays = 60
refreshToekn = refreshToeknList[channelIndex]
retrieveAnalytics = getAnalytics(refreshToekn, channelID, videoID, videoStartDate, videoNumberOfDays)
accessToken, videoAnalytics = retrieveAnalytics.main()
print(videoAnalytics)