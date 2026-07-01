import os
import sys
import shutil
import pandas as pd
from datetime import datetime
import re 
import time
import glob
import gc
import subprocess
from groq import Groq
from google import genai
from google.genai import types

from dotenv import load_dotenv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, 'Config.env')
load_dotenv(ENV_PATH) 

import scout   
import editor 
import uploader
import insta_uploader
import telegram_poster
import thumbnail_engine 

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- SETTINGS ---
BRAVE_PATH = os.getenv("BRAVE_BROWSER_PATH")
BRAVE_USER_DATA_RAW = os.getenv("BRAVE_USER_DATA_DIR")
BRAVE_USER_DATA = os.path.normpath(BRAVE_USER_DATA_RAW) if BRAVE_USER_DATA_RAW else None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

HISTORY_ENV = os.getenv("HISTORY_FILE")
HISTORY_FILE = os.path.join(BASE_DIR, HISTORY_ENV) if HISTORY_ENV else os.path.join(BASE_DIR, "upload_history.csv")

BASE_EXPORT_FOLDER = "Exports"
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# --- OPTIMIZED ALGORITHMIC HASHTAG MATRIX ---
# Selected 5 premium niche tags per category to ensure optimal indexing 
# on both YouTube Shorts and Instagram Reels safely.
CATEGORY_HASHTAGS = {
    "Baby Products": ["#BabyProducts", "#ParentingHacks", "#BabyMustHaves", "#BabyRegistry", "#SmartCartIndia"],
    "Computers & Accessories": ["#TechFinds", "#DeskSetup", "#TechGadgets", "#PCGaming", "#SmartCartIndia"],
    "Home & Kitchen": ["#KitchenGadgets", "#HomeKitchen", "#KitchenHacks", "#SmartHomeTech", "#SmartCartIndia"],
    "Home Improvement": ["#HomeImprovement", "#DIYProjects", "#SmartHome", "#HardwareTools", "#SmartCartIndia"],
    "Car & Motorbike": ["#CarAccessories", "#CarGadgets", "#MotorbikeLife", "#AutomotiveFinds", "#SmartCartIndia"],
    "Clothing & Accessories": ["#FashionFinds", "#OOTDIndia", "#AmazonFashion", "#StyleInspiration", "#SmartCartIndia"],
    "Jewellery": ["#JewelleryDesign", "#FashionJewellery", "#AccessoriesLovers", "#JewelleryDeals", "#SmartCartIndia"],
    "Default": ["#AmazonFinds", "#TrendingGadgets", "#SmartCartIndia", "#ViralProducts", "#DailyDeals","#Amazon", "#Trending", "#Viral", "#Deals","#Gadgets","#Smart"]
}

def reframe_product_for_youtube(raw_name, raw_specs):
    """
    Uses the free, blazing-fast Groq API to analyze complex Amazon
    product details and return highly tailored, viral marketing scripts.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("⚠️ Groq API key missing in Config.env! Falling back to raw titles.")
        # Safe fallback so your automation loop doesn't crash if the key fails to load
        return raw_name[:45], "Check out this amazing find on Amazon right now!"

    try:
        # Initialize the official Groq pipeline client
        client = Groq(api_key=api_key)
        
        # Craft a strict prompt to make sure it only returns what our pipeline needs
        prompt = f"""
        You are an expert viral marketer for YouTube Shorts and Instagram Reels.
        Analyze the raw product information below and transform it into high-retention content.

        PRODUCT NAME: {raw_name}
        SPECIFICATIONS: {raw_specs}

        OUTPUT REGULATION: You must return exactly 3 lines of text. Do not add introductions, explanations, or markdown symbols like asterisks.

        Line 1: Punchy Viral Title (Max 5 words, clear, NO technical model numbers).
        Line 2: Catchy Hook Sentence (0-3 seconds of the video, focuses on an everyday problem or high curiosity, Max 10 words).
        Line 3: Short Script Body (3-12 seconds of the video, highlights 2 major lifestyle benefits naturally, Min 10 and Max 15 words).
        """

        # Execute high-speed text inference using Llama 3
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant",  # <--- Changed from llama3-8b-8092
            temperature=0.7,
            max_tokens=250
        )

        # Parse and clean the output response text
        raw_output = chat_completion.choices[0].message.content.strip()
        lines = [line.strip() for line in raw_output.split('\n') if line.strip()]

        if len(lines) >= 3:
            # Line 1 becomes the overlay title for your video metadata and cards
            viral_title = lines[0].replace("Line 1:", " ").replace('"', '').strip()
            
            # Clean up line tags if the AI prints them literally
            hook = lines[1].replace("Line 2:", " ").strip()
            body = lines[2].replace("Line 3:", " ").strip()
            
            # Combine hook and body into a smooth audio text script for edge_tts to read
            voiceover_script_tmp = f"{hook} @ {body}     Direct deal link is pinned in the comments below!"
            voiceover_script = re.sub(r'\d+\.\s*', '', voiceover_script_tmp)
            return viral_title, voiceover_script
        else:
            return raw_name[:45], "Check out this trending Amazon asset find right now!"

    except Exception as e:
        print(f"❌ Groq API Processing Failure: {e}")
        return raw_name[:45], "Check out this amazing find on Amazon right now!"

def get_crisp_catchy_title(raw_name):
    """
    Cleans up bloated Amazon product titles into crisp, simple, and catchy titles
    by stripping out technical specs, parentheticals, and repetitive keywords.
    """
    # 1. Strip out everything inside parentheses or brackets (e.g., "(Black, 8GB RAM)", "[Pack of 2]")
    clean = re.sub(r'\([^)]*\)', '', raw_name)
    clean = re.sub(r'\[[^\]]*\]', '', clean)
    
    # 2. Remove common technical suffix noise (e.g., "with Garlic Press", "Model 2026", dimensions like 15cm x 10cm)
    clean = re.sub(r'\b\d+\s*(gb|mb|tb|mah|w|v|cm|mm|inch|ltr|liters|pc|pcs|pack|pk)\b.*', '', clean, flags=re.IGNORECASE)
    clean = re.sub(r'\b(with|for|compatible\s+with)\b.*', '', clean, flags=re.IGNORECASE)
    
    # 3. Strip special punctuation characters often used to separate SEO features
    clean = re.sub(r'[|,\-_:+•]', ' ', clean)
    
    # 4. Collapse multiple spaces and extract words
    words = clean.split()
    
    # 5. Grab only the first 4 to 6 words (the brand name + core product identifier)
    crisp_title = " ".join(words[:5]).title()
    
    # 6. Add an optional catchy flair or hook if desired (e.g., "Smart Find:")
    return crisp_title.strip()

def cleanup_temp_files():
    import time
    import gc
    import cv2  # Import cv2 directly here to clear window frames
    
    print("⏳ Allowing background threads and API servers 5 seconds to fully close...")
        
    try:
        cv2.destroyAllWindows()  # Force OpenCV to release any cached image frames
    except:
        pass
        
    gc.collect() # Force free unused memory pointers
    
    patterns = ["temp_*.jpg", "manual_temp_*.jpg"]
    
    for pattern in patterns:
        temp_files = glob.glob(os.path.join(os.getcwd(), pattern))
        for file in temp_files:
            try:
                if os.path.exists(file):
                    os.remove(file)
                    print(f"🗑️ Cleaned up leftover temporary asset: {os.path.basename(file)}")
            except PermissionError:
                # Fallback: If it's a temporary lock, try to rename or delete again after a micro-nap
                try:
                    time.sleep(1)
                    if os.path.exists(file):
                        os.remove(file)
                        print(f"🗑️ Cleaned up asset on secondary sweeping run: {os.path.basename(file)}")
                except Exception as e:
                    print(f"⚠️ Windows system file-lock actively preventing deletion of {os.path.basename(file)}. (Reason: {e})")
            except Exception as e:
                print(f"⚠️ Could not delete asset {os.path.basename(file)}: {e}")

def compile_landing_page(asin, name, product_url, local_image_path, price, output_dir=None):
    """
    Automates a responsive mobile-first grid landing page.
    Copies the product image into the local assets folder for stable GitHub Pages hosting.
    """
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))
        
    html_path = os.path.join(output_dir, "index.html")
    assets_dir = os.path.join(output_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    # ─── 📸 HOST IMAGE LOCALLY ON GITHUB ───
    # Determine where the image will live inside our GitHub repository
    github_image_relative_path = f"assets/{asin}.jpg"
    destination_path = os.path.join(assets_dir, f"{asin}.jpg")
    
    if local_image_path and os.path.exists(local_image_path):
        try:
            # Copy the image from your temporary folder to the assets tracking folder
            shutil.copy2(local_image_path, destination_path)
            print(f"📸 [Landing Page] Image successfully copied to assets: {github_image_relative_path}")
        except Exception as e:
            print(f"⚠️ [Landing Page] Failed to copy image to assets: {e}")
    else:
        # Fallback if the local file isn't found
        github_image_relative_path = "https://via.placeholder.com/150"
    # ────────────────────────────────────────
    
    clean_title = name.replace('"', "'")[:75] + "..."
    
    new_card_html = f"""
        <div class="deal-card" id="card-{asin}">
            <img class="deal-thumb" src="{github_image_relative_path}" alt="{clean_title}">
            <div class="deal-details">
                <h3 class="deal-title">{clean_title}</h3>
                <div class="deal-meta">
                    <span class="deal-price"></span>
                    <a class="deal-btn" href="{product_url}" target="_blank">Get Deal ➔</a>
                </div>
            </div>
        </div>
    """

    if not os.path.exists(html_path):
        print("🌐 [Landing Page] Base index.html file missing. Generating core brand template...")
        base_scaffolding = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 Best Daily Deals - SmartCart India 🔥</title>
    <style>
        :root {{ --bg: #0d0d11; --card-bg: #16161f; --text: #f3f4f6; --accent: #ff9900; --border: #262636; }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text); padding: 15px; display: flex; flex-direction: column; align-items: center; }}
        .header-panel {{ text-align: center; margin: 25px 0; max-width: 480px; width: 100%; }}
        .header-panel h1 {{ font-size: 1.6rem; color: var(--text); margin-bottom: 5px; }}
        .header-panel p {{ font-size: 0.9rem; color: #8b8ba7; }}
        .deals-container {{ max-width: 480px; width: 100%; display: flex; flex-direction: column; gap: 15px; }}
        .deal-card {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; display: flex; padding: 12px; gap: 12px; align-items: center; transition: transform 0.2s; }}
        .deal-card:hover {{ transform: scale(1.01); border-color: var(--accent); }}
        .deal-thumb {{ width: 85px; height: 85px; object-fit: contain; background: #fff; border-radius: 8px; padding: 4px; flex-shrink: 0; }}
        .deal-details {{ flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between; height: 100%; min-width: 0; }}
        .deal-title {{ font-size: 0.95rem; font-weight: 600; color: #e5e7eb; line-height: 1.3; margin-bottom: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .deal-meta {{ display: flex; justify-content: space-between; align-items: center; margin-top: auto; }}
        .deal-price {{ font-size: 1.1rem; font-weight: 700; color: var(--accent); }}
        .deal-btn {{ background: var(--accent); color: #000; text-decoration: none; font-size: 0.85rem; font-weight: 700; padding: 8px 14px; border-radius: 6px; transition: opacity 0.2s; }}
        .deal-btn:hover {{ opacity: 0.9; }}
    </style>
</head>
<body>
    <div class="header-panel">
        <h1>🛒 SmartCart India Deals</h1>
        <p>Click any product below to grab the live discount link direct from Amazon!</p>
    </div>
    <div class="deals-container" id="deals-wrapper">
        {new_card_html}
    </div>
</body>
</html>"""
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(base_scaffolding)
    else:
        with open(html_path, "r", encoding="utf-8") as f:
            web_content = f.read()
            
        if f'id="card-{asin}"' in web_content:
            print(f"ℹ️ [Landing Page] Item [{asin}] already formatted on dashboard deck. Skipping injection.")
            return True

        target_hook = '<div class="deals-container" id="deals-wrapper">'
        updated_web_content = web_content.replace(target_hook, f"{target_hook}\n{new_card_html}")
        
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(updated_web_content)
            
    print(f"✅ [Landing Page] Smoothly compiled deal grid asset updates to: {html_path}")
    return True

def sync_landing_page_to_github():
    """
    Automates staging, committing, and pushing the modified index.html 
    to GitHub Pages dynamically. Safely handles empty/no-change states 
    and suppresses Windows CRLF warning stalls.
    """
    print("🚀 [GitHub Deployment] Packaging and pushing updated storefront live...")
    
    project_dir = os.path.dirname(os.path.abspath(__file__))
    git_cmd = "git" 
    
    possible_git_paths = [
        r"C:\Program Files\Git\cmd\git.exe",
        r"C:\Program Files (x86)\Git\cmd\git.exe",
        os.path.expanduser(r"~\AppData\Local\Programs\Git\cmd\git.exe")
    ]
    
    for path in possible_git_paths:
        if os.path.exists(path):
            git_cmd = path
            break
            
    try:
        # ─── 🛠️ SILENCE WINDOWS LINE-ENDING STALLS ───
        # Tells Git to automatically convert line endings silently without pausing for input
        subprocess.run([git_cmd, "config", "core.autocrlf", "true"], check=True, capture_output=True, shell=True, text=True, cwd=project_dir)
        # ──────────────────────────────────────────────

        # Step 1: Check if index.html actually has modifications compared to the repository
        status_check = subprocess.run([git_cmd, "status", "--porcelain", "index.html"], 
                                      capture_output=True, text=True, shell=True, cwd=project_dir)
        
        # Also check if there are newly added images untracked in assets/
        assets_check = subprocess.run([git_cmd, "status", "--porcelain", "assets/"], 
                                      capture_output=True, text=True, shell=True, cwd=project_dir)
        
        if not status_check.stdout.strip() and not assets_check.stdout.strip():
            print("ℹ️ [GitHub Deployment] Storefront assets have no new modifications. Skipping deployment sync.")
            return True

        # Step 2: Stage BOTH index.html and the new locally hosted image assets cleanly
        subprocess.run([git_cmd, "add", "index.html"], check=True, capture_output=True, shell=True, text=True, cwd=project_dir)
        subprocess.run([git_cmd, "add", "assets/"], check=True, capture_output=True, shell=True, text=True, cwd=project_dir)
        
        # Step 3: Commit the update
        commit_msg = f"Auto-update deals grid: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run([git_cmd, "commit", "-m", commit_msg], check=True, capture_output=True, shell=True, text=True, cwd=project_dir)
        
        # Step 4: Push live to GitHub
        subprocess.run([git_cmd, "push"], check=True, capture_output=True, shell=True, text=True, cwd=project_dir)
        print("✅ [GitHub Deployment] Storefront successfully deployed globally!")
        return True
        
    except subprocess.CalledProcessError as e:
        error_output = e.stderr.lower() if e.stderr else ""
        if "nothing to commit" in error_output or "no changes added" in error_output or "up to date" in error_output:
            print("ℹ️ [GitHub Deployment] Storefront is already up to date.")
            return True
            
        print(f"❌ [GitHub Deployment Error] Pipeline sync stalled. True Git output:\n{e.stderr}")
        return False

def get_safe_filename(name):
    return re.sub(r'[^\w\s-]', '', name).strip()

def get_save_path(asin, prefix="Product"):
    now = datetime.now()
    path = os.path.join(
        os.getcwd(), 
        BASE_EXPORT_FOLDER, 
        now.strftime("%Y"), 
        now.strftime("%B"), 
        now.strftime("%d"), 
        f"{prefix}_{asin}"
    )
    os.makedirs(path, exist_ok=True)
    return path

def record_upload(asin, name):
    new_data = pd.DataFrame([{
        'asin': asin,
        'name': name,
        'date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    }])
    file_exists = os.path.isfile(HISTORY_FILE)
    new_data.to_csv(HISTORY_FILE, mode='a', index=False, header=not file_exists, encoding='utf-8')
    print(f"📝 Recorded {asin} to history.")

def get_uploaded_asins():    
    if not os.path.exists(HISTORY_FILE):
        return set()
    try:
        df = pd.read_csv(HISTORY_FILE, usecols=['asin'], dtype={'asin': str})
        return set(df['asin'].unique())
    except Exception as e:
        print(f"⚠️ Could not read history: {e}")
        return set()

def start_daily_routine():
    product_found = False
    
    while not product_found:
        print("🧹 Closing Brave Browser sessions...")
        if os.getenv("GITHUB_ACTIONS") == "true":
            # Extra safety step for cloud runners to kill hung processes
            pass 
        else:
            os.system("taskkill /f /im brave.exe >nul 2>&1")
        time.sleep(2)

        options = webdriver.ChromeOptions()
        if os.getenv("GITHUB_ACTIONS") == "true":
            print("🌐 Cloud Environment Detected: Configuring Headless Chromium...")
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            driver = webdriver.Chrome(options=options)
        else:
            print("💻 Local Environment Detected: Launching Local Brave Instance...")
            if BRAVE_PATH:
                options.binary_location = BRAVE_PATH
            if BRAVE_USER_DATA:
                options.add_argument(f"--user-data-dir={BRAVE_USER_DATA}")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        try:
            pool_size_env = os.getenv("pool_size")
            pool_size = int(pool_size_env) if pool_size_env else 5
            products_pool = scout.get_bestsellers(driver, count=pool_size)
            
            if not products_pool:
                print("❌ No products found on Amazon category page. Retrying fresh loop...")
                driver.quit()
                continue
            
            uploaded_asins = get_uploaded_asins() 
            new_products = [p for p in products_pool if p['asin'] not in uploaded_asins]

            if not new_products:
                print(f"Total {len(products_pool)} products checked, but all are already uploaded. 😴 Retrying...")
                driver.quit()
                continue
            
            product_count_env = os.getenv("Product_Count")
            product_count = int(product_count_env) if product_count_env else 1
            products_found = new_products[:product_count]  

            for i, item in enumerate(products_found):
                print(f"✨ Found new product: {item['name'][:50]}...")
                asin = item.get('asin')

                if asin in uploaded_asins:
                    print(f"⏭️ Skipping {asin} - already uploaded.")
                    continue

                safe_name = item.get('name')
                specs = item.get('specs', '').replace(" | ","\n-")
                temp_images = item.get('images', [])

                if not temp_images:
                    print("⚠️ Missing images for this selection. Retrying loop...")
                    continue

                # Let the loop know we found a valid product so we can terminate the while condition
                product_found = True

                folder = get_save_path(asin, prefix="Product")
                video_path = os.path.join(folder, f"Video_{asin}.mp4")
                
                final_images = []
                
                for idx, img in enumerate(temp_images):
                    dest = os.path.join(folder, f"img_{idx}.jpg")
                    if os.path.exists(img):
                        shutil.move(img, dest)
                        final_images.append(dest)            
                
                viral_title, viral_voiceover_script = reframe_product_for_youtube(safe_name, specs)
                voice_script = f"{viral_title}. {viral_voiceover_script}."
                print(f"💬 Generated script text: {voice_script}")

                print("🎨 Invoking Dynamic Thumbnail Engine...")
                generated_thumb_path = thumbnail_engine.generate_thumbnail_multi(
                    asin=asin, product_name=viral_title, specifications=[], image_paths_list=final_images
                )
                
                video_render_images = final_images.copy()
                if generated_thumb_path and os.path.exists(generated_thumb_path):
                    video_render_images.insert(0, generated_thumb_path)

                editor.create_pro_video(video_render_images, viral_title, video_path, voice_text=voice_script)

                if generated_thumb_path and os.path.exists(generated_thumb_path):
                    thumb_dest_path = os.path.join(folder, f"tn_{asin}.jpg")
                    shutil.move(generated_thumb_path, thumb_dest_path)
                
                product_url = f"https://www.amazon.in/dp/{asin}?tag={os.getenv('Affiliate_Code')}"
                current_category = item.get('category', 'Default')
                selected_tags = CATEGORY_HASHTAGS.get(current_category, CATEGORY_HASHTAGS["Default"])
                hashtag_string_block = " ".join(selected_tags)
                backend_yt_tags = ", ".join([tag.replace("#", "").lower() for tag in selected_tags])

                description_text = (
                    f"📦 {viral_title}\n\nBuy Link: {product_url}\n\n"
                    "#(ad) As an Amazon Associate I earn from qualifying purchases.\n"
                    f"{hashtag_string_block}"
                )
                
                desc_path = os.path.join(folder, "description.txt")
                with open(desc_path, "w", encoding="utf-8") as f:
                    f.write(description_text)

                youtube_url = uploader.upload_to_youtube(None, video_path, viral_title, description_text, backend_yt_tags)
                insta_uploader.upload_to_instagram(video_path, description_text, product_url)
                telegram_poster.post_to_telegram(viral_title, product_url, video_path, youtube_url=youtube_url)                

                record_upload(asin, viral_title)

                primary_thumbnail = final_images[0] if final_images else ""
                compile_landing_page(
                    asin=asin, name=viral_title, product_url=product_url,
                    local_image_path=primary_thumbnail, price=item.get('price', 'Check Price')
                )
                
        finally:
            driver.quit()
            print("🧹 Cleaning up unused product images...")
            cleanup_temp_files()
        

def is_already_uploaded(asin, HISTORY_FILE):
    if not os.path.exists(HISTORY_FILE):
        return False
    with open(HISTORY_FILE, "r", encoding='utf-8') as f:
        return asin in f.read()

def run_manual_post(url):
    """Bypasses the daily routine but keeps the same high-quality output."""
    print("🧹 Closing Brave Browser sessions...")
    os.system("taskkill /f /im brave.exe >nul 2>&1")
    time.sleep(2)

    options = webdriver.ChromeOptions()
    options.binary_location = BRAVE_PATH
    options.add_argument(f"--user-data-dir={BRAVE_USER_DATA}")
    options.add_argument(r'--profile-directory=Default')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # 1. Scrape the data
        product = scout.scrape_specific_product(driver, url)
        if not product:
            return

        # 2. DUPLICATE CHECK
        if is_already_uploaded(product['asin'], HISTORY_FILE):
            print(f"🚫 Skipping: {product['asin']} has already been posted before!")
            return
        
        # 3. PREPARE PATHS 
        #safe_name = get_crisp_catchy_title(product['name'])
        safe_name = product['name']

        # if len(safe_name) > 100:
        #     safe_name = safe_name[:100].strip()

        specs = product['specs'].replace(" | ","\n-")

        folder = get_save_path(product['asin'], prefix="Manual")
        video_path = os.path.join(folder, "final_video.mp4")

        # 4. MOVE IMAGES TO FOLDER BEFORE EDITING
        archived_images = []
        for idx, img_path in enumerate(product['images']):
            if os.path.exists(img_path):
                # CHECK FILE SIZE: If the image is less than 2KB, it's corrupted or empty
                file_size = os.path.getsize(img_path)
                
                if file_size < 2048:
                    print(f"⚠️ WARNING: {os.path.basename(img_path)} is empty or corrupted! Skipping.")
                    continue

                destination = os.path.join(folder, f"img_{idx}.jpg")
                try:
                    shutil.move(img_path, destination)
                    archived_images.append(destination)
                except Exception as e:
                    print(f"⚠️ Could not move image: {e}")        

        product['images'] = archived_images

        if not archived_images:
            print("❌ TERMINATING: No valid product images were successfully scraped from Amazon. Video skipped.")
            return

        # 5. CREATE VIDEO 
        print(f"🎬 Generating Manual Video for: {safe_name[:30]}")

        # --- 🎙️ GENERATING THE NARRATION SCRIPT FOR THE VOICEOVER ---
        # Extract first 2 bullet points from specifications for a clean, short audio loop
        # clean_specs_list = [s.strip() for s in specs.split('\n-') if s.strip()]
        # short_specs_summary = " ".join(clean_specs_list[:2])
        
        viral_title, viral_voiceover_script = reframe_product_for_youtube(safe_name, specs)
        
        # Construct a high-retention narration voice hook
        voice_script = f"{viral_title}.{viral_voiceover_script}."
        print(f"💬 Generated script text: {voice_script}")
        # ───────────────────────────────────────────────────────────

        # ─── NEW: GENERATE THE DYNAMIC THUMBNAIL FIRST ───
        print("🎨 Invoking Dynamic Thumbnail Engine to compile video hook frame...")
        # Clean specs array conversion to pass cleanly to the thumbnail cards
        clean_specs_list = [s.strip() for s in specs.split('\n-') if s.strip()]
        
        generated_thumb_path = thumbnail_engine.generate_thumbnail_multi(
            asin=product['asin'],
            product_name=viral_title, # Pass the viral clean name for high-impact typography
            specifications=[],
            image_paths_list=product['images']
        )
        
        # If the engine compiles successfully, slide it into the absolute front of the video list
        video_render_images = product['images'].copy()
        if generated_thumb_path and os.path.exists(generated_thumb_path):
            video_render_images.insert(0, generated_thumb_path)
            print("📌 Thumbnail successfully prioritized as frame 0 for the video timeline.")       
        # ──────────────────────────────────────────────────

        # Pass the updated image list containing the thumbnail into the video editor
        editor.create_pro_video(video_render_images, viral_title, video_path, voice_text=voice_script)

        if generated_thumb_path and os.path.exists(generated_thumb_path):
            thumb_dest_path = os.path.join(folder, f"tn_{product['asin']}.jpg")
            shutil.move(generated_thumb_path, thumb_dest_path)
            print(f"📦 Thumbnail moved cleanly to asset archive: {thumb_dest_path}")

        # Build correct absolute affiliate link
        product_url = f"https://www.amazon.in/dp/{product['asin']}?tag={os.getenv('Affiliate_Code')}"

        # --- 📈 DYNAMIC ALGORITHMIC TAG COMPILER ---
        # 1. Identify which category scout.py extracted (Fallback to Default if missing)
        current_category = product.get('category', 'Default')
        selected_tags = CATEGORY_HASHTAGS.get(current_category, CATEGORY_HASHTAGS["Default"])
        
        # 2. Compile into a clean string string separated by single spaces for description files
        hashtag_string_block = " ".join(selected_tags)
        
        # 3. Clean up the tags into standard comma layout for YouTube's hidden backend registry
        backend_yt_tags = ", ".join([tag.replace("#", "").lower() for tag in selected_tags])
        # ───────────────────────────────────────────

        # 6. SAVE DESCRIPTION FILE (Loaded with contextual optimization strings)
        description_text = (
            f"📦 {safe_name}\n\n"
            #f"Features:\n-{specs}\n\n"        
            f"Buy Link: {product_url}\n\n"
            "#(ad) As an Amazon Associate I earn from qualifying purchases.\n"
            f"{hashtag_string_block}" # Placed perfectly at the baseline footer
        )
        
        desc_path = os.path.join(folder, "description.txt")
        with open(desc_path, "w", encoding="utf-8") as f:
            f.write(description_text)

        # 7. POST TO PLATFORMS        
        # YouTube (API Method - Returns YouTube Link String)
        tags = "amazon, deals, india, gadget"
        youtube_url = uploader.upload_to_youtube(None, video_path, viral_title, description_text, backend_yt_tags)

        # Pass that exact youtube_url string into your updated uploader module!
        insta_uploader.upload_to_instagram(video_path, description_text)

        # # Telegram (Funnel the captured YouTube URL string directly into our layout parameter)
        telegram_poster.post_to_telegram(viral_title, product_url, video_path, youtube_url = '')

        # 8. RECORD HISTORY
        record_upload(product['asin'], viral_title)
        print(f"✅ Manual Post Complete: {product['asin']}")

        # --- 🌐 NEW LANDING PAGE INTEGRATION LOOP STEP ---
        # Fallback cascade to find whatever valid image string your scraper collected
        primary_thumbnail = ""
        if archived_images and len(archived_images) > 0:
            primary_thumbnail = archived_images[0] # Points to folder/img_0.jpg
        
        compile_landing_page(
            asin=product['asin'],
            name=viral_title,
            product_url=product_url,
            local_image_path=primary_thumbnail, # Passing the local file path
            price=product.get('price', 'Check Price')
        )

        # 🚀 NEW: PUSH UPDATES LIVE TO GITHUB PAGES
        sync_landing_page_to_github()

    finally:  
        driver.quit()
        print("🧹 Cleaning up unused product images...")
        cleanup_temp_files()
        

if __name__ == "__main__":
    cleanup_temp_files()
    start_daily_routine()    
    
    # manual_url = "https://www.amazon.in/dp/B0CZ8YG4GN"
    # run_manual_post(manual_url)