import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import lognorm

def plot_log_normal_cdf(mu, sigma, x_range=(0.01, 5), output_filename='lognormal_cdf.jpg'):
    """
    繪製對數常態分布的累積分布函數（CDF），並儲存為 JPG。
    
    Parameters:
    - mu: 常態分布的 μ（對應對數常態的參數）
    - sigma: 常態分布的 σ（對應對數常態的參數）
    - x_range: 要繪圖的 x 軸範圍，例如 (0.01, 5)
    - output_filename: 輸出 JPG 檔名
    """
    x = np.linspace(x_range[0], x_range[1], 500)
    cdf = lognorm.cdf(x, s=sigma, scale=np.exp(mu))

    plt.figure(figsize=(8, 5))
    plt.plot(x, cdf, label=f'Log-normal CDF\nμ={mu}, σ={sigma}')
    plt.xlabel('x')
    plt.ylabel('CDF')
    plt.title('Log-normal Cumulative Distribution Function')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_filename, format='jpg')
    plt.close()

# 範例使用：
plot_log_normal_cdf(mu=1.5, sigma=0.4, x_range=(0.01, 5), output_filename='lognormal_cdf.jpg')
