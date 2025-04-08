import requests
from bs4 import BeautifulSoup
import csv

def fetch_bus_route_data(route_id):
    # 網頁 URL 模板，將路線代碼替換進去
    url = f'https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}'
    
    # 發送 HTTP 請求
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error: Unable to fetch data for route {route_id}")
        return
    
    # 解析 HTML 頁面
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 擷取包含公車站資料的 JSON 格式資料
    script_tag = soup.find('script', text=lambda text: text and 'arrival_info' in text)
    
    if not script_tag:
        print("Error: Unable to find bus data in the page")
        return
    
    # 提取 JSON 資料
    script_content = script_tag.string
    start_idx = script_content.find('[')
    end_idx = script_content.find(']') + 1
    json_data = script_content[start_idx:end_idx]
    
    # 將資料轉換為列表
    import json
    data = json.loads(json_data)
    
    # 整理資料並輸出為 CSV 格式
    csv_data = []
    for stop in data:
        stop_info = {
            'arrival_info': stop.get('arrival_info', ''),
            'stop_number': stop.get('stop_number', ''),
            'stop_name': stop.get('stop_name', ''),
            'stop_id': stop.get('stop_id', ''),
            'latitude': stop.get('latitude', ''),
            'longitude': stop.get('longitude', '')
        }
        csv_data.append(stop_info)
    
    # 保存為 CSV 檔案
    csv_filename = f'{route_id}_bus_route.csv'
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['arrival_info', 'stop_number', 'stop_name', 'stop_id', 'latitude', 'longitude'])
        writer.writeheader()
        writer.writerows(csv_data)
    
    print(f"Data for route {route_id} has been saved to {csv_filename}")

# 範例使用
route_id = '0100000A00'  # 輸入你想查詢的公車代碼
fetch_bus_route_data(route_id)
