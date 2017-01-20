# This script is to fetch top 20 similar titles of a specific topic on YouTube.
# Results are saved in the array called "videos"
# Please ensure that you have enabled the YouTube Data API for your project.


from apiclient.discovery import build


DEVELOPER_KEY = "REPLACE YOUR KEY IN HERE"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


topic = " League of Lengends" # this can be changed to any topic
# title = "League of Lengends gameplay episode 1"  Can switch topic search by title search


youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)




search_response = youtube.search().list(
   q= topic, # title
   part="id,snippet",
   maxResults=20  #can be changed to any number
  ).execute()


search_videos = []


for search_result in search_response.get("items", []):
   if search_result["id"]["kind"] == "youtube#video":
       Ids = search_result["id"]["videoId"]
       search_videos.append(Ids)
video_ids = ",".join(search_videos)


video_response = youtube.videos().list(
    id=video_ids,
    part='id,topicDetails,snippet'
).execute()


videos = []


for video_result in video_response.get("items", []):
    videoTitle = video_result['snippet']['title']
    videos.append(videoTitle)


print(videos)
