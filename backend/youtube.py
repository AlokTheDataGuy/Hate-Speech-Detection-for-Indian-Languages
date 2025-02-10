import re
from googleapiclient.discovery import build

# Replace with your actual YouTube Data API v3 key
API_KEY = "AIzaSyBgsEzrFPrpTOBpsyx5LTeP-HzXg_KgLRk"

# Function to extract video ID from a full YouTube URL
def extract_video_id(url):
    # Use regex to match video ID in YouTube URLs
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if match:
        return match.group(1)
    return url  # Return as-is if already a video ID

def get_comments(video_url):
    video_id = extract_video_id(video_url)
    
    # Initialize the YouTube API client
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    comments = []
    next_page_token = None

    while True:
        # Call the YouTube API to fetch comments
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            pageToken=next_page_token,
            maxResults=100,  # Maximum allowed per request
            textFormat="plainText"
        )
        response = request.execute()
        
        # Process each comment in the response
        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)
        
        # Check for more pages
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
    
    return comments

# Example usage with a full YouTube URL
video_url = "https://youtu.be/7kLi8u2dJz0?si=Yy0_GXz5AI6PdeR6"
video_comments = get_comments(video_url)

# Display all comments
for idx, comment in enumerate(video_comments):
    print(f"Comment {idx+1}: {comment}")
