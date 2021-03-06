import httplib2
import os
import sys
from urllib.request import urlopen
import simplejson as json

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


CLIENT_SECRETS_FILE = "client_secrets.json"
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    scope=YOUTUBE_READ_WRITE_SCOPE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))


def retrieveVideoInfo(youtube, video_id):
  results = youtube.videos().list(
    id=video_id,
    part="contentDetails"
  ).execute()
  print(results)



videoIDs = 'O3UN1N-EpOQ'




if __name__ == "__main__":
  argparser.add_argument("--videoid", default=videoIDs)
  args = argparser.parse_args()
  youtube = get_authenticated_service(args)
  try:
    retrieveVideoInfo(youtube, args.videoid)
  except HttpError:
    print ("An HTTP error")
  else:
    print (args.videoid)

