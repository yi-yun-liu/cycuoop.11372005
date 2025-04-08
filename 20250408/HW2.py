import sys
import io
from datetime import datetime, timezone
from jdcal import gcal2jd

# 讓 stdout 使用 UTF-8 編碼，避免亂碼
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def time_info(input_time_str):
    input_dt = datetime.strptime(input_time_str, "%Y-%m-%d %H:%M")
    now = datetime.now(timezone.utc)

    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    weekday_str = weekdays[input_dt.weekday()]

    input_jd = sum(gcal2jd(input_dt.year, input_dt.month, input_dt.day))
    input_jd += (input_dt.hour + input_dt.minute / 60) / 24

    now_jd = sum(gcal2jd(now.year, now.month, now.day))
    now_jd += (now.hour + now.minute / 60 + now.second / 3600) / 24

    elapsed_julian_days = now_jd - input_jd

    return weekday_str, elapsed_julian_days

# 🧑‍💻 手動輸入
user_input = input("請輸入時間（格式：YYYY-MM-DD HH:MM）：")

try:
    weekday, elapsed_days = time_info(user_input)
    print("該日為：", weekday)
    print("至今已過：", elapsed_days, "個太陽日")
except Exception as e:
    print("❌ 輸入格式錯誤，請使用 YYYY-MM-DD HH:MM，例如：2020-04-15 20:30")
    print("錯誤訊息：", e)


