from urllib.request import urlopen
import simplejson as json



ChanelId = 'UCgRvm1yLFoaQKhmaTqXk9SA'  #UCaK87UTTMacD35eQITej2VA  #UCgRvm1yLFoaQKhmaTqXk9SA
DeveloperKey = "PUT YOUR KEY HERE"
maxResults = '50'
playlistInfo = []
channelUrl = "https://www.googleapis.com/youtube/v3/playlists?key=" + DeveloperKey + "&channelId=" + ChanelId + "&part=id,snippet&maxResults=" +maxResults
videoResults = urlopen(channelUrl)
videoResults = json.load(videoResults)
for searchResult in videoResults.get("items", []):
    if 'title' in searchResult['snippet']:
        playlistTitle = searchResult['snippet']['title']
    else:
        playlistTitle = 'None'
    playlistId = searchResult['id']
    publishDate = searchResult['snippet']['publishedAt']
    videoIds = []
    Playlist = "https://www.googleapis.com/youtube/v3/playlistItems?key=" + DeveloperKey + "&playlistId=" + playlistId + "&part=snippet&maxResults=" + maxResults
    PlaylistResults = urlopen(Playlist)
    PlaylistResults = json.load(PlaylistResults)
    for searchResult in PlaylistResults.get("items", []):
        videoIds.append(searchResult['snippet']['resourceId']['videoId'])
    playlistInfo.append({'PlaylistId': playlistId, 'PlaylistTitle' : playlistTitle, 'PublishDate':publishDate, 'videos': videoIds})
    print(playlistId,videoIds)

print(playlistInfo)
