#!/usr/bin/python

import httplib2
import os
import sys

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run
from optparse import OptionParser

parser = OptionParser()
parser.add_option("--src", dest="src",
        help="ID of source playlist to copy videos from")
parser.add_option("--dest", dest="dest",
        help="ID of destination playlist to copy videos to")
(options, args) = parser.parse_args()

# CLIENT_SECRETS_FILE, name of a file containing the OAuth 2.0 information for
# this application, including client_id and client_secret. You can acquire an
# ID/secret pair from the API Access tab on the Google APIs Console
#   http://code.google.com/apis/console#access
# For more information about using OAuth2 to access Google APIs, please visit:
#   https://developers.google.com/accounts/docs/OAuth2
# For more information about the client_secrets.json file format, please visit:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
# Please ensure that you have enabled the YouTube Data API for your project.
CLIENT_SECRETS_FILE = "client_secrets.json"

# Helpful message to display if the CLIENT_SECRETS_FILE is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the APIs Console
https://code.google.com/apis/console#access

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
        message=MISSING_CLIENT_SECRETS_MESSAGE,
        scope=YOUTUBE_READONLY_SCOPE)

storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()

if credentials is None or credentials.invalid:
    credentials = run(flow, storage)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
  http=credentials.authorize(httplib2.Http()))

SRC_PLAYLIST_ID = options.src

next_page_token = ""

src_playlist = []

print "Trying to fetch contents of playlist with id %s" % SRC_PLAYLIST_ID

while next_page_token is not None:
    playlist_response = youtube.playlistItems().list(part="id,contentDetails,snippet", 
            playlistId=SRC_PLAYLIST_ID, 
            maxResults=50, 
            pageToken=next_page_token).execute()

    for item in playlist_response["items"]:
        id = item["contentDetails"]["videoId"]
        title = item["snippet"]["title"]
        src_playlist.append((id, title))
    
    next_page_token = playlist_response.get("tokenPagination", {}).get("nextPageToken") or \
        playlist_response.get("nextPageToken")

src_playlist = dict(src_playlist)
DEST_PLAYLIST_ID = options.dest

response = raw_input("Got %d videos. Add to playlist with id %s? [Y/n]" % (len(src_playlist), DEST_PLAYLIST_ID))

if response != "Y":
    print "Exiting"
    sys.exit(0)

for id, title in src_playlist.items():
    body = dict(
            snippet=dict(
                playlistId=DEST_PLAYLIST_ID,
                resourceId=dict(
                    kind="youtube#video",
                    videoId=id
                )
            )
    )

    print "Trying to add video with id %s, title %s" % (id, title)
    
    youtube.playlistItems().insert(
        part=",".join(body.keys()),
        body=body
    ).execute()

print "Done."
