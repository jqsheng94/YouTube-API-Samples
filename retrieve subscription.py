import requests
from urllib.request import urlopen
import simplejson as json


class retrieveSubscriptionList:
    def __init__(self, channelID):
        self.channelID = channelID
        self.key = 'PUT YOUR KEY HERE'
    
    def main(self):
        subscriptionChannelIDList = []
        loopFlag = True
        loopCounter = 0
        pageToken = ''
        while loopFlag:
            if not pageToken:
                subscriptionListURL = "https://www.googleapis.com/youtube/v3/subscriptions?part=snippet&channelId=" + self.channelID + "&key=" + self.key + \
                                      "&maxResults=50"
            else:
                subscriptionListURL = "https://www.googleapis.com/youtube/v3/subscriptions?part=snippet&channelId=" + self.channelID + "&key=" + self.key + \
                                      "&maxResults=50&pageToken=" + pageToken
            subscriptionListData = []
            try:
               subscriptionListData = urlopen(subscriptionListURL)
            except:
               print('fetchSubscriptionUrl error', subscriptionListURL)
            if subscriptionListData:
               subscriptionListData = json.load(subscriptionListData)
               for results in subscriptionListData['items']:
                   if "resourceId" in results["snippet"]:
                      subscriptionChannelIDList.append(results["snippet"]["resourceId"]["channelId"])
               if "nextPageToken" in subscriptionListData:
                   pageToken = subscriptionListData["nextPageToken"]
               else:
                   loopFlag = False           
            loopCounter += 1
            if loopCounter > 10: loopFlag = False
        return subscriptionChannelIDList

##############################################################################
channelID = "UCMk_WSPy3EE16aK5HLzCJzw"
subsList = retrieveSubscriptionList(channelID).main()
print(subsList)