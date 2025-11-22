from googleapiclient.discovery import build
import pandas as pd
import re


class youtube_data:

    def __init__(self,video_url):

        self.video_id = self.extract_video_id(video_url)

    def extract_video_id(self, video_url):
        """
        Private method to extract a YouTube video ID.
        Supports:
        - Standard URLs (watch?v=)
        - Short URLs (youtu.be)
        - Shorts URLs
        - Embed URLs
        - Raw video IDs
        """
        input_value = video_url.strip()

        # Case 1: Input is already a valid ID (11 characters, no '/')
        if len(input_value) == 11 and "/" not in input_value:
            return input_value

        # Case 2: Extract ID from URL
        pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})"
        match = re.search(pattern, input_value)

        if match:
            return match.group(1)

        raise ValueError("Invalid YouTube video URL or ID!")

    def get_video_id(self):
        """Returns the extracted clean video ID."""
        return self.video_id
    
 

# Function to get all comments (including replies) for a single video
    def get_comments_for_video(youtube, video_id):
        all_comments = []
        next_page_token = None

        while True:
            comment_request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                pageToken=next_page_token,
                textFormat="plainText",
                maxResults=100
            )
            comment_response = comment_request.execute()

            for item in comment_response['items']:
                top_comment = item['snippet']['topLevelComment']['snippet']
                all_comments.append({
                    'Timestamp': top_comment['publishedAt'],
                    'Username': top_comment['authorDisplayName'],
                    'VideoID': video_id,  # Directly using video_id from function parameter
                    'Comment': top_comment['textDisplay'],
                    'Date': top_comment['updatedAt'] if 'updatedAt' in top_comment else top_comment['publishedAt']
                })
            

            next_page_token = comment_response.get('nextPageToken')
            if not next_page_token:
                break


    

        # Create DataFrame
        comments_df = pd.DataFrame(all_comments).head(10)
        return comments_df['Comment']



