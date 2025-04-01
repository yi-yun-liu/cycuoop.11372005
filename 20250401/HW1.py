import sys
sys.stdout.reconfigure(encoding="utf-8")  # 修正 Windows cmd 編碼問題

import requests
import html
import pandas as pd
from bs4 import BeautifulSoup

# 目標 URL
url = "https://pda5284.gov.taipei/MQS/route.jsp?rid=10417"

# 設定 Headers，避免被網站阻擋
headers = {
    "User-Agent": "Mozilla/5.0"
}

# 發送 GET 請求
response = requests.get(url, headers=headers)

# 確保請求成功
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")
    dataframes = []

    for table in tables:
        rows = []
        for tr in table.find_all("tr", class_=["ttego1", "ttego2"]):
            td = tr.find("td")
            if td:
                stop_name = html.unescape(td.text.strip())  # 站名
                a_tag = td.find("a")  # 超連結
                stop_link = a_tag["href"] if a_tag and "href" in a_tag.attrs else None
                rows.append({"站點名稱": stop_name, "連結": stop_link})

        if rows:
            df = pd.DataFrame(rows)
            dataframes.append(df)

    if len(dataframes) >= 2:
        df1, df2 = dataframes[0], dataframes[1]
        print("【忠孝幹線 - 去程】")  # 移除 emoji
        print(df1.to_string(index=False))  
        print("\n【忠孝幹線 - 回程】")  # 移除 emoji
        print(df2.to_string(index=False))
    else:
        print("❌ 未找到足夠的表格資料。")
else:
    print(f"❌ 無法下載網頁，HTTP 狀態碼: {response.status_code}")


