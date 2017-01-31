from urllib.request import urlopen
import simplejson as json

DeveloperKey = "PUT YOUR KEY HERE"
part = 'snippet'
id = '21'

List = []
Url = "https://www.googleapis.com/youtube/v3/videoCategories?key=" + \
      DeveloperKey + "&part=" + part + "&id=" + id
Results = urlopen(Url)
Results = json.load(Results)
for searchResult in Results.get("items", []):
    if 'snippet' in searchResult:
        Snippet = searchResult['snippet']
        if 'title' in Snippet:
            Title = Snippet['title']
        else:
            Title = 'None'
        if 'channelId' in Snippet:
            channelId = Snippet['channelId']
        else:
            channelId = 'None'

    List.append((Title, channelId))

print(List)

