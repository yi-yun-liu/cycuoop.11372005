def is_palindrome(word):
    """檢查字串是否為回文"""
    return word == ''.join(reversed(word))

# 測試函式
print(is_palindrome("noon"))      # True
print(is_palindrome("rotator"))   # True
print(is_palindrome("hello"))     # False

# 單字列表
word_list = ["racecar", "hello", "rotator", "banana", "level", "deified", "noon", "madam"]

# 找出長度至少 7 的回文詞
for word in word_list:
    if len(word) >= 7 and is_palindrome(word):
        print(word)

