# 台北市公車資訊查詢應用程式主體
import pandas as pd
import requests
import folium
import tkinter as tk
from tkinter import simpledialog, messagebox
from geopy.geocoders import Nominatim

# ===== 資料載入與設定 =====
routes_df = pd.read_csv("C:\\Users\\yiyun1\\Desktop\\cycuoop.11372005\\20250304\\路線資訊20250610.csv")
stops_df = pd.read_csv("C:\\Users\\yiyun1\\Desktop\\cycuoop.11372005\\20250304\\台北市_公車路線_站牌資料.csv")

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
        return None

access_token = get_access_token()
headers = {"Authorization": f"Bearer {access_token}"} if access_token else {}

# ===== 路線查詢與比對邏輯 =====
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

# ===== 查詢 ETA =====
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

# ===== 使用 TDX API 抓 GPS 並補 geopy =====
def get_stop_gps(route_uid):
    url = f"https://tdx.transportdata.tw/api/basic/v2/Bus/StopOfRoute/City/Taipei/{route_uid}?$format=JSON"
    res = requests.get(url, headers=headers)
    gps_map = {}
    if res.status_code == 200:
        for section in res.json():
            for stop in section.get("Stops", []):
                name = stop.get("StopName", {}).get("Zh_tw")
                position = stop.get("StopPosition", {})
                lat, lon = position.get("PositionLat"), position.get("PositionLon")
                if name and lat and lon:
                    gps_map[name.strip()] = (lat, lon)
    return gps_map

# ===== 即時地圖標示公車位置與站點 =====
def plot_route_map(route):
    gps_data = get_stop_gps(route['RouteUID'])
    geolocator = Nominatim(user_agent="bus_route_mapper")
    m = folium.Map(location=[25.0330, 121.5654], zoom_start=13)
    coords = []
    for i in range(route['StartIndex'], route['EndIndex'] + 1):
        stop_name = route['Stops'].iloc[i]['StopNameZh']
        if stop_name in gps_data:
            latlon = gps_data[stop_name]
        else:
            try:
                location = geolocator.geocode("台北市" + stop_name)
                if location:
                    latlon = (location.latitude, location.longitude)
                    gps_data[stop_name] = latlon  # 補上 geopy 查詢座標
                else:
                    print(f"❌ 找不到 {stop_name} 的座標")
                    continue
            except:
                print(f"⚠️ geopy 查詢 {stop_name} 失敗")
                continue
        coords.append(latlon)
        folium.Marker(latlon, popup=stop_name).add_to(m)
    if coords:
        folium.PolyLine(coords, color="blue").add_to(m)
        m.save("bus_route_map.html")
        print("✅ 地圖已儲存為 bus_route_map.html，可用瀏覽器開啟查看")
    else:
        print("⚠️ 找不到足夠的站點座標，地圖無法產生")

# ===== GUI 主介面 =====
def run_gui():
    root = tk.Tk()
    root.withdraw()
    start = simpledialog.askstring("出發站輸入", "請輸入出發站名稱（中文）")
    end = simpledialog.askstring("目的站輸入", "請輸入目的站名稱（中文）")
    if not start or not end:
        messagebox.showwarning("輸入錯誤", "請正確輸入出發站與目的站")
        return
    routes = find_routes(start, end)
    if not routes:
        messagebox.showinfo("查無資料", "找不到可搭乘的公車路線")
    else:
        output = ""
        for route in routes:
            output += f"\n[公車：{route['RouteName']}（方向：{route['Direction']}）]\n"
            for i in range(route['StartIndex'], route['EndIndex'] + 1):
                stop = route['Stops'].iloc[i]['StopNameZh']
                eta = get_eta(route['RouteUID'], route['Direction'], stop)
                output += f" - {stop}｜{eta}\n"
            plot_route_map(route)
            output += "地圖已產生，請查看 bus_route_map.html\n------\n"
        messagebox.showinfo("查詢結果", output)

# 執行 GUI
run_gui()
