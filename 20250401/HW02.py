import sys
import requests
import html
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 修正 Windows cmd 編碼問題
sys.stdout.reconfigure(encoding="utf-8")

# 目標 URL
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
    print(f"找到 {len(tables)} 個表格")  # 檢查表格數量

    rows = []

    for table in tables:
        for tr in table.find_all("tr"):  # 取消 class 限制，確保抓到所有站點
            td = tr.find("td")
            if td:
                stop_name = html.unescape(td.text.strip())  # 站名
                a_tag = td.find("a")  # 連結
                stop_link = a_tag["href"] if a_tag and "href" in a_tag.attrs else None
                rows.append({"站點名稱": stop_name, "連結": stop_link})

    # 存成 CSV 檔案
    df = pd.DataFrame(rows)
    df.to_csv("bus_stations.csv", index=False, encoding="utf-8-sig")
    print

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
