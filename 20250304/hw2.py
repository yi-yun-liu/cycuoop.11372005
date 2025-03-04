def gcd(a, b):
    # 基本情況：當 b 為 0 時，gcd 就是 a
    if b == 0:
        return a
    # 否則，遞迴呼叫 gcd
    return gcd(b, a % b)

# 測試範例
print(f"7 和 49 的最大公因數是 {gcd(7, 49)}")
print(f"11 和 121 的最大公因數是 {gcd(11, 121)}")

