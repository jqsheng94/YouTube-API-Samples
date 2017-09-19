from urllib.request import urlopen
import numpy as np
import simplejson as json
import re
from datetime import datetime, timedelta, date




class getAnalytics(object):
    def __init__(self, **kwargs):
        self.channelID = kwargs.get("channelID")
        self.startDate = kwargs.get("publishAfter")
        self.DeveloperKey = "PUT YOUR KEY HERE"
        self.noVideos = str(50)
        self.videoList = self.main()

    def main(self):
        videoMeta = []
        next_page_token = ''
        while next_page_token is not None:
            channelUrl = "https://www.googleapis.com/youtube/v3/search?key=" + self.DeveloperKey + "&channelId=" + self.channelID + "&part=snippet,id&order=date&maxResults=" + self.noVideos + "&pageToken=" + next_page_token
            videoResults = urlopen(channelUrl)
            videoResults = json.load(videoResults)
            for searchResult in videoResults.get("items", []):
                if 'videoId' in searchResult['id']:
                    videoId =searchResult['id']['videoId']
                    if 'publishedAt' in searchResult['snippet']:
                        publish = searchResult['snippet']['publishedAt']
                        title = searchResult['snippet']['title']
                        Diff = (date(int(publish[0:4]), int(publish[5:7]), int(publish[8:10])) - date(int(self.startDate[0:4]), int(self.startDate[5:7]), int(self.startDate[8:10]))).days
                        if Diff >= 0 :
                            videoMeta.append((videoId, publish, title))
            next_page_token = videoResults.get('nextPageToken')
        return videoMeta

    def videoDuration(self):
      NewVideoMeta = []
      for i in self.videoList:
        VideoId = i[0]
        VideoURL = 'https://www.googleapis.com/youtube/v3/videos?part=contentDetails,liveStreamingDetails&id=' + VideoId + '&key=' + self.DeveloperKey
        videoResults = urlopen(VideoURL)
        videoResults = json.load(videoResults)
        for searchResult in videoResults.get("items", []):
          if 'duration' in searchResult['contentDetails']:
            videoDuration = searchResult['contentDetails']['duration']
            S = re.findall(r"(\d+)S", videoDuration)
            M = re.findall(r"(\d+)M", videoDuration)
            H = re.findall(r"(\d+)H", videoDuration)
            D = re.findall(r"(\d+)D", videoDuration)
            if len(S) == 0:
              S = 0
            else:
              S = int(S[0])
            if len(M) == 0:
              M = 0
            else:
              M = int(M[0])
            if len(H) == 0:
              H = 0
            else:
              H = int(H[0])
            if len(D) == 0:
              D = 0
            else:
              D = int(D[0])
            videoDuration = S + M * 60 + H * 3600 + D * 86400
          else:
            videoDuration = 0
          if 'liveStreamingDetails' in searchResult:
            live = 'live'
          else:
            live = 'regular'
        i = list(i)
        i.insert(3, videoDuration)
        i.insert(4, live)
        NewVideoMeta.append(i)
      return NewVideoMeta


videoMeta= getAnalytics(channelID = 'UCBMvWaA97BAegvJ_Hz6Vwuw', publishAfter = '2017-01-01').videoDuration()
print(videoMeta)
