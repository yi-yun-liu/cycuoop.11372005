# exam1.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def plot_normal_pdf(mu, sigma, output_file="normal_pdf.jpg"):
    """
    繪製常態分佈的機率密度函數圖，並儲存為 JPG 圖檔

    參數:
    mu (float): 平均數
    sigma (float): 標準差，必須為正數
    output_file (str): 儲存的圖檔名稱（預設為 normal_pdf.jpg）
    """
    if sigma <= 0:
        raise ValueError("標準差 sigma 必須為正數")

    # 建立 x 軸數值範圍（從 mu-4σ 到 mu+4σ）
    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 500)

    # 計算常態分布的 PDF
    y = norm.pdf(x, mu, sigma)

    # 繪圖設定
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, label=f"μ={mu}, σ={sigma}", color="blue")
    plt.title("Normal Distribution PDF")
    plt.xlabel("x")
    plt.ylabel("Probability Density")
    plt.grid(True)
    plt.legend()

    # 儲存圖檔為 JPG 格式
    plt.savefig(output_file, format='jpg')
    plt.close()

# 範例執行（可修改參數）
if __name__ == "__main__":
    plot_normal_pdf(mu=0, sigma=1.0)
    print("常態分布 PDF 圖已儲存為 normal_pdf.jpg")
