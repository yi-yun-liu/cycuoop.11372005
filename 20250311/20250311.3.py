import pandas as pd
import matplotlib.pyplot as plt

# 讀取 Excel 檔案
df = pd.read_excel('C:/Users/User/Desktop/cycuoop.11372005/20250311/311.xlsx')

# 假設欄位名稱為 'x' 和 'y'
df['sum'] = df['x'] + df['y']

# 印出相加結果
print(df['sum'])

# 繪製 x 和 y 的散佈圖
plt.scatter(df['x'], df['y'])
plt.xlabel('x')
plt.ylabel('y')
plt.title('Scatter Plot of x and y')
plt.show()