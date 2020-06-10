from opencc import OpenCC
import re

def s2t(string):
    cc = OpenCC('s2t')
    return cc.convert(string)

def t2s(string):
    cc = OpenCC('t2s')
    return cc.convert(string)

def _remove_string(target_list, string):
    for target in target_list:
        string = string.replace(target, "")
    return string


def _replace_string(target_list, string, replacer):
    for target in target_list:
        string = string.replace(target, replacer)
    return string

def remove_num(string):
    return re.sub(r'\d', '', string)

def remove_space(string):
    return re.sub(r'\s', '', string)

def remove_punc(string):
    punctuations = '''!()-[]{};:'"\\,<>./?@#$%^&*_~～‵！＠＄％︿＆＊（）－＿｜＼＝｛｝“”〝〞‘’、′’‵？／＞＜。，…．・=「」；《》：––?'''
    return _remove_string(punctuations, string)



def remove_en_alphabets(string):
    en_alphabets = '''qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'''
    return _remove_string(en_alphabets, string)

def remove_common_words_zh(string):
    common_words = ['參考資料','參考文獻','于年月日','在年月日','年月日','外部連結']
    return _remove_string(common_words, string)

def prepro_for_zh(string):
    return s2t(remove_common_words_zh(remove_en_alphabets(remove_num(remove_space(remove_punc(string))))))

def remove_punc_en(string):
    punctuations = '''=.();,"'''
    return _remove_string(punctuations, string)

def remove_space_en(string):
    spaces = '\n\t'
    return _remove_string(spaces, string)

def remove_common_words_en(string):
    common_words = [' external links ', ' references ', ' see also ', ' other ']
    return _replace_string(common_words, string, ' ')

def remove_stop_words_en(string):
    stop_words = ["me", "my", "myself", "we", "our", "ours", "ourselves", 
    "you", "your", "yours", "yourself", "yourselves", 
    "he", "him", "his", "himself", "she", "her", "hers", "herself", 
    "it", "its", "itself", "they", "them", "their", "theirs", "themselves", 
    "what", "which", "who", "whom", "this", "that", 
    "these", "those", "am", "is", "are", "was", "were", 
    "be", "been", "being", "have", "has", "had", "having", 
    "do", "does", "did", "doing", "a", "an", "the", "and", 
    "but", "if", "or", "because", "as", "until", "while", 
    "of", "at", "by", "for", "with", "about", "against", 
    "between", "into", "through", "during", "before", "after", 
    "above", "below", "to", "from", "up", "down", "the",
    "in", "out", "on", "off", "over", "under", "again", 
    "further", "then", "once", "here", "there", "when", "who",
    "where", "why", "how", "all", "any", "both", "each", "also"
    "few", "more", "most", "other", "some", "such", "no", "nor", "-to-",
    "not", "only", "own", "same", "so", "than", "too", "very", "can", "will", "just", "don", "should", "now"]

    stop_words = [" " + stop_word + " " for stop_word in stop_words]
    return _replace_string(stop_words, string, ' ')

def prepro_for_en(string):
    return remove_stop_words_en(remove_common_words_en(remove_space_en(remove_punc_en(string.lower()))))

