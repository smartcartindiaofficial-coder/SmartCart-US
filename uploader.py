import os
import time
import pickle
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, 'Config.env')
load_dotenv(ENV_PATH)

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.force-ssl' # Gives full comment threading access
]

def clean_amazon_url(url):
    """
    Strips unnecessary tracking parameters from an Amazon link,
    leaving a clean, short URL that is easier to copy/read.
    """
    import re
    # Look for the product ID standard pattern (ASIN)
    asin_match = re.search(r'/(dp|gp/product)/([A-Z0-9]{10})', url)
    if asin_match:
        asin = asin_match.group(2)
        # Rebuild a clean short link using your store tag
        return f"https://amazon.in/dp/{asin}/?tag={os.getenv('Affiliate_Code')}"
    return url

def get_youtube_service():
    """Handles OAuth2 authentication and returns a YouTube API service object."""
    creds = None
    # token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    # If there are no valid credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('client_secrets.json'):
                raise FileNotFoundError(
                    "❌ 'client_secrets.json' missing! Please download it from Google Cloud Console "
                    "and place it in your root folder: {current_working_dir}"
                )
            flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('youtube', 'v3', credentials=creds)

def upload_to_youtube(driver, video_path, title, description, tags):
    """
    Uploads a video to YouTube using the official YouTube Data API v3.
    Accepts 'driver' parameter to keep signature compatibility with main.py,
    but does not use it.
    """
    print(f"🚀 [API] Initiating secure upload for: {title[:30]}...")
    
    try:
        youtube = get_youtube_service()
        
        # Format tags string into a list structure expected by the API
        tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []

        body = {
            'snippet': {
                'title': title[:100], # YouTube limit
                'description': description,
                'tags': tag_list,
                'categoryId': '22'  # 22 represents 'People & Blogs' / standard shorts category
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }

        # Setup the media file upload wrapper
        media = MediaFileUpload(
            os.path.abspath(video_path), 
            chunksize=-1, 
            resumable=True, 
            mimetype='video/mp4'
        )

        request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )

        print("📤 Uploading video chunks directly to Google servers...")
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"📦 Uploaded {int(status.progress() * 100)}%")

        print(f"🎉 SUCCESS: Video Published via API! Video ID: {response['id']}")
        youtube_video_id = response['id']
        
        # # ─── 🚀 AUTOMATED FIRST COMMENT YOUTUBE LAYER ───
        # try:
        #     print("💬 Dropping pinned-style channel comment onto YouTube Short...")
        #     import re
        #     link_match = re.search(r'https://[^\s]+', description)
        #     buy_link = link_match.group(0) if link_match else ""
            
        #     comment_body = {
        #         "snippet": {
        #             "videoId": youtube_video_id,
        #             "topLevelComment": {
        #                 "snippet": {
        #                     'textOriginal': f"🛍️ Clickable Direct Buy Link: {clean_amazon_url(buy_link)}\n\n👉 Subscribe for daily smart tech finds!"
        #                 }
        #             }
        #         }
        #     }
        #     # Execute the comment insert API call using the same authenticated 'youtube' service object
        #     youtube.commentThreads().insert(
        #         part="snippet",
        #         body=comment_body
        #     ).execute()
        #     print("✅ YouTube channel first comment dropped successfully!")
        # except Exception as yt_comment_err:
        #     print(f"⚠️ Could not drop automated YouTube comment: {yt_comment_err}")
        # # ────────────────────────────────────────────────

        # ────────────────────────────────────────────────
        # 📊 AUTOMATED CONVERSION COMMENT & POLL SYSTEM
        # ────────────────────────────────────────────────
        try:
            print("💬 Checking timezone metrics for automated pinned comment styling...")
            import re
            from datetime import datetime, timedelta, timezone

            # 1. Parse out the base amazon link from the description string
            link_match = re.search(r'https://[^\s]+', description)
            buy_link = link_match.group(0) if link_match else ""
            clean_url = clean_amazon_url(buy_link)

            # Establish Indian Standard Time (IST) explicitly via UTC offset (+5.5 hours)
            ist_tz = timezone(timedelta(hours=5, minutes=30))
            now_ist = datetime.now(timezone.utc).astimezone(ist_tz)
            
            current_weekday = now_ist.weekday() # Monday=0, Wednesday=2, Friday=4, Saturday=5
            current_hour = now_ist.hour

            # Target Windows: Wednesday (2), Friday (4), Saturday (5) AND after 5:00 PM IST (17:00)
            target_days = [2, 4, 5] 
            
            if current_weekday in target_days and current_hour >= 17:
                print("🔥 Engagement Window Active! Parsing features dynamically for the poll...")
                
                cleaned_options = []
                
                # Strategy A: Check for standard bracket features [Like This]
                bracket_features = re.findall(r'\[([^\]]+)\]', description)
                
                if bracket_features:
                    for feat in bracket_features:
                        clean_text = re.sub(r'[^a-zA-Z0-9\s\-\.]', '', feat).strip()
                        words = clean_text.split()
                        short_phrase = " ".join(words[:4]) + "..." if len(words) > 4 else " ".join(words)
                        if short_phrase and "FEATURES" not in short_phrase.upper():
                            cleaned_options.append(short_phrase)
                
                # Strategy B: Fallback for colon headlines (e.g., "-Feature Name: Description")
                else:
                    raw_lines = description.split('\n')
                    for line in raw_lines:
                        if ':' in line and (line.strip().startswith('-') or line.strip().startswith('*')):
                            # Isolate the headline text before the colon character
                            headline = line.split(':')[0].strip("-* ")
                            # Remove non-alphanumeric clutter
                            clean_text = re.sub(r'[^a-zA-Z0-9\s\-\.]', '', headline).strip()
                            words = clean_text.split()
                            short_phrase = " ".join(words[:4]) + "..." if len(words) > 4 else " ".join(words)
                            if short_phrase and "FEATURES" not in short_phrase.upper() and "APPLICATIONS" not in short_phrase.upper():
                                cleaned_options.append(short_phrase)

                # 3. Fallback defaults if no structural features match
                opt_a = cleaned_options[0] if len(cleaned_options) > 0 else "High Performance Build"
                opt_b = cleaned_options[1] if len(cleaned_options) > 1 else "Value for Money"
                
                # 4. Assemble the interactive text poll block
                comment_text = (
                    f"📊 QUICK POLL: Which feature matters most to you?\n\n"
                    f"痕 Option A: {opt_a}\n"
                    f"尾 Option B: {opt_b}\n"
                    f"🆃 Option C: Premium Design & Brand Trust\n\n"
                    f"👇 Reply below with your choice (A, B, or C)!\n\n"
                    f"🛍️ Direct Buy Link: {clean_url}\n"
                    f"👉 Subscribe to SmartCart India for daily smart finds!"
                )
            else:
                # Default clean comment layout for standard posting windows
                print("📝 Standard window active. Dropping traditional affiliate link comment.")
                comment_text = f"🛍️ Clickable Direct Buy Link: {clean_url}\n\n👉 Subscribe for daily smart finds!"

            comment_body = {
                "snippet": {
                    "videoId": youtube_video_id,
                    "topLevelComment": {
                        "snippet": {
                            'textOriginal': comment_text
                        }
                    }
                }
            }
            
            # Execute the official YouTube Comment Thread insert call
            youtube.commentThreads().insert(
                part="snippet",
                body=comment_body
            ).execute()
            print("✅ YouTube channel automated comment drop completed successfully!")
            
        except Exception as yt_comment_err:
            print(f"⚠️ Could not complete automated comment routines: {yt_comment_err}")
        # ────────────────────────────────────────────────
            
        except Exception as yt_comment_err:
            print(f"⚠️ Could not complete automated comment routines: {yt_comment_err}")
        # ────────────────────────────────────────────────

        # Build the clean, official YouTube Shorts watch link
        youtube_shorts_url = f"https://youtube.com/shorts/{youtube_video_id}"
        return youtube_shorts_url

    except Exception as e:
        print(f"❌ YouTube API Upload Failed: {e}")
        return None # Return None if the upload fails