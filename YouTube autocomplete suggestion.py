import re
from urllib.request import urlopen
import simplejson as json
import urllib.parse



query = 'justin' #can be changed to other topics  
query = urllib.parse.quote(query)
url = 'http://suggestqueries.google.com/complete/search?callback=?&client=youtube&jsonp=suggestCallBack&ds=yt&q='+query
response = urlopen(url)
response = response.read().decode('utf-8')
response = re.sub(r'[\{](.*?)[\}]', '', response)
response = re.findall(r'["](.*?)["]', response)
del(response[0])
for i in response:
    print(bytes(i, 'ascii').decode('unicode-escape'))


