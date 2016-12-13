import urllib.request
from bs4 import BeautifulSoup

# YouTube ChannelId is a 24-character string begins with UC
ChannelId = 'UCXXXXXXXXXXXXXXXXXXXXXX'
linkInfo = []
url = 'https://www.youtube.com/channel/'+ ChannelId +'/about'
text = urllib.request.urlopen(url).read()
soup = BeautifulSoup(text, "lxml")
data = soup.findAll('a', attrs={'class': 'about-channel-link'})
for i in data:
    link = (i['href'])
    title = (i['title'])
    linkInfo.append({title:link})
result = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in linkInfo)]
print(result)

# title is the name of the embedded link shown on YouTube
# link is external URL