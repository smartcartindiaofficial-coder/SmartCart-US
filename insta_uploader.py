import os
import time
import requests
from dotenv import load_dotenv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__ ))
ENV_PATH = os.path.join(SCRIPT_DIR, 'Config.env')
load_dotenv(ENV_PATH)

ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")

def clean_amazon_url(url):
    import re
    asin_match = re.search(r'/(dp|gp/product)/([A-Z0-9]{10})', url)
    if asin_match:
        asin = asin_match.group(2)
        return f"https://amazon.in/dp/{asin}/?tag={os.getenv('Affiliate_Code')}"
    return url

def upload_to_tmpfiles(local_video_path):
    """
    Uploads the local video file to tmpfiles.org to get an instant,
    publicly accessible raw URL for Meta ingestion.
    """
    print(f"☁️ Uploading temporary video asset to cloud provider for Meta parsing...")
    try:
        url = "https://tmpfiles.org/api/v1/upload"
        with open(local_video_path, 'rb') as f:
            files = {'file': f}
            res = requests.post(url, files=files).json()
            
        # tmpfiles.org returns a view URL; we must change it to a raw download URL
        # Example conversion: https://tmpfiles.org/123/video.mp4 -> https://tmpfiles.org/dl/123/video.mp4
        view_url = res['data']['url']
        raw_url = view_url.replace("https://tmpfiles.org/", "https://tmpfiles.org/dl/")
        print(f"🔗 Public temporary URL generated: {raw_url}")
        return raw_url
    except Exception as e:
        print(f"❌ Temporary cloud upload failed: {e}")
        return None

def upload_to_instagram(local_video_path, description_text, buy_link):
    """
    Accepts the local file path on the runner, uploads it temporarily,
    and passes it straight to Meta Graph API.
    """
    if not ACCESS_TOKEN or not INSTAGRAM_ACCOUNT_ID:
        print("❌ Instagram Credentials missing from environment.")
        return None

    # Get a working public URL instantly
    public_video_url = upload_to_tmpfiles(local_video_path)
    if not public_video_url:
        print("❌ Aborting Instagram post: Could not generate public file asset link.")
        return None

    print(f"🎬 Initiating Meta Container Ingestion for URL: {public_video_url}")
    
    try:
        # Step 1: Initialize Container
        url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ACCOUNT_ID}/media"
        payload = {
            'media_type': 'REELS',
            'video_url': public_video_url,
            'caption': description_text,
            'access_token': ACCESS_TOKEN
        }
        
        res = requests.post(url, data=payload).json()
        container_id = res.get('id')
        
        if not container_id:
            print(f"❌ Container Ingestion Failed: {res}")
            return None
            
        print(f"⏳ Video Container Created (ID: {container_id}). Waiting for Meta processing...")
        
        # Step 2: Await Meta Processing completion
        status_url = f"https://graph.facebook.com/v19.0/{container_id}"
        status_payload = {'fields': 'status_code', 'access_token': ACCESS_TOKEN}
        
        attempts = 0
        while attempts < 30:
            time.sleep(10)
            attempts += 1
            status_res = requests.get(status_url, params=status_payload).json()
            status = status_res.get('status_code')
            print(f"🔄 Meta Processing Status: {status}")
            
            if status == "FINISHED":
                break
            elif status == "ERROR":
                print(f"❌ Meta conversion pipeline error: {status_res}")
                return None

        # Step 3: Publish container live
        publish_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"
        publish_payload = {'creation_id': container_id, 'access_token': ACCESS_TOKEN}
        publish_res = requests.post(publish_url, data=publish_payload).json()
        
        published_media_id = publish_res.get('id')
        if published_media_id:
            print(f"🚀 SUCCESS: Reel is officially live on Instagram! ID: {published_media_id}")
            
            # Step 4: Drop First Comment (Affiliate Link)
            try:
                comment_url = f"https://graph.facebook.com/v19.0/{published_media_id}/comments"
                comment_payload = {
                    'message': f"🛍️ Direct buy link: {clean_amazon_url(buy_link)}",
                    'access_token': ACCESS_TOKEN
                }
                requests.post(comment_url, data=comment_payload)
                print("✅ Instagram first comment dropped successfully!")
            except Exception as comment_err:
                print(f"⚠️ Could not drop automated Instagram comment: {comment_err}")

            return f"https://www.instagram.com/p/{published_media_id}/"
        else:
            print(f"❌ Publishing Execution Failed: {publish_res}")
            return None

    except Exception as e:
        print(f"❌ Instagram Graph API Error: {e}")
        return None