import requests
import pymysql
import pymysql.cursors
from datetime import timedelta
from datetime import datetime
from urllib.request import urlopen
import simplejson as json
import dateutil.relativedelta
import numpy as np
import dateutil.parser


class getChannelRefreshTokenLanguage():
    def __init__(self, noChannels):
        self.noChannels = str(noChannels)

    def main(self):
        hostname = 'XXXX'
        username = 'XXXXX'
        password = 'XXXXXX'
        database = 'XXXXXXX'
        myConnection = pymysql.connect(host=hostname, user=username, password=password, db=database)
        cursor = myConnection.cursor()

        sql = "SELECT channelYid, refreshToken, language FROM ytChannel Where refreshToken <> '' ORDER by crawlTime DESC LIMIT " + self.noChannels + ";"
        cursor.execute(sql)
        fetchedData = cursor.fetchall()
        cursor.close()
        myConnection.close()

        refreshToeknList = []
        channelIDList = []
        languageList = []
        for fetchedDataItem in fetchedData:
            channelIDList.append(fetchedDataItem[0])
            refreshToeknList.append(fetchedDataItem[1])
            languageList.append(fetchedDataItem[2])
        return channelIDList, refreshToeknList, languageList


class getVideos():
    def __init__(self, channelID):
        self.channelID = channelID
        self.noVideos = str(50)
        self.DeveloperKey = "XXXX"

    def main(self):
        videoIDs = []
        startDates = []
        next_page_token = ''
        while next_page_token is not None:
            channelUrl = "https://www.googleapis.com/youtube/v3/search?key=" + self.DeveloperKey + "&channelId=" + self.channelID + "&part=snippet,id&order=date&maxResults=" + self.noVideos + "&pageToken=" + next_page_token
            videoResults = urlopen(channelUrl)
            videoResults = json.load(videoResults)
            for searchResult in videoResults.get("items", []):
                if 'videoId' in searchResult['id']:
                    videoIDs.append(searchResult['id']['videoId'])
                if 'publishedAt' in searchResult['snippet']:
                    startDates.append(searchResult['snippet']['publishedAt'])
            next_page_token = videoResults.get('nextPageToken')
        return videoIDs, startDates


class getAnalytics():
    def __init__(self, refreshToekn, channelID):
        self.refreshToekn = refreshToekn
        self.channelID = channelID

    def refreshAccessToken(self):
        url = 'https://accounts.google.com/o/oauth2/token'
        payload = {
            "client_id": "XXXX",
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

    def fetchAnalytics(self, videoID, startDate, endDate, metrics, dimension, accesstoken, sortCrit, filterstat,
                       country):

        if sortCrit:
            fetchUrl = "https://www.googleapis.com/youtube/analytics/v1/reports?ids=" + \
                       "channel==" + self.channelID + "&start-date=" + startDate + "&end-date=" + endDate + "&metrics=" + metrics + \
                       "&dimensions=" + dimension + "&filters=" + filterstat + "&max-results=10&sort=" + sortCrit + "&access_token=" + accesstoken
        elif (videoID == '') and (country == ''):
            fetchUrl = "https://www.googleapis.com/youtube/analytics/v1/reports?ids=" + \
                       "channel==" + self.channelID + "&start-date=" + startDate + "&end-date=" + endDate + "&metrics=" + metrics + \
                       "&dimensions=" + dimension + "&access_token=" + accesstoken
        elif (videoID == '') and (country != ''):
            fetchUrl = "https://www.googleapis.com/youtube/analytics/v1/reports?ids=" + \
                       "channel==" + self.channelID + "&start-date=" + startDate + "&end-date=" + endDate + "&metrics=" + metrics + \
                       "&dimensions=" + dimension + "&filters=country==" + country + "&access_token=" + accesstoken
        else:
            fetchUrl = "https://www.googleapis.com/youtube/analytics/v1/reports?ids=" + \
                       "channel==" + self.channelID + "&start-date=" + startDate + "&end-date=" + endDate + "&metrics=" + metrics + \
                       "&dimensions=" + dimension + "&filters=video==" + videoID + "&access_token=" + accesstoken
        results = urlopen(fetchUrl)
        results = json.load(results)
        return results

    def fetchTrafficSource(self, videoID, startDate, endDate, metrics, dimension, DetailType, accesstoken, sortCrit,
                           maxResults):
        fetchUrl = "https://www.googleapis.com/youtube/analytics/v1/reports?ids=" + \
                   "channel==" + self.channelID + "&start-date=" + startDate + "&end-date=" + endDate + "&metrics=" + metrics + \
                   "&dimensions=" + dimension + "&filters=video==" + videoID + ";insightTrafficSourceType==" + DetailType + "&max-results=" + maxResults + "&sort=-" + sortCrit + "&access_token=" + accesstoken
        results = urlopen(fetchUrl)
        results = json.load(results)
        return results

    def retrieveChannelLevelResults(self, accessToken, country, dimension, channelNumberOfDaysMonthsWeeks):
        metrics = "likes,dislikes,views,shares,comments,averageViewDuration,subscribersGained," + \
                  "subscribersLost,estimatedMinutesWatched,annotationCloseRate,annotationClickThroughRate"
        if (dimension == "day") or (dimension == "7DayTotals"):
            now = datetime.now()
            endDate = now.strftime('%Y-%m-%d')
            startDateTD = now - timedelta(days=channelNumberOfDaysMonthsWeeks)
            startDate = startDateTD.strftime('%Y-%m-%d')
        elif dimension == "month":
            now = datetime.now()
            now = now.replace(day=1)
            endDate = now.strftime('%Y-%m-%d')
            startDateTD = now + dateutil.relativedelta.relativedelta(months=-channelNumberOfDaysMonthsWeeks)
            startDate = startDateTD.strftime('%Y-%m-%d')

        sortCriterion = []
        filterStatement = []

        videoID = ''
        getAnalytics.channelAnalytics = {}
        if accessToken:
            channelAnalyticsResults = self.fetchAnalytics(videoID, startDate, endDate, metrics, dimension, accessToken,
                                                          sortCriterion, filterStatement, country)
            if 'rows' in channelAnalyticsResults:
                for analyticsResult in channelAnalyticsResults['rows']:
                    (getAnalytics.channelAnalytics).setdefault('Channel Dates', []).append(analyticsResult[0])
                    (getAnalytics.channelAnalytics).setdefault('Channel Likes', []).append(analyticsResult[1])
                    (getAnalytics.channelAnalytics).setdefault('Channel Dislikes', []).append(analyticsResult[2])
                    (getAnalytics.channelAnalytics).setdefault('Channel Views', []).append(analyticsResult[3])
                    (getAnalytics.channelAnalytics).setdefault('Channel Shares', []).append(analyticsResult[4])
                    (getAnalytics.channelAnalytics).setdefault('Channel Comments', []).append(analyticsResult[5])
                    (getAnalytics.channelAnalytics).setdefault('Channel Average View Duration', []).append(
                        analyticsResult[6])
                    (getAnalytics.channelAnalytics).setdefault('Channel Subscribers Gained', []).append(
                        analyticsResult[7])
                    (getAnalytics.channelAnalytics).setdefault('Channel Subscribers Lost', []).append(
                        analyticsResult[8])
                    (getAnalytics.channelAnalytics).setdefault('Channel Estimated Minutes Watched', []).append(
                        analyticsResult[9])
                    (getAnalytics.channelAnalytics).setdefault('Channel Annotation Close Rate', []).append(
                        analyticsResult[10])
                    (getAnalytics.channelAnalytics).setdefault('Channel Annotation Click Through Rate', []).append(
                        analyticsResult[11])
        return getAnalytics.channelAnalytics

    def retrieveDemographicAnalytics(self, accessToken, numberOfDays, videoID, country):
        now = datetime.now()
        endDate = now.strftime('%Y-%m-%d')
        startDateTD = now - timedelta(days=numberOfDays)
        startDate = startDateTD.strftime('%Y-%m-%d')
        metrics = "viewerPercentage"
        dimension = "ageGroup,gender"
        sortCriterion = []
        filterStatement = []
        demographicInfo = []
        if accessToken:
            analyticsResults = self.fetchAnalytics(videoID, startDate, endDate, metrics, dimension, accessToken,
                                                   sortCriterion, filterStatement, country)
            if 'rows' in analyticsResults:
                demographicInfo = analyticsResults['rows']
        return demographicInfo



noChannels = 20
getChannel = getChannelRefreshTokenLanguage(noChannels)
channelIDList, refreshToeknList, languageList = getChannel.main()

channelIndex = 8
channelID = channelIDList[channelIndex]
getvideos = getVideos(channelID)
videoIDs, startDates = getvideos.main()

channelNumberOfDays = 31
channelNumberOfMonths = 12
channelNumberOfWeeks = 20
channelNumberOfDaysForDemographic = 50

refreshToekn = refreshToeknList[channelIndex]
country = ''
retrieveChannelAnalytics = getAnalytics(refreshToekn, channelID)
accessToken = retrieveChannelAnalytics.refreshAccessToken()

dailyChannelAnalytics = retrieveChannelAnalytics.retrieveChannelLevelResults(accessToken, country, 'day', channelNumberOfDays)
print(dailyChannelAnalytics)
monthlyChannelAnalytics = retrieveChannelAnalytics.retrieveChannelLevelResults(accessToken, country, 'month', channelNumberOfMonths)
print(monthlyChannelAnalytics)
weeklyChannelAnalytics = retrieveChannelAnalytics.retrieveChannelLevelResults(accessToken, country, '7DayTotals', channelNumberOfWeeks)
print(weeklyChannelAnalytics)
demographicChannelAnalytics = retrieveChannelAnalytics.retrieveDemographicAnalytics(accessToken, channelNumberOfDaysForDemographic,  '', country)
print(demographicChannelAnalytics)




