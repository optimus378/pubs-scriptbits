from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Initialize the YouTube Data API client using the API key
API_KEY = 'YOURAPIKEY'
youtube = build('youtube', 'v3', developerKey=API_KEY)

# 1. Retrieve the channel ID based on a provided channel name
channel_name = 'YOURCHANNELNAME' ## Case Sensitive. 
search_response = youtube.search().list(part='snippet', q=channel_name, type='channel').execute()

channel_id = None
for channel in search_response['items']:
    if channel['snippet']['title'] == channel_name:
        channel_id = channel['id']['channelId']
        break

if not channel_id:
    print(f"No channel found with the name: {channel_name}")
    exit()

# 2. Use the retrieved channel ID to iterate through all videos
search_string = 'Khun'
page_token = None

while True:
    search_response = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        q=search_string,
        type='video',
        pageToken=page_token,
        maxResults=50  # Maximum allowed by the API
    ).execute()

    for video in search_response['items']:
        video_id = video['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_response = youtube.videos().list(part='snippet', id=video_id).execute()
        
        # Ensure the video_response contains the expected data before extracting details
        if video_response['items']:
            video_description = video_response['items'][0]['snippet']['description']
            video_title = video_response['items'][0]['snippet']['title']

            # Print the video title, description, and URL
            print("Video Title:", video_title)
            print("Video Description:", video_description)
            print("Video URL:", video_url)
            print("-" * 50)  # Separator for better readability
        else:
            print(f"No details found for video with ID {video_id}.")

    page_token = search_response.get('nextPageToken')
    if not page_token:
        break  # Exit the loop if there's no more videos to retrieve
