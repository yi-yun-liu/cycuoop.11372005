# 台北市公車資訊查詢應用程式主體
import pandas as pd

# 載入資料：路線資料與站牌資料
routes_df = pd.read_csv("路線資訊20250610.csv")
stops_df = pd.read_csv("台北市_公車路線_站牌資料.csv")

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
                "Stops": stops_list
            })
    return results

# 顯示結果
user_start = input("請輸入出發站：")
user_end = input("請輸入目的站：")
routes = find_routes(user_start, user_end)

if not routes:
    print("沒有找到符合條件的公車路線")
else:
    for route in routes:
        print(f"公車路線：{route['RouteName']}（方向：{route['Direction']}）")
        print("經過站點：")
        for stop in route['Stops']:
            print(f" - {stop}")
        print("------")
