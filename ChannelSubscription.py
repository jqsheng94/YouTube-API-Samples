from urllib.request import urlopen
import simplejson as json


ChannelID = 'UCaK87UTTMacD35eQITej2VA' # own channel
DeveloperKey = "PUT YOUR KEY HERE"
part = 'snippet,contentDetails'
maxResults = '50'
List = []
Url = "https://www.googleapis.com/youtube/v3/subscriptions?key=" + DeveloperKey + "&channelId=" + ChannelID + "&part="+ part + "&maxResults=" +maxResults + "&textFormat=plainText"
Results = urlopen(Url)
Results = json.load(Results)
for searchResult in Results.get("items", []):
    if 'snippet' in searchResult:
        Snippet = searchResult['snippet']
        PublishDay = Snippet['publishedAt']
        if 'title' in Snippet:
            title = Snippet['title']
        else:
            title = 'No title info'
        if 'resourceId' in Snippet:
            ResourceId = Snippet['resourceId']
            channelId = ResourceId['channelId']
    if 'contentDetails' in searchResult:
        contentDetails = searchResult['contentDetails']
        newItemCount = contentDetails['newItemCount']
        totalItemCount = contentDetails['totalItemCount']
    else:
        contentDetails = ''
        newItemCount = 0
        totalItemCount = 0
    print('channelId: %s, title: %s, publish day: %s, newItemCount: %s, totalItemCount: %s' % (channelId, title, PublishDay, newItemCount, totalItemCount))





