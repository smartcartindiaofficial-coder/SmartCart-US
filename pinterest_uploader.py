import os
import time
import requests

# Pinterest API v5 Endpoints
PINTEREST_API_BASE = "https://api.pinterest.com/v5"

class PinterestUploader:
    def __init__(self):
        self.access_token = os.getenv("PINTEREST_ACCESS_TOKEN")
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def register_media_upload(self):
        """Registers a video upload session with Pinterest API v5."""
        url = f"{PINTEREST_API_BASE}/media"
        payload = {"media_type": "video"}
        
        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code == 201:
            return response.json()
        else:
            print(f"❌ [Pinterest] Failed to register media: {response.text}")
            return None

    def upload_video_file(self, upload_url, upload_parameters, video_path):
        """Uploads the raw .mp4 video file to Pinterest S3 storage bucket."""
        with open(video_path, 'rb') as f:
            files = {'file': f}
            # Pinterest upload endpoints use multipart form-data without Bearer token
            response = requests.post(upload_url, data=upload_parameters, files=files)
            return response.status_code in [200, 204]

    def wait_for_media_processing(self, media_id):
        """Polls Pinterest API until the uploaded video is fully processed."""
        url = f"{PINTEREST_API_BASE}/media/{media_id}"
        print("⏳ [Pinterest] Processing video...")
        
        for _ in range(30):  # Poll for up to 2.5 minutes
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                status = response.json().get("status")
                if status == "succeeded":
                    print("✅ [Pinterest] Video processing complete!")
                    return True
                elif status == "failed":
                    print("❌ [Pinterest] Video processing failed on Pinterest servers.")
                    return False
            time.sleep(5)
        return False

    def create_video_pin(self, board_id, title, description, link, video_path):
        """Main method to upload video and create a Pin."""
        print("\n📌 Starting Pinterest Pin Creation...")

        # Step A: Register Upload Session
        media_data = self.register_media_upload()
        if not media_data:
            return False

        media_id = media_data["media_id"]
        upload_url = media_data["upload_url"]
        upload_params = media_data["upload_parameters"]

        # Step B: Upload File to S3
        print("📤 [Pinterest] Uploading video binary...")
        if not self.upload_video_file(upload_url, upload_params, video_path):
            print("❌ [Pinterest] Binary file upload failed.")
            return False

        # Step C: Wait for processing
        if not self.wait_for_media_processing(media_id):
            return False

        # Step D: Post Pin to Board with Affiliate Link
        pin_url = f"{PINTEREST_API_BASE}/pins"
        pin_payload = {
            "board_id": board_id,
            "title": title[:100],  # Max 100 chars
            "description": f"{description}\n\n🛒 Buy Here: {link}",
            "link": link,  # Direct Amazon Affiliate Link or GitHub Pages URL!
            "media_source": {
                "source_type": "video_id",
                "media_id": media_id
            }
        }

        response = requests.post(pin_url, json=pin_payload, headers=self.headers)
        if response.status_code == 201:
            pin_id = response.json().get("id")
            print(f"🎉 [Pinterest] Pin published successfully! Pin ID: {pin_id}")
            return True
        else:
            print(f"❌ [Pinterest] Failed to publish Pin: {response.text}")
            return False


if __name__ == "__main__":
    uploader = PinterestUploader()