import requests, json, hashlib, hmac, base64
from datetime import datetime
import pytz

APP_ID = "YOUR_APP_ID"
APP_KEY = "YOUR_APP_KEY"

def get_auth_header():
    gmt = datetime.now(pytz.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
    signature = base64.b64encode(hmac.new(APP_KEY.encode(), f"x-date: {gmt}".encode(), hashlib.sha1).digest()).decode()
    auth = f'hmac username="{APP_ID}", algorithm="hmac-sha1", headers="x-date", signature="{signature}"'
    return {"Authorization": auth, "x-date": gmt, "Accept-Encoding": "gzip"}

def fetch_json(url):
    return requests.get(url, headers=get_auth_header()).json()

# 取得路線清單
routes = fetch_json("https://ptx.transportdata.tw/MOTC/v2/Bus/Route/City/Taipei?$format=JSON")
print(f"共抓到 {len(routes)} 條路線。")

# 取得前 5 條的站序作為示範
for r in routes[:5]:
    route_name = r['RouteName']['Zh_tw']
    stops = fetch_json(f"https://ptx.transportdata.tw/MOTC/v2/Bus/StopOfRoute/City/Taipei/{route_name}?$format=JSON")
    for direction in stops:
        names = [s['StopName']['Zh_tw'] for s in direction['Stops']]
        print(route_name, direction['Direction'], names[:5], "...")

