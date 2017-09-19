import httplib2
import os
import sys
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


CLIENT_SECRETS_FILE = "client_secrets.json"
YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
  scope=YOUTUBE_READONLY_SCOPE)

storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()

if credentials is None or credentials.invalid:
  flags = argparser.parse_args()
  credentials = run_flow(flow, storage, flags)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
  http=credentials.authorize(httplib2.Http()))

channels_response = youtube.channels().list(
  mine=True,
  part="contentDetails"
).execute()

for channel in channels_response["items"]:
  uploads_list_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]

  print ("Videos in the Playlist %s" % uploads_list_id)

  playlistitems_list_request = youtube.playlistItems().list(
    playlistId=uploads_list_id,
    part="snippet",
    maxResults=50  #maximum is 50
  )

  while playlistitems_list_request:
    playlistitems_list_response = playlistitems_list_request.execute()
    for playlist_item in playlistitems_list_response["items"]:
      title = playlist_item["snippet"]["title"]
      video_id = playlist_item["snippet"]["resourceId"]["videoId"]
      print ("Title: %s VideoId: %s" % (title, video_id))

    playlistitems_list_request = youtube.playlistItems().list_next(
      playlistitems_list_request, playlistitems_list_response)
  print