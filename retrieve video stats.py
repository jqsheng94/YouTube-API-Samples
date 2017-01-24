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
        hostname = 'XXX'
        username = 'XXXX'
        password = 'XXXXX'
        database = 'XXXXXX'
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
        self.DeveloperKey = "XXXXX"

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
            "client_id": "1091265123933-qn01tf22vr5s73mlh026284m9absk154.apps.googleusercontent.com",
            "client_secret": "cNAfQv1tqf8o2B3LzNAT4jz9",
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


    def retrieveVideoLevelResults(self, accessToken, videoID, dimension, videoNumberOfDaysMonthsWeeks):
        metrics = "likes,dislikes,views,shares,comments,averageViewDuration,subscribersGained," + \
                  "subscribersLost,estimatedMinutesWatched,annotationCloseRate,annotationClickThroughRate"

        if (dimension == "day") or (dimension == "7DayTotals"):
            now = datetime.now()
            endDate = now.strftime('%Y-%m-%d')
            startDateTD = now - timedelta(days=videoNumberOfDaysMonthsWeeks)
            startDate = startDateTD.strftime('%Y-%m-%d')
        elif dimension == "month":
            now = datetime.now()
            now = now.replace(day=1)
            endDate = now.strftime('%Y-%m-%d')
            startDateTD = now + dateutil.relativedelta.relativedelta(months=-videoNumberOfDaysMonthsWeeks)
            startDate = startDateTD.strftime('%Y-%m-%d')

        sortCriterion = []
        filterStatement = []
        getAnalytics.videoAnalytics = {}
        if accessToken:
            analyticsResults = self.fetchAnalytics(videoID, startDate, endDate, metrics, dimension, accessToken,
                                                   sortCriterion, filterStatement, '')
            if 'rows' in analyticsResults:
                for analyticsResult in analyticsResults['rows']:
                    (getAnalytics.videoAnalytics).setdefault('Dates', []).append(analyticsResult[0])
                    (getAnalytics.videoAnalytics).setdefault('Likes', []).append(analyticsResult[1])
                    (getAnalytics.videoAnalytics).setdefault('Dislikes', []).append(analyticsResult[2])
                    (getAnalytics.videoAnalytics).setdefault('Views', []).append(analyticsResult[3])
                    (getAnalytics.videoAnalytics).setdefault('Shares', []).append(analyticsResult[4])
                    (getAnalytics.videoAnalytics).setdefault('Comments', []).append(analyticsResult[5])
                    (getAnalytics.videoAnalytics).setdefault('Average View Duration', []).append(analyticsResult[6])
                    (getAnalytics.videoAnalytics).setdefault('Subscribers Gained', []).append(analyticsResult[7])
                    (getAnalytics.videoAnalytics).setdefault('Subscribers Lost', []).append(analyticsResult[8])
                    (getAnalytics.videoAnalytics).setdefault('Estimated Minutes Watched', []).append(analyticsResult[9])
                    (getAnalytics.videoAnalytics).setdefault('Annotation Close Rate', []).append(analyticsResult[10])
                    (getAnalytics.videoAnalytics).setdefault('Annotation Click Through Rate', []).append(
                        analyticsResult[11])
        return getAnalytics.videoAnalytics


    def retrieveUploadVideoLevelResults(self, accessToken, videoID, videoStartDate, uploadVideoNumberOfDays):
        metrics = "likes,dislikes,views,shares,comments,averageViewDuration,subscribersGained," + \
                  "subscribersLost,estimatedMinutesWatched,annotationCloseRate,annotationClickThroughRate"
        dimension = "day"
        startDateTD = dateutil.parser.parse(videoStartDate)
        startDate = startDateTD.strftime('%Y-%m-%d')
        endDateTD = startDateTD + timedelta(days=uploadVideoNumberOfDays)
        endDate = endDateTD.strftime('%Y-%m-%d')

        sortCriterion = []
        filterStatement = []
        getAnalytics.uploadVideoAnalytics = {}
        if accessToken:
            analyticsResults = self.fetchAnalytics(videoID, startDate, endDate, metrics, dimension, accessToken,
                                                   sortCriterion, filterStatement, '')
            if 'rows' in analyticsResults:
                for analyticsResult in analyticsResults['rows']:
                    (getAnalytics.uploadVideoAnalytics).setdefault('Dates', []).append(analyticsResult[0])
                    (getAnalytics.uploadVideoAnalytics).setdefault('Likes', []).append(analyticsResult[1])
                    (getAnalytics.uploadVideoAnalytics).setdefault('Dislikes', []).append(analyticsResult[2])
                    (getAnalytics.uploadVideoAnalytics).setdefault('Views', []).append(analyticsResult[3])
                    (getAnalytics.uploadVideoAnalytics).setdefault('Shares', []).append(analyticsResult[4])
                    (getAnalytics.uploadVideoAnalytics).setdefault('Comments', []).append(analyticsResult[5])
                    (getAnalytics.uploadVideoAnalytics).setdefault('Average View Duration', []).append(
                        analyticsResult[6])
                    (getAnalytics.uploadVideoAnalytics).setdefault('Subscribers Gained', []).append(analyticsResult[7])
                    (getAnalytics.uploadVideoAnalytics).setdefault('Subscribers Lost', []).append(analyticsResult[8])
                    (getAnalytics.uploadVideoAnalytics).setdefault('Estimated Minutes Watched', []).append(
                        analyticsResult[9])
                    (getAnalytics.uploadVideoAnalytics).setdefault('Annotation Close Rate', []).append(
                        analyticsResult[10])
                    (getAnalytics.uploadVideoAnalytics).setdefault('Annotation Click Through Rate', []).append(
                        analyticsResult[11])
        return getAnalytics.uploadVideoAnalytics



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

videoNumberOfDays = 31
videoNumberOfMonths = 12
videoNumberOfWeeks = 20
videoNumberOfDaysForDemographic = 50
uploadVideoNumberOfDays = 30

refreshToekn = refreshToeknList[channelIndex]
country = ''
retrieveChannelAnalytics = getAnalytics(refreshToekn, channelID)
accessToken = retrieveChannelAnalytics.refreshAccessToken()


demographicVideoAnalytics = {}

retrieveAnalytics = getAnalytics(refreshToekn, channelID)
for idx, videoID in enumerate(videoIDs):
    print(videoID)
    dailyVideoAnalytics = retrieveAnalytics.retrieveVideoLevelResults(accessToken, videoID, 'day', videoNumberOfDays)
    print(dailyVideoAnalytics)
    monthlyVideoAnalytics = retrieveAnalytics.retrieveVideoLevelResults(accessToken, videoID, 'month', videoNumberOfMonths)
    print(monthlyVideoAnalytics)
    weeklyVideoAnalytics = retrieveAnalytics.retrieveVideoLevelResults(accessToken, videoID, '7DayTotals', videoNumberOfWeeks)
    print(weeklyVideoAnalytics)
    demographicVideoAnalytics[videoID] = retrieveAnalytics.retrieveDemographicAnalytics(accessToken, videoNumberOfDaysForDemographic, videoID, '')
    print(demographicVideoAnalytics[videoID])
    uploadVideoAnalytics = retrieveAnalytics.retrieveUploadVideoLevelResults(accessToken, videoID, startDates[idx],uploadVideoNumberOfDays)
    print(uploadVideoAnalytics)

