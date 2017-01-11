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
        
    def fetchAnalytics(self, videoID, startDate, endDate, metrics, dimension, accesstoken):
        if videoID == '':        
            fetchUrl = "https://www.googleapis.com/youtube/analytics/v1/reports?ids=" + \
                       "channel==" + self.channelID + "&start-date=" + startDate + "&end-date=" + endDate + "&metrics=" + metrics + \
                       "&dimensions=" + dimension + "&access_token=" + accesstoken
        elif dimension == 'insightTrafficSourceDetail':
            fetchUrl = "https://www.googleapis.com/youtube/analytics/v1/reports?ids=" + \
                       "channel==" + self.channelID + "&start-date=" + startDate + "&end-date=" + endDate + "&metrics=" + metrics + \
                       "&dimensions=" + dimension + "&filters=video==" + videoID + ";insightTrafficSourceType==YT_SEARCH&max-results=10&sort=-views" + "&access_token=" + accesstoken
        else:
            fetchUrl = "https://www.googleapis.com/youtube/analytics/v1/reports?ids=" + \
                       "channel==" + self.channelID + "&start-date=" + startDate + "&end-date=" + endDate + "&metrics=" + metrics + \
                       "&dimensions=" + dimension + "&filters=video=="  + videoID + "&access_token=" + accesstoken
        results = urlopen(fetchUrl)
        results = json.load(results)
        return results


    def retrieveTrafficSourceType(self):
        startDateTD = dateutil.parser.parse(self.videoStartDate)
        startDate = startDateTD.strftime('%Y-%m-%d')
        endDateTD = startDateTD + timedelta(days = self.videoNumberOfDays)
        endDate = endDateTD.strftime('%Y-%m-%d')
        metrics = "views"
        dimension1 = "insightTrafficSourceType"
        dimension2 = "insightTrafficSourceDetail"
        TrafficSourceType = []
        TrafficSourceDetail = []
        if getAnalytics.accessToken:
           videoID = self.videoID
           analyticsResults1 = self.fetchAnalytics(videoID, startDate, endDate, metrics, dimension1, getAnalytics.accessToken)
           analyticsResults2 = self.fetchAnalytics(videoID, startDate, endDate, metrics, dimension2, getAnalytics.accessToken)
           if analyticsResults1:
              for analyticsResult in analyticsResults1['rows']:
                  TrafficSourceType.append(analyticsResult)
           if analyticsResults2:
              for analyticsResult in analyticsResults2['rows']:
                  TrafficSourceDetail.append(analyticsResult)
        getAnalytics.videoAnalytics1 = {}
        getAnalytics.videoAnalytics1['insightTrafficSourceType'] = TrafficSourceType
        getAnalytics.videoAnalytics1['insightTrafficSourceDetail'] = TrafficSourceDetail
        return TrafficSourceType, TrafficSourceDetail
        
    def main(self):
        getAnalytics.accessToken = self.refreshAccessToken()
        self.retrieveTrafficSourceType()
        return getAnalytics.accessToken, getAnalytics.videoAnalytics1


def gbplot_pie(fractions, labels, cm_name='Pastel1', autopct='%1.1f%%', labeldistance=1.05, shadow=True, startangle=90, edgecolor='w', width=8, height=8, grouping_threshold=None, grouping_label=None):  # what the label the grouped wedge
    if not grouping_threshold == None:
        if grouping_label == None:
            grouping_label = 'Others'
        row_mask = fractions > grouping_threshold
        meets_threshold = fractions[row_mask]
        all_others = pd.Series(fractions[~row_mask].sum())
        all_others.index = [grouping_label]
        fractions = meets_threshold.append(all_others)
        labels = fractions.index
    color_map = cm.get_cmap(cm_name)
    num_of_colors = len(fractions)
    colors = color_map([x / float(num_of_colors) for x in range(num_of_colors)])
    fig, ax = plt.subplots(figsize=[width, height])
    wedges = ax.pie(fractions, labels=labels, labeldistance=labeldistance, autopct=autopct, colors=colors, shadow=shadow, startangle=startangle)
    for wedge in wedges[0]:
        wedge.set_edgecolor(edgecolor)

def plotBarChart (YouTubeSearchTerms_X, YouTubeSearchTerms_Y):
    fig, ax = plt.subplots(figsize=[10, 6])
    index = np.arange(len(YouTubeSearchTerms_Y))
    bar_width = 0.8
    plt.barh(index, YouTubeSearchTerms_Y, bar_width, alpha=0.4, color='lightcoral', label='Number of views',align='center', edgecolor='w')
    plt.yticks(index, YouTubeSearchTerms_X)
    plt.legend()
    plt.tight_layout()
    plt.margins(0.05)
    plt.xlim(xmin=0)
    plt.show()


noChannels = 50
getChannel = getChannelRefreshTokenLanguage(noChannels)
channelIDList, refreshToeknList = getChannel.main()

channelIndex = 12
channelID = channelIDList[channelIndex]
noVideos = 10
getvideos =getVideos(channelID, noVideos)
videoIDs, startDates = getvideos.main()

videoIndex = 1
videoID = videoIDs[videoIndex]
videoStartDate = startDates[videoIndex]
videoNumberOfDays = 60
refreshToekn = refreshToeknList[channelIndex]
retrieveAnalytics = getAnalytics(refreshToekn, channelID, videoID, videoStartDate, videoNumberOfDays)
accessToken, videoAnalytics1 = retrieveAnalytics.main()
insightTrafficSourceType = videoAnalytics1['insightTrafficSourceType']
print(insightTrafficSourceType)
insightTrafficSourceType_X = [i[0] for i in insightTrafficSourceType]
insightTrafficSourceType_Y = [i[1] for i in insightTrafficSourceType]
gbplot_pie(fractions = insightTrafficSourceType_Y,
           labels = insightTrafficSourceType_X)
print(videoAnalytics1['insightTrafficSourceDetail'])
YouTubeSearchTerms_X = [i[0] for i in videoAnalytics1['insightTrafficSourceDetail'] if i[0] != 'unknown']
YouTubeSearchTerms_Y = [i[1] for i in videoAnalytics1['insightTrafficSourceDetail'] if i[0] != 'unknown']
plotBarChart(YouTubeSearchTerms_X, YouTubeSearchTerms_Y)