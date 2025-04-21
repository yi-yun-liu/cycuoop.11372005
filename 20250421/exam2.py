from datetime import datetime
import time

def analyze_datetime(input_str):
    # 定義星期對照表
    weekdays = {
        1: "星期一",
        2: "星期二",
        3: "星期三",
        4: "星期四",
        5: "星期五",
        6: "星期六",
        7: "星期日"
    }

    # 將字串轉為 datetime 物件
    dt = datetime.strptime(input_str, "%Y-%m-%d %H:%M")
    
    # 1. 回傳星期幾
    weekday_str = weekdays[dt.isoweekday()]

    # 2. 當年的第幾天
    day_of_year = dt.timetuple().tm_yday

    # 3. 計算太陽日（Julian date 的差異）
    now = datetime.now()
    delta_seconds = (now - dt).total_seconds()
    julian_days = delta_seconds / 86400  # 每日為 86400 秒

    return weekday_str, day_of_year, julian_days

# 範例使用
weekday, doy, jd_diff = analyze_datetime("2020-04-15 20:30")
print(f"星期幾: {weekday}")
print(f"當年的第幾天: {doy}")
print(f"與現在相差的太陽日數: {jd_diff:.6f}")
