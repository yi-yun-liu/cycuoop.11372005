import requests
import csv

def fetch_bus_data(route_id, go_back=0, output_csv="bus_data.csv"):
    url = f"https://ebus.gov.taipei/EBus/VsSimpleMap/GetStopData?rid={route_id}&gb={go_back}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"連線失敗，狀態碼：{response.status_code}")
        return

    try:
        stops_data = response.json()
    except:
        print("資料解析失敗，請檢查 route_id 是否正確")
        return

    data = []
    for i, stop in enumerate(stops_data, 1):
        arrival_time = stop.get("arrtime", "無資料")
        stop_number = i
        stop_name = stop.get("n", "")
        stop_id = stop.get("sid", "")
        lat = stop.get("lat", "")
        lon = stop.get("lng", "")

        data.append([
            arrival_time,
            stop_number,
            stop_name,
            stop_id,
            lat,
            lon
        ])

    # 寫入 CSV 檔案
    with open(output_csv, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["公車到達時間", "車站序號", "車站名稱", "車站編號", "latitude", "longitude"])
        writer.writerows(data)

    print(f"資料成功儲存為 {output_csv}")

# 🧪 範例使用（0100023250 為松山機場路線）
fetch_bus_data("0100023250", go_back=0)


