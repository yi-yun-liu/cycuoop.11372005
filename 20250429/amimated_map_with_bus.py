import folium
import time
import sqlite3
import pandas as pd

# 載入 SQLite 資料庫並讀取路線點資料
def load_route_points():
    conn = sqlite3.connect('hermes_ebus_taipei.sqlite3')
    query = "SELECT latitude, longitude FROM data_route_info_busstop WHERE route_id = '0161000900' ORDER BY stop_number"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 繪製地圖並在路線上加上小人和公車的動畫
def create_animated_map(route_points):
    # 設置地圖
    start_coords = [route_points.iloc[0]['latitude'], route_points.iloc[0]['longitude']]
    m = folium.Map(location=start_coords, zoom_start=13)

    # 把路線點畫到地圖上
    route = folium.PolyLine(
        locations=route_points[['latitude', 'longitude']].values.tolist(),
        color='blue', weight=4.5, opacity=0.7
    ).add_to(m)

    # 小人圖示（代表公車）
    person_marker = folium.Marker(
        location=[route_points.iloc[0]['latitude'], route_points.iloc[0]['longitude']],
        icon=folium.Icon(icon='cloud', color='red')
    ).add_to(m)

    # 模擬公車移動的動畫
    def move_person():
        for i in range(1, len(route_points)):
            person_marker.location = [route_points.iloc[i]['latitude'], route_points.iloc[i]['longitude']]
            time.sleep(0.5)

    # 動畫開始
    move_person()

    # 保存地圖為 HTML 文件
    map_file = "/mnt/data/animated_bus_map_with_person.html"
    m.save(map_file)

    return map_file

# 主程式
if __name__ == "__main__":
    route_points = load_route_points()  # 載入承德幹線的資料
    map_file = create_animated_map(route_points)
    print(f"Map has been saved as: {map_file}")

