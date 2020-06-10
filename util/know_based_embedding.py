from scraper.wiki_scraper import WikiScraper
from util.lcs import lcs_for_zh, lcs_for_en
from util.nlp_math import triangular_combinations, vectorize_bow, cos_sim
from util.preprocess import prepro_for_zh, prepro_for_en
from util.word_cutter import cut_word_zh, cut_word_en
import copy
import datetime

class WordEmbedder:
    #function mapping for zh en functions
    prepro_functions = {'zh': prepro_for_zh, 'en': prepro_for_en}
    lcs_functions = {'zh': lcs_for_zh, 'en': lcs_for_en}
    word_cutter_funtions = {'zh': cut_word_zh,'en': cut_word_en}

    def __init__(self, lang):
        self.lang = lang
        self.scraper = WikiScraper(lang)
        self.lcs = self.__class__.lcs_functions[lang]
        self.prepro = self.__class__.prepro_functions[lang]
        self.word_cut = self.__class__.word_cutter_funtions[lang]
        self.lcs_set = set()
        self.bag_of_words = set()
        self.word_vec = {}

    def lcs_extraction(self, word, iter = 3):
        self.scraper.get_contents(word)
        self.training_corpus = self._prepro_for_corpus(self.scraper.contents)
        self.tfidf_bg_corpus = copy.deepcopy(self.training_corpus)
        i = 0
        while i < 3:
            self._lcs_extraction()
            i = i + 1

    def transform_lcs_set_to_bow(self):
        for lcs in self.lcs_set:
            bag_of_words = self.word_cut(lcs)
            for word in bag_of_words:
                if self.lang == 'en':
                    self.bag_of_words.add(word)
                elif self.lang == 'zh':
                    self.bag_of_words.add(word)
    
    def generate_word_vec(self):
        self.word_vec = vectorize_bow(self.bag_of_words, self.tfidf_bg_corpus)

    def _lcs_extraction(self):
        self._find_lcs_for_corpus(self.training_corpus)
        self._remove_lcs_from_corpus()

    def _prepro_for_corpus(self, training_corpus):
        return [self.prepro(doc) for doc in training_corpus]

    # find longest common substring for training corpus
    def _find_lcs_for_corpus(self, training_corpus):
        training_corpus_pairs = triangular_combinations(training_corpus)
        for pair in training_corpus_pairs:
            lcs = self.lcs(pair[0],(pair[1]))
            if lcs:
                if self.lang == 'en':
                    self.lcs_set.add(lcs.strip())
                elif self.lang == 'zh':
                    self.lcs_set.add(lcs)
        
    def _remove_lcs_from_corpus(self):
        for lcs in self.lcs_set:
            for i in range(len(self.training_corpus)):
                self.training_corpus[i] = self.training_corpus[i].replace(lcs, '')



