import time
import urllib.request
import os
import random
import json
import re
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, 'Config.env')
load_dotenv(ENV_PATH)

blacklist = ["Credit Card", "Gift Card", "Subscription", "recharge", "lpg", "amazon pay", "blink plus"]

CATEGORIES = {
    "Appliances/Cooktops":"https://www.amazon.com/Best-Sellers-Appliances-Cooktops/zgbs/appliances/3741261/ref=zg_bs_nav_appliances_1",
    "Appliances/Dishwashers":"https://www.amazon.com/Best-Sellers-Appliances-Dishwashers/zgbs/appliances/3741271/ref=zg_bs_nav_appliances_1",
    "Appliances/Freezers":"https://www.amazon.com/Best-Sellers-Appliances-Freezers/zgbs/appliances/3741331/ref=zg_bs_nav_appliances_1",
    "Appliances/Ice Makers":"https://www.amazon.com/Best-Sellers-Appliances-Ice-Makers/zgbs/appliances/2399939011/ref=zg_bs_nav_appliances_1",
    "Appliances/Range Hoods":"https://www.amazon.com/Best-Sellers-Appliances-Range-Hoods/zgbs/appliances/3741441/ref=zg_bs_nav_appliances_1",
    "Appliances/Ranges":"https://www.amazon.com/Best-Sellers-Appliances-Ranges/zgbs/appliances/3741411/ref=zg_bs_nav_appliances_1",
    "Appliances/Wall Ovens":"https://www.amazon.com/Best-Sellers-Appliances-Wall-Ovens/zgbs/appliances/3741481/ref=zg_bs_nav_appliances_1",
    "Appliances/Warming Drawers":"https://www.amazon.com/Best-Sellers-Appliances-Warming-Drawers/zgbs/appliances/2399955011/ref=zg_bs_nav_appliances_1",
    "Appliances/Washers & Dryers":"https://www.amazon.com/Best-Sellers-Appliances-Washers-Dryers/zgbs/appliances/2383576011/ref=zg_bs_nav_appliances_1",
    "Appliances/Wine Cellars":"https://www.amazon.com/Best-Sellers-Appliances-Wine-Cellars/zgbs/appliances/3741521/ref=zg_bs_nav_appliances_1",
    "Automotive/Tools & Equipment":"https://www.amazon.com/Best-Sellers-Automotive-Automotive-Tools-Equipment/zgbs/automotive/15706941/ref=zg_bs_nav_automotive_1",
    "Camera & Photo Products/Accessories":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-Camera-Photo-Accessories/zgbs/photo/172435/ref=zg_bs_nav_photo_1",
    "Camera & Photo Products/Bags & Cases":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-Camera-Bags-Cases/zgbs/photo/172437/ref=zg_bs_nav_photo_1",
    "Camera & Photo Products/Binoculars & Scopes":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-Binoculars-Telescopes-Optics/zgbs/photo/499320/ref=zg_bs_nav_photo_1",
    "Camera & Photo Products/Camcorders":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-Camcorders/zgbs/photo/172421/ref=zg_bs_nav_photo_1",
    "Camera & Photo Products/DSLR Cameras":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-DSLR-Cameras/zgbs/photo/3017941/ref=zg_bs_nav_photo_1",
    "Camera & Photo Products/Digital Picture Frames":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-Digital-Picture-Frames/zgbs/photo/525460/ref=zg_bs_nav_photo_1",
    "Camera & Photo Products/Lenses":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-Camcorder-Camera-Lenses/zgbs/photo/499248/ref=zg_bs_nav_photo_1",
    "Camera & Photo Products/Point & Shoot Digital Cameras":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-Digital-Point-Shoot-Cameras/zgbs/photo/330405011/ref=zg_bs_nav_photo_1",
    "Camera & Photo Products/Surveillance Cameras":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-Surveillance-Security-Cameras/zgbs/photo/898400/ref=zg_bs_nav_photo_1",
    "Cell Phones & Accessories/Accessories":"https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Accessories/zgbs/wireless/2407755011/ref=zg_bs_nav_wireless_1",
    "Cell Phones & Accessories/Cases, Holsters & Clips":"https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Cases-Covers/zgbs/wireless/2407760011/ref=zg_bs_nav_wireless_1",
    "Cell Phones & Accessories/Cell Phones":"https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phones/zgbs/wireless/7072561011/ref=zg_bs_nav_wireless_1",
    "Collectible Coins/Coin Sets":"https://www.amazon.com/Best-Sellers-Collectible-Coins-Collectible-Coin-Sets/zgbs/coins/9003136011/ref=zg_bs_nav_coins_1",
    "Collectible Coins/Individual Coins":"https://www.amazon.com/Best-Sellers-Collectible-Coins-Individual-Collectible-Coins/zgbs/coins/9003133011/ref=zg_bs_nav_coins_1",
    "Computers & Accessories/Computer Accessories & Peripherals":"https://www.amazon.com/Best-Sellers-Computers-Accessories-Computer-Accessories-Peripherals/zgbs/pc/172456/ref=zg_bs_nav_pc_1",
    "Computers & Accessories/Computer Components":"https://www.amazon.com/Best-Sellers-Computers-Accessories-Computer-Components/zgbs/pc/193870011/ref=zg_bs_nav_pc_1",
    "Computers & Accessories/Data Storage":"https://www.amazon.com/Best-Sellers-Computers-Accessories-Data-Storage/zgbs/pc/1292110011/ref=zg_bs_nav_pc_1",
    "Computers & Accessories/Desktops":"https://www.amazon.com/Best-Sellers-Computers-Accessories-Desktop-Computers/zgbs/pc/565098/ref=zg_bs_nav_pc_1",
    "Computers & Accessories/External Components":"https://www.amazon.com/Best-Sellers-Computers-Accessories-Computer-External-Components/zgbs/pc/3012292011/ref=zg_bs_nav_pc_1",
    "Computers & Accessories/Laptop Accessories":"https://www.amazon.com/Best-Sellers-Computers-Accessories-Laptop-Accessories/zgbs/pc/3011391011/ref=zg_bs_nav_pc_1",
    "Computers & Accessories/Laptops":"https://www.amazon.com/Best-Sellers-Computers-Accessories-Laptop-Computers/zgbs/pc/565108/ref=zg_bs_nav_pc_1",
    "Computers & Accessories/Monitors":"https://www.amazon.com/Best-Sellers-Computers-Accessories-Computer-Monitors/zgbs/pc/1292115011/ref=zg_bs_nav_pc_1",
    "Computers & Accessories/Networking Products":"https://www.amazon.com/Best-Sellers-Computers-Accessories-Computer-Networking/zgbs/pc/172504/ref=zg_bs_nav_pc_1",
    "Computers & Accessories/Printers":"https://www.amazon.com/Best-Sellers-Computers-Accessories-Computer-Printers/zgbs/pc/172635/ref=zg_bs_nav_pc_1",
    "Computers & Accessories/Routers":"https://www.amazon.com/Best-Sellers-Computers-Accessories-Computer-Routers/zgbs/pc/300189/ref=zg_bs_nav_pc_1",
    "Computers & Accessories/Scanners":"https://www.amazon.com/Best-Sellers-Computers-Accessories-Computer-Scanners/zgbs/pc/172584/ref=zg_bs_nav_pc_1",
    "Computers & Accessories/Servers":"https://www.amazon.com/Best-Sellers-Computers-Accessories-Computer-Servers/zgbs/pc/11036071/ref=zg_bs_nav_pc_1",
    "Computers & Accessories/Tablet Accessories":"https://www.amazon.com/Best-Sellers-Computers-Accessories-Tablet-Accessories/zgbs/pc/2348628011/ref=zg_bs_nav_pc_1",
    "Computers & Accessories/Tablets":"https://www.amazon.com/Best-Sellers-Computers-Accessories-Computer-Tablets/zgbs/pc/1232597011/ref=zg_bs_nav_pc_1",
    "Electronics/Accessories & Supplies":"https://www.amazon.com/Best-Sellers-Electronics-Electronics-Accessories-Supplies/zgbs/electronics/281407/ref=zg_bs_nav_electronics_1",
    "Electronics/Camera & Photo":"https://www.amazon.com/Best-Sellers-Electronics-Camera-Photo-Products/zgbs/electronics/502394/ref=zg_bs_nav_electronics_1",
    "Electronics/Car Electronics":"https://www.amazon.com/Best-Sellers-Electronics-Car-Electronics/zgbs/electronics/1077068/ref=zg_bs_nav_electronics_1",
    "Electronics/GPS & Navigation":"https://www.amazon.com/Best-Sellers-Electronics-GPS-Finders-Accessories/zgbs/electronics/172526/ref=zg_bs_nav_electronics_1",
    "Electronics/Headphones":"https://www.amazon.com/Best-Sellers-Electronics-Headphones-Earbuds/zgbs/electronics/172541/ref=zg_bs_nav_electronics_1",
    "Electronics/Home Audio & Theater":"https://www.amazon.com/Best-Sellers-Electronics-Home-Audio-Theater-Products/zgbs/electronics/667846011/ref=zg_bs_nav_electronics_1",
    "Electronics/Marine Electronics":"https://www.amazon.com/Best-Sellers-Electronics-Marine-Electronics/zgbs/electronics/319574011/ref=zg_bs_nav_electronics_1",
    "Electronics/Office Electronics":"https://www.amazon.com/Best-Sellers-Electronics-Office-Electronics-Products/zgbs/electronics/172574/ref=zg_bs_nav_electronics_1",
    "Electronics/Portable Audio & Video":"https://www.amazon.com/Best-Sellers-Electronics-Portable-Audio-Video/zgbs/electronics/172623/ref=zg_bs_nav_electronics_1",
    "Electronics/Security & Surveillance":"https://www.amazon.com/Best-Sellers-Electronics-Security-Surveillance-Equipment/zgbs/electronics/524136/ref=zg_bs_nav_electronics_1",
    "Electronics/Service & Replacement Plans":"https://www.amazon.com/Best-Sellers-Electronics-Computers-Electronics-Service-Plans/zgbs/electronics/16285901/ref=zg_bs_nav_electronics_1",
    "Electronics/Televisions & Video":"https://www.amazon.com/Best-Sellers-Electronics-Televisions-Video-Products/zgbs/electronics/1266092011/ref=zg_bs_nav_electronics_1",
    "Electronics/Video Game Consoles & Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Video-Game-Consoles-Accessories/zgbs/electronics/7926841011/ref=zg_bs_nav_electronics_1",
    "Electronics/Video Projectors":"https://www.amazon.com/Best-Sellers-Electronics-Video-Projectors/zgbs/electronics/300334/ref=zg_bs_nav_electronics_1",
    "Electronics/Wearable Technology":"https://www.amazon.com/Best-Sellers-Electronics-Wearable-Technology/zgbs/electronics/10048700011/ref=zg_bs_nav_electronics_1",
    "Handmade Products/Handmade Baby":"https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Baby/zgbs/handmade/121190737011/ref=zg_bs_nav_handmade_1",
    "Handmade Products/Handmade Beauty & Personal Care":"https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Beauty-Personal-Care/zgbs/handmade/121190632011/ref=zg_bs_nav_handmade_1",
    "Handmade Products/Handmade Clothing & Accessories":"https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Clothing-Accessories/zgbs/handmade/121190502011/ref=zg_bs_nav_handmade_1",
    "Handmade Products/Handmade Home Décor":"https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Home-Dcor/zgbs/handmade/121190508011/ref=zg_bs_nav_handmade_1",
    "Handmade Products/Handmade Jewelry":"https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Jewelry/zgbs/handmade/121179460011/ref=zg_bs_nav_handmade_1",
    "Handmade Products/Handmade Kitchen & Dining":"https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Kitchen-Dining/zgbs/handmade/121190509011/ref=zg_bs_nav_handmade_1",
    "Handmade Products/Handmade Pet Supplies":"https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Pet-Supplies/zgbs/handmade/121190752011/ref=zg_bs_nav_handmade_1",
    "Handmade Products/Handmade Stationery & Party Supplies":"https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Stationery-Party-Supplies/zgbs/handmade/121190727011/ref=zg_bs_nav_handmade_1",
    "Handmade Products/Handmade Toys & Games":"https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Toys-Games/zgbs/handmade/121190630011/ref=zg_bs_nav_handmade_1",
    "Home & Kitchen/Bath":"https://www.amazon.com/Best-Sellers-Home-Kitchen-Bath-Products/zgbs/home-garden/1063236/ref=zg_bs_nav_home-garden_1",
    "Home & Kitchen/Bedding":"https://www.amazon.com/Best-Sellers-Home-Kitchen-Bedding/zgbs/home-garden/1063252/ref=zg_bs_nav_home-garden_1",
    "Home & Kitchen/Cleaning Supplies":"https://www.amazon.com/Best-Sellers-Home-Kitchen-Household-Cleaning-Supplies/zgbs/home-garden/10802561/ref=zg_bs_nav_home-garden_1",
    "Home & Kitchen/Furniture":"https://www.amazon.com/Best-Sellers-Home-Kitchen-Furniture/zgbs/home-garden/1063306/ref=zg_bs_nav_home-garden_1",
    "Home & Kitchen/Heating, Cooling & Air Quality":"https://www.amazon.com/Best-Sellers-Home-Kitchen-Heating-Cooling-Air-Quality/zgbs/home-garden/3206324011/ref=zg_bs_nav_home-garden_1",
    "Home & Kitchen/Home Décor":"https://www.amazon.com/Best-Sellers-Home-Kitchen-Home-Dcor-Products/zgbs/home-garden/1063278/ref=zg_bs_nav_home-garden_1",
    "Home & Kitchen/Irons & Steamers":"https://www.amazon.com/Best-Sellers-Home-Kitchen-Ironing-Products/zgbs/home-garden/510240/ref=zg_bs_nav_home-garden_1",
    "Home & Kitchen/Kids' Home Store":"https://www.amazon.com/Best-Sellers-Home-Kitchen-Kids-Home-Store/zgbs/home-garden/3206325011/ref=zg_bs_nav_home-garden_1",
    "Home & Kitchen/Party Supplies":"https://www.amazon.com/Best-Sellers-Home-Kitchen-Event-Party-Supplies/zgbs/home-garden/901590/ref=zg_bs_nav_home-garden_1",
    "Home & Kitchen/Seasonal Décor":"https://www.amazon.com/Best-Sellers-Home-Kitchen-Seasonal-Dcor/zgbs/home-garden/13679381/ref=zg_bs_nav_home-garden_1",
    "Home & Kitchen/Storage & Organization":"https://www.amazon.com/Best-Sellers-Home-Kitchen-Home-Storage-Organization/zgbs/home-garden/3610841/ref=zg_bs_nav_home-garden_1",
    "Home & Kitchen/Vacuums & Floor Care":"https://www.amazon.com/Best-Sellers-Home-Kitchen-Vacuum-Cleaners-Floor-Care/zgbs/home-garden/510106/ref=zg_bs_nav_home-garden_1",
    "Home & Kitchen/Wall Décor":"https://www.amazon.com/Best-Sellers-Home-Kitchen-Wall-Art/zgbs/home-garden/3736081/ref=zg_bs_nav_home-garden_1",
    "Kitchen & Dining/Bakeware":"https://www.amazon.com/Best-Sellers-Kitchen-Dining-Bakeware/zgbs/kitchen/289668/ref=zg_bs_nav_kitchen_1",
    "Kitchen & Dining/Bar Tools & Drinkware":"https://www.amazon.com/Best-Sellers-Kitchen-Dining-Bar-Tools-Drinkware/zgbs/kitchen/289728/ref=zg_bs_nav_kitchen_1",
    "Kitchen & Dining/Coffee, Tea & Espresso Appliances":"https://www.amazon.com/Best-Sellers-Kitchen-Dining-Coffee-Tea-Espresso-Appliances/zgbs/kitchen/289742/ref=zg_bs_nav_kitchen_1",
    "Kitchen & Dining/Cookware":"https://www.amazon.com/Best-Sellers-Kitchen-Dining-Kitchen-Cookware/zgbs/kitchen/289814/ref=zg_bs_nav_kitchen_1",
    "Kitchen & Dining/Dining & Entertaining":"https://www.amazon.com/Best-Sellers-Kitchen-Dining-Dining-Entertaining/zgbs/kitchen/13162311/ref=zg_bs_nav_kitchen_1",
    "Kitchen & Dining/Glassware & Drinkware":"https://www.amazon.com/Best-Sellers-Kitchen-Dining-Glassware-Drinkware/zgbs/kitchen/13217501/ref=zg_bs_nav_kitchen_1",
    "Kitchen & Dining/Home Brewing & Wine Making":"https://www.amazon.com/Best-Sellers-Kitchen-Dining-Home-Brewing-Wine-Making/zgbs/kitchen/979832011/ref=zg_bs_nav_kitchen_1",
    "Kitchen & Dining/Kitchen & Table Linens":"https://www.amazon.com/Best-Sellers-Kitchen-Dining-Kitchen-Table-Linens/zgbs/kitchen/1063916/ref=zg_bs_nav_kitchen_1",
    "Kitchen & Dining/Kitchen Utensils & Gadgets":"https://www.amazon.com/Best-Sellers-Kitchen-Dining-Kitchen-Utensils-Gadgets/zgbs/kitchen/289754/ref=zg_bs_nav_kitchen_1",
    "Kitchen & Dining/Small Appliances":"https://www.amazon.com/Best-Sellers-Kitchen-Dining-Kitchen-Small-Appliances/zgbs/kitchen/289913/ref=zg_bs_nav_kitchen_1",
    "Kitchen & Dining/Storage & Organization":"https://www.amazon.com/Best-Sellers-Kitchen-Dining-Kitchen-Storage-Organization/zgbs/kitchen/510136/ref=zg_bs_nav_kitchen_1",
    "Kitchen & Dining/Wine Accessories":"https://www.amazon.com/Best-Sellers-Kitchen-Dining-Wine-Accessories/zgbs/kitchen/13299291/ref=zg_bs_nav_kitchen_1",
    "Musical Instruments/Amplifiers & Effects":"https://www.amazon.com/Best-Sellers-Musical-Instruments-Musical-Instrument-Amplifiers-Effects/zgbs/musical-instruments/8882494011/ref=zg_bs_nav_musical-instruments_1",
    "Musical Instruments/Band & Orchestra":"https://www.amazon.com/Best-Sellers-Musical-Instruments-Band-Orchestra-Musical-Instruments/zgbs/musical-instruments/405758011/ref=zg_bs_nav_musical-instruments_1",
    "Musical Instruments/Bass Guitars":"https://www.amazon.com/Best-Sellers-Musical-Instruments-Bass-Guitars/zgbs/musical-instruments/11971311/ref=zg_bs_nav_musical-instruments_1",
    "Musical Instruments/DJ, Electronic Music & Karaoke":"https://www.amazon.com/Best-Sellers-Musical-Instruments-Electronic-Music-DJ-Karaoke/zgbs/musical-instruments/11973881/ref=zg_bs_nav_musical-instruments_1",
    "Musical Instruments/Drums & Percussion":"https://www.amazon.com/Best-Sellers-Musical-Instruments-Drums-Percussion/zgbs/musical-instruments/11970241/ref=zg_bs_nav_musical-instruments_1",
    "Musical Instruments/Guitars":"https://www.amazon.com/Best-Sellers-Musical-Instruments-Guitars/zgbs/musical-instruments/11971241/ref=zg_bs_nav_musical-instruments_1",
    "Musical Instruments/Instrument Accessories":"https://www.amazon.com/Best-Sellers-Musical-Instruments-Musical-Instrument-Accessories/zgbs/musical-instruments/11965871/ref=zg_bs_nav_musical-instruments_1",
    "Musical Instruments/Keyboards":"https://www.amazon.com/Best-Sellers-Musical-Instruments-Musical-Instrument-Keyboards-MIDI/zgbs/musical-instruments/11969981/ref=zg_bs_nav_musical-instruments_1",
    "Musical Instruments/Live Sound & Stage":"https://www.amazon.com/Best-Sellers-Musical-Instruments-Stage-Sound-Equipment/zgbs/musical-instruments/405757011/ref=zg_bs_nav_musical-instruments_1",
    "Musical Instruments/Recording Equipment":"https://www.amazon.com/Best-Sellers-Musical-Instruments-Music-Recording-Equipment/zgbs/musical-instruments/11973111/ref=zg_bs_nav_musical-instruments_1",
    "Musical Instruments/Ukuleles, Mandolins & Banjos":"https://www.amazon.com/Best-Sellers-Musical-Instruments-Ukuleles-Mandolins-Banjos/zgbs/musical-instruments/14733114011/ref=zg_bs_nav_musical-instruments_1",
    "Sports & Outdoors/Accessories":"https://www.amazon.com/Best-Sellers-Sports-Outdoors-Sports-Outdoor-Recreation-Accessories/zgbs/sporting-goods/3394801/ref=zg_bs_nav_sporting-goods_1",
    "Sports & Outdoors/Exercise & Fitness":"https://www.amazon.com/Best-Sellers-Sports-Outdoors-Exercise-Fitness-Equipment/zgbs/sporting-goods/3407731/ref=zg_bs_nav_sporting-goods_1",
    "Sports & Outdoors/Fan Shop":"https://www.amazon.com/Best-Sellers-Sports-Outdoors-Sports-Fan-Shop/zgbs/sporting-goods/3386071/ref=zg_bs_nav_sporting-goods_1",
    "Sports & Outdoors/Hunting & Fishing":"https://www.amazon.com/Best-Sellers-Sports-Outdoors-Hunting-Fishing-Products/zgbs/sporting-goods/706813011/ref=zg_bs_nav_sporting-goods_1",
    "Sports & Outdoors/Memorabilia Display & Storage":"https://www.amazon.com/Best-Sellers-Sports-Outdoors-Memorabilia-Display-Storage/zgbs/sporting-goods/2358921011/ref=zg_bs_nav_sporting-goods_1",
    "Sports & Outdoors/Outdoor Recreation":"https://www.amazon.com/Best-Sellers-Sports-Outdoors-Outdoor-Recreation/zgbs/sporting-goods/706814011/ref=zg_bs_nav_sporting-goods_1",
    "Sports & Outdoors/Sports":"https://www.amazon.com/Best-Sellers-Sports-Outdoors-Sports-Apparel-Equipment/zgbs/sporting-goods/10971181011/ref=zg_bs_nav_sporting-goods_1",
    "Sports & Outdoors/Sports Medicine":"https://www.amazon.com/Best-Sellers-Sports-Outdoors-Sports-Medicine-Products/zgbs/sporting-goods/3422351/ref=zg_bs_nav_sporting-goods_1",
    "Toys & Games/Action & Toy Figures":"https://www.amazon.com/Best-Sellers-Toys-Games-Toy-Figures-Playsets/zgbs/toys-and-games/165993011/ref=zg_bs_nav_toys-and-games_1",
    "Toys & Games/Arts & Crafts":"https://www.amazon.com/Best-Sellers-Toys-Games-Arts-Crafts-Supplies/zgbs/toys-and-games/166057011/ref=zg_bs_nav_toys-and-games_1",
    "Toys & Games/Baby & Toddler Toys":"https://www.amazon.com/Best-Sellers-Toys-Games-Baby-Toddler-Toys/zgbs/toys-and-games/196601011/ref=zg_bs_nav_toys-and-games_1",
    "Toys & Games/Bikes, Skates & Ride-Ons":"https://www.amazon.com/Best-Sellers-Toys-Games-Tricycles-Scooters-Wagons/zgbs/toys-and-games/256994011/ref=zg_bs_nav_toys-and-games_1",
    "Toys & Games/Building & Construction Toys":"https://www.amazon.com/Best-Sellers-Toys-Games-Building-Toys/zgbs/toys-and-games/166092011/ref=zg_bs_nav_toys-and-games_1",
    "Toys & Games/Collectible Card Games":"https://www.amazon.com/Best-Sellers-Toys-Games-Collectible-Card-Games/zgbs/toys-and-games/166242011/ref=zg_bs_nav_toys-and-games_1",
    "Toys & Games/Dolls & Accessories":"https://www.amazon.com/Best-Sellers-Toys-Games-Dolls-Accessories/zgbs/toys-and-games/166118011/ref=zg_bs_nav_toys-and-games_1",
    "Toys & Games/Dressing Up & Costumes":"https://www.amazon.com/Best-Sellers-Toys-Games-Kids-Dress-Up-Pretend-Play/zgbs/toys-and-games/166316011/ref=zg_bs_nav_toys-and-games_1",
    "Toys & Games/Electronics for Kids":"https://www.amazon.com/Best-Sellers-Toys-Games-Kids-Electronics/zgbs/toys-and-games/166164011/ref=zg_bs_nav_toys-and-games_1",
    "Toys & Games/Games":"https://www.amazon.com/Best-Sellers-Toys-Games-Games-Accessories/zgbs/toys-and-games/166220011/ref=zg_bs_nav_toys-and-games_1",
    "Toys & Games/Learning & Education":"https://www.amazon.com/Best-Sellers-Toys-Games-Learning-Education-Toys/zgbs/toys-and-games/166269011/ref=zg_bs_nav_toys-and-games_1",
    "Toys & Games/Novelty & Gag Toys":"https://www.amazon.com/Best-Sellers-Toys-Games-Novelty-Toys-Amusements/zgbs/toys-and-games/166027011/ref=zg_bs_nav_toys-and-games_1",
    "Toys & Games/Party Supplies":"https://www.amazon.com/Best-Sellers-Toys-Games-Kids-Party-Supplies/zgbs/toys-and-games/1266203011/ref=zg_bs_nav_toys-and-games_1",
    "Toys & Games/Play Vehicles":"https://www.amazon.com/Best-Sellers-Toys-Games-Toy-Vehicles/zgbs/toys-and-games/23539911011/ref=zg_bs_nav_toys-and-games_1",
    "Toys & Games/Puppets & Puppet Theaters":"https://www.amazon.com/Best-Sellers-Toys-Games-Puppets-Puppet-Theaters/zgbs/toys-and-games/166333011/ref=zg_bs_nav_toys-and-games_1",
    "Toys & Games/Puzzles":"https://www.amazon.com/Best-Sellers-Toys-Games-Puzzles/zgbs/toys-and-games/166359011/ref=zg_bs_nav_toys-and-games_1",
    "Toys & Games/Remote- & App-Controlled Toys":"https://www.amazon.com/Best-Sellers-Toys-Games-Hobby-Remote-App-Controlled-Vehicles-Parts/zgbs/toys-and-games/6925830011/ref=zg_bs_nav_toys-and-games_1",
    "Toys & Games/Sports & Outdoor Play":"https://www.amazon.com/Best-Sellers-Toys-Games-Sports-Outdoor-Play-Toys/zgbs/toys-and-games/166420011/ref=zg_bs_nav_toys-and-games_1",
    "Toys & Games/Stuffed Animals & Toys":"https://www.amazon.com/Best-Sellers-Toys-Games-Stuffed-Animals-Plush-Toys/zgbs/toys-and-games/166461011/ref=zg_bs_nav_toys-and-games_1",
    "Unique Finds/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_boost_0_2",
}

def generate_tags(name, specs):
    base_tags = ["AmazonFinds", "CoolGadgets", "AmazonUS"]
    keywords = [w for w in name.split() if len(w) > 4][:6]
    return ", ".join(list(set(base_tags + keywords)))

def get_bestsellers(driver, count):

    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    import datetime

    # --- 🔄 DYNAMIC 7-DAY COOLDOWN SELECTION MATRIX ---
    history_file = os.path.join(SCRIPT_DIR, "category_history.json")
    category_history = {}
    
    # Load past category picks
    if os.path.exists(history_file):
        try:
            with open(history_file, "r") as f:
                category_history = json.load(f)
        except Exception as e:
            print(f"⚠️ Could not read category history: {e}")

    now = datetime.datetime.now()
    available_categories = {}

    # Filter out categories picked less than 7 days ago
    for name, url in CATEGORIES.items():
        if name in category_history:
            last_picked_time = datetime.datetime.fromisoformat(category_history[name])
            days_passed = (now - last_picked_time).days
            if days_passed < 4:
                continue  # Skip this category, it's cooling down
        available_categories[name] = url

    # Fallback safety: If all categories are on cooldown, reset and use all of them
    if not available_categories:
        print("🔄 All categories are currently resting on cooldown! Flushing history matrix...")
        available_categories = CATEGORIES
        category_history = {}

    # Pick a random category out of the remaining eligible ones
    cat_name, cat_url = random.choice(list(available_categories.items()))
    print(f"🎲 Strategy Pick: {cat_name} (Passed 7-day cooldown clearance)")

    # Record the timestamp for the selected category
    category_history[cat_name] = now.isoformat()
    try:
        with open(history_file, "w") as f:
            json.dump(category_history, f, indent=4)
    except Exception as e:
        print(f"⚠️ Failed to write category tracking file: {e}")
    # ───────────────────────────────────────────────────
    
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
            high_res_urls = []
            thumbs = []

            try:
                # Find all distinct structural image items that have dynamic image configurations
                image_elements = driver.find_elements(By.XPATH, "//*[@data-a-dynamic-image]")
                seen_base_images = set()

                for el in image_elements:
                    dyn_img_attr = el.get_attribute("data-a-dynamic-image")
                    if not dyn_img_attr or len(high_res_urls) >= 5:
                        continue
                        
                    try:
                        # Convert resolution map to python dictionary
                        dyn_data = json.loads(dyn_img_attr)
                        if dyn_data:
                            # Pull out the target URL with the maximum resolution width (index 0 of the dimensions list)
                            best_url = max(dyn_data.items(), key=lambda item: item[1][0])[0]
                            
                            # Clean up base identifier (e.g., matching the unique asset token ID) to prevent duplicates
                            base_identifier = best_url.split("/images/I/")[1].split(".")[0] if "/images/I/" in best_url else best_url
                            
                            if base_identifier not in seen_base_images:
                                seen_base_images.add(base_identifier)
                                high_res_urls.append(best_url)
                    except Exception:
                        continue
                        
                print(f"📸 Strategy 1: Extracted {len(high_res_urls)} distinct product image targets.")
            except Exception as e:
                print(f"⚠️ Strategy 1 failed or bypassed: {e}")

            # --- STRATEGY 2: Inline Script JSON Parser Fallback ---
            if not high_res_urls:
                try:
                    page_source = driver.page_source
                    image_data_match = re.search(r'\'colorImages\':\s*\{\s*\'initial\':\s*(\[.+?\])', page_source)
                    if image_data_match:
                        image_json = json.loads(image_data_match.group(1))
                        high_res_urls = [img.get('hiRes') or img.get('large') for img in image_json if img]
                        high_res_urls = [url for url in high_res_urls if url]
                        print(f"📸 Strategy 2: Extracted {len(high_res_urls)} assets via inline layout script.")
                except Exception as e:
                    print(f"⚠️ Strategy 2 failed: {e}")

            # --- STRATEGY 3: Alt Thumbnails Raw Scraping (Final Fallback) ---
            if not high_res_urls:
                try:
                    thumbs = driver.find_elements(By.CSS_SELECTOR, "#altImages img, #altimages img, .imgTagWrapper img")
                    for img in thumbs:
                        src = img.get_attribute("data-old-hires") or img.get_attribute("src")
                        if src and not src.startswith("data:"):
                            # Normalize low-res thumbnail links to full resolution
                            clean_url = re.sub(r'\._[A-Z0-9_-]+\.', '.', src)
                            if clean_url not in high_res_urls:
                                high_res_urls.append(clean_url)
                    print(f"📸 Strategy 3: Collected {len(high_res_urls)} raw asset paths from visible tags.")
                except Exception as e:
                    print(f"⚠️ Strategy 3 failed: {e}")

            # --- DOWNLOAD PROCESSOR ---
            found = 0
            for idx, high_res in enumerate(high_res_urls):
                if found >= 5: break
                
                # Filter out obvious utility/video files
                if any(x in high_res.lower() for x in ["video", "play-button", "gif", "icon"]):
                    continue
                    
                try:
                    # ✅ FIXED: Changed hardcoded index high_res_urls[0] to unique loop item 'high_res'
                    local_file = os.path.join(os.getcwd(), f"temp_{i}_{idx}.jpg")
                    
                    # Spoof headers clearly to match your Selenium session profile
                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')]
                    urllib.request.install_opener(opener)
                    
                    urllib.request.urlretrieve(high_res, local_file)
                    if os.path.getsize(local_file) > 1000:
                        img_paths.append(local_file)
                        found += 1
                except Exception as e:
                    print(f"❌ Download failed for {high_res}: {e}")
                    
            bullets = driver.find_elements(By.CSS_SELECTOR, "#feature-bullets ul li span, #pqv-feature-bullets ul li span")
            specs = " | ".join([b.text.strip() for b in bullets if len(b.text.strip()) > 10][:7])
            
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