import time
import urllib.request
import os
import random
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, 'Config.env')
load_dotenv(ENV_PATH)

blacklist = ["Credit Card Bill", "Gift Card", "Subscription","Volume Control - for Fire TV Stick"]

CATEGORIES = {
    "Electronics":"https://www.amazon.in/gp/bestsellers/electronics/ref=zg_bs_unv_electronics_1_1388867031_1",
    "Accessories": "https://www.amazon.in/gp/bestsellers/electronics/1388867031/ref=zg_bs_nav_electronics_1",
    "Cameras & Photography": "https://www.amazon.in/gp/bestsellers/electronics/1388977031/ref=zg_bs_nav_electronics_1",
    "Car & Vehicle Electronics": "https://www.amazon.in/gp/bestsellers/electronics/1389221031/ref=zg_bs_nav_electronics_1",
    "Computers & Accessories": "https://www.amazon.in/gp/bestsellers/electronics/1458204031/ref=zg_bs_nav_electronics_1",
    "GPS & Accessories": "https://www.amazon.in/gp/bestsellers/electronics/1389315031/ref=zg_bs_nav_electronics_1",
    "Headphones": "https://www.amazon.in/gp/bestsellers/electronics/1388921031/ref=zg_bs_nav_electronics_1",
    "Hi-Fi & Home Audio": "https://www.amazon.in/gp/bestsellers/electronics/1389335031/ref=zg_bs_nav_electronics_1",
    "Home Theatre, TV & Video": "https://www.amazon.in/gp/bestsellers/electronics/1389375031/ref=zg_bs_nav_electronics_1",
    "Mobiles & Tablets": "https://www.amazon.in/gp/bestsellers/electronics/92071051031/ref=zg_bs_nav_electronics_1",
    "Portable Media Players": "https://www.amazon.in/gp/bestsellers/electronics/1389433031/ref=zg_bs_nav_electronics_1",
    "Telephones & Accessories": "https://www.amazon.in/gp/bestsellers/electronics/1389481031/ref=zg_bs_nav_electronics_1",
    "Warranties": "https://www.amazon.in/gp/bestsellers/electronics/1389493031/ref=zg_bs_nav_electronics_1",
    "Wearable Technology": "https://www.amazon.in/gp/bestsellers/electronics/11599648031/ref=zg_bs_nav_electronics_1",
    "eBook Readers & Accessories": "https://www.amazon.in/gp/bestsellers/electronics/1389494031/ref=zg_bs_nav_electronics_1",
    "Accessories (1388978031)": "https://www.amazon.in/gp/bestsellers/electronics/1388978031/ref=zg_bs_nav_electronics_2_1388867031",
    "Accessories (1389316031)": "https://www.amazon.in/gp/bestsellers/electronics/1389316031/ref=zg_bs_nav_electronics_2_1388867031",
    "Accessories (1389434031)": "https://www.amazon.in/gp/bestsellers/electronics/1389434031/ref=zg_bs_nav_electronics_2_1388867031",
    "Accessories (1389463031)": "https://www.amazon.in/gp/bestsellers/electronics/1389463031/ref=zg_bs_nav_electronics_2_1388867031",
    "Accessories (1389482031)": "https://www.amazon.in/gp/bestsellers/electronics/1389482031/ref=zg_bs_nav_electronics_2_1388867031",
    "Blank Media Cases & Wallets": "https://www.amazon.in/gp/bestsellers/electronics/1375260031/ref=zg_bs_nav_electronics_2_1388867031",
    "Car & Vehicle Electronics Accessories": "https://www.amazon.in/gp/bestsellers/electronics/1389226031/ref=zg_bs_nav_electronics_2_1388867031",
    "Memory Cards": "https://www.amazon.in/gp/bestsellers/electronics/1388963031/ref=zg_bs_nav_electronics_2_1388867031",
    "Mobile Accessories": "https://www.amazon.in/gp/bestsellers/electronics/1389402031/ref=zg_bs_nav_electronics_2_1388867031",
    "Tablet Accessories": "https://www.amazon.in/gp/bestsellers/electronics/1375328031/ref=zg_bs_nav_electronics_2_1388867031",
    "Action Cameras": "https://www.amazon.in/gp/bestsellers/electronics/3404636031/ref=zg_bs_nav_electronics_2_1388977031",
    "Binoculars, Telescopes & Optics": "https://www.amazon.in/gp/bestsellers/electronics/1389159031/ref=zg_bs_nav_electronics_2_1388977031",
    "Body Mounted Cameras": "https://www.amazon.in/gp/bestsellers/electronics/51419882031/ref=zg_bs_nav_electronics_2_1388977031",
    "Cases & Bags": "https://www.amazon.in/gp/bestsellers/electronics/1389018031/ref=zg_bs_nav_electronics_2_1388977031",
    "Digital Cameras": "https://www.amazon.in/gp/bestsellers/electronics/1389175031/ref=zg_bs_nav_electronics_2_1388977031",
    "Film Cameras": "https://www.amazon.in/gp/bestsellers/electronics/1389183031/ref=zg_bs_nav_electronics_2_1388977031",
    "Film Scanners": "https://www.amazon.in/gp/bestsellers/electronics/1375455031/ref=zg_bs_nav_electronics_2_1388977031",
    "Flashes": "https://www.amazon.in/gp/bestsellers/electronics/1389193031/ref=zg_bs_nav_electronics_2_1388977031",
    "Lenses": "https://www.amazon.in/gp/bestsellers/electronics/1389197031/ref=zg_bs_nav_electronics_2_1388977031",
    "Photo Printers": "https://www.amazon.in/gp/bestsellers/electronics/1375450031/ref=zg_bs_nav_electronics_2_1388977031",
    "Photo Studio & Lighting": "https://www.amazon.in/gp/bestsellers/electronics/1389103031/ref=zg_bs_nav_electronics_2_1388977031",
    "Professional Video Cameras": "https://www.amazon.in/gp/bestsellers/electronics/51419880031/ref=zg_bs_nav_electronics_2_1388977031",
    "Projectors": "https://www.amazon.in/gp/bestsellers/electronics/1389388031/ref=zg_bs_nav_electronics_2_1388977031",
    "Security Cameras": "https://www.amazon.in/gp/bestsellers/electronics/1389203031/ref=zg_bs_nav_electronics_2_1388977031",
    "Simulated Cameras": "https://www.amazon.in/gp/bestsellers/electronics/1389206031/ref=zg_bs_nav_electronics_2_1388977031",  
    "Underwater Video & Photography": "https://www.amazon.in/gp/bestsellers/electronics/1389214031/ref=zg_bs_nav_electronics_2_1388977031",
    "Video Cameras": "https://www.amazon.in/gp/bestsellers/electronics/1389174031/ref=zg_bs_nav_electronics_2_1388977031",
    "Car & Vehicle Electronics Accessories": "https://www.amazon.in/gp/bestsellers/electronics/1389226031/ref=zg_bs_nav_electronics_2_1389221031",
    "Car & Vehicle GPS Devices": "https://www.amazon.in/gp/bestsellers/electronics/1389266031/ref=zg_bs_nav_electronics_2_1389221031",
    "Car Electronics": "https://www.amazon.in/gp/bestsellers/electronics/1389267031/ref=zg_bs_nav_electronics_2_1389221031",
    "Marine Electronics": "https://www.amazon.in/gp/bestsellers/electronics/1389297031/ref=zg_bs_nav_electronics_2_1389221031",
    "Motorcycle Electronics": "https://www.amazon.in/gp/bestsellers/electronics/1389310031/ref=zg_bs_nav_electronics_2_1389221031",
    "Accessories": "https://www.amazon.in/gp/bestsellers/electronics/1375248031/ref=zg_bs_nav_electronics_2_1458204031",
    "Audio & Video Accessories": "https://www.amazon.in/gp/bestsellers/electronics/1375459031/ref=zg_bs_nav_electronics_2_1458204031",
    "Components": "https://www.amazon.in/gp/bestsellers/electronics/1375344031/ref=zg_bs_nav_electronics_2_1458204031",
    "External Devices & Data Storage": "https://www.amazon.in/gp/bestsellers/electronics/1375393031/ref=zg_bs_nav_electronics_2_1458204031",
    "Keyboards, Mice & Input Devices": "https://www.amazon.in/gp/bestsellers/electronics/1375412031/ref=zg_bs_nav_electronics_2_1458204031",
    "Networking Devices": "https://www.amazon.in/gp/bestsellers/electronics/1375427031/ref=zg_bs_nav_electronics_2_1458204031",
    "Accessories": "https://www.amazon.in/gp/bestsellers/electronics/1389316031/ref=zg_bs_nav_electronics_2_1389315031",
    "Car GPS": "https://www.amazon.in/gp/bestsellers/electronics/1389328031/ref=zg_bs_nav_electronics_2_1389315031",
    "GPS Trackers": "https://www.amazon.in/gp/bestsellers/electronics/1389329031/ref=zg_bs_nav_electronics_2_1389315031",
    "GPS Units": "https://www.amazon.in/gp/bestsellers/electronics/3403901031/ref=zg_bs_nav_electronics_2_1389315031",
    "Item Finders": "https://www.amazon.in/gp/bestsellers/electronics/21529666031/ref=zg_bs_nav_electronics_2_1389315031",
    "Marine GPS": "https://www.amazon.in/gp/bestsellers/electronics/1389330031/ref=zg_bs_nav_electronics_2_1389315031",
    "Motorcycle GPS": "https://www.amazon.in/gp/bestsellers/electronics/1389331031/ref=zg_bs_nav_electronics_2_1389315031",
    "In-Ear": "https://www.amazon.in/gp/bestsellers/electronics/14146389031/ref=zg_bs_nav_electronics_2_1388921031",
    "On-Ear": "https://www.amazon.in/gp/bestsellers/electronics/14146391031/ref=zg_bs_nav_electronics_2_1388921031",
    "Open-Ear Headphones": "https://www.amazon.in/gp/bestsellers/electronics/76028196031/ref=zg_bs_nav_electronics_2_1388921031",
    "Over-Ear": "https://www.amazon.in/gp/bestsellers/electronics/14146390031/ref=zg_bs_nav_electronics_2_1388921031",
    "Accessories": "https://www.amazon.in/gp/bestsellers/electronics/1389336031/ref=zg_bs_nav_electronics_2_1389335031",
    "Compact Stereos": "https://www.amazon.in/gp/bestsellers/electronics/1389338031/ref=zg_bs_nav_electronics_2_1389335031",
    "Media Streaming Devices": "https://www.amazon.in/gp/bestsellers/electronics/1389339031/ref=zg_bs_nav_electronics_2_1389335031",
    "Radios & Boomboxes": "https://www.amazon.in/gp/bestsellers/electronics/1389343031/ref=zg_bs_nav_electronics_2_1389335031",
    "Receivers & Separates": "https://www.amazon.in/gp/bestsellers/electronics/1389349031/ref=zg_bs_nav_electronics_2_1389335031",
    "Speakers": "https://www.amazon.in/gp/bestsellers/electronics/1389365031/ref=zg_bs_nav_electronics_2_1389335031",
    "AV Receivers & Amplifiers": "https://www.amazon.in/gp/bestsellers/electronics/1389376031/ref=zg_bs_nav_electronics_2_1389375031",
    "Accessories": "https://www.amazon.in/gp/bestsellers/electronics/1389377031/ref=zg_bs_nav_electronics_2_1389375031",
    "Blu-ray Players & Recorders": "https://www.amazon.in/gp/bestsellers/electronics/1389379031/ref=zg_bs_nav_electronics_2_1389375031",
    "DVD Players & Recorders": "https://www.amazon.in/gp/bestsellers/electronics/1389382031/ref=zg_bs_nav_electronics_2_1389375031",
    "Home Theater Systems": "https://www.amazon.in/gp/bestsellers/electronics/1389387031/ref=zg_bs_nav_electronics_2_1389375031",
    "Media Streaming Devices": "https://www.amazon.in/gp/bestsellers/electronics/1389339031/ref=zg_bs_nav_electronics_2_1389375031",
    "Portable DVD & Blu-ray Players": "https://www.amazon.in/gp/bestsellers/electronics/1389457031/ref=zg_bs_nav_electronics_2_1389375031",
    "Projectors": "https://www.amazon.in/gp/bestsellers/electronics/1389388031/ref=zg_bs_nav_electronics_2_1389375031",    
    "Speakers": "https://www.amazon.in/gp/bestsellers/electronics/51419895031/ref=zg_bs_nav_electronics_2_1389375031",
    "TV Receivers": "https://www.amazon.in/gp/bestsellers/electronics/1389392031/ref=zg_bs_nav_electronics_2_1389375031",
    "Televisions": "https://www.amazon.in/gp/bestsellers/electronics/1389396031/ref=zg_bs_nav_electronics_2_1389375031",
    "Video Glasses": "https://www.amazon.in/gp/bestsellers/electronics/1389397031/ref=zg_bs_nav_electronics_2_1389375031",
    "Video Players & Recorders": "https://www.amazon.in/gp/bestsellers/electronics/1389398031/ref=zg_bs_nav_electronics_2_1389375031",
    "Mobile Accessories": "https://www.amazon.in/gp/bestsellers/electronics/1389402031/ref=zg_bs_nav_electronics_2_92071051031",
    "Smartphones & Basic Mobiles": "https://www.amazon.in/gp/bestsellers/electronics/1389432031/ref=zg_bs_nav_electronics_2_92071051031",
    "Tablet Accessories": "https://www.amazon.in/gp/bestsellers/electronics/1375328031/ref=zg_bs_nav_electronics_2_92071051031",
    "Tablets": "https://www.amazon.in/gp/bestsellers/electronics/1375458031/ref=zg_bs_nav_electronics_2_92071051031",
    "Accessories": "https://www.amazon.in/gp/bestsellers/electronics/1389434031/ref=zg_bs_nav_electronics_2_1389433031",
    "Boomboxes": "https://www.amazon.in/gp/bestsellers/electronics/1389454031/ref=zg_bs_nav_electronics_2_1389433031",
    "CD Players": "https://www.amazon.in/gp/bestsellers/electronics/1389455031/ref=zg_bs_nav_electronics_2_1389433031",
    "Cassette Players": "https://www.amazon.in/gp/bestsellers/electronics/1389456031/ref=zg_bs_nav_electronics_2_1389433031",
    "MP3/MP4 Players": "https://www.amazon.in/gp/bestsellers/electronics/1389458031/ref=zg_bs_nav_electronics_2_1389433031",
    "MiniDisc Players": "https://www.amazon.in/gp/bestsellers/electronics/1389459031/ref=zg_bs_nav_electronics_2_1389433031",
    "Portable DVD & Blu-ray Players": "https://www.amazon.in/gp/bestsellers/electronics/1389457031/ref=zg_bs_nav_electronics_2_1389433031",
    "Radios": "https://www.amazon.in/gp/bestsellers/electronics/1389460031/ref=zg_bs_nav_electronics_2_1389433031",
    "Shortwave Receivers": "https://www.amazon.in/gp/bestsellers/electronics/1389347031/ref=zg_bs_nav_electronics_2_1389433031",
    "Activity Trackers": "https://www.amazon.in/gp/bestsellers/electronics/4730577031/ref=zg_bs_nav_electronics_2_11599648031",
    "Arm & Wristband Accessories": "https://www.amazon.in/gp/bestsellers/electronics/11599650031/ref=zg_bs_nav_electronics_2_11599648031",
    "Baby Wearables": "https://www.amazon.in/gp/bestsellers/electronics/11599652031/ref=zg_bs_nav_electronics_2_11599648031",
    "Glasses": "https://www.amazon.in/gp/bestsellers/electronics/11599657031/ref=zg_bs_nav_electronics_2_11599648031",
    "Pendants": "https://www.amazon.in/gp/bestsellers/electronics/11599655031/ref=zg_bs_nav_electronics_2_11599648031",
    "Rings": "https://www.amazon.in/gp/bestsellers/electronics/11599656031/ref=zg_bs_nav_electronics_2_11599648031",
    "Single Ear Bluetooth Headsets": "https://www.amazon.in/gp/bestsellers/electronics/21529672031/ref=zg_bs_nav_electronics_2_11599648031",
    "Smart Clip Accessories": "https://www.amazon.in/gp/bestsellers/electronics/11599651031/ref=zg_bs_nav_electronics_2_11599648031",
    "Smart Watches": "https://www.amazon.in/gp/bestsellers/electronics/5605728031/ref=zg_bs_nav_electronics_2_11599648031",
    "Smart Watches & Accessories": "https://www.amazon.in/gp/bestsellers/electronics/74711502031/ref=zg_bs_nav_electronics_2_11599648031",
    "Temporary Tattoos": "https://www.amazon.in/gp/bestsellers/electronics/11599658031/ref=zg_bs_nav_electronics_2_11599648031",
    "VR Mobile Phone Headsets": "https://www.amazon.in/gp/bestsellers/electronics/12467536031/ref=zg_bs_nav_electronics_2_11599648031",
    "Wristbands": "https://www.amazon.in/gp/bestsellers/electronics/11599653031/ref=zg_bs_nav_electronics_2_11599648031"
}

def generate_tags(name, specs):
    base_tags = ["AmazonFinds", "CoolGadgets", "AmazonIndia"]
    keywords = [w for w in name.split() if len(w) > 4][:6]
    return ", ".join(list(set(base_tags + keywords)))

def get_bestsellers(driver, count):

    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    
    cat_name, cat_url = random.choice(list(CATEGORIES.items()))
    print(f"🎲 Randomly selected category: {cat_name}")
    
    driver.get(cat_url)
    time.sleep(30)
    products = []
    
    for i in range(count):
        cards = driver.find_elements(By.CSS_SELECTOR, ".zg-grid-general-faceout")
        if i >= len(cards): break
        
        try:
            card = cards[i]

            name = card.text.split('\n')[0].strip()

            if any(keyword in name for keyword in blacklist):
                print(f"⏭️ Skipping: {name}")
                continue

            link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
            asin = link.split("/dp/")[1].split("/")[0]

            driver.set_window_size(1920, 1080)
            
            driver.get(link)
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, 350);")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            img_paths = []
            thumbs = []
            try:
                # Check if standard thumbnails exist within a reasonable 10s wait window
                WebDriverWait(driver, 10).until(
                    lambda d: d.find_elements(By.CSS_SELECTOR, "#altImages img") or 
                            d.find_elements(By.CSS_SELECTOR, "#altimages img")
                )
                thumbs = driver.find_elements(By.CSS_SELECTOR, "#altImages img, #altimages img")
                print(f"✅ Successfully found standard thumbnail grid. Elements: {len(thumbs)}")
                
            except Exception:
                print("⏳ Standard thumbnail container missing (Anti-bot layout detected). Engaging emergency image grabber...")
                # 🚀 Fix 3: Target the main display images, variant arrays, or main view panels directly
                fallback_selectors = [
                    "#landingImage", 
                    "#imgBlkFront", 
                    ".imgTagWrapper img", 
                    "#main-image-container img",
                    "img.main-image"
                ]
                for selector in fallback_selectors:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        for el in elements:
                            if el not in thumbs:
                                thumbs.append(el)
                print(f"🔮 Emergency grabber isolated {len(thumbs)} raw asset layout target targets.")
            
            print(f"image count in thumbs variable: {len(thumbs)}")

            found = 0
            for idx, img in enumerate(thumbs):
                if found >= 7: break
            
                # 1. Pull the element attributes
                alt_text = (img.get_attribute("alt") or "").strip().lower()
                src = img.get_attribute("data-old-hires") or img.get_attribute("src")
                
                if not src:
                    continue

                # 🚀 STRICT FILTER: Drop video cards based on explicit text values or thumbnail decorations
                if "video" in alt_text:
                    print(f"⏭️ Skipping element {idx}: Matched alt label '{img.get_attribute('alt')}'")
                    continue
                    
                if any(x in src for x in ["play-button", "gif", "inline-twister", "video-placeholder", "play-icon-overlay"]):
                    print(f"⏭️ Skipping element {idx}: Detected video/interactive decoration string in URL")
                    continue
                                    
                # 2. Convert thumbnail asset signature into clean, full-resolution image path
                high_res = src
                if "._S" in src:
                    high_res = src.split("._S")[0] + ".jpg"
                elif "._" in src:
                    high_res = src.split("._")[0] + ".jpg"
                    
                try:
                    local_file = os.path.join(os.getcwd(), f"temp_{i}_{idx}.jpg")
                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')]
                    urllib.request.install_opener(opener)                    
                    urllib.request.urlretrieve(high_res, local_file)                    
                    if os.path.getsize(local_file) > 1000: # Ensure it's a real valid image
                        img_paths.append(local_file)
                        found += 1
                except Exception as e:
                    print(f"❌ Download failed: {e}")
            
            bullets = driver.find_elements(By.CSS_SELECTOR, "#feature-bullets ul li span, #pqv-feature-bullets ul li span")
            specs = " | ".join([b.text.strip() for b in bullets if len(b.text.strip()) > 10][:7])
            
            print(f"image count in img_paths variable: {len(img_paths)}")

            products.append({
                "asin": asin, "name": name, "link": f"{link}?tag=smartcart03b-21",
                "images": img_paths, "specs": specs, "tags": generate_tags(name, specs)
            })
            driver.back()
            time.sleep(3)
        except:
            continue
    return products

def scrape_specific_product(driver, product_url):
    print(f"🎯 Manual Target: {product_url}")
    driver.get(product_url)
    time.sleep(5)

    try:
        name = driver.find_element(By.ID, "productTitle").text.strip()
        asin = product_url.split("/dp/")[1].split("/")[0] if "/dp/" in product_url else "MANUAL"        
        bullets = driver.find_elements(By.CSS_SELECTOR, "#feature-bullets ul li span")
        specs = " | ".join([b.text.strip() for b in bullets if len(b.text.strip()) > 10][:3])
        try:
            price = driver.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
            price = f"₹{price}"
        except:
            price = "Check Link"

        img_paths = []
        thumbs = driver.find_elements(By.CSS_SELECTOR, "#altImages img")
        found = 0
        for idx, img in enumerate(thumbs):
            if found >= 7: break
            src = img.get_attribute("src")
            if not src: continue

            if "play-button" not in src and "._S" in src:
                high_res = src.split("._")[0] + ".jpg"                
                try:
                    local_file = os.path.join(os.getcwd(), f"manual_temp_{found}.jpg")
                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                    urllib.request.install_opener(opener)                    
                    urllib.request.urlretrieve(high_res, local_file)                    
                    if os.path.getsize(local_file) > 1000: # Ensure it's a real image
                        img_paths.append(local_file)
                        found += 1
                except Exception as e:
                    print(f"❌ Download failed: {e}")

        return {
            "asin": asin,
            "name": name,
            "link": f"https://www.amazon.in/dp/{asin}?tag={os.getenv('Affiliate_Code')}",
            "price": price,
            "specs": specs,
            "images": img_paths
        }
    except Exception as e:
        print(f"❌ Manual Scrape Failed: {e}")
        return None