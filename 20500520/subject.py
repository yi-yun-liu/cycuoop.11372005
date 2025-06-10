import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

csv_path = r"C:\Users\User\Desktop\cycuoop.11372005\20500520\midterm_scores.csv"

if not os.path.exists(csv_path):
    print(f"找不到檔案：{csv_path}")
    exit()

df = pd.read_csv(csv_path, encoding='utf-8-sig')

subjects = ['Chinese', 'English', 'Math', 'History', 'Geography', 'Physics', 'Chemistry']
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'purple']

bins = np.arange(0, 110, 10)  # 分數區間 0,10,20,...,100

plt.figure(figsize=(12, 7))

bar_width = 10 / len(subjects)  # 每個柱寬 (10 是一個區間寬度)

for i, subject in enumerate(subjects):
    counts, _ = np.histogram(df[subject], bins=bins)
    plt.bar(bins[:-1] + i*bar_width, counts, width=bar_width, color=colors[i], edgecolor='black', label=subject)

plt.xlabel('Score Range')
plt.ylabel('Number of Students')
plt.title('Score Distribution for Each Subject')
plt.xticks(bins)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig("combined_score_distribution.png")
print("圖檔已儲存：combined_score_distribution.png")
plt.show()


