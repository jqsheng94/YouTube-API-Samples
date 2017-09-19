import requests
from urllib.request import urlopen
import simplejson as json
import configparser


class retrieveSubscriptionList:
    def __init__(self, **kwargs):
        Config = configparser.ConfigParser()
        Config.read("configuration/config.ini")
        self.key = Config['YTKeys']['apikey']
        self.channelID = kwargs.get("channelID")
    
    def main(self):
        subscriptionChannelIDList = []
        loopFlag = True
        loopCounter = 0
        pageToken = ''
        while loopFlag:
            if not pageToken:
                subscriptionListURL = "https://www.googleapis.com/youtube/v3/subscriptions?part=snippet&channelId=" + self.channelID + "&key=" + self.key + \
                                      "&maxResults=50&order=relevance"
            else:
                subscriptionListURL = "https://www.googleapis.com/youtube/v3/subscriptions?part=snippet&channelId=" + self.channelID + "&key=" + self.key + \
                                      "&maxResults=50&order=relevance&pageToken=" + pageToken
            subscriptionListData = []
            try:
               subscriptionListData = urlopen(subscriptionListURL)
            except:
                pass
               # print('fetchSubscriptionUrl error', subscriptionListURL)
            if subscriptionListData:
               subscriptionListData = json.load(subscriptionListData)
               for results in subscriptionListData['items']:
                   if "resourceId" in results["snippet"]:
                      subscriptionChannelIDList.append(results["snippet"]["resourceId"]["channelId"])
               if "nextPageToken" in subscriptionListData:
                   pageToken = subscriptionListData["nextPageToken"]
               else:
                   loopFlag = False
            else:
                loopFlag = False
            loopCounter += 1
            if loopCounter > 10: loopFlag = False
        return subscriptionChannelIDList

##############################################################################

# subsList = retrieveSubscriptionList(channelID = "UCMk_WSPy3EE16aK5HLzCJzw").main()
# print(subsList)
