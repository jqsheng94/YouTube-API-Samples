# fetch n most popular videos of  a channel


from apiclient.discovery import build
import os.path
import csv


rint( "=========================== list of Youtube videos ================================")


YT_channel_ids = ['UCmf7DwvMqFi3kLPMLIANIrg']     # Add ChannelIds in here


print ("===================================================================================")


DEVELOPER_KEY = "PUT YOUR KEY HERE"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

videos_by_channel = {}


for channel_id in YT_channel_ids:
    search_response = youtube.search().list(part="id,snippet",
                                            type='video',
                                            order='date',    # can be changed to 'viewcount'
                                            channelId=channel_id,
                                            maxResults=30).execute()  #30 is the number of videos to extract from the channel
    videoIds=[]
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videoIds.append(search_result['id']['videoId'])
    print(videoIds)


# After get the video Ids, save them into a csv file in the folder.

    file_exists = os.path.isfile("/PUT THE PATH HERE/video.csv")
    with open("/PUT THE PATH HERE/video.csv", 'a') as f:
        writer = csv.writer(f, delimiter = ',')
        writer.writerow(["videoYid"])
        writer.writerow(videoIds)


