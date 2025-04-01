import sys
import requests
import html
import pandas as pd
from bs4 import BeautifulSoup

# 修正 Windows cmd 編碼問題
sys.stdout.reconfigure(encoding="utf-8")

# 目標 URL（換成你的公車路線）
url = "https://pda.5284.gov.taipei/MQS/route.jsp?rid=10417"

# 設定 Headers，避免被網站擋掉
headers = {
    "User-Agent": "Mozilla/5.0"
}

# 發送 GET 請求
response = requests.get(url, headers=headers)

# 確保請求成功
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 找出所有表格
    tables = soup.find_all("table")

    rows = []

    for table in tables:
        for tr in table.find_all("tr"):  # 確保抓到所有站點
            td_list = tr.find_all("td")
            if len(td_list) >= 2:
                stop_name = html.unescape(td_list[0].text.strip())  # 站名
                arrival_time = html.unescape(td_list[1].text.strip())  # 預計到站時間

                # 修正 a_tag 變數的錯誤
                a_tag = td_list[0].find("a")  # 檢查站名內是否有 <a> 連結
                stop_link = a_tag["href"] if a_tag and "href" in a_tag.attrs else None

                rows.append({"站點名稱": stop_name, "預計到站時間": arrival_time, "連結": stop_link})

    # 存成 CSV 檔案
    df = pd.DataFrame(rows)
    df.to_csv("bus_stations_times.csv", index=False, encoding="utf-8-sig")
    print("✅ 已成功存成 bus_stations_times.csv")

else:
    print("❌ 無法取得網頁內容，請檢查網址")
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# 設定 User-Agent 避免被封鎖
headers = {
    "User-Agent": "Mozilla/5.0"
}

# 目標網站（請改成你的公車網站首頁）
BASE_URL = "https://bus-website.com/"
MAIN_URL = BASE_URL + "bus_stops_list"  # 公車站列表頁面（請替換為正確網址）

# 先抓取所有公車站點的連結
response = requests.get(MAIN_URL, headers=headers)
if response.status_code != 200:
    print("❌ 無法獲取公車站列表，請檢查網址")
    exit
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# 設定 Headers 避免被擋
headers = {
    "User-Agent": "Mozilla/5.0"
}

# 目標網址（替換成你的公車路線網址）
URL = "https://pda5284.gov.taipei/MQS/route.jsp?rid=10417"

# 發送請求
response = requests.get(URL, headers=headers)
if response.status_code != 200:
    print("❌ 無法獲取公車時刻表，請檢查網址")
    exit()

# 解析 HTML
soup = BeautifulSoup(response.text, "html.parser")

# 找到站點時刻表
tables = soup.find_all("table")

if not tables:
    print("❌ 沒有找到任何公車時刻表，請檢查 HTML 結構")
    exit()

print(f"✅ 找到 {len(tables)} 個公車時刻表")

# 存放所有站點資訊
all_data = []

# 解析每個站點的資訊
for table in tables:
    for tr in table.find_all("tr"):
        td_list = tr.find_all("td")
        if len(td_list) >= 2:  # 確保有站點與時間
            stop_name = td_list[0].text.strip()  # 站名
            arrival_time = td_list[1].text.strip()  # 預計到站時間
            all_data.append({
                "站點名稱": stop_name,
                "預計到站時間": arrival_time
            })

# 存成 CSV 檔案
df = pd.DataFrame(all_data)
df.to_csv("taipei_bus_times.csv", index=False, encoding="utf-8-sig")

print("🎉 公車時刻表已存成 taipei_bus_times.csv")


