from urllib.request import urlopen
import simplejson as json


ChannelId = 'UCgHXsynhD8GxbFcNlPEn-_w'
DeveloperKey = "PUT YOUR KEY HERE"
part = 'statistics,brandingSettings,topicDetails'
Url = "https://www.googleapis.com/youtube/v3/channels?key=" + DeveloperKey + "&id=" + ChannelId + "&part=" + part
Results = urlopen(Url)
Results = json.load(Results)
for searchResult in Results.get("items", []):
    if 'topicDetails' in searchResult:
        topicIds = searchResult['topicDetails']['topicIds']
    else:
         topicIds = 'None'
    if 'statistics' in searchResult:
        viewCount= searchResult['statistics']['viewCount']
        subscriberCount = searchResult['statistics']['subscriberCount']
        videoCount = searchResult['statistics']['videoCount']
    else:
        viewCount = 0
        subscriberCount = 0
        videoCount = 0
    if 'brandingSettings' in searchResult:
        brandingSettings = searchResult['brandingSettings']['channel']
        title = brandingSettings['title']
        if 'keywords' in brandingSettings:
            keywords = brandingSettings['keywords']
        else:
            keywords = ''
        if 'description' in brandingSettings:
            description = brandingSettings['description']
        else:
            description = ''
    print ('Views: %s, Number of subscribers: %s, Number of videos in the channel: %s,Channel title: %s, Channel description: %s, Channel topicIds: %s'%(viewCount, subscriberCount, videoCount, title, description, topicIds))




