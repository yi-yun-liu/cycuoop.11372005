import pandas as pd
import os

# 指定檔案的絕對路徑
input_file = r"C:\Users\User\Desktop\cycuoop.11372005\20500520\midterm_scores.csv"
output_file = r"C:\Users\User\Desktop\cycuoop.11372005\20500520\被二一的名單.csv"

try:
    # 顯示執行位置與檔案位置
    print("程式目前位置：", os.path.abspath(__file__))
    print("讀取資料檔案：", input_file)

    # 讀取 CSV 檔
    df = pd.read_csv(input_file)

    # 科目欄位從第3欄開始（跳過 Name 和 StudentID）
    subject_cols = df.columns[2:]

    # 計算不及格科目數量
    df["FailCount"] = (df[subject_cols] < 60).sum(axis=1)

    # 篩選出被二一的學生（不及格科目數 >= 3）
    fail_df = df[df["FailCount"] >= 3][["Name", "StudentID", "FailCount"]]

    # 輸出成新 CSV 檔案
    fail_df.to_csv(output_file, index=False, encoding="utf-8-sig")

    print(f"名單產生成功！共 {len(fail_df)} 位學生被二一")
    print(f"已儲存為：{output_file}")

except FileNotFoundError:
    print(f"錯誤：找不到檔案 {input_file}，請確認路徑與檔名是否正確。")
except Exception as e:
    print(f"發生其他錯誤：{e}")

