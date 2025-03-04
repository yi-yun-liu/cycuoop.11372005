def count_silence(lyrics, word='silence'):
    # 將歌詞轉換為小寫，並計算指定單詞出現的次數
    lyrics_lower = lyrics.lower()  # 轉換為小寫以進行不區分大小寫的比較
    count = lyrics_lower.split().count(word.lower())  # 將歌詞拆分為單詞並計算出現次數
    return count

# 測試
print(count_silence(lyrics))

def count_keyword(lyrics, keyword):
    # 將歌詞轉換為小寫並計算關鍵字的出現次數
    lyrics_lower = lyrics.lower()  # 轉換為小寫以進行不區分大小寫的比較
    count = lyrics_lower.split().count(keyword.lower())  # 將歌詞拆分為單詞並計算出現次數
    return count

# 測試
lyrics = '''When you're weary
Feeling small
When tears are in your eyes
I will dry them all
I'm on your side
Oh, when times get rough
And friends just can't be found
Like a bridge over troubled water
I will lay me down
Like a bridge over troubled water
I will lay me down
When you're down and out
When you're on the street
When evening falls so hard
I will comfort you
I'll take your part
Oh, when darkness comes
And pain is all around
Like a bridge over troubled water
I will lay me down
Like a bridge over troubled water
I will lay me down
Sail on, silver girl
Sail on by
Your time has come to shine
All your dreams are on their way
See how they shine
Oh, if you need a friend
I'm sailing right behind
Like a bridge over troubled water
I will ease your mind
Like a bridge over troubled water
I will ease your mind
'''

key_word = 'bridge'
print(count_keyword(lyrics, key_word))
