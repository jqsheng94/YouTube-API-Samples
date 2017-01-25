from urllib.request import urlopen
import simplejson as json



ChannelID = 'UCgHXsynhD8GxbFcNlPEn-_w'
DeveloperKey = "PUT YOUR KEY HERE"
part = 'contentDetails'
maxResults = '50' # maximum number of comments
List = []
Url = "https://www.googleapis.com/youtube/v3/channelSections?key=" + DeveloperKey + "&channelId=" + ChannelID + "&part="+ part + "&maxResults=" +maxResults + "&textFormat=plainText"
Results = urlopen(Url)
Results = json.load(Results)
for searchResult in Results.get("items", []):
    if 'contentDetails' in searchResult:
        ContentDetails = searchResult['contentDetails']
        Playlists = ContentDetails['playlists']
        List = List + Playlists

ChannelPlaylist = set(List)
print(ChannelPlaylist)

part2 = 'snippet'
Url2 = "https://www.googleapis.com/youtube/v3/channelSections?key=" + DeveloperKey + "&channelId=" + ChannelID + "&part="+ part2 + "&maxResults=" +maxResults + "&textFormat=plainText"
Results2 = urlopen(Url2)
Results2 = json.load(Results2)
for searchResult in Results2.get("items", []):
    id = searchResult['id']
    if 'snippet' in searchResult:
        Snippet = searchResult['snippet']
        if 'type' in Snippet:
            type = Snippet['type']
        else:
            type = 'No type info'
        if 'style' in Snippet:
            Style = Snippet['style']
        else:
            Style = 'No style info'
        if 'title' in Snippet:
            title = Snippet['title']
        else:
            title = 'No title info'
        print('id: %s, type: %s, style: %s, title: %s'%(id, type, Style, title))



