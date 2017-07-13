from urllib.request import urlopen
import simplejson as json



ChannelId = 'UCVp3nfGRxmMadNDuVbJSk8A'
DeveloperKey = "PUT YOUR KEY HERE"
part = 'id'
maxResults = '50'
order='viewcount'

List = []
Url = "https://www.googleapis.com/youtube/v3/search?part=" + part + "&id=" + ChannelId + "&order=" + order + "&maxResults=" + maxResults + "&key=" + DeveloperKey
Results = urlopen(Url)
Results = json.load(Results)
for searchResult in Results.get("items", []):
    Id = searchResult['id']
    if 'videoId' in Id:
        videoID = Id['videoId']
        List.append((videoID))
print(List)        
        
