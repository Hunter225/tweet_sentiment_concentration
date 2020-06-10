# coding=utf-8
from numpy import dot
from numpy.linalg import norm
from math import log

def triangular_combinations(str_list):
    combinations = []

    for i in range(len(str_list)):
        for j in range(i+1,len(str_list)):
            combinations.append((str_list[i], str_list[j]))
    return combinations


def vectorize_word(word, bg_corpus):
    return tfidf(word, bg_corpus) * entropy(word, bg_corpus)

def vectorize_bow(bow, bg_corpus):
    vectorized_bow = {}
    for word in bow:
        vectorized_bow[word] = vectorize_word(word, bg_corpus)
    return vectorized_bow

def tfidf(word, bg_corpus):
    joint_bg_corpus = ' '.join(bg_corpus)
    term_frequency = float(joint_bg_corpus.count(word))
    doc_number = float(len(bg_corpus))
    doc_frequency = float(sum([1 for doc in bg_corpus if word in doc]))
    if doc_frequency == 0:
        doc_frequency = 1
    inverse_doc_frequency = log( 1 + doc_number / doc_frequency )
    return term_frequency * inverse_doc_frequency

def entropy(word, bg_corpus, lang = 'zh'):
    if lang == 'zh':
        len_of_words_counted = _count(word, bg_corpus) * len(word)
        total_len_of_corpus = len("".join(bg_corpus))
    elif lang == 'en':
        len_of_words_counted = _count(word, bg_corpus) * len(word.split(' '))
        total_len_of_corpus = len((" ".join(bg_corpus)).split(' '))
    return - ( _entropy(len_of_words_counted, total_len_of_corpus))

def _entropy(count1, count2):
    if count1 == 0:
        return 0.0
    p = float(count1 / count2)
    return p * log(p)

def _count(word, str_list):
    c = 0
    for string in str_list:
        if word in string:
            c = c + sum([1 for string in str_list if word in string])
    return c

def cos_sim(vector1, vector2):
    normalized_vector1 = []
    normalized_vector2 = []
    dimensions_set1 = vector1.keys()
    dimensions_set2 = vector2.keys()
    all_dimensions = set(dimensions_set1).union(dimensions_set2)
    for dimension in all_dimensions:
        if dimension in dimensions_set1:
            normalized_vector1.append(vector1[dimension])
        else:
            normalized_vector1.append(0.0)
        if dimension in dimensions_set2:
            normalized_vector2.append(vector2[dimension])
        else:
            normalized_vector2.append(0.0)
    return dot(normalized_vector1, normalized_vector2)/(norm(normalized_vector1)*norm(normalized_vector2))