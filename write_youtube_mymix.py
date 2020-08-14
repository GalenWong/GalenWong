from googleapiclient.discovery import build
import google.oauth2.credentials
import json
import itertools
import os

TOKEN = os.environ['TOKEN']
REFRESH_TOKEN = os.environ['REFRESH_TOKEN']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

credentials = google.oauth2.credentials.Credentials(
    token_uri='https://oauth2.googleapis.com/token',
    token=TOKEN, 
    refresh_token=REFRESH_TOKEN,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET)

youtube = build('youtube', 'v3', credentials=credentials)

resp = youtube.playlistItems().list(part='snippet', maxResults=25, playlistId='RDMM').execute()

# transform to list of { name, link }
# select only the top 5 
videos = []
for video_item in itertools.islice(resp['items'], 5):
    name = video_item['snippet']['title']
    video_id = video_item['snippet']['resourceId']['videoId']
    link = f'https://www.youtube.com/watch?v={video_id}'

    videos.append({ 'name': name, 'link': link })

# create the markdown
li_items = []
for video in videos:
    name = video['name']
    link = video['link']
    li_items.append(f'- [{name}]({link})')

ul_list = '\n'.join(li_items)

print(ul_list)

# read readme 

START_MARKER = '<!-- YOUTUBE-MYMIX-LIST:START -->'
END_MARKER = '<!-- YOUTUBE-MYMIX-LIST:END -->'

with open('README.md') as f:
    readme = f.read()

start_index = readme.index(START_MARKER) + len(START_MARKER)
end_index = readme.index(END_MARKER)

# inject the list
new_readme = readme[:start_index] + '\n' + ul_list + '\n' + readme[end_index:]

with open('README.md', 'w') as f:
    f.write(new_readme)
