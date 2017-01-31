from urllib.request import urlopen
import simplejson as json




DeveloperKey = "PUT YOUR KEY HERE"
part = 'snippet'
location = '37.42307%2C+-122.08427'
maxResults = '50' 
locationRadius = '50km'
order='date'
query='trump'
Searchtype='video'

List = []
Url = "https://www.googleapis.com/youtube/v3/search?key=" +\
DeveloperKey + "&q" + query + "&part="+ part + "&maxResults=" + maxResults +\
 "&location=" + location + "&locationRadius=" + locationRadius + "&type=" + Searchtype
Results = urlopen(Url)
Results = json.load(Results)
for searchResult in Results.get("items", []):
    Id = searchResult['id']
    if 'videoId' in Id:
        videoID = Id['videoId']
    else:
        videoID = 'None'
    if 'snippet' in searchResult:
        Snippet = searchResult['snippet']
        if 'title' in Snippet:
            videoTitle = Snippet['title']
        else:
            videoTitle = 'None'
        if 'publishedAt' in Snippet:
            publishTime = Snippet['publishedAt']
        else:
            publishTime = 'None'

    List.append((videoID, videoTitle, publishTime)) 

        
print(List)        
        
