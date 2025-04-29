import folium
import sqlite3
from datetime import datetime

# 建立連接到 SQLite 資料庫
conn = sqlite3.connect('bus_data.db')
cursor = conn.cursor()

# 查詢承德幹線的公車進站時間和座標數據
cursor.execute("SELECT bus_id, station_name, latitude, longitude, arrival_time FROM bus_schedule WHERE bus_id = '0161000900'")
bus_data = cursor.fetchall()

# 假設我們有一個進站時間，並轉換為數字格式，這樣才能在地圖上動態顯示
def time_to_seconds(time_str):
    t = datetime.strptime(time_str, "%H:%M:%S")
    return t.hour * 3600 + t.minute * 60 + t.second

# 創建一個地圖對象
m = folium.Map(location=[25.066, 121.513], zoom_start=14)

# 在地圖上添加公車和進站時間
for bus in bus_data:
    bus_id, station_name, lat, lon, arrival_time = bus
    arrival_seconds = time_to_seconds(arrival_time)
    
    # 在地圖上添加標記
    folium.Marker(
        location=[lat, lon],
        popup=f"Bus: {bus_id} - {station_name} \nArrival Time: {arrival_time}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# 保存地圖為 HTML
map_html_file = "bus_map.html"
m.save(map_html_file)

# 生成地圖與動畫的 HTML 文件
with open("bus_animation.html", "w") as file:
    file.write(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bus Animation</title>
        <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
        <style>
            #map {{ width: 100%; height: 600px; }}
            .bus-icon {{ width: 50px; height: 50px; background-image: url('https://cdn-icons-png.flaticon.com/512/2710/2710887.png'); background-size: cover; }}
        </style>
    </head>
    <body>
        <h2>Bus Animation</h2>
        <div id="map"></div>
        <script>
            var map = L.map('map').setView([25.066, 121.513], 14);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {{
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }}).addTo(map);

            // 添加公車標記
            var busMarker = L.marker([25.066, 121.513], {{
                icon: L.divIcon({{
                    className: 'bus-icon',
                    iconSize: [50, 50]
                }})
            }}).addTo(map);

            var busLocations = [
                {{"lat": 25.066, "lon": 121.513}},  // 替換為各站點經緯度
                {{"lat": 25.067, "lon": 121.514}},
                {{"lat": 25.068, "lon": 121.515}},
                // 更多站點
            ];

            var currentIndex = 0;

            // 動畫控制
            setInterval(function() {{
                if (currentIndex < busLocations.length) {{
                    busMarker.setLatLng([busLocations[currentIndex].lat, busLocations[currentIndex].lon]);
                    currentIndex++;
                }}
            }}, 1000);  // 每秒移動一次
        </script>
    </body>
    </html>
    """)

# 關閉資料庫連接
conn.close()

print("HTML file with bus animation generated!")
