from urllib.request import urlopen
import simplejson as json



ChannelID = 'UCCJdqnlqrmTUAYvS6i3nAXA'
DeveloperKey = "PUT YOUR KEY HERE"
maxResults = '50'
CommentsList = []
CommentsUrl = "https://www.googleapis.com/youtube/v3/commentThreads?key=" + DeveloperKey + "&channelId=" + ChannelID + "&part=snippet&maxResults=" +maxResults + "&textFormat=plainText"
Results = urlopen(CommentsUrl)
Results = json.load(Results)
for searchResult in Results.get("items", []):
    if 'topLevelComment' in searchResult['snippet']:
        comment = searchResult['snippet']["topLevelComment"]
        author = comment["snippet"]["authorDisplayName"]
        text = comment["snippet"]["textDisplay"]
        print (author, text)
        CommentsList.append(text)

print(CommentsList)
