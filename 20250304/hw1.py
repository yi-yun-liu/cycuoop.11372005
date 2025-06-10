# 台北市公車資訊查詢應用程式主體
import pandas as pd
import requests
import folium
from geopy.geocoders import Nominatim

# 載入資料：路線資料與站牌資料
routes_df = pd.read_csv("C:\\Users\\yiyun1\\Desktop\\cycuoop.11372005\\20250304\\路線資訊20250610.csv")
stops_df = pd.read_csv("C:\\Users\\yiyun1\\Desktop\\cycuoop.11372005\\20250304\\台北市_公車路線_站牌資料.csv")

# ===== TDX 授權取得 access token =====
CLIENT_ID = "s10922162-b260784c-343c-4531"
CLIENT_SECRET = "93293696-25db-4089-9530-8fb8aad95d97"

def get_access_token():
    url = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("無法取得 access token，請檢查授權資訊")
        return None

access_token = get_access_token()
headers = {"Authorization": f"Bearer {access_token}"} if access_token else {}

# 使用者輸入出發站與目的站（皆為中文）
def find_routes(start_stop, end_stop):
    candidates = stops_df.groupby(['RouteUID', 'Direction']).filter(
        lambda x: start_stop in list(x['StopNameZh']) and end_stop in list(x['StopNameZh'])
    )

    results = []
    for (route_uid, direction), group in candidates.groupby(['RouteUID', 'Direction']):
        sorted_stops = group.sort_values('StopSequence')
        stops_list = list(sorted_stops['StopNameZh'])
        if stops_list.index(start_stop) < stops_list.index(end_stop):
            route_name = sorted_stops['RouteNameZh'].iloc[0]
            results.append({
                "RouteUID": route_uid,
                "RouteName": route_name,
                "Direction": direction,
                "Stops": sorted_stops,
                "StartIndex": stops_list.index(start_stop),
                "EndIndex": stops_list.index(end_stop)
            })
    return results

# 顯示即時到站情形
def get_eta(route_uid, direction, stop_name):
    url = f"https://tdx.transportdata.tw/api/basic/v2/Bus/EstimatedTimeOfArrival/City/Taipei/{route_uid}?$format=JSON"
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            data = res.json()
            for entry in data:
                if entry.get("Direction") == direction and entry.get("StopName", {}).get("Zh_tw") == stop_name:
                    seconds = entry.get("EstimateTime")
                    if seconds:
                        return f"預估 {seconds // 60} 分鐘後抵達"
                    else:
                        return "尚無預估時間"
    except:
        return "無法取得即時資料"
    return "查無資料"

# 建立地圖標示站點與路線
def plot_route_map(route):
    geolocator = Nominatim(user_agent="bus_route_mapper")
    m = folium.Map(location=[25.0330, 121.5654], zoom_start=13)
    coords = []
    for i in range(route['StartIndex'], route['EndIndex'] + 1):
        stop_name = route['Stops'].iloc[i]['StopNameZh']
        try:
            location = geolocator.geocode("台北市" + stop_name)
            if location:
                latlon = (location.latitude, location.longitude)
                coords.append(latlon)
                folium.Marker(latlon, popup=stop_name).add_to(m)
        except:
            continue
    if coords:
        folium.PolyLine(coords, color="blue").add_to(m)
        m.save("bus_route_map.html")
        print("✅ 地圖已儲存為 bus_route_map.html，可使用瀏覽器開啟查看")
    else:
        print("⚠️ 無法定位任何站點，地圖無法產生")

# 主程式邏輯
user_start = input("請輸入出發站：")
user_end = input("請輸入目的站：")
routes = find_routes(user_start, user_end)

if not routes:
    print("沒有找到符合條件的公車路線")
else:
    for route in routes:
        print(f"\n公車路線：{route['RouteName']}（方向：{route['Direction']}）")
        print("經過站點與預估到站時間：")
        for i in range(route['StartIndex'], route['EndIndex'] + 1):
            stop = route['Stops'].iloc[i]['StopNameZh']
            eta = get_eta(route['RouteUID'], route['Direction'], stop)
            print(f" - {stop}｜{eta}")
        plot_route_map(route)
        print("------")