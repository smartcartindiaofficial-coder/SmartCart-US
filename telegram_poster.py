import os
import telebot
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from telebot import apihelper
from dotenv import load_dotenv

# ─── FORCE ROOT FOLDER PATH LOOKUP FOR TELEGRAM ───
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, 'Config.env')
load_dotenv(ENV_PATH)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

if not BOT_TOKEN:
    raise ValueError(
        f"❌ Critical Config Error: 'TELEGRAM_BOT_TOKEN' was not found in your environment!\n"
        f"The script searched explicitly inside: {ENV_PATH}\n"
        f"Please verify your file placement and ensure the key name matches exactly."
    )

# Maximize internal pyTelegramBotAPI limits to give slow handshakes breathing room
apihelper.CONNECT_TIMEOUT = 120
apihelper.READ_TIMEOUT = 120

bot = telebot.TeleBot(BOT_TOKEN)

def post_to_telegram(product_name, product_link, media_path, youtube_url=None, price="Check Website"):
    """
    Sends the video/image to Telegram with a professional caption formatted in clean HTML.
    Bypasses ConnectTimeoutError and ISP restrictions via a dual-engine fallback system.
    """
    
    # 1. Build the caption text block using standard HTML tags
    caption = f"📦 <b>{product_name}</b>\n\n"
    
    if youtube_url:
        caption += f"🎬 <b>Watch on YouTube Shorts (Like & Subscribe!):</b>\n{youtube_url}\n\n"
        
    caption += (
        f"💰 <b>Price:</b> {price}\n"
        f"🔗 <a href='{product_link}'>Click Here to Buy on Amazon</a>\n\n"
        f"#AmazonFinds #SmartCartIndia #Deals"
    )
    
    try:
        if os.path.exists(media_path):
            # Check if it's a video or image
            if media_path.endswith(('.mp4', '.mov')):
                print(f"🔄 Initializing deep-buffered upload stream for video: {os.path.basename(media_path)}...")
                
                try:
                    # Setup custom pool size and aggressive connection retry adapters
                    session = requests.Session()
                    retries = Retry(
                        total=5, 
                        backoff_factor=3, # Increased backoff spacing to let local network spikes settle
                        status_forcelist=[500, 502, 503, 504, 408],
                        raise_on_status=False
                    )
                    
                    adapter = HTTPAdapter(pool_connections=15, pool_maxsize=15, max_retries=retries)
                    session.mount('https://', adapter)
                    
                    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
                    
                    with open(media_path, 'rb') as video_file:
                        payload = {
                            'chat_id': CHANNEL_ID,
                            'caption': caption,
                            'parse_mode': 'HTML'
                        }
                        files = {
                            'video': (os.path.basename(media_path), video_file, 'video/mp4')
                        }
                        
                        # UPGRADE: Raised initial connection handshake allowance to 90 seconds
                        response = session.post(url, data=payload, files=files, timeout=(90, 600))
                        
                    if response.status_code == 200:
                        print(f"🚀 Video post successful for: {product_name[:20]}")
                        return True
                    else:
                        print(f"⚠️ Primary Stream engine rejected ({response.status_code}). Triggering backup engine...")
                        raise requests.exceptions.RequestException()
                    
                    print(f"⚠️ Chandu")
                        
                except Exception as stream_err:
                    print(f"⚠️ Primary Stream failed due to local ISP network blocks. Engaging Emergency Fallback Wrapper...")
                    # EMERGENCY FALLBACK: Uses telebot's native internal worker if custom request session gets blocked
                    with open(media_path, 'rb') as fallback_video:
                        bot.send_video(
                            CHANNEL_ID,
                            fallback_video,
                            caption=caption,
                            parse_mode="HTML",
                            timeout=300
                        )
                    print(f"🚀 Video post successful via Emergency Backup Engine for: {product_name[:20]}")
                    return True
            else:
                # Photos processing
                with open(media_path, 'rb') as photo:
                    bot.send_photo(
                        CHANNEL_ID, 
                        photo, 
                        caption=caption, 
                        parse_mode="HTML"   
                    )
                print(f"🚀 Photo post successful for: {product_name[:20]}")
                return True
        else:
            # Fallback to text only if media is missing
            bot.send_message(CHANNEL_ID, caption, parse_mode="HTML")
            return True

    except Exception as e:
        print(f"❌ Telegram Media Error: {e}")
        return False