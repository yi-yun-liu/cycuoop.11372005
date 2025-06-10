import folium
from folium.plugins import AntPath
import pandas as pd
import random
import time
import math

# 載入 SQLite 資料庫並讀取路線點資料
def load_route_points():
    import sqlite3

    conn = sqlite3.connect('hermes_ebus_taipei.sqlite3')
    query = "SELECT latitude, longitude FROM data_route_info_busstop WHERE route_id = '0161000900' ORDER BY stop_number"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 繪製地圖並在路線上加上小人動畫
def create_animated_map(route_points):
    # 設置地圖
    start_coords = [route_points.iloc[0]['latitude'], route_points.iloc[0]['longitude']]
    m = folium.Map(location=start_coords, zoom_start=13)

    # 把路線點畫到地圖上
    route = folium.PolyLine(
        locations=route_points[['latitude', 'longitude']].values.tolist(),
        color='blue', weight=4.5, opacity=0.7
    ).add_to(m)

    # 小人圖示
    person_marker = folium.Marker(
        location=[route_points.iloc[0]['latitude'], route_points.iloc[0]['longitude']],
        icon=folium.Icon(icon='cloud', color='red')
    ).add_to(m)

    # 定義動畫效果
