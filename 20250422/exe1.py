from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Selenium 設定
options = Options()
options.add_argument('--headless')  # 若你要看到瀏覽器，可以移除此行
options.add_argument('--disable-gpu')

# 指定 chromedriver.exe 路徑（換成你自己的）
driver = webdriver.Chrome(
    options=options,
    executable_path='C:\\chromedriver\\chromedriver.exe'
)

# 開啟網頁
driver.get("https://bus.pcrest.tw/Search/")
time.sleep(2)

routes_to_find = ["承德幹線", "基隆路幹線", "1818"]

for route_name in routes_to_find:
    search_box = driver.find_element(By.ID, "RouteName")
    search_box.clear()
    search_box.send_keys(route_name)

    search_button = driver.find_element(By.ID, "search_btn")
    search_button.click()

    time.sleep(2)

    try:
        results = driver.find_elements(By.CSS_SELECTOR, "div.routeitem")
        print(f"\n✅ {route_name} 的查詢結果：")
        for result in results:
            print(result.text.strip())
    except Exception as e:
        print(f"\n❌ 查詢 {route_name} 發生錯誤：{e}")

driver.quit()
