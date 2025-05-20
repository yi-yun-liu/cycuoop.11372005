import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# 1. 讀取北北基桃行政區邊界
boundary = gpd.read_file("taiwan_admin_boundary.geojson", encoding="utf-8")
north_cities = ['臺北市', '新北市', '基隆市', '桃園市']
north_area = boundary[boundary['COUNTYNAME'].isin(north_cities)].to_crs(epsg=4326)

# 2. 讀取公車資料（去程與回程）
df_go = pd.read_csv("bus_route_10417_ttego.csv")
df_back = pd.read_csv("bus_route_10417_tteback.csv")
df_all = pd.concat([df_go, df_back], ignore_index=True).dropna(subset=['longitude', 'latitude'])

# 3. 建立 GeoDataFrame
geometry = [Point(xy) for xy in zip(df_all['longitude'], df_all['latitude'])]
bus_gdf = gpd.GeoDataFrame(df_all, geometry=geometry, crs="EPSG:4326")

# 4. 空間篩選站點在北北基桃
bus_gdf = gpd.sjoin(bus_gdf, north_area, how='inner', predicate='within')

# 5. 繪圖
fig, ax = plt.subplots(figsize=(14, 14))
north_area.boundary.plot(ax=ax, color="black", linewidth=1)
bus_gdf.plot(ax=ax, marker='o', color='blue', markersize=8, alpha=0.5)

# 簡略標註部分站名與路線（避免過多重疊）
sampled = bus_gdf.sample(n=100, random_state=1)
for idx, row in sampled.iterrows():
    label = f"{row['stop_name']} ({row['route_name']})"
    ax.text(row.geometry.x + 0.001, row.geometry.y + 0.001, label, fontsize=6)

plt.title("北北基桃 公車站牌與路線", fontsize=18)
plt.xlabel("經度")
plt.ylabel("緯度")
plt.grid(True)
plt.tight_layout()
plt.savefig("map_output.png", dpi=300)
plt.show()
