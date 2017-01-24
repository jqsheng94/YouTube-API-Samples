from urllib.request import urlopen
import simplejson as json



ChannelID = 'UCCJdqnlqrmTUAYvS6i3nAXA'
DeveloperKey = "PUT YOUR KEY HERE"
maxResults = '50' # maximum number of comments
CommentsList = []
CommentsUrl = "https://www.googleapis.com/youtube/v3/commentThreads?key=" + DeveloperKey + "&channelId=" + ChannelID + "&part=snippet&maxResults=" +maxResults + "&textFormat=plainText"
videoResults = urlopen(CommentsUrl)
videoResults = json.load(videoResults)
for searchResult in videoResults.get("items", []):
    if 'topLevelComment' in searchResult['snippet']:
        comment = searchResult['snippet']["topLevelComment"]
        author = comment["snippet"]["authorDisplayName"]
        text = comment["snippet"]["textDisplay"]
        print (author, text)
        CommentsList.append(text)

print(CommentsList)
