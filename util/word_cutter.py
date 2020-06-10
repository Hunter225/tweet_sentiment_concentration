import jieba
jieba.initialize()

def cut_word_zh(string):
    words = ' '.join(jieba.cut_for_search(string)).split(' ')
    words = [word for word in words if len(word) > 1]
    return words

def cut_word_en(string):
    words = string.split(' ')
    words = [word for word in words if len(word) > 1]
    return words