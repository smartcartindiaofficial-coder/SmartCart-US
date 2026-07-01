import time
import urllib.request
import os
import random
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, 'Config.env')
load_dotenv(ENV_PATH)

blacklist = ["Credit Card Bill", "Gift Card", "Subscription","Volume Control - for Fire TV Stick","renewal"]

CATEGORIES = {
    "Electronics":"https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/ref=zg_bs_nav_electronics_0",
    "Accessories & Supplies":"https://www.amazon.com/Best-Sellers-Electronics-Electronics-Accessories-Supplies/zgbs/electronics/281407/ref=zg_bs_nav_electronics_1",
    "Camera & Photo":"https://www.amazon.com/Best-Sellers-Electronics-Camera-Photo-Products/zgbs/electronics/502394/ref=zg_bs_nav_electronics_1",
    "Car Electronics":"https://www.amazon.com/Best-Sellers-Electronics-Car-Electronics/zgbs/electronics/1077068/ref=zg_bs_nav_electronics_1",
    "Cell Phones & Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Cell-Phones-Accessories/zgbs/electronics/2811119011/ref=zg_bs_nav_electronics_1",
    "Computers & Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Computers-Accessories/zgbs/electronics/541966/ref=zg_bs_nav_electronics_1",
    "GPS & Navigation":"https://www.amazon.com/Best-Sellers-Electronics-GPS-Finders-Accessories/zgbs/electronics/172526/ref=zg_bs_nav_electronics_1",
    "Headphones":"https://www.amazon.com/Best-Sellers-Electronics-Headphones-Earbuds/zgbs/electronics/172541/ref=zg_bs_nav_electronics_1",
    "Home Audio & Theater":"https://www.amazon.com/Best-Sellers-Electronics-Home-Audio-Theater-Products/zgbs/electronics/667846011/ref=zg_bs_nav_electronics_1",
    "Marine Electronics":"https://www.amazon.com/Best-Sellers-Electronics-Marine-Electronics/zgbs/electronics/319574011/ref=zg_bs_nav_electronics_1",
    "Office Electronics":"https://www.amazon.com/Best-Sellers-Electronics-Office-Electronics-Products/zgbs/electronics/172574/ref=zg_bs_nav_electronics_1",
    "Portable Audio & Video":"https://www.amazon.com/Best-Sellers-Electronics-Portable-Audio-Video/zgbs/electronics/172623/ref=zg_bs_nav_electronics_1",
    "Security & Surveillance":"https://www.amazon.com/Best-Sellers-Electronics-Security-Surveillance-Equipment/zgbs/electronics/524136/ref=zg_bs_nav_electronics_1",
    "Service & Replacement Plans":"https://www.amazon.com/Best-Sellers-Electronics-Computers-Electronics-Service-Plans/zgbs/electronics/16285901/ref=zg_bs_nav_electronics_1",
    "Televisions & Video":"https://www.amazon.com/Best-Sellers-Electronics-Televisions-Video-Products/zgbs/electronics/1266092011/ref=zg_bs_nav_electronics_1",
    "Video Game Consoles & Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Video-Game-Consoles-Accessories/zgbs/electronics/7926841011/ref=zg_bs_nav_electronics_1",
    "Video Projectors":"https://www.amazon.com/Best-Sellers-Electronics-Video-Projectors/zgbs/electronics/300334/ref=zg_bs_nav_electronics_1",
    "Wearable Technology":"https://www.amazon.com/Best-Sellers-Electronics-Wearable-Technology/zgbs/electronics/10048700011/ref=zg_bs_nav_electronics_1",
    "eBook Readers & Accessories":"https://www.amazon.com/Best-Sellers-Electronics-eBook-Readers-Accessories/zgbs/electronics/2642125011/ref=zg_bs_nav_electronics_1",
    "Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Camera-Photo-Accessories/zgbs/electronics/172435/ref=zg_bs_nav_electronics_2_281407",
    "Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Cell-Phone-Accessories/zgbs/electronics/2407755011/ref=zg_bs_nav_electronics_2_281407",
    "Cable Organizer Bags & Cases":"https://www.amazon.com/Best-Sellers-Electronics-Cable-Organizer-Bags-Cases/zgbs/electronics/290458/ref=zg_bs_nav_electronics_2_281407",
    "Cables":"https://www.amazon.com/Best-Sellers-Electronics-Electronics-Cables/zgbs/electronics/12954861/ref=zg_bs_nav_electronics_2_281407",
    "Cord Management":"https://www.amazon.com/Best-Sellers-Electronics-Electrical-Cord-Management/zgbs/electronics/11042051/ref=zg_bs_nav_electronics_2_281407",
    "GPS System Accessories":"https://www.amazon.com/Best-Sellers-Electronics-GPS-System-Accessories/zgbs/electronics/559942/ref=zg_bs_nav_electronics_2_281407",
    "Installation Services":"https://www.amazon.com/Best-Sellers-Electronics-Consumer-Electronics-Installation-Services/zgbs/electronics/2632817011/ref=zg_bs_nav_electronics_2_281407",
    "Microphones & Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Recording-Microphones-Accessories/zgbs/electronics/11974521/ref=zg_bs_nav_electronics_2_281407",
    "Mounts":"https://www.amazon.com/Best-Sellers-Electronics-Electronics-Mounts/zgbs/electronics/10966911/ref=zg_bs_nav_electronics_2_281407",
    "Office Electronics Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Office-Electronics-Accessories/zgbs/electronics/172575/ref=zg_bs_nav_electronics_2_281407",
    "Power Protection":"https://www.amazon.com/Best-Sellers-Electronics-Electronics-Power-Protection-Products/zgbs/electronics/2223901011/ref=zg_bs_nav_electronics_2_281407",
    "Power Strips & Surge Protectors":"https://www.amazon.com/Best-Sellers-Electronics-Power-Strips-Surge-Protectors/zgbs/electronics/17854127011/ref=zg_bs_nav_electronics_2_281407",
    "Telephone Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Telephone-Accessories/zgbs/electronics/172607/ref=zg_bs_nav_electronics_2_281407",
    "Vehicle Electronics Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Car-Electronics-Accessories/zgbs/electronics/10981291/ref=zg_bs_nav_electronics_2_281407",
    "Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Camera-Photo-Accessories/zgbs/electronics/172435/ref=zg_bs_nav_electronics_2_502394",
    "Bags & Cases":"https://www.amazon.com/Best-Sellers-Electronics-Camera-Bags-Cases/zgbs/electronics/172437/ref=zg_bs_nav_electronics_2_502394",
    "Binoculars & Scopes":"https://www.amazon.com/Best-Sellers-Electronics-Binoculars-Telescopes-Optics/zgbs/electronics/499320/ref=zg_bs_nav_electronics_2_502394",
    "Digital Cameras":"https://www.amazon.com/Best-Sellers-Electronics-Digital-Cameras/zgbs/electronics/281052/ref=zg_bs_nav_electronics_2_502394",
    "Film Photography":"https://www.amazon.com/Best-Sellers-Electronics-Film-Photography/zgbs/electronics/7161070011/ref=zg_bs_nav_electronics_2_502394",
    "Flashes":"https://www.amazon.com/Best-Sellers-Electronics-Camera-Flashes/zgbs/electronics/172447/ref=zg_bs_nav_electronics_2_502394",
    "Lenses":"https://www.amazon.com/Best-Sellers-Electronics-Camcorder-Camera-Lenses/zgbs/electronics/499248/ref=zg_bs_nav_electronics_2_502394",
    "Lighting & Studio":"https://www.amazon.com/Best-Sellers-Electronics-Lighting-Studio-Equipment/zgbs/electronics/7161086011/ref=zg_bs_nav_electronics_2_502394",
    "Photo Printers":"https://www.amazon.com/Best-Sellers-Electronics-Photo-Printers/zgbs/electronics/17939179011/ref=zg_bs_nav_electronics_2_502394",
    "Printers & Scanners":"https://www.amazon.com/Best-Sellers-Electronics-Photo-Printers-Scanners/zgbs/electronics/499328/ref=zg_bs_nav_electronics_2_502394",
    "Simulated Cameras":"https://www.amazon.com/Best-Sellers-Electronics-Simulated-Surveillance-Cameras/zgbs/electronics/14241441/ref=zg_bs_nav_electronics_2_502394",
    "Slide & Negative Scanners":"https://www.amazon.com/Best-Sellers-Electronics-Slide-Negative-Scanners/zgbs/electronics/5728049011/ref=zg_bs_nav_electronics_2_502394",
    "Tripods & Monopods":"https://www.amazon.com/Best-Sellers-Electronics-Camera-Tripods-Monopods/zgbs/electronics/499306/ref=zg_bs_nav_electronics_2_502394",
    "Underwater Photography":"https://www.amazon.com/Best-Sellers-Electronics-Underwater-Photography-Products/zgbs/electronics/3350161/ref=zg_bs_nav_electronics_2_502394",
    "Video":"https://www.amazon.com/Best-Sellers-Electronics-Video-Equipment/zgbs/electronics/7161073011/ref=zg_bs_nav_electronics_2_502394",
    "Video Projectors":"https://www.amazon.com/Best-Sellers-Electronics-Video-Projectors/zgbs/electronics/300334/ref=zg_bs_nav_electronics_2_502394",
    "Video Surveillance":"https://www.amazon.com/Best-Sellers-Electronics-Video-Surveillance-Equipment/zgbs/electronics/7161091011/ref=zg_bs_nav_electronics_2_502394",
    "CB Radios & Scanners":"https://www.amazon.com/Best-Sellers-Electronics-Portable-CB-Radios/zgbs/electronics/226183/ref=zg_bs_nav_electronics_2_1077068",
    "Car Audio":"https://www.amazon.com/Best-Sellers-Electronics-Car-Audio/zgbs/electronics/226184/ref=zg_bs_nav_electronics_2_1077068",
    "Car Safety & Security":"https://www.amazon.com/Best-Sellers-Electronics-Car-Security-Products/zgbs/electronics/3008971/ref=zg_bs_nav_electronics_2_1077068",
    "Car Video":"https://www.amazon.com/Best-Sellers-Electronics-Car-Video/zgbs/electronics/10980521/ref=zg_bs_nav_electronics_2_1077068",
    "In-Dash Mounting Kits":"https://www.amazon.com/Best-Sellers-Electronics-Car-Audio-Video-Dash-Mounting-Kits/zgbs/electronics/10981321/ref=zg_bs_nav_electronics_2_1077068",
    "Installation Accessories & Harnesses":"https://www.amazon.com/Best-Sellers-Electronics-Car-Audio-Video-Installation-Products/zgbs/electronics/10981311/ref=zg_bs_nav_electronics_2_1077068",
    "Radar Detectors":"https://www.amazon.com/Best-Sellers-Electronics-Radar-Detectors/zgbs/electronics/172529/ref=zg_bs_nav_electronics_2_1077068",
    "Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Cell-Phone-Accessories/zgbs/electronics/2407755011/ref=zg_bs_nav_electronics_2_2811119011",
    "Cases, Holsters & Clips":"https://www.amazon.com/Best-Sellers-Electronics-Cell-Phone-Cases-Covers/zgbs/electronics/2407760011/ref=zg_bs_nav_electronics_2_2811119011",
    "Cell Phones":"https://www.amazon.com/Best-Sellers-Electronics-Cell-Phones/zgbs/electronics/7072561011/ref=zg_bs_nav_electronics_2_2811119011",
    "SIM Cards & Prepaid Minutes":"https://www.amazon.com/Best-Sellers-Electronics-SIM-Cards-Prepaid-Minutes/zgbs/electronics/3345523011/ref=zg_bs_nav_electronics_2_2811119011",
    "Computer Accessories & Peripherals":"https://www.amazon.com/Best-Sellers-Electronics-Computer-Accessories-Peripherals/zgbs/electronics/172456/ref=zg_bs_nav_electronics_2_541966",
    "Computer Components":"https://www.amazon.com/Best-Sellers-Electronics-Computer-Components/zgbs/electronics/193870011/ref=zg_bs_nav_electronics_2_541966",
    "Computers & Tablets":"https://www.amazon.com/Best-Sellers-Electronics-Computers-Tablets/zgbs/electronics/13896617011/ref=zg_bs_nav_electronics_2_541966",
    "Data Storage":"https://www.amazon.com/Best-Sellers-Electronics-Data-Storage/zgbs/electronics/1292110011/ref=zg_bs_nav_electronics_2_541966",
    "Laptop Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Laptop-Accessories/zgbs/electronics/3011391011/ref=zg_bs_nav_electronics_2_541966",
    "Monitors":"https://www.amazon.com/Best-Sellers-Electronics-Computer-Monitors/zgbs/electronics/1292115011/ref=zg_bs_nav_electronics_2_541966",
    "Networking Products":"https://www.amazon.com/Best-Sellers-Electronics-Computer-Networking/zgbs/electronics/172504/ref=zg_bs_nav_electronics_2_541966",
    "Servers":"https://www.amazon.com/Best-Sellers-Electronics-Computer-Servers/zgbs/electronics/11036071/ref=zg_bs_nav_electronics_2_541966",
    "Tablet Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Tablet-Accessories/zgbs/electronics/2348628011/ref=zg_bs_nav_electronics_2_541966",
    "Tablet Replacement Parts":"https://www.amazon.com/Best-Sellers-Electronics-Tablet-Replacement-Parts/zgbs/electronics/15524379011/ref=zg_bs_nav_electronics_2_541966",
    "Warranties & Services":"https://www.amazon.com/Best-Sellers-Electronics-Computer-Warranties-Services/zgbs/electronics/16285851/ref=zg_bs_nav_electronics_2_541966",
    "GPS System Accessories":"https://www.amazon.com/Best-Sellers-Electronics-GPS-System-Accessories/zgbs/electronics/559942/ref=zg_bs_nav_electronics_2_172526",
    "GPS Trackers":"https://www.amazon.com/Best-Sellers-Electronics-GPS-Trackers/zgbs/electronics/617650011/ref=zg_bs_nav_electronics_2_172526",
    "Item Finders":"https://www.amazon.com/Best-Sellers-Electronics-Item-Finders/zgbs/electronics/18022313011/ref=zg_bs_nav_electronics_2_172526",
    "Sports & Handheld GPS":"https://www.amazon.com/Best-Sellers-Electronics-GPS-Units/zgbs/electronics/219536011/ref=zg_bs_nav_electronics_2_172526",
    "Trucking GPS":"https://www.amazon.com/Best-Sellers-Electronics-Trucking-GPS-Units/zgbs/electronics/3248683011/ref=zg_bs_nav_electronics_2_172526",
    "Vehicle GPS":"https://www.amazon.com/Best-Sellers-Electronics-Vehicle-GPS-Units-Equipment/zgbs/electronics/559938/ref=zg_bs_nav_electronics_2_172526",
    "Earbud Headphones":"https://www.amazon.com/Best-Sellers-Electronics-Earbud-In-Ear-Headphones/zgbs/electronics/12097478011/ref=zg_bs_nav_electronics_2_172541",
    "On-Ear Headphones":"https://www.amazon.com/Best-Sellers-Electronics-On-Ear-Headphones/zgbs/electronics/12097480011/ref=zg_bs_nav_electronics_2_172541",
    "Open-Ear Headphones":"https://www.amazon.com/Best-Sellers-Electronics-Open-Ear-Headphones/zgbs/electronics/99530371011/ref=zg_bs_nav_electronics_2_172541",
    "Over-Ear Headphones":"https://www.amazon.com/Best-Sellers-Electronics-Over-Ear-Headphones/zgbs/electronics/12097479011/ref=zg_bs_nav_electronics_2_172541",
    "Compact Radios & Stereos":"https://www.amazon.com/Best-Sellers-Electronics-Compact-Radios-Stereos/zgbs/electronics/9977441011/ref=zg_bs_nav_electronics_2_667846011",
    "Home Audio Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Home-Audio-Accessories/zgbs/electronics/3236443011/ref=zg_bs_nav_electronics_2_667846011",
    "Home Theater":"https://www.amazon.com/Best-Sellers-Electronics-Home-Theater-Audio/zgbs/electronics/9977442011/ref=zg_bs_nav_electronics_2_667846011",
    "Speakers":"https://www.amazon.com/Best-Sellers-Electronics-Home-Audio-Speakers/zgbs/electronics/172563/ref=zg_bs_nav_electronics_2_667846011",
    "Stereo System Components":"https://www.amazon.com/Best-Sellers-Electronics-Home-Stereo-System-Components/zgbs/electronics/12097483011/ref=zg_bs_nav_electronics_2_667846011",
    "Turntables & Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Turntables-Accessories/zgbs/electronics/9977443011/ref=zg_bs_nav_electronics_2_667846011",
    "Wireless & Streaming Audio":"https://www.amazon.com/Best-Sellers-Electronics-Wireless-Streaming-Audio-Systems/zgbs/electronics/322215011/ref=zg_bs_nav_electronics_2_667846011",
    "Boomboxes":"https://www.amazon.com/Best-Sellers-Electronics-Boomboxes/zgbs/electronics/172633/ref=zg_bs_nav_electronics_2_172623",
    "CB & Two-Way Radios":"https://www.amazon.com/Best-Sellers-Electronics-CB-Two-Way-Radios/zgbs/electronics/172654/ref=zg_bs_nav_electronics_2_172623",
    "Cassette Players & Recorders":"https://www.amazon.com/Best-Sellers-Electronics-Portable-Cassette-Players-Recorders/zgbs/electronics/172628/ref=zg_bs_nav_electronics_2_172623",
    "Digital Voice Recorders":"https://www.amazon.com/Best-Sellers-Electronics-Digital-Voice-Recorders/zgbs/electronics/227758/ref=zg_bs_nav_electronics_2_172623",
    "MP3 & MP4 Player Accessories":"https://www.amazon.com/Best-Sellers-Electronics-MP3-MP4-Player-Accessories/zgbs/electronics/290438/ref=zg_bs_nav_electronics_2_172623",
    "MP3 & MP4 Players":"https://www.amazon.com/Best-Sellers-Electronics-MP3-MP4-Players/zgbs/electronics/1264866011/ref=zg_bs_nav_electronics_2_172623",
    "Microcassette Recorders":"https://www.amazon.com/Best-Sellers-Electronics-Portable-Microcassette-Recorders/zgbs/electronics/172632/ref=zg_bs_nav_electronics_2_172623",
    "Minidisc Players":"https://www.amazon.com/Best-Sellers-Electronics-Portable-Minidisc-Players/zgbs/electronics/172631/ref=zg_bs_nav_electronics_2_172623",
    "Portable CD Players":"https://www.amazon.com/Best-Sellers-Electronics-Portable-CD-Players/zgbs/electronics/465608/ref=zg_bs_nav_electronics_2_172623",
    "Portable DVD Players":"https://www.amazon.com/Best-Sellers-Electronics-Portable-DVD-Players/zgbs/electronics/172521/ref=zg_bs_nav_electronics_2_172623",
    "Portable Speakers & Docks":"https://www.amazon.com/Best-Sellers-Electronics-Portable-Cell-Phone-Speakers-Audio-Docks/zgbs/electronics/689637011/ref=zg_bs_nav_electronics_2_172623",
    "Radios":"https://www.amazon.com/Best-Sellers-Electronics-Portable-Radios/zgbs/electronics/172681/ref=zg_bs_nav_electronics_2_172623",
    "Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Security-Surveillance-Accessories/zgbs/electronics/11041121/ref=zg_bs_nav_electronics_2_524136",
    "Biometrics":"https://www.amazon.com/Best-Sellers-Electronics-Security-Surveillance-Biometrics/zgbs/electronics/14241141/ref=zg_bs_nav_electronics_2_524136",
    "Home Security Systems":"https://www.amazon.com/Best-Sellers-Electronics-Home-Security-Systems/zgbs/electronics/3180341/ref=zg_bs_nav_electronics_2_524136",
    "Horns & Sirens":"https://www.amazon.com/Best-Sellers-Electronics-Security-Horns-Sirens/zgbs/electronics/11041181/ref=zg_bs_nav_electronics_2_524136",
    "Motion Detectors":"https://www.amazon.com/Best-Sellers-Electronics-Motion-Detectors/zgbs/electronics/11040971/ref=zg_bs_nav_electronics_2_524136",
    "Radio Scanners":"https://www.amazon.com/Best-Sellers-Electronics-Radio-Scanners/zgbs/electronics/172530/ref=zg_bs_nav_electronics_2_524136",
    "Surveillance Video Equipment":"https://www.amazon.com/Best-Sellers-Electronics-Surveillance-Video-Equipment/zgbs/electronics/14248481/ref=zg_bs_nav_electronics_2_524136",
    "AV Receivers & Amplifiers":"https://www.amazon.com/Best-Sellers-Electronics-AudioVideo-Receivers-Amplifiers/zgbs/electronics/3213035011/ref=zg_bs_nav_electronics_2_1266092011",
    "Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Home-Theater-Accessories/zgbs/electronics/3230976011/ref=zg_bs_nav_electronics_2_1266092011",
    "Analog-to-Digital (DTV) Converters":"https://www.amazon.com/Best-Sellers-Electronics-Analog-to-Digital-DTV-Converters/zgbs/electronics/979935011/ref=zg_bs_nav_electronics_2_1266092011",
    "Blu-ray Players & Recorders":"https://www.amazon.com/Best-Sellers-Electronics-Blu-ray-Players-Recorders/zgbs/electronics/3213025011/ref=zg_bs_nav_electronics_2_1266092011",
    "DVD Players & Recorders":"https://www.amazon.com/Best-Sellers-Electronics-DVD-Players-Recorders/zgbs/electronics/3213027011/ref=zg_bs_nav_electronics_2_1266092011",
    "DVD-VCR Combos":"https://www.amazon.com/Best-Sellers-Electronics-DVD-VCR-Combos/zgbs/electronics/886258/ref=zg_bs_nav_electronics_2_1266092011",
    "HD DVD Players":"https://www.amazon.com/Best-Sellers-Electronics-HD-DVD-Players/zgbs/electronics/352696011/ref=zg_bs_nav_electronics_2_1266092011",
    "Home Theater Systems":"https://www.amazon.com/Best-Sellers-Electronics-Home-Theater-Systems/zgbs/electronics/281056/ref=zg_bs_nav_electronics_2_1266092011",
    "Satellite Television":"https://www.amazon.com/Best-Sellers-Electronics-Satellite-Television-Products/zgbs/electronics/400080/ref=zg_bs_nav_electronics_2_1266092011",
    "Streaming Media Players":"https://www.amazon.com/Best-Sellers-Electronics-Streaming-Media-Players/zgbs/electronics/13447451/ref=zg_bs_nav_electronics_2_1266092011",
    "TV-DVD Combos":"https://www.amazon.com/Best-Sellers-Electronics-TV-DVD-Combinations/zgbs/electronics/578960/ref=zg_bs_nav_electronics_2_1266092011",
    "Televisions":"https://www.amazon.com/Best-Sellers-Electronics-Televisions/zgbs/electronics/172659/ref=zg_bs_nav_electronics_2_1266092011",
    "VCRs":"https://www.amazon.com/Best-Sellers-Electronics-VCRs/zgbs/electronics/172669/ref=zg_bs_nav_electronics_2_1266092011",
    "Video Glasses":"https://www.amazon.com/Best-Sellers-Electronics-Video-Display-Glasses/zgbs/electronics/3213034011/ref=zg_bs_nav_electronics_2_1266092011",
    "Fire TV":"https://www.amazon.com/Best-Sellers-Electronics-Fire-TV-Devices-Accessories/zgbs/electronics/8946437011/ref=zg_bs_nav_electronics_2_7926841011",
    "Nintendo 3DS":"https://www.amazon.com/Best-Sellers-Electronics-Nintendo-3DS-Consoles-Accessories/zgbs/electronics/7926850011/ref=zg_bs_nav_electronics_2_7926841011",
    "Nintendo DS":"https://www.amazon.com/Best-Sellers-Electronics-Nintendo-DS-Consoles-Accessories/zgbs/electronics/7926849011/ref=zg_bs_nav_electronics_2_7926841011",
    "Nintendo Switch":"https://www.amazon.com/Best-Sellers-Electronics-Nintendo-Switch-Consoles-Accessories/zgbs/electronics/16227139011/ref=zg_bs_nav_electronics_2_7926841011",
    "PlayStation 3":"https://www.amazon.com/Best-Sellers-Electronics-PlayStation-3-Consoles-Accessories/zgbs/electronics/7926843011/ref=zg_bs_nav_electronics_2_7926841011",
    "PlayStation 4":"https://www.amazon.com/Best-Sellers-Electronics-PlayStation-4-Consoles-Accessories/zgbs/electronics/7926842011/ref=zg_bs_nav_electronics_2_7926841011",
    "PlayStation Vita":"https://www.amazon.com/Best-Sellers-Electronics-PlayStation-Vita-Consoles-Accessories/zgbs/electronics/7926852011/ref=zg_bs_nav_electronics_2_7926841011",
    "Sony PSP":"https://www.amazon.com/Best-Sellers-Electronics-Sony-PSP-Consoles-Accessories/zgbs/electronics/7926851011/ref=zg_bs_nav_electronics_2_7926841011",
    "Wii":"https://www.amazon.com/Best-Sellers-Electronics-Wii-Consoles-Accessories/zgbs/electronics/7926847011/ref=zg_bs_nav_electronics_2_7926841011",
    "Wii U":"https://www.amazon.com/Best-Sellers-Electronics-Wii-U-Consoles-Accessories/zgbs/electronics/7926848011/ref=zg_bs_nav_electronics_2_7926841011",
    "Xbox 360":"https://www.amazon.com/Best-Sellers-Electronics-Xbox-360-Consoles-Accessories/zgbs/electronics/7926846011/ref=zg_bs_nav_electronics_2_7926841011",
    "Xbox One":"https://www.amazon.com/Best-Sellers-Electronics-Xbox-One-Consoles-Accessories/zgbs/electronics/7926844011/ref=zg_bs_nav_electronics_2_7926841011",
    "Accessories & Supplies":"https://www.amazon.com/Best-Sellers-Electronics-Electronics-Accessories-Supplies/zgbs/electronics/281407/ref=zg_bs_nav_electronics_1_300334",
    "Camera & Photo":"https://www.amazon.com/Best-Sellers-Electronics-Camera-Photo-Products/zgbs/electronics/502394/ref=zg_bs_nav_electronics_1_300334",
    "Car Electronics":"https://www.amazon.com/Best-Sellers-Electronics-Car-Electronics/zgbs/electronics/1077068/ref=zg_bs_nav_electronics_1_300334",
    "Cell Phones & Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Cell-Phones-Accessories/zgbs/electronics/2811119011/ref=zg_bs_nav_electronics_1_300334",
    "Computers & Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Computers-Accessories/zgbs/electronics/541966/ref=zg_bs_nav_electronics_1_300334",
    "GPS & Navigation":"https://www.amazon.com/Best-Sellers-Electronics-GPS-Finders-Accessories/zgbs/electronics/172526/ref=zg_bs_nav_electronics_1_300334",
    "Headphones":"https://www.amazon.com/Best-Sellers-Electronics-Headphones-Earbuds/zgbs/electronics/172541/ref=zg_bs_nav_electronics_1_300334",
    "Home Audio & Theater":"https://www.amazon.com/Best-Sellers-Electronics-Home-Audio-Theater-Products/zgbs/electronics/667846011/ref=zg_bs_nav_electronics_1_300334",
    "Marine Electronics":"https://www.amazon.com/Best-Sellers-Electronics-Marine-Electronics/zgbs/electronics/319574011/ref=zg_bs_nav_electronics_1_300334",
    "Office Electronics":"https://www.amazon.com/Best-Sellers-Electronics-Office-Electronics-Products/zgbs/electronics/172574/ref=zg_bs_nav_electronics_1_300334",
    "Portable Audio & Video":"https://www.amazon.com/Best-Sellers-Electronics-Portable-Audio-Video/zgbs/electronics/172623/ref=zg_bs_nav_electronics_1_300334",
    "Security & Surveillance":"https://www.amazon.com/Best-Sellers-Electronics-Security-Surveillance-Equipment/zgbs/electronics/524136/ref=zg_bs_nav_electronics_1_300334",
    "Service & Replacement Plans":"https://www.amazon.com/Best-Sellers-Electronics-Computers-Electronics-Service-Plans/zgbs/electronics/16285901/ref=zg_bs_nav_electronics_1_300334",
    "Televisions & Video":"https://www.amazon.com/Best-Sellers-Electronics-Televisions-Video-Products/zgbs/electronics/1266092011/ref=zg_bs_nav_electronics_1_300334",
    "Video Game Consoles & Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Video-Game-Consoles-Accessories/zgbs/electronics/7926841011/ref=zg_bs_nav_electronics_1_300334",
    "Wearable Technology":"https://www.amazon.com/Best-Sellers-Electronics-Wearable-Technology/zgbs/electronics/10048700011/ref=zg_bs_nav_electronics_1_300334",
    "eBook Readers & Accessories":"https://www.amazon.com/Best-Sellers-Electronics-eBook-Readers-Accessories/zgbs/electronics/2642125011/ref=zg_bs_nav_electronics_1_300334",
    "Activity & Fitness Trackers":"https://www.amazon.com/Best-Sellers-Electronics-Activity-Fitness-Trackers/zgbs/electronics/5393958011/ref=zg_bs_nav_electronics_2_10048700011",
    "Arm & Wristband Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Smart-Arm-Wristband-Accessories/zgbs/electronics/10048712011/ref=zg_bs_nav_electronics_2_10048700011",
    "Glasses":"https://www.amazon.com/Best-Sellers-Electronics-Wearable-Tech-Glasses/zgbs/electronics/10048708011/ref=zg_bs_nav_electronics_2_10048700011",
    "Rings":"https://www.amazon.com/Best-Sellers-Electronics-Smart-Rings/zgbs/electronics/10048711011/ref=zg_bs_nav_electronics_2_10048700011",
    "Single Ear Bluetooth Headsets":"https://www.amazon.com/Best-Sellers-Electronics-Single-Ear-Bluetooth-Cell-Phone-Headsets/zgbs/electronics/18021376011/ref=zg_bs_nav_electronics_2_10048700011",
    "Smart Clip Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Smart-Clip-Accessories/zgbs/electronics/10048713011/ref=zg_bs_nav_electronics_2_10048700011",
    "Smartwatch Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Smartwatch-Accessories/zgbs/electronics/7939902011/ref=zg_bs_nav_electronics_2_10048700011",
    "Smartwatches":"https://www.amazon.com/Best-Sellers-Electronics-Smartwatches/zgbs/electronics/7939901011/ref=zg_bs_nav_electronics_2_10048700011",
    "Virtual Reality":"https://www.amazon.com/Best-Sellers-Electronics-Wearable-Tech-Virtual-Reality-Gear/zgbs/electronics/14775003011/ref=zg_bs_nav_electronics_2_10048700011",
    "Virtual Reality (VR) Headsets":"https://www.amazon.com/Best-Sellers-Electronics-Cell-Phone-Virtual-Reality-VR-Headsets/zgbs/electronics/14775002011/ref=zg_bs_nav_electronics_2_10048700011",
    "Wristbands":"https://www.amazon.com/Best-Sellers-Electronics-Wearable-Tech-Wristbands/zgbs/electronics/10048706011/ref=zg_bs_nav_electronics_2_10048700011",
    "Bundles":"https://www.amazon.com/Best-Sellers-Electronics-eBook-Reader-Accessory-Bundles/zgbs/electronics/2642130011/ref=zg_bs_nav_electronics_2_2642125011",
    "Covers":"https://www.amazon.com/Best-Sellers-Electronics-eBook-Reader-Covers/zgbs/electronics/2642131011/ref=zg_bs_nav_electronics_2_2642125011",
    "Power Adapters":"https://www.amazon.com/Best-Sellers-Electronics-eBook-Reader-Power-Adapters/zgbs/electronics/2642132011/ref=zg_bs_nav_electronics_2_2642125011",
    "Power Cables":"https://www.amazon.com/Best-Sellers-Electronics-eBook-Reader-Power-Cables/zgbs/electronics/2642133011/ref=zg_bs_nav_electronics_2_2642125011",
    "Reading Lights":"https://www.amazon.com/Best-Sellers-Electronics-eBook-Reading-Lights/zgbs/electronics/2642134011/ref=zg_bs_nav_electronics_2_2642125011",
    "Screen Protectors":"https://www.amazon.com/Best-Sellers-Electronics-eBook-Reader-Screen-Protectors/zgbs/electronics/2642135011/ref=zg_bs_nav_electronics_2_2642125011",
    "Skins":"https://www.amazon.com/Best-Sellers-Electronics-eBook-Reader-Skins/zgbs/electronics/2642136011/ref=zg_bs_nav_electronics_2_2642125011",
    "Sleeves":"https://www.amazon.com/Best-Sellers-Electronics-eBook-Reader-Sleeves/zgbs/electronics/2642137011/ref=zg_bs_nav_electronics_2_2642125011",
    "Stands":"https://www.amazon.com/Best-Sellers-Electronics-eBook-Reader-Stands/zgbs/electronics/2642138011/ref=zg_bs_nav_electronics_2_2642125011",
    "eBook Readers":"https://www.amazon.com/Best-Sellers-Electronics-eBook-Readers/zgbs/electronics/2642129011/ref=zg_bs_nav_electronics_2_2642125011"
}

def generate_tags(name, specs):
    base_tags = ["AmazonFinds", "CoolGadgets", "AmazonUS"]
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
        print(f"name: {name}")
        asin = product_url.split("/dp/")[1].split("/")[0] if "/dp/" in product_url else "MANUAL"        
        print(f"asin: {asin}")
        bullets = driver.find_elements(By.CSS_SELECTOR, "#feature-bullets ul li span")
        print(f"bullets: {bullets}")
        specs = " | ".join([b.text.strip() for b in bullets if len(b.text.strip()) > 10][:3])
        print(f"specs: {specs}")
        try:
            price = driver.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
            price = f"₹{price}"
        except:
            price = "Check Link"

        img_paths = []
        thumbs = driver.find_elements(By.CSS_SELECTOR, "#altImages img")
        print(f"thumbs: {thumbs}")
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
                    
                if any(x in src for x in ["play-button", "gif", "inline-twister", "video-placeholder", "play-icon-overlay","png"]):
                    print(f"⏭️ Skipping element {idx}: Detected video/interactive decoration string in URL")
                    continue
                                    
                # 2. Convert thumbnail asset signature into clean, full-resolution image path
                high_res = src
                if "._S" in src:
                    high_res = src.split("._S")[0] + ".jpg"
                elif "._" in src:
                    high_res = src.split("._")[0] + ".jpg"
                    
                try:
                    local_file = os.path.join(os.getcwd(), f"Manual_temp_{idx}.jpg")
                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')]
                    urllib.request.install_opener(opener)                    
                    urllib.request.urlretrieve(high_res, local_file)                    
                    if os.path.getsize(local_file) > 1000: # Ensure it's a real valid image
                        img_paths.append(local_file)
                        found += 1
                except Exception as e:
                    print(f"❌ Download failed: {e}")
        
        print(f"image count: {len(img_paths)}")

        return {
            "asin": asin,
            "name": name,
            "link": f"https://www.amazon.com/dp/{asin}?tag={os.getenv('Affiliate_Code')}",
            "price": price,
            "specs": specs,
            "images": img_paths
        }
    except Exception as e:
        print(f"❌ Manual Scrape Failed: {e}")
        return None