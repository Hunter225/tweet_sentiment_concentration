from util.know_based_embedding import WordEmbedder
from util.nlp_math import cos_sim
import datetime

def calculate_feature_correlation(word1, word2):
    zh_word_embedder1 = WordEmbedder('zh')
    zh_word_embedder1.lcs_extraction(word1)
    zh_word_embedder1.transform_lcs_set_to_bow()
    zh_word_embedder1.generate_word_vec()

    zh_word_embedder2 = WordEmbedder('zh')
    zh_word_embedder2.lcs_extraction(word2)
    zh_word_embedder2.transform_lcs_set_to_bow()
    zh_word_embedder2.generate_word_vec()

    correlation_zh = cos_sim(zh_word_embedder1.word_vec, zh_word_embedder2.word_vec)

    en_word_embedder1 = WordEmbedder('en')
    en_word_embedder1.lcs_extraction(word1)
    en_word_embedder1.transform_lcs_set_to_bow()
    en_word_embedder1.generate_word_vec()

    en_word_embedder2 = WordEmbedder('en')
    en_word_embedder2.lcs_extraction(word2)
    en_word_embedder2.transform_lcs_set_to_bow()
    en_word_embedder2.generate_word_vec()

    correlation_en = cos_sim(zh_word_embedder1.word_vec, zh_word_embedder2.word_vec)

    bilingual_correlation = correlation_zh + correlation_en

    return bilingual_correlation


if __name__ == '__main__':
    pairs = [['hello kitty','pokemon'],['Newton','Einstein'],['twitter', 'facebook'], ['bird flu', 'world war']]

    results = []

    for pair in pairs:
        correlation = calculate_feature_correlation
        results.append([pair[0], pair[1], correlation])


    with open('./result/word_correlation/' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.csv', 'w') as result_file:
        for result in results:
            result_file.write(str(result[0]))
            result_file.write(',')
            result_file.write(str(result[1]))
            result_file.write(',')
            result_file.write(str(result[2]))
            result_file.write('\n')