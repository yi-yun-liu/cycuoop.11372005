import math

# 修正的絕對值函式，確保 x == 0 時也有返回值
def absolute_value_fixed(x):
    if x < 0:
        return -x
    return x  # Covers both x > 0 and x == 0

# 移除無效程式碼的絕對值函式
def absolute_value_clean(x):
    if x < 0:
        return -x
    return x

# 簡化的整除判斷函式
def is_divisible(x, y):
    return x % y == 0

# 計算兩點距離的函式
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
