import geopandas as gpd
import matplotlib.pyplot as plt

# 從 GitHub 讀取 geojson（記得用 raw 連結）
geojson_url = "https://raw.githubusercontent.com/chengtaoyang/cycu_1132_oop_ctyang/main/20250422/bus_stop2.geojson"
gdf = gpd.read_file(geojson_url)

# 畫圖
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, color='blue', markersize=10, label='Bus Stops')

ax.set_title("Bus Stops Map", fontsize=16)
ax.set_xlabel("Longitude", fontsize=12)
ax.set_ylabel("Latitude", fontsize=12)
plt.legend()

# 儲存圖片
output_path = "bus_stops.png"
plt.savefig(output_path, dpi=300)
print(f"圖片已儲存為 {output_path}")

# 顯示圖片
plt.show()
