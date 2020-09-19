try:
    # it doesn't belong to default libarary
    from googleapiclient.discovery import build
except ImportError:
    import os
    os.system("pip install google-api-python-client")

# these belong to the default library
from datetime import timedelta
import re

while True:
    try:
        api_key = str(input("Enter your API token: ")) # fetching the api_key
        youtube = build('youtube', 'v3', developerKey=api_key)
    except Exception:
        print("It is an INVALID API key")

    else:
        break

# to find out Hours, minutes, and seconds
hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')

total_seconds = 0

while True:
    try:
        playlistId = str(input("Please enter the playlist URl: ")) # write the playlist Id here
    except ValueError:
        print("Please enter a string !!")
    else:
        break

temp = []
temp.append(playlistId[38:])
playlistId = ''

for i in temp:
    playlistId += i

nextPageToken = None
del temp

while True:
    try:
        pl_request = youtube.playlistItems().list(
            # contentDetails to get playlistId
            part='contentDetails',
            playlistId=playlistId,
            maxResults=50,
            pageToken=nextPageToken
        )

        pl_response = pl_request.execute() # exequting query

    except Exception: # invalid youtbe link
        print("Please enter a valid youtube link!!")
        break


    vid_ids = []
    for item in pl_response['items']:
        # stroring vidoeId in an array
        vid_ids.append(item['contentDetails']['videoId'])

    vid_request = youtube.videos().list(
        # contentDetails to get duration
        part="contentDetails",
        id=','.join(vid_ids) # providing videos id
    )

    vid_response = vid_request.execute() # exequting query

    for item in vid_response['items']:
        duration = item['contentDetails']['duration']

        # finding out the hours,minuts and seconds
        hours = hours_pattern.search(duration)
        minutes = minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)

        # casting those umbers into int
        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0

        # finding total seconds
        video_seconds = timedelta(
            hours=hours,
            minutes=minutes,
            seconds=seconds
        ).total_seconds()

        total_seconds += video_seconds

    nextPageToken = pl_response.get('nextPageToken') # to get the next page

    if not nextPageToken: # loop continues until no page is available
        break

total_seconds = int(total_seconds) # castig total_second to int

if total_seconds == 0:
    exit(code="Invalid")

minutes, seconds = divmod(total_seconds, 60)
hours, minutes = divmod(minutes, 60)

print(f'{hours} hours\\{minutes} mins\\{seconds} sec')
