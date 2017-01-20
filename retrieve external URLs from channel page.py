# This script is to extract external links embedded in user's channel page info.  This info is not available in the YouTube API.

import re
from urllib.request import urlopen
import simplejson as json
import urllib.parse

class getDescriptionData():

    DeveloperKey = "PUT YOUR KEY HERE"

    def __init__(self, YtVideoId):
        self.YtVideoId = YtVideoId
        self.results = json.load(urlopen("https://www.googleapis.com/youtube/v3/videos?part=id,snippet&id=" + self.YtVideoId + "&key=" + self.DeveloperKey))
        self.description = self.videoDescription()



    def videoDescription (self):
        for searchResult in self.results.get("items", []):
            if 'description' in searchResult['snippet']:
                description = searchResult['snippet']['description']  # video description
            else:
                description = ''
        return description

    def link(self):
        Allhttp = re.findall(r"http\S+", self.description)
        Allhttp = [word.rstrip("'()[]{},.:;!#$%^&*-") for word in Allhttp]
        AllRedirectURL = []
        for i in Allhttp:
            i = urllib.parse.quote(i.encode('utf-8'), ':/=?!$%^*()-+_;`~')
            try:
                request = urlopen(i)
                AllRedirectURL.append(request.geturl())
            except:
                urllib.error.HTTPError
        return Allhttp, AllRedirectURL

YtVideoId = 'SME6c_H6LDk'
getData = getDescriptionData(YtVideoId)
URLs = getData.link()
print(URLs)
