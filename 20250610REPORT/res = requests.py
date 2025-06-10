import requests
import pandas as pd
from datetime import datetime, timedelta

# 使用者提供的 Client ID 與 Secret
client_id = "s10922162-b260784c-343c-4531"
client_secret = "93293696-25db-4089-9530-8fb8aad95d97"

# Step 1: 取得 access token
token_url = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
token_data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret
}

token_response = requests.post(token_url, data=token_data)
access_token = token_response.json().get("access_token")

# Step 2: 使用 access token 取得台北市公車路線的站牌資料
headers = {"Authorization": f"Bearer {access_token}"}
stop_of_route_url = "https://tdx.transportdata.tw/api/basic/v2/Bus/StopOfRoute/City/Taipei?$format=JSON"

response = requests.get(stop_of_route_url, headers=headers)
data = response.json()

# Step 3: 整理資料成 DataFrame 格式
records = []
for route in data:
    route_uid = route.get("RouteUID")
    route_name = route.get("RouteName", {}).get("Zh_tw", "")
    direction = route.get("Direction")
    for stop in route.get("Stops", []):
        stop_name = stop.get("StopName", {}).get("Zh_tw", "")
        stop_uid = stop.get("StopUID", "")
        stop_sequence = stop.get("StopSequence")
        records.append({
            "RouteUID": route_uid,
            "RouteNameZh": route_name,
            "Direction": direction,
            "StopSequence": stop_sequence,
            "StopUID": stop_uid,
            "StopNameZh": stop_name
        })

df_stops = pd.DataFrame(records)

# 儲存資料為 CSV
df_stops.to_csv("台北市_公車路線_站牌資料.csv", index=False, encoding="utf-8-sig")
print("✅ 已儲存為 CSV")
