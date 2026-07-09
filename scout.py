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
    "Amazon Devices & Accessories/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_amazon-devices_0_1",
    "Amazon Devices & Accessories/Amazon Device Accessories":"https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Amazon-Device-Accessories/zgbs/amazon-devices/370783011/ref=zg_bs_nav_amazon-devices_1",
    "Amazon Devices & Accessories/Amazon Device Subscriptions":"https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Amazon-Device-Subscriptions/zgbs/amazon-devices/121475272011/ref=zg_bs_nav_amazon-devices_1",
    "Amazon Devices & Accessories/Amazon Devices":"https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Amazon-Devices/zgbs/amazon-devices/2102313011/ref=zg_bs_nav_amazon-devices_1",
    "Amazon Devices & Accessories/1":"https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories/zgbs/amazon-devices/ref=zg_bs_pg_1_amazon-devices?_encoding=UTF8&pg=1",
    "Amazon Devices & Accessories/2":"https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories/zgbs/amazon-devices/ref=zg_bs_pg_2_amazon-devices?_encoding=UTF8&pg=2",
    "Amazon Devices & Accessories/Next page":"https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories/zgbs/amazon-devices/ref=zg_bs_pg_2_amazon-devices?_encoding=UTF8&pg=2",
    "Amazon Renewed/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_amazon-renewed_0_1",
    "Amazon Renewed/Renewed Automotive":"https://www.amazon.com/Best-Sellers-Amazon-Renewed-Renewed-Automotive/zgbs/amazon-renewed/24430048011/ref=zg_bs_nav_amazon-renewed_1",
    "Amazon Renewed/Renewed Camera & Photo":"https://www.amazon.com/Best-Sellers-Amazon-Renewed-Renewed-Camera-Photo/zgbs/amazon-renewed/17871145011/ref=zg_bs_nav_amazon-renewed_1",
    "Amazon Renewed/Renewed Computers & Accessories":"https://www.amazon.com/Best-Sellers-Amazon-Renewed-Renewed-Computers-Accessories/zgbs/amazon-renewed/17871138011/ref=zg_bs_nav_amazon-renewed_1",
    "Amazon Renewed/Renewed Headphones":"https://www.amazon.com/Best-Sellers-Amazon-Renewed-Renewed-Headphones/zgbs/amazon-renewed/17871147011/ref=zg_bs_nav_amazon-renewed_1",
    "Amazon Renewed/Renewed Home & Kitchen":"https://www.amazon.com/Best-Sellers-Amazon-Renewed-Renewed-Home-Kitchen/zgbs/amazon-renewed/17871150011/ref=zg_bs_nav_amazon-renewed_1",
    "Amazon Renewed/Renewed Home Entertainment":"https://www.amazon.com/Best-Sellers-Amazon-Renewed-Renewed-Home-Entertainment/zgbs/amazon-renewed/17871148011/ref=zg_bs_nav_amazon-renewed_1",
    "Amazon Renewed/Renewed Laptops":"https://www.amazon.com/Best-Sellers-Amazon-Renewed-Renewed-Laptops/zgbs/amazon-renewed/21614632011/ref=zg_bs_nav_amazon-renewed_1",
    "Amazon Renewed/Renewed Musical Instruments":"https://www.amazon.com/Best-Sellers-Amazon-Renewed-Renewed-Musical-Instruments/zgbs/amazon-renewed/17871157011/ref=zg_bs_nav_amazon-renewed_1",
    "Amazon Renewed/Renewed Office Products":"https://www.amazon.com/Best-Sellers-Amazon-Renewed-Renewed-Office-Products/zgbs/amazon-renewed/17871156011/ref=zg_bs_nav_amazon-renewed_1",
    "Amazon Renewed/Renewed Patio, Lawn & Garden":"https://www.amazon.com/Best-Sellers-Amazon-Renewed-Renewed-Patio-Lawn-Garden/zgbs/amazon-renewed/17871155011/ref=zg_bs_nav_amazon-renewed_1",
    "Amazon Renewed/Renewed Portable Bluetooth Speakers":"https://www.amazon.com/Best-Sellers-Amazon-Renewed-Renewed-Portable-Bluetooth-Speakers/zgbs/amazon-renewed/17871154011/ref=zg_bs_nav_amazon-renewed_1",
    "Amazon Renewed/Renewed Smartphones":"https://www.amazon.com/Best-Sellers-Amazon-Renewed-Renewed-Smartphones/zgbs/amazon-renewed/17871142011/ref=zg_bs_nav_amazon-renewed_1",
    "Amazon Renewed/Renewed Smartwatches":"https://www.amazon.com/Best-Sellers-Amazon-Renewed-Renewed-Smartwatches/zgbs/amazon-renewed/18730483011/ref=zg_bs_nav_amazon-renewed_1",
    "Amazon Renewed/Renewed Sports & Outdoors":"https://www.amazon.com/Best-Sellers-Amazon-Renewed-Renewed-Sports-Outdoors/zgbs/amazon-renewed/17939807011/ref=zg_bs_nav_amazon-renewed_1",
    "Amazon Renewed/Renewed Tablets":"https://www.amazon.com/Best-Sellers-Amazon-Renewed-Renewed-Tablets/zgbs/amazon-renewed/17871139011/ref=zg_bs_nav_amazon-renewed_1",
    "Amazon Renewed/Renewed Tools & Home Improvement":"https://www.amazon.com/Best-Sellers-Amazon-Renewed-Renewed-Tools-Home-Improvement/zgbs/amazon-renewed/17871151011/ref=zg_bs_nav_amazon-renewed_1",
    "Amazon Renewed/Renewed Video Game Consoles & Accessories":"https://www.amazon.com/Best-Sellers-Amazon-Renewed-Renewed-Video-Game-Consoles-Accessories/zgbs/amazon-renewed/17871146011/ref=zg_bs_nav_amazon-renewed_1",
    "Amazon Renewed/1":"https://www.amazon.com/Best-Sellers-Amazon-Renewed/zgbs/amazon-renewed/ref=zg_bs_pg_1_amazon-renewed?_encoding=UTF8&pg=1",
    "Amazon Renewed/2":"https://www.amazon.com/Best-Sellers-Amazon-Renewed/zgbs/amazon-renewed/ref=zg_bs_pg_2_amazon-renewed?_encoding=UTF8&pg=2",
    "Amazon Renewed/Next page":"https://www.amazon.com/Best-Sellers-Amazon-Renewed/zgbs/amazon-renewed/ref=zg_bs_pg_2_amazon-renewed?_encoding=UTF8&pg=2",
    "Appliances/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_appliances_0_1",
    "Appliances/Appliance Warranties":"https://www.amazon.com/Best-Sellers-Appliances-Home-Appliance-Warranties/zgbs/appliances/2242350011/ref=zg_bs_nav_appliances_1",
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
    "Appliances/1":"https://www.amazon.com/Best-Sellers-Appliances/zgbs/appliances/ref=zg_bs_pg_1_appliances?_encoding=UTF8&pg=1",
    "Appliances/2":"https://www.amazon.com/Best-Sellers-Appliances/zgbs/appliances/ref=zg_bs_pg_2_appliances?_encoding=UTF8&pg=2",
    "Appliances/Next page":"https://www.amazon.com/Best-Sellers-Appliances/zgbs/appliances/ref=zg_bs_pg_2_appliances?_encoding=UTF8&pg=2",
    "Apps & Games/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_mobile-apps_0_1",
    "Apps & Games/Books & Comics":"https://www.amazon.com/Best-Sellers-Apps-Games-Books-Comics/zgbs/mobile-apps/9408444011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Business":"https://www.amazon.com/Best-Sellers-Apps-Games-Business/zgbs/mobile-apps/10298305011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Communication":"https://www.amazon.com/Best-Sellers-Apps-Games-Communication/zgbs/mobile-apps/9408466011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Customization":"https://www.amazon.com/Best-Sellers-Apps-Games-Customization/zgbs/mobile-apps/9408481011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Education":"https://www.amazon.com/Best-Sellers-Apps-Games-Education/zgbs/mobile-apps/9408490011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Finance":"https://www.amazon.com/Best-Sellers-Apps-Games-Finance/zgbs/mobile-apps/9408433011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Food & Drink":"https://www.amazon.com/Best-Sellers-Apps-Games-Food-Drink/zgbs/mobile-apps/9408523011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Games":"https://www.amazon.com/Best-Sellers-Apps-Games-Games/zgbs/mobile-apps/9209902011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Health & Fitness":"https://www.amazon.com/Best-Sellers-Apps-Games-Health-Wellness/zgbs/mobile-apps/9408749011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Kids":"https://www.amazon.com/Best-Sellers-Apps-Games-Kids/zgbs/mobile-apps/9408582011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Lifestyle":"https://www.amazon.com/Best-Sellers-Apps-Games-Lifestyle/zgbs/mobile-apps/9408710011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Local":"https://www.amazon.com/Best-Sellers-Apps-Games-Local/zgbs/mobile-apps/10298309011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Magazines":"https://www.amazon.com/Best-Sellers-Apps-Games-Magazines/zgbs/mobile-apps/9408805011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Medical":"https://www.amazon.com/Best-Sellers-Apps-Games-Medical/zgbs/mobile-apps/10298306011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Music & Audio":"https://www.amazon.com/Best-Sellers-Apps-Games-Music-Audio/zgbs/mobile-apps/9408771011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/News":"https://www.amazon.com/Best-Sellers-Apps-Games-News/zgbs/mobile-apps/9408802011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Novelty":"https://www.amazon.com/Best-Sellers-Apps-Games-Novelty/zgbs/mobile-apps/9408852011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Photo & Video":"https://www.amazon.com/Best-Sellers-Apps-Games-Photo-Video/zgbs/mobile-apps/9408874011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Productivity":"https://www.amazon.com/Best-Sellers-Apps-Games-Productivity/zgbs/mobile-apps/9408449011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Reference":"https://www.amazon.com/Best-Sellers-Apps-Games-Reference/zgbs/mobile-apps/9408491011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Social":"https://www.amazon.com/Best-Sellers-Apps-Games-Social/zgbs/mobile-apps/9408464011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Sports":"https://www.amazon.com/Best-Sellers-Apps-Games-Sports-Fitness/zgbs/mobile-apps/9408876011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Transportation":"https://www.amazon.com/Best-Sellers-Apps-Games-Transportation/zgbs/mobile-apps/10298308011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Travel":"https://www.amazon.com/Best-Sellers-Apps-Games-Travel/zgbs/mobile-apps/9408785011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Utilities":"https://www.amazon.com/Best-Sellers-Apps-Games-Utilities/zgbs/mobile-apps/9408914011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Weather":"https://www.amazon.com/Best-Sellers-Apps-Games-Weather/zgbs/mobile-apps/9408850011/ref=zg_bs_nav_mobile-apps_1",
    "Apps & Games/Top 100 Free":"https://www.amazon.com/gp/bestsellers/mobile-apps/ref=zg_bs?ie=UTF8&tf=1",
    "Apps & Games/1":"https://www.amazon.com/Best-Sellers-Apps-Games/zgbs/mobile-apps/ref=zg_bs_pg_1_mobile-apps?_encoding=UTF8&pg=1",
    "Apps & Games/2":"https://www.amazon.com/Best-Sellers-Apps-Games/zgbs/mobile-apps/ref=zg_bs_pg_2_mobile-apps?_encoding=UTF8&pg=2",
    "Apps & Games/Next page":"https://www.amazon.com/Best-Sellers-Apps-Games/zgbs/mobile-apps/ref=zg_bs_pg_2_mobile-apps?_encoding=UTF8&pg=2",
    "Arts, Crafts & Sewing/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_arts-crafts_0_1",
    "Arts, Crafts & Sewing/Beading & Jewelry Making":"https://www.amazon.com/Best-Sellers-Arts-Crafts-Sewing-Beading-Jewelry-Making/zgbs/arts-crafts/12896081/ref=zg_bs_nav_arts-crafts_1",
    "Arts, Crafts & Sewing/Craft Supplies":"https://www.amazon.com/Best-Sellers-Arts-Crafts-Sewing-Craft-Supplies-Materials/zgbs/arts-crafts/378733011/ref=zg_bs_nav_arts-crafts_1",
    "Arts, Crafts & Sewing/Fabric":"https://www.amazon.com/Best-Sellers-Arts-Crafts-Sewing-Craft-Hobby-Fabric/zgbs/arts-crafts/12899121/ref=zg_bs_nav_arts-crafts_1",
    "Arts, Crafts & Sewing/Fabric Painting & Dyeing":"https://www.amazon.com/Best-Sellers-Arts-Crafts-Sewing-Fabric-Decorating/zgbs/arts-crafts/12896841/ref=zg_bs_nav_arts-crafts_1",
    "Arts, Crafts & Sewing/Knitting & Crochet":"https://www.amazon.com/Best-Sellers-Arts-Crafts-Sewing-Knitting-Crochet-Supplies/zgbs/arts-crafts/12897221/ref=zg_bs_nav_arts-crafts_1",
    "Arts, Crafts & Sewing/Needlework":"https://www.amazon.com/Best-Sellers-Arts-Crafts-Sewing-Needlework-Supplies/zgbs/arts-crafts/2237329011/ref=zg_bs_nav_arts-crafts_1",
    "Arts, Crafts & Sewing/Organization & Storage":"https://www.amazon.com/Best-Sellers-Arts-Crafts-Sewing-Arts-Crafts-Sewing-Storage/zgbs/arts-crafts/2237594011/ref=zg_bs_nav_arts-crafts_1",
    "Arts, Crafts & Sewing/Painting, Drawing & Art Supplies":"https://www.amazon.com/Best-Sellers-Arts-Crafts-Sewing-Painting-Drawing-Art-Supplies/zgbs/arts-crafts/2747968011/ref=zg_bs_nav_arts-crafts_1",
    "Arts, Crafts & Sewing/Photo Transfer & Coloring Supplies":"https://www.amazon.com/Best-Sellers-Arts-Crafts-Sewing-Scrapbooking-Photo-Transfer-Coloring/zgbs/arts-crafts/12898411/ref=zg_bs_nav_arts-crafts_1",
    "Arts, Crafts & Sewing/Printmaking":"https://www.amazon.com/Best-Sellers-Arts-Crafts-Sewing-Printmaking-Supplies/zgbs/arts-crafts/12898451/ref=zg_bs_nav_arts-crafts_1",
    "Arts, Crafts & Sewing/Scrapbooking":"https://www.amazon.com/Best-Sellers-Arts-Crafts-Sewing-Scrapbooking-Stamping-Supplies/zgbs/arts-crafts/12898821/ref=zg_bs_nav_arts-crafts_1",
    "Arts, Crafts & Sewing/Sewing":"https://www.amazon.com/Best-Sellers-Arts-Crafts-Sewing-Sewing-Products/zgbs/arts-crafts/12899091/ref=zg_bs_nav_arts-crafts_1",
    "Arts, Crafts & Sewing/Thread & Floss":"https://www.amazon.com/Best-Sellers-Arts-Crafts-Sewing-Sewing-Thread-Floss/zgbs/arts-crafts/12897331/ref=zg_bs_nav_arts-crafts_1",
    "Arts, Crafts & Sewing/Yarn":"https://www.amazon.com/Best-Sellers-Arts-Crafts-Sewing-Yarn/zgbs/arts-crafts/262625011/ref=zg_bs_nav_arts-crafts_1",
    "Arts, Crafts & Sewing/1":"https://www.amazon.com/Best-Sellers-Arts-Crafts-Sewing/zgbs/arts-crafts/ref=zg_bs_pg_1_arts-crafts?_encoding=UTF8&pg=1",
    "Arts, Crafts & Sewing/2":"https://www.amazon.com/Best-Sellers-Arts-Crafts-Sewing/zgbs/arts-crafts/ref=zg_bs_pg_2_arts-crafts?_encoding=UTF8&pg=2",
    "Arts, Crafts & Sewing/Next page":"https://www.amazon.com/Best-Sellers-Arts-Crafts-Sewing/zgbs/arts-crafts/ref=zg_bs_pg_2_arts-crafts?_encoding=UTF8&pg=2",
    "Audible Books & Originals/Now Trending":"https://www.amazon.com/Best-Sellers-Audible-Audiobooks/zgbs/audible/?_encoding=UTF8&ref_=nav_sn_adbl_subnav_ref1_adbl_subnav_ref3_aj",
    "Audible Books & Originals/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_audible_0_1",
    "Audible Books & Originals/Arts & Entertainment":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals-Arts-Entertainment/zgbs/audible/18571910011/ref=zg_bs_nav_audible_1",
    "Audible Books & Originals/Biographies & Memoirs":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals-Biographies-Memoirs/zgbs/audible/18571951011/ref=zg_bs_nav_audible_1",
    "Audible Books & Originals/Business & Careers":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals-Business-Careers/zgbs/audible/18572029011/ref=zg_bs_nav_audible_1",
    "Audible Books & Originals/Children's Audiobooks":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals-Audiobooks-for-Children/zgbs/audible/18572091011/ref=zg_bs_nav_audible_1",
    "Audible Books & Originals/Comedy & Humor":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals-Comedy-Humor/zgbs/audible/24427740011/ref=zg_bs_nav_audible_1",
    "Audible Books & Originals/Computers & Technology":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals-Computers-Technology/zgbs/audible/18573211011/ref=zg_bs_nav_audible_1",
    "Audible Books & Originals/Education & Learning":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals-Education-Learning/zgbs/audible/18573267011/ref=zg_bs_nav_audible_1",
    "Audible Books & Originals/Erotica":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals-Erotica/zgbs/audible/18573351011/ref=zg_bs_nav_audible_1",
    "Audible Books & Originals/Health & Wellness":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals-Health-Wellness/zgbs/audible/18573370011/ref=zg_bs_nav_audible_1",
    "Audible Books & Originals/History":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals-History/zgbs/audible/18573518011/ref=zg_bs_nav_audible_1",
    "Audible Books & Originals/Home & Garden":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals-Home-Garden/zgbs/audible/18573701011/ref=zg_bs_nav_audible_1",
    "Audible Books & Originals/LGBTQ+":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals-LGBTQ/zgbs/audible/18573743011/ref=zg_bs_nav_audible_1",
    "Audible Books & Originals/Literature & Fiction":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals-Literature-Fiction/zgbs/audible/18574426011/ref=zg_bs_nav_audible_1",
    "Audible Books & Originals/Money & Finance":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals-Money-Finance/zgbs/audible/18574547011/ref=zg_bs_nav_audible_1",
    "Audible Books & Originals/Mystery, Thriller & Suspense":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals-Mystery-Thriller-Suspense/zgbs/audible/18574597011/ref=zg_bs_nav_audible_1",
    "Audible Books & Originals/Politics & Social Sciences":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals-Politics-Social-Sciences/zgbs/audible/18574641011/ref=zg_bs_nav_audible_1",
    "Audible Books & Originals/Relationships, Parenting & Personal Development":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals-Relationships-Parenting-Personal-Development/zgbs/audible/18574784011/ref=zg_bs_nav_audible_1",
    "Audible Books & Originals/Religion & Spirituality":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals-Religion-Spirituality/zgbs/audible/18574839011/ref=zg_bs_nav_audible_1",
    "Audible Books & Originals/Romance":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals-Romance/zgbs/audible/18580518011/ref=zg_bs_nav_audible_1",
    "Audible Books & Originals/Science & Engineering":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals-Science-Engineering/zgbs/audible/18580540011/ref=zg_bs_nav_audible_1",
    "Audible Books & Originals/Science Fiction & Fantasy":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals-Science-Fiction-Fantasy/zgbs/audible/18580606011/ref=zg_bs_nav_audible_1",
    "Audible Books & Originals/Teen & Young Adult":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals-Teen-Young-Adult/zgbs/audible/18580715011/ref=zg_bs_nav_audible_1",
    "Audible Books & Originals/Travel & Tourism":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals-Travel-Tourism/zgbs/audible/18581095011/ref=zg_bs_nav_audible_1",
    "Audible Books & Originals/1":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals/zgbs/audible/ref=zg_bs_pg_1_audible?_encoding=UTF8&pg=1",
    "Audible Books & Originals/2":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals/zgbs/audible/ref=zg_bs_pg_2_audible?_encoding=UTF8&pg=2",
    "Audible Books & Originals/Next page":"https://www.amazon.com/Best-Sellers-Audible-Books-Originals/zgbs/audible/ref=zg_bs_pg_2_audible?_encoding=UTF8&pg=2",
    "Automotive/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_automotive_0_1",
    "Automotive/Car Care":"https://www.amazon.com/Best-Sellers-Automotive-Car-Care/zgbs/automotive/15718271/ref=zg_bs_nav_automotive_1",
    "Automotive/Exterior Accessories":"https://www.amazon.com/Best-Sellers-Automotive-Automotive-Exterior-Accessories/zgbs/automotive/15857511/ref=zg_bs_nav_automotive_1",
    "Automotive/Interior Accessories":"https://www.amazon.com/Best-Sellers-Automotive-Automotive-Interior-Accessories/zgbs/automotive/15857501/ref=zg_bs_nav_automotive_1",
    "Automotive/Light & Lighting Accessories":"https://www.amazon.com/Best-Sellers-Automotive-Automotive-Lights-Bulbs-Indicators/zgbs/automotive/15736321/ref=zg_bs_nav_automotive_1",
    "Automotive/Motorcycle & ATV":"https://www.amazon.com/Best-Sellers-Automotive-Motorcycle-Powersports/zgbs/automotive/346333011/ref=zg_bs_nav_automotive_1",
    "Automotive/Oils & Fluids":"https://www.amazon.com/Best-Sellers-Automotive-Oils-Fluids/zgbs/automotive/15718791/ref=zg_bs_nav_automotive_1",
    "Automotive/Paint & Paint Supplies":"https://www.amazon.com/Best-Sellers-Automotive-Automotive-Paint-Paint-Supplies/zgbs/automotive/13591416011/ref=zg_bs_nav_automotive_1",
    "Automotive/Performance Parts & Accessories":"https://www.amazon.com/Best-Sellers-Automotive-Automotive-Performance-Parts-Accessories/zgbs/automotive/15710351/ref=zg_bs_nav_automotive_1",
    "Automotive/RV Parts & Accessories":"https://www.amazon.com/Best-Sellers-Automotive-RV-Parts-Accessories/zgbs/automotive/2258019011/ref=zg_bs_nav_automotive_1",
    "Automotive/Replacement Parts":"https://www.amazon.com/Best-Sellers-Automotive-Automotive-Replacement-Parts/zgbs/automotive/15719731/ref=zg_bs_nav_automotive_1",
    "Automotive/Tools & Equipment":"https://www.amazon.com/Best-Sellers-Automotive-Automotive-Tools-Equipment/zgbs/automotive/15706941/ref=zg_bs_nav_automotive_1",
    "Automotive/Wheels & Tires":"https://www.amazon.com/Best-Sellers-Automotive-Automotive-Tires-Wheels/zgbs/automotive/15706571/ref=zg_bs_nav_automotive_1",
    "Automotive/1":"https://www.amazon.com/Best-Sellers-Automotive/zgbs/automotive/ref=zg_bs_pg_1_automotive?_encoding=UTF8&pg=1",
    "Automotive/2":"https://www.amazon.com/Best-Sellers-Automotive/zgbs/automotive/ref=zg_bs_pg_2_automotive?_encoding=UTF8&pg=2",
    "Automotive/Next page":"https://www.amazon.com/Best-Sellers-Automotive/zgbs/automotive/ref=zg_bs_pg_2_automotive?_encoding=UTF8&pg=2",
    "Baby/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_baby-products_0_1",
    "Baby/Activity & Entertainment":"https://www.amazon.com/Best-Sellers-Baby-Baby-Activity-Entertainment-Products/zgbs/baby-products/239225011/ref=zg_bs_nav_baby-products_1",
    "Baby/Baby Care":"https://www.amazon.com/Best-Sellers-Baby-Baby-Care-Products/zgbs/baby-products/17720255011/ref=zg_bs_nav_baby-products_1",
    "Baby/Car Seats":"https://www.amazon.com/Best-Sellers-Baby-Child-Safety-Car-Seats-Accessories/zgbs/baby-products/166835011/ref=zg_bs_nav_baby-products_1",
    "Baby/Diapering":"https://www.amazon.com/Best-Sellers-Baby-Baby-Diapering-Products/zgbs/baby-products/166764011/ref=zg_bs_nav_baby-products_1",
    "Baby/Feeding":"https://www.amazon.com/Best-Sellers-Baby-Baby-Toddler-Feeding-Supplies/zgbs/baby-products/166777011/ref=zg_bs_nav_baby-products_1",
    "Baby/For Moms":"https://www.amazon.com/Best-Sellers-Baby-Pregnancy-Maternity-Products/zgbs/baby-products/166804011/ref=zg_bs_nav_baby-products_1",
    "Baby/Gifts":"https://www.amazon.com/Best-Sellers-Baby-Baby-Gifts/zgbs/baby-products/239226011/ref=zg_bs_nav_baby-products_1",
    "Baby/Nursery":"https://www.amazon.com/Best-Sellers-Baby-Nursery-Furniture-Bedding-Dcor/zgbs/baby-products/695338011/ref=zg_bs_nav_baby-products_1",
    "Baby/Potty Training":"https://www.amazon.com/Best-Sellers-Baby-Toilet-Training-Products/zgbs/baby-products/166887011/ref=zg_bs_nav_baby-products_1",
    "Baby/Safety":"https://www.amazon.com/Best-Sellers-Baby-Baby-Safety-Products/zgbs/baby-products/166863011/ref=zg_bs_nav_baby-products_1",
    "Baby/Strollers":"https://www.amazon.com/Best-Sellers-Baby-Baby-Strollers/zgbs/baby-products/166842011/ref=zg_bs_nav_baby-products_1",
    "Baby/Travel Gear":"https://www.amazon.com/Best-Sellers-Baby-Baby-Travel-Gear/zgbs/baby-products/17726796011/ref=zg_bs_nav_baby-products_1",
    "Baby/1":"https://www.amazon.com/Best-Sellers-Baby/zgbs/baby-products/ref=zg_bs_pg_1_baby-products?_encoding=UTF8&pg=1",
    "Baby/2":"https://www.amazon.com/Best-Sellers-Baby/zgbs/baby-products/ref=zg_bs_pg_2_baby-products?_encoding=UTF8&pg=2",
    "Baby/Next page":"https://www.amazon.com/Best-Sellers-Baby/zgbs/baby-products/ref=zg_bs_pg_2_baby-products?_encoding=UTF8&pg=2",
    "Beauty & Personal Care/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_beauty_0_1",
    "Beauty & Personal Care/Foot, Hand & Nail Care":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care-Foot-Hand-Nail-Care-Products/zgbs/beauty/17242866011/ref=zg_bs_nav_beauty_1",
    "Beauty & Personal Care/Fragrance":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care-Perfumes-Fragrances/zgbs/beauty/11056591/ref=zg_bs_nav_beauty_1",
    "Beauty & Personal Care/Gift Sets":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care-Beauty-Gift-Sets/zgbs/beauty/120225719011/ref=zg_bs_nav_beauty_1",
    "Beauty & Personal Care/Hair Care":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care-Hair-Care-Products/zgbs/beauty/11057241/ref=zg_bs_nav_beauty_1",
    "Beauty & Personal Care/Makeup":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care-Makeup/zgbs/beauty/11058281/ref=zg_bs_nav_beauty_1",
    "Beauty & Personal Care/Personal Care":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care-Personal-Care-Products/zgbs/beauty/3777891/ref=zg_bs_nav_beauty_1",
    "Beauty & Personal Care/Salon & Spa Equipment":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care-Salon-Spa-Equipment/zgbs/beauty/15144566011/ref=zg_bs_nav_beauty_1",
    "Beauty & Personal Care/Shave & Hair Removal":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care-Shaving-Hair-Removal-Products/zgbs/beauty/3778591/ref=zg_bs_nav_beauty_1",
    "Beauty & Personal Care/Skin Care":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care-Skin-Care-Products/zgbs/beauty/11060451/ref=zg_bs_nav_beauty_1",
    "Beauty & Personal Care/Tools & Accessories":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care-Beauty-Tools-Accessories/zgbs/beauty/11062741/ref=zg_bs_nav_beauty_1",
    "Beauty & Personal Care/1":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care/zgbs/beauty/ref=zg_bs_pg_1_beauty?_encoding=UTF8&pg=1",
    "Beauty & Personal Care/2":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care/zgbs/beauty/ref=zg_bs_pg_2_beauty?_encoding=UTF8&pg=2",
    "Beauty & Personal Care/Next page":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care/zgbs/beauty/ref=zg_bs_pg_2_beauty?_encoding=UTF8&pg=2",
    "Books/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_books_0_1",
    "Books/Arts & Photography":"https://www.amazon.com/Best-Sellers-Books-Arts-Photography/zgbs/books/1/ref=zg_bs_nav_books_1",
    "Books/Biographies & Memoirs":"https://www.amazon.com/Best-Sellers-Books-Biographies/zgbs/books/2/ref=zg_bs_nav_books_1",
    "Books/Books on CD":"https://www.amazon.com/Best-Sellers-Books-Books-on-CD/zgbs/books/69724/ref=zg_bs_nav_books_1",
    "Books/Business & Money":"https://www.amazon.com/Best-Sellers-Books-Business-Money/zgbs/books/3/ref=zg_bs_nav_books_1",
    "Books/Calendars":"https://www.amazon.com/Best-Sellers-Books-Calendars/zgbs/books/3248857011/ref=zg_bs_nav_books_1",
    "Books/Children's Books":"https://www.amazon.com/Best-Sellers-Books-Childrens-Books/zgbs/books/4/ref=zg_bs_nav_books_1",
    "Books/Christian Books & Bibles":"https://www.amazon.com/Best-Sellers-Books-Christian-Books-Bibles/zgbs/books/12290/ref=zg_bs_nav_books_1",
    "Books/Comics & Graphic Novels":"https://www.amazon.com/Best-Sellers-Books-Comics-Graphic-Novels/zgbs/books/4366/ref=zg_bs_nav_books_1",
    "Books/Computers & Technology":"https://www.amazon.com/Best-Sellers-Books-Computers-Technology/zgbs/books/5/ref=zg_bs_nav_books_1",
    "Books/Cookbooks, Food & Wine":"https://www.amazon.com/Best-Sellers-Books-Cookbooks-Food-Wine/zgbs/books/6/ref=zg_bs_nav_books_1",
    "Books/Crafts, Hobbies & Home":"https://www.amazon.com/Best-Sellers-Books-Crafts-Hobbies-Home/zgbs/books/48/ref=zg_bs_nav_books_1",
    "Books/Education & Teaching":"https://www.amazon.com/Best-Sellers-Books-Education-Teaching/zgbs/books/8975347011/ref=zg_bs_nav_books_1",
    "Books/Engineering & Transportation":"https://www.amazon.com/Best-Sellers-Books-Engineering-Transportation/zgbs/books/173507/ref=zg_bs_nav_books_1",
    "Books/Health, Fitness & Dieting":"https://www.amazon.com/Best-Sellers-Books-Health-Fitness-Dieting/zgbs/books/10/ref=zg_bs_nav_books_1",
    "Books/History":"https://www.amazon.com/Best-Sellers-Books-History/zgbs/books/9/ref=zg_bs_nav_books_1",
    "Books/Humor & Entertainment":"https://www.amazon.com/Best-Sellers-Books-Humor-Entertainment/zgbs/books/86/ref=zg_bs_nav_books_1",
    "Books/Law":"https://www.amazon.com/Best-Sellers-Books-Law/zgbs/books/10777/ref=zg_bs_nav_books_1",
    "Books/Lesbian, Gay, Bisexual & Transgender Books":"https://www.amazon.com/Best-Sellers-Books-LGBTQ-Books/zgbs/books/301889/ref=zg_bs_nav_books_1",
    "Books/Libros en español":"https://www.amazon.com/Best-Sellers-Books-Libros-en-espaol/zgbs/books/16568978011/ref=zg_bs_nav_books_1",
    "Books/Literature & Fiction":"https://www.amazon.com/Best-Sellers-Books-Literature-Fiction/zgbs/books/17/ref=zg_bs_nav_books_1",
    "Books/Medical Books":"https://www.amazon.com/Best-Sellers-Books-Medical-Books/zgbs/books/173514/ref=zg_bs_nav_books_1",
    "Books/Mystery, Thriller & Suspense":"https://www.amazon.com/Best-Sellers-Books-Mystery-Thriller-Suspense/zgbs/books/18/ref=zg_bs_nav_books_1",
    "Books/New, Used & Rental Textbooks":"https://www.amazon.com/Best-Sellers-Books-Textbooks/zgbs/books/465600/ref=zg_bs_nav_books_1",
    "Books/Parenting & Relationships":"https://www.amazon.com/Best-Sellers-Books-Parenting-Relationships/zgbs/books/20/ref=zg_bs_nav_books_1",
    "Books/Politics & Social Sciences":"https://www.amazon.com/Best-Sellers-Books-Politics-Social-Sciences/zgbs/books/3377866011/ref=zg_bs_nav_books_1",
    "Books/Reference":"https://www.amazon.com/Best-Sellers-Books-Reference/zgbs/books/21/ref=zg_bs_nav_books_1",
    "Books/Religion & Spirituality":"https://www.amazon.com/Best-Sellers-Books-Religion-Spirituality/zgbs/books/22/ref=zg_bs_nav_books_1",
    "Books/Romance":"https://www.amazon.com/Best-Sellers-Books-Romance/zgbs/books/23/ref=zg_bs_nav_books_1",
    "Books/Science & Math":"https://www.amazon.com/Best-Sellers-Books-Science-Math/zgbs/books/75/ref=zg_bs_nav_books_1",
    "Books/Science Fiction & Fantasy":"https://www.amazon.com/Best-Sellers-Books-Science-Fiction-Fantasy/zgbs/books/25/ref=zg_bs_nav_books_1",
    "Books/Self-Help":"https://www.amazon.com/Best-Sellers-Books-Self-Help/zgbs/books/4736/ref=zg_bs_nav_books_1",
    "Books/Teens":"https://www.amazon.com/Best-Sellers-Books-Teen-Young-Adult-Books/zgbs/books/28/ref=zg_bs_nav_books_1",
    "Books/Test Preparation":"https://www.amazon.com/Best-Sellers-Books-Test-Preparation/zgbs/books/5267710011/ref=zg_bs_nav_books_1",
    "Books/Travel":"https://www.amazon.com/Best-Sellers-Books-Travel/zgbs/books/27/ref=zg_bs_nav_books_1",
    "Books/1":"https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/ref=zg_bs_pg_1_books?_encoding=UTF8&pg=1",
    "Books/2":"https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/ref=zg_bs_pg_2_books?_encoding=UTF8&pg=2",
    "Books/Next page":"https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/ref=zg_bs_pg_2_books?_encoding=UTF8&pg=2",
    "Camera & Photo Products/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_photo_0_1",
    "Camera & Photo Products/Accessories":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-Camera-Photo-Accessories/zgbs/photo/172435/ref=zg_bs_nav_photo_1",
    "Camera & Photo Products/Bags & Cases":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-Camera-Bags-Cases/zgbs/photo/172437/ref=zg_bs_nav_photo_1",
    "Camera & Photo Products/Binoculars & Scopes":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-Binoculars-Telescopes-Optics/zgbs/photo/499320/ref=zg_bs_nav_photo_1",
    "Camera & Photo Products/Camcorders":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-Camcorders/zgbs/photo/172421/ref=zg_bs_nav_photo_1",
    "Camera & Photo Products/DSLR Cameras":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-DSLR-Cameras/zgbs/photo/3017941/ref=zg_bs_nav_photo_1",
    "Camera & Photo Products/Digital Picture Frames":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-Digital-Picture-Frames/zgbs/photo/525460/ref=zg_bs_nav_photo_1",
    "Camera & Photo Products/Lenses":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-Camcorder-Camera-Lenses/zgbs/photo/499248/ref=zg_bs_nav_photo_1",
    "Camera & Photo Products/Point & Shoot Digital Cameras":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-Digital-Point-Shoot-Cameras/zgbs/photo/330405011/ref=zg_bs_nav_photo_1",
    "Camera & Photo Products/Surveillance Cameras":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-Surveillance-Security-Cameras/zgbs/photo/898400/ref=zg_bs_nav_photo_1",
    "Camera & Photo Products/1":"https://www.amazon.com/best-sellers-camera-photo/zgbs/photo/ref=zg_bs_pg_1_photo?_encoding=UTF8&pg=1",
    "Camera & Photo Products/2":"https://www.amazon.com/best-sellers-camera-photo/zgbs/photo/ref=zg_bs_pg_2_photo?_encoding=UTF8&pg=2",
    "Camera & Photo Products/Next page":"https://www.amazon.com/best-sellers-camera-photo/zgbs/photo/ref=zg_bs_pg_2_photo?_encoding=UTF8&pg=2",
    "CDs & Vinyl/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_music_0_1",
    "CDs & Vinyl/Alternative Rock":"https://www.amazon.com/Best-Sellers-CDs-Vinyl-Alternative-Rock/zgbs/music/30/ref=zg_bs_nav_music_1",
    "CDs & Vinyl/Blues":"https://www.amazon.com/Best-Sellers-CDs-Vinyl-Blues/zgbs/music/31/ref=zg_bs_nav_music_1",
    "CDs & Vinyl/Broadway & Vocalists":"https://www.amazon.com/Best-Sellers-CDs-Vinyl-Broadway-Vocalists/zgbs/music/265640/ref=zg_bs_nav_music_1",
    "CDs & Vinyl/Children's Music":"https://www.amazon.com/Best-Sellers-CDs-Vinyl-Childrens-Music/zgbs/music/173425/ref=zg_bs_nav_music_1",
    "CDs & Vinyl/Christian":"https://www.amazon.com/Best-Sellers-CDs-Vinyl-Christian-Gospel/zgbs/music/173429/ref=zg_bs_nav_music_1",
    "CDs & Vinyl/Classic Rock":"https://www.amazon.com/Best-Sellers-CDs-Vinyl-Classic-Rock/zgbs/music/67204/ref=zg_bs_nav_music_1",
    "CDs & Vinyl/Classical":"https://www.amazon.com/Best-Sellers-CDs-Vinyl-Classical/zgbs/music/85/ref=zg_bs_nav_music_1",
    "CDs & Vinyl/Country":"https://www.amazon.com/Best-Sellers-CDs-Vinyl-Country/zgbs/music/16/ref=zg_bs_nav_music_1",
    "CDs & Vinyl/Dance & Electronic":"https://www.amazon.com/Best-Sellers-CDs-Vinyl-Dance-Electronic/zgbs/music/7/ref=zg_bs_nav_music_1",
    "CDs & Vinyl/Folk":"https://www.amazon.com/Best-Sellers-CDs-Vinyl-Folk/zgbs/music/32/ref=zg_bs_nav_music_1",
    "CDs & Vinyl/Gospel":"https://www.amazon.com/Best-Sellers-CDs-Vinyl-Gospel/zgbs/music/2231705011/ref=zg_bs_nav_music_1",
    "CDs & Vinyl/Hard Rock & Metal":"https://www.amazon.com/Best-Sellers-CDs-Vinyl-Metal/zgbs/music/67207/ref=zg_bs_nav_music_1",
    "CDs & Vinyl/Indie & Lo-Fi":"https://www.amazon.com/Best-Sellers-CDs-Vinyl-Indie-Lo-Fi/zgbs/music/468300/ref=zg_bs_nav_music_1",
    "CDs & Vinyl/International Music":"https://www.amazon.com/Best-Sellers-CDs-Vinyl-International-Music/zgbs/music/33/ref=zg_bs_nav_music_1",
    "CDs & Vinyl/Jazz":"https://www.amazon.com/Best-Sellers-CDs-Vinyl-Jazz/zgbs/music/34/ref=zg_bs_nav_music_1",
    "CDs & Vinyl/Latin Music":"https://www.amazon.com/Best-Sellers-CDs-Vinyl-Latin/zgbs/music/289122/ref=zg_bs_nav_music_1",
    "CDs & Vinyl/Miscellaneous":"https://www.amazon.com/Best-Sellers-CDs-Vinyl-Special-Interest/zgbs/music/35/ref=zg_bs_nav_music_1",
    "CDs & Vinyl/New Age":"https://www.amazon.com/Best-Sellers-CDs-Vinyl-New-Age/zgbs/music/36/ref=zg_bs_nav_music_1",
    "CDs & Vinyl/Opera & Vocal":"https://www.amazon.com/Best-Sellers-CDs-Vinyl-Opera-Vocal/zgbs/music/84/ref=zg_bs_nav_music_1",
    "CDs & Vinyl/Pop":"https://www.amazon.com/Best-Sellers-CDs-Vinyl-Pop/zgbs/music/37/ref=zg_bs_nav_music_1",
    "CDs & Vinyl/R&B":"https://www.amazon.com/Best-Sellers-CDs-Vinyl-RB/zgbs/music/39/ref=zg_bs_nav_music_1",
    "CDs & Vinyl/Rap & Hip-Hop":"https://www.amazon.com/Best-Sellers-CDs-Vinyl-Rap-Hip-Hop/zgbs/music/38/ref=zg_bs_nav_music_1",
    "CDs & Vinyl/Rock":"https://www.amazon.com/Best-Sellers-CDs-Vinyl-Rock/zgbs/music/40/ref=zg_bs_nav_music_1",
    "CDs & Vinyl/Soundtracks":"https://www.amazon.com/Best-Sellers-CDs-Vinyl-Soundtracks/zgbs/music/42/ref=zg_bs_nav_music_1",
    "CDs & Vinyl/1":"https://www.amazon.com/best-sellers-music-albums/zgbs/music/ref=zg_bs_pg_1_music?_encoding=UTF8&pg=1",
    "CDs & Vinyl/2":"https://www.amazon.com/best-sellers-music-albums/zgbs/music/ref=zg_bs_pg_2_music?_encoding=UTF8&pg=2",
    "CDs & Vinyl/Next page":"https://www.amazon.com/best-sellers-music-albums/zgbs/music/ref=zg_bs_pg_2_music?_encoding=UTF8&pg=2",
    "Cell Phones & Accessories/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_wireless_0_1",
    "Cell Phones & Accessories/Accessories":"https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Accessories/zgbs/wireless/2407755011/ref=zg_bs_nav_wireless_1",
    "Cell Phones & Accessories/Cases, Holsters & Clips":"https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Cases-Covers/zgbs/wireless/2407760011/ref=zg_bs_nav_wireless_1",
    "Cell Phones & Accessories/Cell Phones":"https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phones/zgbs/wireless/7072561011/ref=zg_bs_nav_wireless_1",
    "Cell Phones & Accessories/SIM Cards & Prepaid Minutes":"https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-SIM-Cards-Prepaid-Minutes/zgbs/wireless/3345523011/ref=zg_bs_nav_wireless_1",
    "Cell Phones & Accessories/1":"https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories/zgbs/wireless/ref=zg_bs_pg_1_wireless?_encoding=UTF8&pg=1",
    "Cell Phones & Accessories/2":"https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories/zgbs/wireless/ref=zg_bs_pg_2_wireless?_encoding=UTF8&pg=2",
    "Cell Phones & Accessories/Next page":"https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories/zgbs/wireless/ref=zg_bs_pg_2_wireless?_encoding=UTF8&pg=2",
    "Clothing, Shoes & Jewelry/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_fashion_0_1",
    "Clothing, Shoes & Jewelry/Boys":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Boys-Fashion/zgbs/fashion/7147443011/ref=zg_bs_nav_fashion_1",
    "Clothing, Shoes & Jewelry/Costumes & Accessories":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Costumes-Accessories/zgbs/fashion/7586165011/ref=zg_bs_nav_fashion_1",
    "Clothing, Shoes & Jewelry/Girls":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Girls-Fashion/zgbs/fashion/7147442011/ref=zg_bs_nav_fashion_1",
    "Clothing, Shoes & Jewelry/Luggage & Travel Gear":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Luggage-Travel-Gear/zgbs/fashion/9479199011/ref=zg_bs_nav_fashion_1",
    "Clothing, Shoes & Jewelry/Men":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Fashion/zgbs/fashion/7147441011/ref=zg_bs_nav_fashion_1",
    "Clothing, Shoes & Jewelry/Novelty & More":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Novelty-More/zgbs/fashion/7147445011/ref=zg_bs_nav_fashion_1",
    "Clothing, Shoes & Jewelry/Shoe, Jewelry & Watch Accessories":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Shoe-Jewelry-Watch-Accessories/zgbs/fashion/7586146011/ref=zg_bs_nav_fashion_1",
    "Clothing, Shoes & Jewelry/Sport Specific Clothing":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Sport-Specific-Clothing/zgbs/fashion/23575629011/ref=zg_bs_nav_fashion_1",
    "Clothing, Shoes & Jewelry/Uniforms, Work & Safety":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Uniforms-Work-Safety/zgbs/fashion/7586144011/ref=zg_bs_nav_fashion_1",
    "Clothing, Shoes & Jewelry/Women":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Womens-Fashion/zgbs/fashion/7147440011/ref=zg_bs_nav_fashion_1",
    "Clothing, Shoes & Jewelry/1":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry/zgbs/fashion/ref=zg_bs_pg_1_fashion?_encoding=UTF8&pg=1",
    "Clothing, Shoes & Jewelry/2":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry/zgbs/fashion/ref=zg_bs_pg_2_fashion?_encoding=UTF8&pg=2",
    "Clothing, Shoes & Jewelry/Next page":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry/zgbs/fashion/ref=zg_bs_pg_2_fashion?_encoding=UTF8&pg=2",
    "Collectible Coins/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_coins_0_1",
    "Collectible Coins/Coin Sets":"https://www.amazon.com/Best-Sellers-Collectible-Coins-Collectible-Coin-Sets/zgbs/coins/9003136011/ref=zg_bs_nav_coins_1",
    "Collectible Coins/Individual Coins":"https://www.amazon.com/Best-Sellers-Collectible-Coins-Individual-Collectible-Coins/zgbs/coins/9003133011/ref=zg_bs_nav_coins_1",
    "Collectible Coins/1":"https://www.amazon.com/Best-Sellers-Collectible-Coins/zgbs/coins/ref=zg_bs_pg_1_coins?_encoding=UTF8&pg=1",
    "Collectible Coins/2":"https://www.amazon.com/Best-Sellers-Collectible-Coins/zgbs/coins/ref=zg_bs_pg_2_coins?_encoding=UTF8&pg=2",
    "Collectible Coins/Next page":"https://www.amazon.com/Best-Sellers-Collectible-Coins/zgbs/coins/ref=zg_bs_pg_2_coins?_encoding=UTF8&pg=2",
    "Computers & Accessories/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_pc_0_1",
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
    "Computers & Accessories/Warranties & Services":"https://www.amazon.com/Best-Sellers-Computers-Accessories-Computer-Warranties-Services/zgbs/pc/16285851/ref=zg_bs_nav_pc_1",
    "Computers & Accessories/1":"https://www.amazon.com/Best-Sellers-Computers-Accessories/zgbs/pc/ref=zg_bs_pg_1_pc?_encoding=UTF8&pg=1",
    "Computers & Accessories/2":"https://www.amazon.com/Best-Sellers-Computers-Accessories/zgbs/pc/ref=zg_bs_pg_2_pc?_encoding=UTF8&pg=2",
    "Computers & Accessories/Next page":"https://www.amazon.com/Best-Sellers-Computers-Accessories/zgbs/pc/ref=zg_bs_pg_2_pc?_encoding=UTF8&pg=2",
    "Digital Educational Resources/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_digital-educational-resources_0_2",
    "Digital Music/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_dmusic_0_1",
    "Digital Music/Albums":"https://www.amazon.com/Best-Sellers-Albums/zgbs/dmusic/digital-music-album/ref=zg_bs_nav_dmusic_1",
    "Digital Music/Songs":"https://www.amazon.com/Best-Sellers-Songs/zgbs/dmusic/digital-music-track/ref=zg_bs_nav_dmusic_1",
    "Electronics/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_electronics_0_1",
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
    "Electronics/eBook Readers & Accessories":"https://www.amazon.com/Best-Sellers-Electronics-eBook-Readers-Accessories/zgbs/electronics/2642125011/ref=zg_bs_nav_electronics_1",
    "Electronics/1":"https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/ref=zg_bs_pg_1_electronics?_encoding=UTF8&pg=1",
    "Electronics/2":"https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/ref=zg_bs_pg_2_electronics?_encoding=UTF8&pg=2",
    "Electronics/Next page":"https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/ref=zg_bs_pg_2_electronics?_encoding=UTF8&pg=2",
    "Entertainment Collectibles/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_entertainment-collectibles_0_1",
    "Entertainment Collectibles/Animation":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Animation-Collectibles/zgbs/entertainment-collectibles/7463352011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Apparel":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Apparel/zgbs/entertainment-collectibles/5263598011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Artwork By Celebrities":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Artwork-By-Celebrities/zgbs/entertainment-collectibles/6250511011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Backstage Passes":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Backstage-Passes/zgbs/entertainment-collectibles/5263599011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Comic Art":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Comic-Art/zgbs/entertainment-collectibles/7463351011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Comic Books":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Collectible-Comic-Books/zgbs/entertainment-collectibles/11873140011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Contracts":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Contracts/zgbs/entertainment-collectibles/5263604011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Correspondence":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Correspondence/zgbs/entertainment-collectibles/5263605011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Cut Signatures":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Cut-Signatures/zgbs/entertainment-collectibles/5931157011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Figurines":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Figurines/zgbs/entertainment-collectibles/19419881011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Flyers":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Flyers/zgbs/entertainment-collectibles/5263607011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Framed Record Award Sets":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Framed-Record-Award-Sets/zgbs/entertainment-collectibles/5525078011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Lobby Cards":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Lobby-Cards/zgbs/entertainment-collectibles/10434532011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Magazines":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Magazines/zgbs/entertainment-collectibles/5263609011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Movies & Music":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Movies-Music/zgbs/entertainment-collectibles/10394942011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Photographs":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Photographs/zgbs/entertainment-collectibles/5263611011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Plates":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Plates/zgbs/entertainment-collectibles/5263612011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Playbills":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Playbills/zgbs/entertainment-collectibles/5263613011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Postcards":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Postcards/zgbs/entertainment-collectibles/5263614011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Prints & Posters":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Prints-Posters/zgbs/entertainment-collectibles/5227492011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Programs":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Programs/zgbs/entertainment-collectibles/5263615011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Props":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Props/zgbs/entertainment-collectibles/5263616011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Publicity Photo Cards":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Publicity-Photo-Cards/zgbs/entertainment-collectibles/5263617011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Scripts":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Scripts/zgbs/entertainment-collectibles/5263618011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Sheet Music":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Sheet-Music/zgbs/entertainment-collectibles/5263619011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Signed Personal Checks":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Personal-Checks/zgbs/entertainment-collectibles/5263610011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Ticket Stubs":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Ticket-Stubs/zgbs/entertainment-collectibles/5263620011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Trading Cards":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Trading-Cards/zgbs/entertainment-collectibles/5263621011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/Wardrobe Items":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles-Entertainment-Collectible-Wardrobe-Items/zgbs/entertainment-collectibles/5263624011/ref=zg_bs_nav_entertainment-collectibles_1",
    "Entertainment Collectibles/1":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles/zgbs/entertainment-collectibles/ref=zg_bs_pg_1_entertainment-collectibles?_encoding=UTF8&pg=1",
    "Entertainment Collectibles/2":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles/zgbs/entertainment-collectibles/ref=zg_bs_pg_2_entertainment-collectibles?_encoding=UTF8&pg=2",
    "Entertainment Collectibles/Next page":"https://www.amazon.com/Best-Sellers-Entertainment-Collectibles/zgbs/entertainment-collectibles/ref=zg_bs_pg_2_entertainment-collectibles?_encoding=UTF8&pg=2",
    "Gift Cards/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_gift-cards_0_1",
    "Gift Cards/Baby & Expecting":"https://www.amazon.com/Best-Sellers-Gift-Cards-Baby-Expecting/zgbs/gift-cards/120225710011/ref=zg_bs_nav_gift-cards_1",
    "Gift Cards/Birthday":"https://www.amazon.com/Best-Sellers-Gift-Cards-Birthday/zgbs/gift-cards/120225714011/ref=zg_bs_nav_gift-cards_1",
    "Gift Cards/Christmas":"https://www.amazon.com/Best-Sellers-Gift-Cards-Christmas/zgbs/gift-cards/120225703011/ref=zg_bs_nav_gift-cards_1",
    "Gift Cards/Departments":"https://www.amazon.com/Best-Sellers-Gift-Cards-Gift-Cards-Store/zgbs/gift-cards/2864120011/ref=zg_bs_nav_gift-cards_1",
    "Gift Cards/Father's Day":"https://www.amazon.com/Best-Sellers-Gift-Cards-Fathers-Day/zgbs/gift-cards/120225713011/ref=zg_bs_nav_gift-cards_1",
    "Gift Cards/For Her":"https://www.amazon.com/Best-Sellers-Gift-Cards-For-Her/zgbs/gift-cards/120225711011/ref=zg_bs_nav_gift-cards_1",
    "Gift Cards/For Him":"https://www.amazon.com/Best-Sellers-Gift-Cards-For-Him/zgbs/gift-cards/120225704011/ref=zg_bs_nav_gift-cards_1",
    "Gift Cards/Graduation":"https://www.amazon.com/Best-Sellers-Gift-Cards-Graduation/zgbs/gift-cards/120225709011/ref=zg_bs_nav_gift-cards_1",
    "Gift Cards/Kids":"https://www.amazon.com/Best-Sellers-Gift-Cards-Kids/zgbs/gift-cards/120225706011/ref=zg_bs_nav_gift-cards_1",
    "Gift Cards/Mother's Day":"https://www.amazon.com/Best-Sellers-Gift-Cards-Mothers-Day/zgbs/gift-cards/120225708011/ref=zg_bs_nav_gift-cards_1",
    "Gift Cards/New Year's":"https://www.amazon.com/Best-Sellers-Gift-Cards-New-Years/zgbs/gift-cards/120225705011/ref=zg_bs_nav_gift-cards_1",
    "Gift Cards/Restaurants":"https://www.amazon.com/Best-Sellers-Gift-Cards-Restaurants/zgbs/gift-cards/120225715011/ref=zg_bs_nav_gift-cards_1",
    "Gift Cards/Teens":"https://www.amazon.com/Best-Sellers-Gift-Cards-Teens/zgbs/gift-cards/120225712011/ref=zg_bs_nav_gift-cards_1",
    "Gift Cards/Thank You & Appreciation":"https://www.amazon.com/Best-Sellers-Gift-Cards-Thank-You-Appreciation/zgbs/gift-cards/120225707011/ref=zg_bs_nav_gift-cards_1",
    "Gift Cards/Wedding & Engagement":"https://www.amazon.com/Best-Sellers-Gift-Cards-Wedding-Engagement/zgbs/gift-cards/120225717011/ref=zg_bs_nav_gift-cards_1",
    "Gift Cards/Winter Holidays":"https://www.amazon.com/Best-Sellers-Gift-Cards-Winter-Holidays/zgbs/gift-cards/120225716011/ref=zg_bs_nav_gift-cards_1",
    "Gift Cards/1":"https://www.amazon.com/Best-Sellers-Gift-Cards/zgbs/gift-cards/ref=zg_bs_pg_1_gift-cards?_encoding=UTF8&pg=1",
    "Gift Cards/2":"https://www.amazon.com/Best-Sellers-Gift-Cards/zgbs/gift-cards/ref=zg_bs_pg_2_gift-cards?_encoding=UTF8&pg=2",
    "Gift Cards/Next page":"https://www.amazon.com/Best-Sellers-Gift-Cards/zgbs/gift-cards/ref=zg_bs_pg_2_gift-cards?_encoding=UTF8&pg=2",
    "Grocery & Gourmet Food/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_grocery_0_1",
    "Grocery & Gourmet Food/Alcoholic Beverages":"https://www.amazon.com/Best-Sellers-Grocery-Gourmet-Food-Alcoholic-Beverages/zgbs/grocery/2983371011/ref=zg_bs_nav_grocery_1",
    "Grocery & Gourmet Food/Baby Foods":"https://www.amazon.com/Best-Sellers-Grocery-Gourmet-Food-Baby-Foods/zgbs/grocery/16323111/ref=zg_bs_nav_grocery_1",
    "Grocery & Gourmet Food/Beverages":"https://www.amazon.com/Best-Sellers-Grocery-Gourmet-Food-Beverages/zgbs/grocery/16310231/ref=zg_bs_nav_grocery_1",
    "Grocery & Gourmet Food/Breads & Bakery":"https://www.amazon.com/Best-Sellers-Grocery-Gourmet-Food-Breads-Bakery/zgbs/grocery/16318751/ref=zg_bs_nav_grocery_1",
    "Grocery & Gourmet Food/Breakfast Cereal":"https://www.amazon.com/Best-Sellers-Grocery-Gourmet-Food-Breakfast-Cereal/zgbs/grocery/118518014011/ref=zg_bs_nav_grocery_1",
    "Grocery & Gourmet Food/Breakfast Foods":"https://www.amazon.com/Best-Sellers-Grocery-Gourmet-Food-Breakfast-Foods/zgbs/grocery/16310251/ref=zg_bs_nav_grocery_1",
    "Grocery & Gourmet Food/Dairy, Eggs & Plant-Based Alternatives":"https://www.amazon.com/Best-Sellers-Grocery-Gourmet-Food-Dairy-Eggs-Plant-Based-Alternatives/zgbs/grocery/371460011/ref=zg_bs_nav_grocery_1",
    "Grocery & Gourmet Food/Deli & Prepared Foods":"https://www.amazon.com/Best-Sellers-Grocery-Gourmet-Food-Deli-Prepared-Foods/zgbs/grocery/18773724011/ref=zg_bs_nav_grocery_1",
    "Grocery & Gourmet Food/Food & Beverage Gifts":"https://www.amazon.com/Best-Sellers-Grocery-Gourmet-Food-Food-Beverage-Gifts/zgbs/grocery/2255571011/ref=zg_bs_nav_grocery_1",
    "Grocery & Gourmet Food/Fresh Flowers & Live Indoor Plants":"https://www.amazon.com/Best-Sellers-Grocery-Gourmet-Food-Fresh-Flowers-Live-Indoor-Plants/zgbs/grocery/3745171/ref=zg_bs_nav_grocery_1",
    "Grocery & Gourmet Food/Fresh Meal Kits":"https://www.amazon.com/Best-Sellers-Grocery-Gourmet-Food-Fresh-Meal-Ingredient-Kits/zgbs/grocery/15709227011/ref=zg_bs_nav_grocery_1",
    "Grocery & Gourmet Food/Frozen":"https://www.amazon.com/Best-Sellers-Grocery-Gourmet-Food-Frozen-Foods/zgbs/grocery/6459122011/ref=zg_bs_nav_grocery_1",
    "Grocery & Gourmet Food/Home Brewing & Winemaking":"https://www.amazon.com/Best-Sellers-Grocery-Gourmet-Food-Home-Brewing-Winemaking/zgbs/grocery/979861011/ref=zg_bs_nav_grocery_1",
    "Grocery & Gourmet Food/Meat & Seafood":"https://www.amazon.com/Best-Sellers-Grocery-Gourmet-Food-Meat-Seafood/zgbs/grocery/371469011/ref=zg_bs_nav_grocery_1",
    "Grocery & Gourmet Food/Meat Substitutes":"https://www.amazon.com/Best-Sellers-Grocery-Gourmet-Food-Meat-Substitutes/zgbs/grocery/6518859011/ref=zg_bs_nav_grocery_1",
    "Grocery & Gourmet Food/Pantry Staples":"https://www.amazon.com/Best-Sellers-Grocery-Gourmet-Food-Pantry-Staples/zgbs/grocery/18787303011/ref=zg_bs_nav_grocery_1",
    "Grocery & Gourmet Food/Produce":"https://www.amazon.com/Best-Sellers-Grocery-Gourmet-Food-Fresh-Produce/zgbs/grocery/6506977011/ref=zg_bs_nav_grocery_1",
    "Grocery & Gourmet Food/Snacks & Sweets":"https://www.amazon.com/Best-Sellers-Grocery-Gourmet-Food-Snacks-Sweets/zgbs/grocery/23759921011/ref=zg_bs_nav_grocery_1",
    "Grocery & Gourmet Food/1":"https://www.amazon.com/Best-Sellers-Grocery-Gourmet-Food/zgbs/grocery/ref=zg_bs_pg_1_grocery?_encoding=UTF8&pg=1",
    "Grocery & Gourmet Food/2":"https://www.amazon.com/Best-Sellers-Grocery-Gourmet-Food/zgbs/grocery/ref=zg_bs_pg_2_grocery?_encoding=UTF8&pg=2",
    "Grocery & Gourmet Food/Next page":"https://www.amazon.com/Best-Sellers-Grocery-Gourmet-Food/zgbs/grocery/ref=zg_bs_pg_2_grocery?_encoding=UTF8&pg=2",
    "Handmade Products/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_handmade_0_1",
    "Handmade Products/Handmade Baby":"https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Baby/zgbs/handmade/121190737011/ref=zg_bs_nav_handmade_1",
    "Handmade Products/Handmade Beauty & Personal Care":"https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Beauty-Personal-Care/zgbs/handmade/121190632011/ref=zg_bs_nav_handmade_1",
    "Handmade Products/Handmade Clothing & Accessories":"https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Clothing-Accessories/zgbs/handmade/121190502011/ref=zg_bs_nav_handmade_1",
    "Handmade Products/Handmade Home Décor":"https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Home-Dcor/zgbs/handmade/121190508011/ref=zg_bs_nav_handmade_1",
    "Handmade Products/Handmade Jewelry":"https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Jewelry/zgbs/handmade/121179460011/ref=zg_bs_nav_handmade_1",
    "Handmade Products/Handmade Kitchen & Dining":"https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Kitchen-Dining/zgbs/handmade/121190509011/ref=zg_bs_nav_handmade_1",
    "Handmade Products/Handmade Pet Supplies":"https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Pet-Supplies/zgbs/handmade/121190752011/ref=zg_bs_nav_handmade_1",
    "Handmade Products/Handmade Stationery & Party Supplies":"https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Stationery-Party-Supplies/zgbs/handmade/121190727011/ref=zg_bs_nav_handmade_1",
    "Handmade Products/Handmade Toys & Games":"https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Toys-Games/zgbs/handmade/121190630011/ref=zg_bs_nav_handmade_1",
    "Handmade Products/1":"https://www.amazon.com/Best-Sellers-Handmade-Products/zgbs/handmade/ref=zg_bs_pg_1_handmade?_encoding=UTF8&pg=1",
    "Handmade Products/2":"https://www.amazon.com/Best-Sellers-Handmade-Products/zgbs/handmade/ref=zg_bs_pg_2_handmade?_encoding=UTF8&pg=2",
    "Handmade Products/Next page":"https://www.amazon.com/Best-Sellers-Handmade-Products/zgbs/handmade/ref=zg_bs_pg_2_handmade?_encoding=UTF8&pg=2",
    "Health & Household/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_hpc_0_1",
    "Health & Household/Baby & Child Care":"https://www.amazon.com/Best-Sellers-Health-Household-Baby-Child-Care-Products/zgbs/hpc/10787321/ref=zg_bs_nav_hpc_1",
    "Health & Household/Diet & Sports Nutrition":"https://www.amazon.com/Best-Sellers-Health-Household-Diet-Sports-Nutrition/zgbs/hpc/3764441/ref=zg_bs_nav_hpc_1",
    "Health & Household/Health Care":"https://www.amazon.com/Best-Sellers-Health-Household-Health-Care-Products/zgbs/hpc/3760941/ref=zg_bs_nav_hpc_1",
    "Health & Household/House Supplies":"https://www.amazon.com/Best-Sellers-Health-Household-Household-Supplies/zgbs/hpc/15342811/ref=zg_bs_nav_hpc_1",
    "Health & Household/Medical Supplies & Equipment":"https://www.amazon.com/Best-Sellers-Health-Household-Home-Use-Medical-Supplies-Equipment/zgbs/hpc/3775161/ref=zg_bs_nav_hpc_1",
    "Health & Household/Oral Care":"https://www.amazon.com/Best-Sellers-Health-Household-Oral-Care-Products/zgbs/hpc/10079992011/ref=zg_bs_nav_hpc_1",
    "Health & Household/Personal Care":"https://www.amazon.com/Best-Sellers-Health-Household-Personal-Care-Products/zgbs/hpc/3777891/ref=zg_bs_nav_hpc_1",
    "Health & Household/Sales & Deals":"https://www.amazon.com/Best-Sellers-Health-Household-Sales-Deals/zgbs/hpc/120225718011/ref=zg_bs_nav_hpc_1",
    "Health & Household/Sexual Wellness":"https://www.amazon.com/Best-Sellers-Health-Household-Sexual-Wellness-Products/zgbs/hpc/3777371/ref=zg_bs_nav_hpc_1",
    "Health & Household/Sports Nutrition":"https://www.amazon.com/Best-Sellers-Health-Household-Sports-Nutrition-Products/zgbs/hpc/6973663011/ref=zg_bs_nav_hpc_1",
    "Health & Household/Stationery & Gift Wrapping Supplies":"https://www.amazon.com/Best-Sellers-Health-Household-Stationery-Gift-Wrapping-Supplies/zgbs/hpc/723418011/ref=zg_bs_nav_hpc_1",
    "Health & Household/Vision Care":"https://www.amazon.com/Best-Sellers-Health-Household-Vision-Products/zgbs/hpc/10079994011/ref=zg_bs_nav_hpc_1",
    "Health & Household/Vitamins, Minerals & Supplements":"https://www.amazon.com/Best-Sellers-Health-Household-Vitamins-Minerals-Supplements/zgbs/hpc/23675621011/ref=zg_bs_nav_hpc_1",
    "Health & Household/Wellness & Relaxation":"https://www.amazon.com/Best-Sellers-Health-Household-Wellness-Relaxation-Products/zgbs/hpc/10079996011/ref=zg_bs_nav_hpc_1",
    "Health & Household/1":"https://www.amazon.com/Best-Sellers-Health-Household/zgbs/hpc/ref=zg_bs_pg_1_hpc?_encoding=UTF8&pg=1",
    "Health & Household/2":"https://www.amazon.com/Best-Sellers-Health-Household/zgbs/hpc/ref=zg_bs_pg_2_hpc?_encoding=UTF8&pg=2",
    "Health & Household/Next page":"https://www.amazon.com/Best-Sellers-Health-Household/zgbs/hpc/ref=zg_bs_pg_2_hpc?_encoding=UTF8&pg=2",
    "Home & Kitchen/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_home-garden_0_1",
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
    "Home & Kitchen/1":"https://www.amazon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden/ref=zg_bs_pg_1_home-garden?_encoding=UTF8&pg=1",
    "Home & Kitchen/2":"https://www.amazon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden/ref=zg_bs_pg_2_home-garden?_encoding=UTF8&pg=2",
    "Home & Kitchen/Next page":"https://www.amazon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden/ref=zg_bs_pg_2_home-garden?_encoding=UTF8&pg=2",
    "Industrial & Scientific/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_industrial_0_1",
    "Industrial & Scientific/Abrasive & Finishing Products":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Abrasive-Finishing-Products/zgbs/industrial/256167011/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Additive Manufacturing Products":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Additive-Manufacturing-Products/zgbs/industrial/6066126011/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Adhesives, Sealants & Lubricants":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Industrial-Adhesives-Sealants-Lubricants/zgbs/industrial/256225011/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Commercial Door Products":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Door-Products/zgbs/industrial/10773802011/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Commercial Lighting":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Commercial-Lighting-Products/zgbs/industrial/5772192011/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Cutting Tools":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Cutting-Tools/zgbs/industrial/383598011/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Digital Signage":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Digital-Signage-Equipment/zgbs/industrial/18746931011/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Fasteners":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Fasteners/zgbs/industrial/383599011/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Filtration":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Filtration/zgbs/industrial/3061625011/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Food Service Equipment & Supplies":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Food-Service-Equipment-Supplies/zgbs/industrial/6054382011/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Hydraulics, Pneumatics & Plumbing":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Hydraulics-Pneumatics-Plumbing/zgbs/industrial/3021479011/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Industrial Electrical":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Electronic-Components/zgbs/industrial/306506011/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Industrial Hardware":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Industrial-Hardware/zgbs/industrial/16412251/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Janitorial & Sanitation Supplies":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Janitorial-Sanitation-Supplies/zgbs/industrial/317971011/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Lab & Scientific Products":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Lab-Scientific-Products/zgbs/industrial/317970011/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Material Handling Products":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Material-Handling-Products/zgbs/industrial/256346011/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Occupational Health & Safety Products":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Occupational-Health-Safety-Products/zgbs/industrial/318135011/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Packaging & Shipping Supplies":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Packaging-Shipping-Supplies/zgbs/industrial/8553197011/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Power & Hand Tools":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Industrial-Power-Hand-Tools/zgbs/industrial/3021459011/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Power Transmission Products":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Power-Transmission-Products/zgbs/industrial/16310181/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Professional Dental Supplies":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Professional-Dental-Supplies/zgbs/industrial/8297371011/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Professional Medical Supplies":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Professional-Medical-Supplies/zgbs/industrial/8297370011/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Raw Materials":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Industrial-Materials/zgbs/industrial/16310191/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Retail Store Fixtures & Equipment":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Retail-Store-Fixtures-Equipment/zgbs/industrial/8615538011/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Robotics":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Robotics/zgbs/industrial/8498884011/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Science Education":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Science-Education-Supplies/zgbs/industrial/393459011/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/Test, Measure & Inspect":"https://www.amazon.com/Best-Sellers-Industrial-Scientific-Test-Measure-Inspect/zgbs/industrial/256409011/ref=zg_bs_nav_industrial_1",
    "Industrial & Scientific/1":"https://www.amazon.com/Best-Sellers-Industrial-Scientific/zgbs/industrial/ref=zg_bs_pg_1_industrial?_encoding=UTF8&pg=1",
    "Industrial & Scientific/2":"https://www.amazon.com/Best-Sellers-Industrial-Scientific/zgbs/industrial/ref=zg_bs_pg_2_industrial?_encoding=UTF8&pg=2",
    "Industrial & Scientific/Next page":"https://www.amazon.com/Best-Sellers-Industrial-Scientific/zgbs/industrial/ref=zg_bs_pg_2_industrial?_encoding=UTF8&pg=2",
    "Kindle Store/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_digital-text_0_1",
    "Kindle Store/Kindle Newsstand":"https://www.amazon.com/Best-Sellers-Kindle-Store-Kindle-Newsstand/zgbs/digital-text/3000678011/ref=zg_bs_nav_digital-text_1",
    "Kindle Store/Kindle Nonfiction Singles":"https://www.amazon.com/Best-Sellers-Kindle-Store-Kindle-Nonfiction-Singles/zgbs/digital-text/5688113011/ref=zg_bs_nav_digital-text_1",
    "Kindle Store/Kindle Short Reads":"https://www.amazon.com/Best-Sellers-Kindle-Store-Kindle-Short-Reads/zgbs/digital-text/8584457011/ref=zg_bs_nav_digital-text_1",
    "Kindle Store/Kindle Singles":"https://www.amazon.com/Best-Sellers-Kindle-Store-Kindle-Singles/zgbs/digital-text/2486013011/ref=zg_bs_nav_digital-text_1",
    "Kindle Store/Kindle eBooks":"https://www.amazon.com/Best-Sellers-Kindle-Store-Kindle-eBooks/zgbs/digital-text/154606011/ref=zg_bs_nav_digital-text_1",
    "Kindle Store/Prime Reading":"https://www.amazon.com/Best-Sellers-Kindle-Store-Prime-Reading/zgbs/digital-text/15195176011/ref=zg_bs_nav_digital-text_1",
    "Kindle Store/Whispersync for Voice":"https://www.amazon.com/Best-Sellers-Kindle-Store-Whispersync-for-Voice/zgbs/digital-text/5744819011/ref=zg_bs_nav_digital-text_1",
    "Kindle Store/Top 100 Free":"https://www.amazon.com/gp/bestsellers/digital-text/ref=zg_bs?ie=UTF8&tf=1",
    "Kindle Store/1":"https://www.amazon.com/Best-Sellers-Kindle-Store/zgbs/digital-text/ref=zg_bs_pg_1_digital-text?_encoding=UTF8&pg=1",
    "Kindle Store/2":"https://www.amazon.com/Best-Sellers-Kindle-Store/zgbs/digital-text/ref=zg_bs_pg_2_digital-text?_encoding=UTF8&pg=2",
    "Kindle Store/Next page":"https://www.amazon.com/Best-Sellers-Kindle-Store/zgbs/digital-text/ref=zg_bs_pg_2_digital-text?_encoding=UTF8&pg=2",
    "Kitchen & Dining/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_kitchen_0_1",
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
    "Kitchen & Dining/1":"https://www.amazon.com/Best-Sellers-Kitchen-Dining/zgbs/kitchen/ref=zg_bs_pg_1_kitchen?_encoding=UTF8&pg=1",
    "Kitchen & Dining/2":"https://www.amazon.com/Best-Sellers-Kitchen-Dining/zgbs/kitchen/ref=zg_bs_pg_2_kitchen?_encoding=UTF8&pg=2",
    "Kitchen & Dining/Next page":"https://www.amazon.com/Best-Sellers-Kitchen-Dining/zgbs/kitchen/ref=zg_bs_pg_2_kitchen?_encoding=UTF8&pg=2",
    "Movies & TV/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_movies-tv_0_1",
    "Movies & TV/Blu-ray":"https://www.amazon.com/Best-Sellers-Movies-TV-Blu-ray/zgbs/movies-tv/2958935011/ref=zg_bs_nav_movies-tv_1",
    "Movies & TV/DVD":"https://www.amazon.com/Best-Sellers-Movies-TV-DVD/zgbs/movies-tv/2958934011/ref=zg_bs_nav_movies-tv_1",
    "Movies & TV/Prime Video":"https://www.amazon.com/Best-Sellers-Movies-TV-Prime-Video/zgbs/movies-tv/2958933011/ref=zg_bs_nav_movies-tv_1",
    "Movies & TV/1":"https://www.amazon.com/best-sellers-movies-TV-DVD-Blu-ray/zgbs/movies-tv/ref=zg_bs_pg_1_movies-tv?_encoding=UTF8&pg=1",
    "Movies & TV/2":"https://www.amazon.com/best-sellers-movies-TV-DVD-Blu-ray/zgbs/movies-tv/ref=zg_bs_pg_2_movies-tv?_encoding=UTF8&pg=2",
    "Movies & TV/Next page":"https://www.amazon.com/best-sellers-movies-TV-DVD-Blu-ray/zgbs/movies-tv/ref=zg_bs_pg_2_movies-tv?_encoding=UTF8&pg=2",
    "Musical Instruments/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_musical-instruments_0_1",
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
    "Musical Instruments/1":"https://www.amazon.com/Best-Sellers-Musical-Instruments/zgbs/musical-instruments/ref=zg_bs_pg_1_musical-instruments?_encoding=UTF8&pg=1",
    "Musical Instruments/2":"https://www.amazon.com/Best-Sellers-Musical-Instruments/zgbs/musical-instruments/ref=zg_bs_pg_2_musical-instruments?_encoding=UTF8&pg=2",
    "Musical Instruments/Next page":"https://www.amazon.com/Best-Sellers-Musical-Instruments/zgbs/musical-instruments/ref=zg_bs_pg_2_musical-instruments?_encoding=UTF8&pg=2",
    "Office Products/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_office-products_0_1",
    "Office Products/Education & Crafts":"https://www.amazon.com/Best-Sellers-Office-Products-Education-Supplies-Craft-Supplies/zgbs/office-products/12899801/ref=zg_bs_nav_office-products_1",
    "Office Products/Envelopes, Mailers & Shipping Supplies":"https://www.amazon.com/Best-Sellers-Office-Products-Mail-Supplies-Shipping-Supplies/zgbs/office-products/1068972/ref=zg_bs_nav_office-products_1",
    "Office Products/Office Electronics":"https://www.amazon.com/Best-Sellers-Office-Products-Office-Electronics-Products/zgbs/office-products/172574/ref=zg_bs_nav_office-products_1",
    "Office Products/Office Furniture & Accessories":"https://www.amazon.com/Best-Sellers-Office-Products-Office-Furniture-Lighting/zgbs/office-products/1069102/ref=zg_bs_nav_office-products_1",
    "Office Products/Office Lighting":"https://www.amazon.com/Best-Sellers-Office-Products-Office-Lighting/zgbs/office-products/1068956/ref=zg_bs_nav_office-products_1",
    "Office Products/Office Supplies":"https://www.amazon.com/Best-Sellers-Office-Products-Office-School-Supplies/zgbs/office-products/1069242/ref=zg_bs_nav_office-products_1",
    "Office Products/Presentation Boards":"https://www.amazon.com/Best-Sellers-Office-Products-Presentation-Supplies/zgbs/office-products/1069254/ref=zg_bs_nav_office-products_1",
    "Office Products/1":"https://www.amazon.com/Best-Sellers-Office-Products/zgbs/office-products/ref=zg_bs_pg_1_office-products?_encoding=UTF8&pg=1",
    "Office Products/2":"https://www.amazon.com/Best-Sellers-Office-Products/zgbs/office-products/ref=zg_bs_pg_2_office-products?_encoding=UTF8&pg=2",
    "Office Products/Next page":"https://www.amazon.com/Best-Sellers-Office-Products/zgbs/office-products/ref=zg_bs_pg_2_office-products?_encoding=UTF8&pg=2",
    "Patio, Lawn & Garden/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_lawn-garden_0_1",
    "Patio, Lawn & Garden/Backyard Birding & Wildlife":"https://www.amazon.com/Best-Sellers-Patio-Lawn-Garden-Backyard-Birding-Wildlife/zgbs/lawn-garden/553632/ref=zg_bs_nav_lawn-garden_1",
    "Patio, Lawn & Garden/Farm & Ranch":"https://www.amazon.com/Best-Sellers-Patio-Lawn-Garden-Farm-Ranch/zgbs/lawn-garden/4619352011/ref=zg_bs_nav_lawn-garden_1",
    "Patio, Lawn & Garden/Gardening":"https://www.amazon.com/Best-Sellers-Patio-Lawn-Garden-Gardening-Lawn-Care/zgbs/lawn-garden/3610851/ref=zg_bs_nav_lawn-garden_1",
    "Patio, Lawn & Garden/Generators & Portable Power":"https://www.amazon.com/Best-Sellers-Patio-Lawn-Garden-Outdoor-Generators-Portable-Power/zgbs/lawn-garden/552808/ref=zg_bs_nav_lawn-garden_1",
    "Patio, Lawn & Garden/Grills & Outdoor Cooking":"https://www.amazon.com/Best-Sellers-Patio-Lawn-Garden-Outdoor-Cooking/zgbs/lawn-garden/553760/ref=zg_bs_nav_lawn-garden_1",
    "Patio, Lawn & Garden/Mowers & Outdoor Power Tools":"https://www.amazon.com/Best-Sellers-Patio-Lawn-Garden-Outdoor-Power-Lawn-Equipment/zgbs/lawn-garden/551242/ref=zg_bs_nav_lawn-garden_1",
    "Patio, Lawn & Garden/Outdoor Décor":"https://www.amazon.com/Best-Sellers-Patio-Lawn-Garden-Outdoor-Dcor/zgbs/lawn-garden/553788/ref=zg_bs_nav_lawn-garden_1",
    "Patio, Lawn & Garden/Outdoor Heating":"https://www.amazon.com/Best-Sellers-Patio-Lawn-Garden-Outdoor-Heating-Cooling/zgbs/lawn-garden/13638732011/ref=zg_bs_nav_lawn-garden_1",
    "Patio, Lawn & Garden/Outdoor Storage":"https://www.amazon.com/Best-Sellers-Patio-Lawn-Garden-Outdoor-Storage-Housing/zgbs/lawn-garden/13400641/ref=zg_bs_nav_lawn-garden_1",
    "Patio, Lawn & Garden/Patio Furniture & Accessories":"https://www.amazon.com/Best-Sellers-Patio-Lawn-Garden-Patio-Furniture-Accessories/zgbs/lawn-garden/553824/ref=zg_bs_nav_lawn-garden_1",
    "Patio, Lawn & Garden/Pest Control":"https://www.amazon.com/Best-Sellers-Patio-Lawn-Garden-Pest-Control-Products/zgbs/lawn-garden/553844/ref=zg_bs_nav_lawn-garden_1",
    "Patio, Lawn & Garden/Pools, Hot Tubs & Supplies":"https://www.amazon.com/Best-Sellers-Patio-Lawn-Garden-Pools-Hot-Tubs-Supplies/zgbs/lawn-garden/1272941011/ref=zg_bs_nav_lawn-garden_1",
    "Patio, Lawn & Garden/Snow Removal":"https://www.amazon.com/Best-Sellers-Patio-Lawn-Garden-Snow-Removal-Tools/zgbs/lawn-garden/3043471/ref=zg_bs_nav_lawn-garden_1",
    "Patio, Lawn & Garden/1":"https://www.amazon.com/Best-Sellers-Patio-Lawn-Garden/zgbs/lawn-garden/ref=zg_bs_pg_1_lawn-garden?_encoding=UTF8&pg=1",
    "Patio, Lawn & Garden/2":"https://www.amazon.com/Best-Sellers-Patio-Lawn-Garden/zgbs/lawn-garden/ref=zg_bs_pg_2_lawn-garden?_encoding=UTF8&pg=2",
    "Patio, Lawn & Garden/Next page":"https://www.amazon.com/Best-Sellers-Patio-Lawn-Garden/zgbs/lawn-garden/ref=zg_bs_pg_2_lawn-garden?_encoding=UTF8&pg=2",
    "Pet Supplies/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_pet-supplies_0_1",
    "Pet Supplies/Birds":"https://www.amazon.com/Best-Sellers-Pet-Supplies-Pet-Bird-Supplies/zgbs/pet-supplies/2975221011/ref=zg_bs_nav_pet-supplies_1",
    "Pet Supplies/Cats":"https://www.amazon.com/Best-Sellers-Pet-Supplies-Cat-Supplies/zgbs/pet-supplies/2975241011/ref=zg_bs_nav_pet-supplies_1",
    "Pet Supplies/Dogs":"https://www.amazon.com/Best-Sellers-Pet-Supplies-Dog-Supplies/zgbs/pet-supplies/2975312011/ref=zg_bs_nav_pet-supplies_1",
    "Pet Supplies/Fish & Aquatic Pets":"https://www.amazon.com/Best-Sellers-Pet-Supplies-Fish-Aquatic-Pets/zgbs/pet-supplies/2975446011/ref=zg_bs_nav_pet-supplies_1",
    "Pet Supplies/Horses":"https://www.amazon.com/Best-Sellers-Pet-Supplies-Horse-Supplies/zgbs/pet-supplies/2975481011/ref=zg_bs_nav_pet-supplies_1",
    "Pet Supplies/Reptiles & Amphibians":"https://www.amazon.com/Best-Sellers-Pet-Supplies-Reptiles-Amphibian-Supplies/zgbs/pet-supplies/2975504011/ref=zg_bs_nav_pet-supplies_1",
    "Pet Supplies/Small Animals":"https://www.amazon.com/Best-Sellers-Pet-Supplies-Small-Animal-Supplies/zgbs/pet-supplies/2975520011/ref=zg_bs_nav_pet-supplies_1",
    "Pet Supplies/1":"https://www.amazon.com/Best-Sellers-Pet-Supplies/zgbs/pet-supplies/ref=zg_bs_pg_1_pet-supplies?_encoding=UTF8&pg=1",
    "Pet Supplies/2":"https://www.amazon.com/Best-Sellers-Pet-Supplies/zgbs/pet-supplies/ref=zg_bs_pg_2_pet-supplies?_encoding=UTF8&pg=2",
    "Pet Supplies/Next page":"https://www.amazon.com/Best-Sellers-Pet-Supplies/zgbs/pet-supplies/ref=zg_bs_pg_2_pet-supplies?_encoding=UTF8&pg=2",
    "Software/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_software_0_1",
    "Software/Accounting & Finance":"https://www.amazon.com/Best-Sellers-Software-Accounting-Finance/zgbs/software/5223260011/ref=zg_bs_nav_software_1",
    "Software/Antivirus & Security":"https://www.amazon.com/Best-Sellers-Software-Antivirus-Security/zgbs/software/229677/ref=zg_bs_nav_software_1",
    "Software/Business & Office":"https://www.amazon.com/Best-Sellers-Software-Business-Office/zgbs/software/229535/ref=zg_bs_nav_software_1",
    "Software/Children's Software":"https://www.amazon.com/Best-Sellers-Software-Childrens-Software/zgbs/software/229548/ref=zg_bs_nav_software_1",
    "Software/Design & Illustration":"https://www.amazon.com/Best-Sellers-Software-Photography-Graphic-Design/zgbs/software/229614/ref=zg_bs_nav_software_1",
    "Software/Education & Reference":"https://www.amazon.com/Best-Sellers-Software-Education-Reference/zgbs/software/229563/ref=zg_bs_nav_software_1",
    "Software/Lifestyle & Hobbies":"https://www.amazon.com/Best-Sellers-Software-Home-Hobbies/zgbs/software/229624/ref=zg_bs_nav_software_1",
    "Software/Mac Software":"https://www.amazon.com/Best-Sellers-Software-Mac-Software/zgbs/software/120225784011/ref=zg_bs_nav_software_1",
    "Software/Music":"https://www.amazon.com/Best-Sellers-Software-Music/zgbs/software/497022/ref=zg_bs_nav_software_1",
    "Software/Networking & Servers":"https://www.amazon.com/Best-Sellers-Software-Networking-Servers/zgbs/software/229637/ref=zg_bs_nav_software_1",
    "Software/Operating Systems":"https://www.amazon.com/Best-Sellers-Software-Operating-Systems/zgbs/software/229653/ref=zg_bs_nav_software_1",
    "Software/Photography":"https://www.amazon.com/Best-Sellers-Software-Photography/zgbs/software/229621/ref=zg_bs_nav_software_1",
    "Software/Programming & Web Development":"https://www.amazon.com/Best-Sellers-Software-Programming-Web-Development/zgbs/software/5223262011/ref=zg_bs_nav_software_1",
    "Software/Tax Preparation":"https://www.amazon.com/Best-Sellers-Software-Tax-Preparation/zgbs/software/229545/ref=zg_bs_nav_software_1",
    "Software/Utilities":"https://www.amazon.com/Best-Sellers-Software-Utilities/zgbs/software/229672/ref=zg_bs_nav_software_1",
    "Software/Video":"https://www.amazon.com/Best-Sellers-Software-Digital-Video/zgbs/software/290542/ref=zg_bs_nav_software_1",
    "Software/1":"https://www.amazon.com/best-sellers-software/zgbs/software/ref=zg_bs_pg_1_software?_encoding=UTF8&pg=1",
    "Software/2":"https://www.amazon.com/best-sellers-software/zgbs/software/ref=zg_bs_pg_2_software?_encoding=UTF8&pg=2",
    "Software/Next page":"https://www.amazon.com/best-sellers-software/zgbs/software/ref=zg_bs_pg_2_software?_encoding=UTF8&pg=2",
    "Sports & Outdoors/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_sporting-goods_0_1",
    "Sports & Outdoors/Accessories":"https://www.amazon.com/Best-Sellers-Sports-Outdoors-Sports-Outdoor-Recreation-Accessories/zgbs/sporting-goods/3394801/ref=zg_bs_nav_sporting-goods_1",
    "Sports & Outdoors/Exercise & Fitness":"https://www.amazon.com/Best-Sellers-Sports-Outdoors-Exercise-Fitness-Equipment/zgbs/sporting-goods/3407731/ref=zg_bs_nav_sporting-goods_1",
    "Sports & Outdoors/Fan Shop":"https://www.amazon.com/Best-Sellers-Sports-Outdoors-Sports-Fan-Shop/zgbs/sporting-goods/3386071/ref=zg_bs_nav_sporting-goods_1",
    "Sports & Outdoors/Hunting & Fishing":"https://www.amazon.com/Best-Sellers-Sports-Outdoors-Hunting-Fishing-Products/zgbs/sporting-goods/706813011/ref=zg_bs_nav_sporting-goods_1",
    "Sports & Outdoors/Memorabilia Display & Storage":"https://www.amazon.com/Best-Sellers-Sports-Outdoors-Memorabilia-Display-Storage/zgbs/sporting-goods/2358921011/ref=zg_bs_nav_sporting-goods_1",
    "Sports & Outdoors/Outdoor Recreation":"https://www.amazon.com/Best-Sellers-Sports-Outdoors-Outdoor-Recreation/zgbs/sporting-goods/706814011/ref=zg_bs_nav_sporting-goods_1",
    "Sports & Outdoors/Sports":"https://www.amazon.com/Best-Sellers-Sports-Outdoors-Sports-Apparel-Equipment/zgbs/sporting-goods/10971181011/ref=zg_bs_nav_sporting-goods_1",
    "Sports & Outdoors/Sports Medicine":"https://www.amazon.com/Best-Sellers-Sports-Outdoors-Sports-Medicine-Products/zgbs/sporting-goods/3422351/ref=zg_bs_nav_sporting-goods_1",
    "Sports & Outdoors/1":"https://www.amazon.com/Best-Sellers-Sports-Outdoors/zgbs/sporting-goods/ref=zg_bs_pg_1_sporting-goods?_encoding=UTF8&pg=1",
    "Sports & Outdoors/2":"https://www.amazon.com/Best-Sellers-Sports-Outdoors/zgbs/sporting-goods/ref=zg_bs_pg_2_sporting-goods?_encoding=UTF8&pg=2",
    "Sports & Outdoors/Next page":"https://www.amazon.com/Best-Sellers-Sports-Outdoors/zgbs/sporting-goods/ref=zg_bs_pg_2_sporting-goods?_encoding=UTF8&pg=2",
    "Sports Collectibles/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_sports-collectibles_0_1",
    "Sports Collectibles/Balls":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Balls/zgbs/sports-collectibles/3311044011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Baseball Bases":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Baseball-Bases/zgbs/sports-collectibles/5395827011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Bats":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Bats/zgbs/sports-collectibles/3311045011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Bobbleheads":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Bobbleheads/zgbs/sports-collectibles/3311046011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Clothing & Uniforms":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Clothing-Uniforms/zgbs/sports-collectibles/7702506011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Cut Signatures":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Memorabilia-Cut-Signatures/zgbs/sports-collectibles/5931158011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Diecast Cars":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Diecast-Cars/zgbs/sports-collectibles/7702514011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Figurines":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Figurines/zgbs/sports-collectibles/7702516011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Flags & Banners":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Flags-Banners/zgbs/sports-collectibles/3311048011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Gloves":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Gloves/zgbs/sports-collectibles/3311051011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Golf Clubs":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Golf-Clubs/zgbs/sports-collectibles/3311052011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Hats":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Hats/zgbs/sports-collectibles/3311053011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Helmets":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Helmets/zgbs/sports-collectibles/3311054011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Hockey Pucks":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Hockey-Pucks/zgbs/sports-collectibles/3311057011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Hockey Sticks & Blades":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Hockey-Sticks-Blades/zgbs/sports-collectibles/3311058011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Jerseys":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Jerseys/zgbs/sports-collectibles/3311061011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Lineup Cards":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Lineup-Cards/zgbs/sports-collectibles/5395826011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Magazines":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Magazines/zgbs/sports-collectibles/3311062011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Personal Checks":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Personal-Checks/zgbs/sports-collectibles/5395829011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Photographs":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Photographs/zgbs/sports-collectibles/3311063011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Postcards & Index Cards":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Postcards-Index-Cards/zgbs/sports-collectibles/3311064011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Prints & Posters":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Prints-Posters/zgbs/sports-collectibles/3311067011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Publications & Media":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Publications-Media/zgbs/sports-collectibles/7702507011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Shoes":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Shoes/zgbs/sports-collectibles/3311068011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Stadium Components":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Stadium-Components/zgbs/sports-collectibles/5395825011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Ticket Stubs":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Ticket-Stubs/zgbs/sports-collectibles/3311069011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Trading Cards":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Collectible-Sports-Trading-Cards/zgbs/sports-collectibles/3311070011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/Trophies":"https://www.amazon.com/Best-Sellers-Sports-Collectibles-Sports-Collectible-Trophies/zgbs/sports-collectibles/5395823011/ref=zg_bs_nav_sports-collectibles_1",
    "Sports Collectibles/1":"https://www.amazon.com/Best-Sellers-Sports-Collectibles/zgbs/sports-collectibles/ref=zg_bs_pg_1_sports-collectibles?_encoding=UTF8&pg=1",
    "Sports Collectibles/2":"https://www.amazon.com/Best-Sellers-Sports-Collectibles/zgbs/sports-collectibles/ref=zg_bs_pg_2_sports-collectibles?_encoding=UTF8&pg=2",
    "Sports Collectibles/Next page":"https://www.amazon.com/Best-Sellers-Sports-Collectibles/zgbs/sports-collectibles/ref=zg_bs_pg_2_sports-collectibles?_encoding=UTF8&pg=2",
    "Tools & Home Improvement/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_hi_0_1",
    "Tools & Home Improvement/Air Tools":"https://www.amazon.com/Best-Sellers-Tools-Home-Improvement-Air-Powered-Tools/zgbs/hi/120225786011/ref=zg_bs_nav_hi_1",
    "Tools & Home Improvement/Building Supplies":"https://www.amazon.com/Best-Sellers-Tools-Home-Improvement-Building-Supplies/zgbs/hi/551240/ref=zg_bs_nav_hi_1",
    "Tools & Home Improvement/Electrical":"https://www.amazon.com/Best-Sellers-Tools-Home-Improvement-Electrical-Equipment/zgbs/hi/495266/ref=zg_bs_nav_hi_1",
    "Tools & Home Improvement/Hardware":"https://www.amazon.com/Best-Sellers-Tools-Home-Improvement-Hardware/zgbs/hi/511228/ref=zg_bs_nav_hi_1",
    "Tools & Home Improvement/Kitchen & Bath Fixtures":"https://www.amazon.com/Best-Sellers-Tools-Home-Improvement-Kitchen-Bath-Fixtures/zgbs/hi/3754161/ref=zg_bs_nav_hi_1",
    "Tools & Home Improvement/Lighting & Ceiling Fans":"https://www.amazon.com/Best-Sellers-Tools-Home-Improvement-Lighting-Ceiling-Fans/zgbs/hi/495224/ref=zg_bs_nav_hi_1",
    "Tools & Home Improvement/Measuring & Layout Tools":"https://www.amazon.com/Best-Sellers-Tools-Home-Improvement-Measuring-Layout/zgbs/hi/553244/ref=zg_bs_nav_hi_1",
    "Tools & Home Improvement/Paint, Wall Treatments & Supplies":"https://www.amazon.com/Best-Sellers-Tools-Home-Improvement-Paint-Wall-Treatments-Supplies/zgbs/hi/228899/ref=zg_bs_nav_hi_1",
    "Tools & Home Improvement/Plumbing":"https://www.amazon.com/Best-Sellers-Tools-Home-Improvement-Pumps-Plumbing-Equipment/zgbs/hi/13749581/ref=zg_bs_nav_hi_1",
    "Tools & Home Improvement/Power & Hand Tools":"https://www.amazon.com/Best-Sellers-Tools-Home-Improvement-Power-Tools-Hand-Tools/zgbs/hi/328182011/ref=zg_bs_nav_hi_1",
    "Tools & Home Improvement/Safety & Security":"https://www.amazon.com/Best-Sellers-Tools-Home-Improvement-Safety-Security/zgbs/hi/3180231/ref=zg_bs_nav_hi_1",
    "Tools & Home Improvement/Storage & Home Organization":"https://www.amazon.com/Best-Sellers-Tools-Home-Improvement-Home-Storage-Organization/zgbs/hi/13400631/ref=zg_bs_nav_hi_1",
    "Tools & Home Improvement/1":"https://www.amazon.com/Best-Sellers-Tools-Home-Improvement/zgbs/hi/ref=zg_bs_pg_1_hi?_encoding=UTF8&pg=1",
    "Tools & Home Improvement/2":"https://www.amazon.com/Best-Sellers-Tools-Home-Improvement/zgbs/hi/ref=zg_bs_pg_2_hi?_encoding=UTF8&pg=2",
    "Tools & Home Improvement/Next page":"https://www.amazon.com/Best-Sellers-Tools-Home-Improvement/zgbs/hi/ref=zg_bs_pg_2_hi?_encoding=UTF8&pg=2",
    "Toys & Games/Shop Best Selling Toys":"https://www.amazon.com/gp/bestsellers/toys-and-games/?ie=UTF8&ie=UTF8&ref_=sv_t_2",
    "Toys & Games/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_toys-and-games_0_1",
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
    "Toys & Games/1":"https://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games/ref=zg_bs_pg_1_toys-and-games?_encoding=UTF8&pg=1",
    "Toys & Games/2":"https://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games/ref=zg_bs_pg_2_toys-and-games?_encoding=UTF8&pg=2",
    "Toys & Games/Next page":"https://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games/ref=zg_bs_pg_2_toys-and-games?_encoding=UTF8&pg=2",
    "Unique Finds/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_boost_0_2",
    "Video Games/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_videogames_0_1",
    "Video Games/Mac Games":"https://www.amazon.com/Best-Sellers-Video-Games-Mac-Games-Accessories/zgbs/videogames/229647/ref=zg_bs_nav_videogames_1",
    "Video Games/Microconsoles":"https://www.amazon.com/Best-Sellers-Video-Games-Microconsoles/zgbs/videogames/19497043011/ref=zg_bs_nav_videogames_1",
    "Video Games/More Systems":"https://www.amazon.com/Best-Sellers-Video-Games-Legacy-Systems/zgbs/videogames/294940/ref=zg_bs_nav_videogames_1",
    "Video Games/Nintendo 3DS & 2DS":"https://www.amazon.com/Best-Sellers-Video-Games-Nintendo-3DS-2DS-Consoles-Games-Accessories/zgbs/videogames/2622269011/ref=zg_bs_nav_videogames_1",
    "Video Games/Nintendo DS":"https://www.amazon.com/Best-Sellers-Video-Games-Nintendo-DS-Games-Consoles-Accessories/zgbs/videogames/11075831/ref=zg_bs_nav_videogames_1",
    "Video Games/Nintendo Switch":"https://www.amazon.com/Best-Sellers-Video-Games-Nintendo-Switch-Consoles-Games-Accessories/zgbs/videogames/16227128011/ref=zg_bs_nav_videogames_1",
    "Video Games/Nintendo Switch 2":"https://www.amazon.com/Best-Sellers-Video-Games-Nintendo-Switch-2-Consoles-Games-Accessories/zgbs/videogames/206234609011/ref=zg_bs_nav_videogames_1",
    "Video Games/PC Games":"https://www.amazon.com/Best-Sellers-Video-Games-PC-Games-Accessories/zgbs/videogames/229575/ref=zg_bs_nav_videogames_1",
    "Video Games/PlayStation 3":"https://www.amazon.com/Best-Sellers-Video-Games-PlayStation-3-Games-Consoles-Accessories/zgbs/videogames/14210751/ref=zg_bs_nav_videogames_1",
    "Video Games/PlayStation 4":"https://www.amazon.com/Best-Sellers-Video-Games-PlayStation-4-Games-Consoles-Accessories/zgbs/videogames/6427814011/ref=zg_bs_nav_videogames_1",
    "Video Games/PlayStation 5":"https://www.amazon.com/Best-Sellers-Video-Games-PlayStation-5-Consoles-Games-Accessories/zgbs/videogames/20972781011/ref=zg_bs_nav_videogames_1",
    "Video Games/PlayStation Vita":"https://www.amazon.com/Best-Sellers-Video-Games-PlayStation-Vita-Games-Consoles-Accessories/zgbs/videogames/3010556011/ref=zg_bs_nav_videogames_1",
    "Video Games/Sony PSP":"https://www.amazon.com/Best-Sellers-Video-Games-Sony-PSP-Games-Consoles-Accessories/zgbs/videogames/11075221/ref=zg_bs_nav_videogames_1",
    "Video Games/Virtual Reality":"https://www.amazon.com/Best-Sellers-Video-Games-Virtual-Reality-Hardware-Accessories/zgbs/videogames/21479453011/ref=zg_bs_nav_videogames_1",
    "Video Games/Wii":"https://www.amazon.com/Best-Sellers-Video-Games-Wii-Games-Consoles-Accessories/zgbs/videogames/14218901/ref=zg_bs_nav_videogames_1",
    "Video Games/Wii U":"https://www.amazon.com/Best-Sellers-Video-Games-Wii-U-Games-Consoles-Accessories/zgbs/videogames/3075112011/ref=zg_bs_nav_videogames_1",
    "Video Games/Xbox 360":"https://www.amazon.com/Best-Sellers-Video-Games-Xbox-360-Games-Consoles-Accessories/zgbs/videogames/14220161/ref=zg_bs_nav_videogames_1",
    "Video Games/Xbox One":"https://www.amazon.com/Best-Sellers-Video-Games-Xbox-One-Games-Consoles-Accessories/zgbs/videogames/6469269011/ref=zg_bs_nav_videogames_1",
    "Video Games/Xbox Series X":"https://www.amazon.com/Best-Sellers-Video-Games-Xbox-Series-X-S-Consoles-Games-Accessories/zgbs/videogames/20972798011/ref=zg_bs_nav_videogames_1",
    "Video Games/1":"https://www.amazon.com/best-sellers-video-games/zgbs/videogames/ref=zg_bs_pg_1_videogames?_encoding=UTF8&pg=1",
    "Video Games/2":"https://www.amazon.com/best-sellers-video-games/zgbs/videogames/ref=zg_bs_pg_2_videogames?_encoding=UTF8&pg=2",
    "Video Games/Next page":"https://www.amazon.com/best-sellers-video-games/zgbs/videogames/ref=zg_bs_pg_2_videogames?_encoding=UTF8&pg=2",
    "See More/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_beauty_0_1",
    "See More/Foot, Hand & Nail Care":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care-Foot-Hand-Nail-Care-Products/zgbs/beauty/17242866011/ref=zg_bs_nav_beauty_1",
    "See More/Fragrance":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care-Perfumes-Fragrances/zgbs/beauty/11056591/ref=zg_bs_nav_beauty_1",
    "See More/Gift Sets":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care-Beauty-Gift-Sets/zgbs/beauty/120225719011/ref=zg_bs_nav_beauty_1",
    "See More/Hair Care":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care-Hair-Care-Products/zgbs/beauty/11057241/ref=zg_bs_nav_beauty_1",
    "See More/Makeup":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care-Makeup/zgbs/beauty/11058281/ref=zg_bs_nav_beauty_1",
    "See More/Personal Care":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care-Personal-Care-Products/zgbs/beauty/3777891/ref=zg_bs_nav_beauty_1",
    "See More/Salon & Spa Equipment":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care-Salon-Spa-Equipment/zgbs/beauty/15144566011/ref=zg_bs_nav_beauty_1",
    "See More/Shave & Hair Removal":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care-Shaving-Hair-Removal-Products/zgbs/beauty/3778591/ref=zg_bs_nav_beauty_1",
    "See More/Skin Care":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care-Skin-Care-Products/zgbs/beauty/11060451/ref=zg_bs_nav_beauty_1",
    "See More/Tools & Accessories":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care-Beauty-Tools-Accessories/zgbs/beauty/11062741/ref=zg_bs_nav_beauty_1",
    "See More/1":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care/zgbs/beauty/ref=zg_bs_pg_1_beauty?_encoding=UTF8&pg=1",
    "See More/2":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care/zgbs/beauty/ref=zg_bs_pg_2_beauty?_encoding=UTF8&pg=2",
    "See More/Next page":"https://www.amazon.com/Best-Sellers-Beauty-Personal-Care/zgbs/beauty/ref=zg_bs_pg_2_beauty?_encoding=UTF8&pg=2",
    "See More/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_electronics_0_1",
    "See More/Accessories & Supplies":"https://www.amazon.com/Best-Sellers-Electronics-Electronics-Accessories-Supplies/zgbs/electronics/281407/ref=zg_bs_nav_electronics_1",
    "See More/Camera & Photo":"https://www.amazon.com/Best-Sellers-Electronics-Camera-Photo-Products/zgbs/electronics/502394/ref=zg_bs_nav_electronics_1",
    "See More/Car Electronics":"https://www.amazon.com/Best-Sellers-Electronics-Car-Electronics/zgbs/electronics/1077068/ref=zg_bs_nav_electronics_1",
    "See More/GPS & Navigation":"https://www.amazon.com/Best-Sellers-Electronics-GPS-Finders-Accessories/zgbs/electronics/172526/ref=zg_bs_nav_electronics_1",
    "See More/Headphones":"https://www.amazon.com/Best-Sellers-Electronics-Headphones-Earbuds/zgbs/electronics/172541/ref=zg_bs_nav_electronics_1",
    "See More/Home Audio & Theater":"https://www.amazon.com/Best-Sellers-Electronics-Home-Audio-Theater-Products/zgbs/electronics/667846011/ref=zg_bs_nav_electronics_1",
    "See More/Marine Electronics":"https://www.amazon.com/Best-Sellers-Electronics-Marine-Electronics/zgbs/electronics/319574011/ref=zg_bs_nav_electronics_1",
    "See More/Office Electronics":"https://www.amazon.com/Best-Sellers-Electronics-Office-Electronics-Products/zgbs/electronics/172574/ref=zg_bs_nav_electronics_1",
    "See More/Portable Audio & Video":"https://www.amazon.com/Best-Sellers-Electronics-Portable-Audio-Video/zgbs/electronics/172623/ref=zg_bs_nav_electronics_1",
    "See More/Security & Surveillance":"https://www.amazon.com/Best-Sellers-Electronics-Security-Surveillance-Equipment/zgbs/electronics/524136/ref=zg_bs_nav_electronics_1",
    "See More/Service & Replacement Plans":"https://www.amazon.com/Best-Sellers-Electronics-Computers-Electronics-Service-Plans/zgbs/electronics/16285901/ref=zg_bs_nav_electronics_1",
    "See More/Televisions & Video":"https://www.amazon.com/Best-Sellers-Electronics-Televisions-Video-Products/zgbs/electronics/1266092011/ref=zg_bs_nav_electronics_1",
    "See More/Video Game Consoles & Accessories":"https://www.amazon.com/Best-Sellers-Electronics-Video-Game-Consoles-Accessories/zgbs/electronics/7926841011/ref=zg_bs_nav_electronics_1",
    "See More/Video Projectors":"https://www.amazon.com/Best-Sellers-Electronics-Video-Projectors/zgbs/electronics/300334/ref=zg_bs_nav_electronics_1",
    "See More/Wearable Technology":"https://www.amazon.com/Best-Sellers-Electronics-Wearable-Technology/zgbs/electronics/10048700011/ref=zg_bs_nav_electronics_1",
    "See More/eBook Readers & Accessories":"https://www.amazon.com/Best-Sellers-Electronics-eBook-Readers-Accessories/zgbs/electronics/2642125011/ref=zg_bs_nav_electronics_1",
    "See More/1":"https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/ref=zg_bs_pg_1_electronics?_encoding=UTF8&pg=1",
    "See More/2":"https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/ref=zg_bs_pg_2_electronics?_encoding=UTF8&pg=2",
    "See More/Next page":"https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/ref=zg_bs_pg_2_electronics?_encoding=UTF8&pg=2",
    "See More/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_fashion_0_1",
    "See More/Boys":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Boys-Fashion/zgbs/fashion/7147443011/ref=zg_bs_nav_fashion_1",
    "See More/Costumes & Accessories":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Costumes-Accessories/zgbs/fashion/7586165011/ref=zg_bs_nav_fashion_1",
    "See More/Girls":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Girls-Fashion/zgbs/fashion/7147442011/ref=zg_bs_nav_fashion_1",
    "See More/Luggage & Travel Gear":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Luggage-Travel-Gear/zgbs/fashion/9479199011/ref=zg_bs_nav_fashion_1",
    "See More/Men":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Fashion/zgbs/fashion/7147441011/ref=zg_bs_nav_fashion_1",
    "See More/Novelty & More":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Novelty-More/zgbs/fashion/7147445011/ref=zg_bs_nav_fashion_1",
    "See More/Shoe, Jewelry & Watch Accessories":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Shoe-Jewelry-Watch-Accessories/zgbs/fashion/7586146011/ref=zg_bs_nav_fashion_1",
    "See More/Sport Specific Clothing":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Sport-Specific-Clothing/zgbs/fashion/23575629011/ref=zg_bs_nav_fashion_1",
    "See More/Uniforms, Work & Safety":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Uniforms-Work-Safety/zgbs/fashion/7586144011/ref=zg_bs_nav_fashion_1",
    "See More/Women":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Womens-Fashion/zgbs/fashion/7147440011/ref=zg_bs_nav_fashion_1",
    "See More/1":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry/zgbs/fashion/ref=zg_bs_pg_1_fashion?_encoding=UTF8&pg=1",
    "See More/2":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry/zgbs/fashion/ref=zg_bs_pg_2_fashion?_encoding=UTF8&pg=2",
    "See More/Next page":"https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry/zgbs/fashion/ref=zg_bs_pg_2_fashion?_encoding=UTF8&pg=2",
    "See More/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_kitchen_0_1",
    "See More/Bakeware":"https://www.amazon.com/Best-Sellers-Kitchen-Dining-Bakeware/zgbs/kitchen/289668/ref=zg_bs_nav_kitchen_1",
    "See More/Bar Tools & Drinkware":"https://www.amazon.com/Best-Sellers-Kitchen-Dining-Bar-Tools-Drinkware/zgbs/kitchen/289728/ref=zg_bs_nav_kitchen_1",
    "See More/Coffee, Tea & Espresso Appliances":"https://www.amazon.com/Best-Sellers-Kitchen-Dining-Coffee-Tea-Espresso-Appliances/zgbs/kitchen/289742/ref=zg_bs_nav_kitchen_1",
    "See More/Cookware":"https://www.amazon.com/Best-Sellers-Kitchen-Dining-Kitchen-Cookware/zgbs/kitchen/289814/ref=zg_bs_nav_kitchen_1",
    "See More/Dining & Entertaining":"https://www.amazon.com/Best-Sellers-Kitchen-Dining-Dining-Entertaining/zgbs/kitchen/13162311/ref=zg_bs_nav_kitchen_1",
    "See More/Glassware & Drinkware":"https://www.amazon.com/Best-Sellers-Kitchen-Dining-Glassware-Drinkware/zgbs/kitchen/13217501/ref=zg_bs_nav_kitchen_1",
    "See More/Home Brewing & Wine Making":"https://www.amazon.com/Best-Sellers-Kitchen-Dining-Home-Brewing-Wine-Making/zgbs/kitchen/979832011/ref=zg_bs_nav_kitchen_1",
    "See More/Kitchen & Table Linens":"https://www.amazon.com/Best-Sellers-Kitchen-Dining-Kitchen-Table-Linens/zgbs/kitchen/1063916/ref=zg_bs_nav_kitchen_1",
    "See More/Kitchen Utensils & Gadgets":"https://www.amazon.com/Best-Sellers-Kitchen-Dining-Kitchen-Utensils-Gadgets/zgbs/kitchen/289754/ref=zg_bs_nav_kitchen_1",
    "See More/Small Appliances":"https://www.amazon.com/Best-Sellers-Kitchen-Dining-Kitchen-Small-Appliances/zgbs/kitchen/289913/ref=zg_bs_nav_kitchen_1",
    "See More/Storage & Organization":"https://www.amazon.com/Best-Sellers-Kitchen-Dining-Kitchen-Storage-Organization/zgbs/kitchen/510136/ref=zg_bs_nav_kitchen_1",
    "See More/Wine Accessories":"https://www.amazon.com/Best-Sellers-Kitchen-Dining-Wine-Accessories/zgbs/kitchen/13299291/ref=zg_bs_nav_kitchen_1",
    "See More/1":"https://www.amazon.com/Best-Sellers-Kitchen-Dining/zgbs/kitchen/ref=zg_bs_pg_1_kitchen?_encoding=UTF8&pg=1",
    "See More/2":"https://www.amazon.com/Best-Sellers-Kitchen-Dining/zgbs/kitchen/ref=zg_bs_pg_2_kitchen?_encoding=UTF8&pg=2",
    "See More/Next page":"https://www.amazon.com/Best-Sellers-Kitchen-Dining/zgbs/kitchen/ref=zg_bs_pg_2_kitchen?_encoding=UTF8&pg=2",
    "See More/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_hpc_0_1",
    "See More/Baby & Child Care":"https://www.amazon.com/Best-Sellers-Health-Household-Baby-Child-Care-Products/zgbs/hpc/10787321/ref=zg_bs_nav_hpc_1",
    "See More/Diet & Sports Nutrition":"https://www.amazon.com/Best-Sellers-Health-Household-Diet-Sports-Nutrition/zgbs/hpc/3764441/ref=zg_bs_nav_hpc_1",
    "See More/Health Care":"https://www.amazon.com/Best-Sellers-Health-Household-Health-Care-Products/zgbs/hpc/3760941/ref=zg_bs_nav_hpc_1",
    "See More/House Supplies":"https://www.amazon.com/Best-Sellers-Health-Household-Household-Supplies/zgbs/hpc/15342811/ref=zg_bs_nav_hpc_1",
    "See More/Medical Supplies & Equipment":"https://www.amazon.com/Best-Sellers-Health-Household-Home-Use-Medical-Supplies-Equipment/zgbs/hpc/3775161/ref=zg_bs_nav_hpc_1",
    "See More/Oral Care":"https://www.amazon.com/Best-Sellers-Health-Household-Oral-Care-Products/zgbs/hpc/10079992011/ref=zg_bs_nav_hpc_1",
    "See More/Personal Care":"https://www.amazon.com/Best-Sellers-Health-Household-Personal-Care-Products/zgbs/hpc/3777891/ref=zg_bs_nav_hpc_1",
    "See More/Sales & Deals":"https://www.amazon.com/Best-Sellers-Health-Household-Sales-Deals/zgbs/hpc/120225718011/ref=zg_bs_nav_hpc_1",
    "See More/Sexual Wellness":"https://www.amazon.com/Best-Sellers-Health-Household-Sexual-Wellness-Products/zgbs/hpc/3777371/ref=zg_bs_nav_hpc_1",
    "See More/Sports Nutrition":"https://www.amazon.com/Best-Sellers-Health-Household-Sports-Nutrition-Products/zgbs/hpc/6973663011/ref=zg_bs_nav_hpc_1",
    "See More/Stationery & Gift Wrapping Supplies":"https://www.amazon.com/Best-Sellers-Health-Household-Stationery-Gift-Wrapping-Supplies/zgbs/hpc/723418011/ref=zg_bs_nav_hpc_1",
    "See More/Vision Care":"https://www.amazon.com/Best-Sellers-Health-Household-Vision-Products/zgbs/hpc/10079994011/ref=zg_bs_nav_hpc_1",
    "See More/Vitamins, Minerals & Supplements":"https://www.amazon.com/Best-Sellers-Health-Household-Vitamins-Minerals-Supplements/zgbs/hpc/23675621011/ref=zg_bs_nav_hpc_1",
    "See More/Wellness & Relaxation":"https://www.amazon.com/Best-Sellers-Health-Household-Wellness-Relaxation-Products/zgbs/hpc/10079996011/ref=zg_bs_nav_hpc_1",
    "See More/1":"https://www.amazon.com/Best-Sellers-Health-Household/zgbs/hpc/ref=zg_bs_pg_1_hpc?_encoding=UTF8&pg=1",
    "See More/2":"https://www.amazon.com/Best-Sellers-Health-Household/zgbs/hpc/ref=zg_bs_pg_2_hpc?_encoding=UTF8&pg=2",
    "See More/Next page":"https://www.amazon.com/Best-Sellers-Health-Household/zgbs/hpc/ref=zg_bs_pg_2_hpc?_encoding=UTF8&pg=2",
    "See More/Any Department":"https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_photo_0_1",
    "See More/Accessories":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-Camera-Photo-Accessories/zgbs/photo/172435/ref=zg_bs_nav_photo_1",
    "See More/Bags & Cases":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-Camera-Bags-Cases/zgbs/photo/172437/ref=zg_bs_nav_photo_1",
    "See More/Binoculars & Scopes":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-Binoculars-Telescopes-Optics/zgbs/photo/499320/ref=zg_bs_nav_photo_1",
    "See More/Camcorders":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-Camcorders/zgbs/photo/172421/ref=zg_bs_nav_photo_1",
    "See More/DSLR Cameras":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-DSLR-Cameras/zgbs/photo/3017941/ref=zg_bs_nav_photo_1",
    "See More/Digital Picture Frames":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-Digital-Picture-Frames/zgbs/photo/525460/ref=zg_bs_nav_photo_1",
    "See More/Lenses":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-Camcorder-Camera-Lenses/zgbs/photo/499248/ref=zg_bs_nav_photo_1",
    "See More/Point & Shoot Digital Cameras":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-Digital-Point-Shoot-Cameras/zgbs/photo/330405011/ref=zg_bs_nav_photo_1",
    "See More/Surveillance Cameras":"https://www.amazon.com/Best-Sellers-Camera-Photo-Products-Surveillance-Security-Cameras/zgbs/photo/898400/ref=zg_bs_nav_photo_1",
    "See More/1":"https://www.amazon.com/best-sellers-camera-photo/zgbs/photo/ref=zg_bs_pg_1_photo?_encoding=UTF8&pg=1",
    "See More/2":"https://www.amazon.com/best-sellers-camera-photo/zgbs/photo/ref=zg_bs_pg_2_photo?_encoding=UTF8&pg=2",
    "See More/Next page":"https://www.amazon.com/best-sellers-camera-photo/zgbs/photo/ref=zg_bs_pg_2_photo?_encoding=UTF8&pg=2"
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
                    if not dyn_img_attr or len(high_res_urls) >= 7:
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