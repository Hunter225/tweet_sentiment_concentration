from datetime import datetime
from util import preprocess, lcs, nlp_math, util
import numpy as np
from sklearn.cluster import AgglomerativeClustering



def identify_key_features(tweets):
    triangular_combinations = nlp_math.triangular_combinations(tweets)
    features = []
    for pair in triangular_combinations:
        feature = lcs.lcs_for_en(pair[0], pair[1])
        if not feature:
            continue
        if feature not in features and len(feature.split(' ')) > 2:
            features.append(feature)
    return features

def find_frequently_used_words(features, tweets, topK=20):
    # Find the most frequently used words of features in tweets    
    bow = set()
    for corpus in features:
        words = corpus.split(' ')
        for word in words:
            if word not in  ['', '-']:
                bow.add(word)

    tweets_vector_space_dimension = []
    for word in bow:
        word_count = 0
        for tweet in tweets:
            if util.is_en_word_in_string(word, tweet):
                word_count = word_count + 1
        tweets_vector_space_dimension.append({"word":word, "frequency":word_count})
    tweets_vector_space_dimension = sorted(tweets_vector_space_dimension, key = lambda i: i['frequency'],reverse=True)
    tweets_vector_space_dimension = tweets_vector_space_dimension[:topK]
    return tweets_vector_space_dimension

def generate_tweets_vectors(tweets_vector_space_dimension, tweets):
    #generate bags of words(bow) vector space
    word_to_vec_dict = {}
    vec_to_word_dict = {}
    cardinality = 0
    for pair in tweets_vector_space_dimension:
        word = pair["word"]
        word_to_vec_dict[word] = cardinality
        vec_to_word_dict[cardinality] = word
        cardinality = cardinality + 1

    #vectorize tweets
    tweets_vectors = []
    for tweet in tweets:
        tweet_vector = [0] * cardinality
        for i in range(cardinality):
            word = vec_to_word_dict[i]

            #tweet_vector[i] = util.count_en_word_in_string(word, tweet)

            if vec_to_word_dict[i] in tweet:
                tweet_vector[i] = 1

        #only append the tweet vector if the tweet vector IS NOT a zero vector
        if np.any(tweet_vector):
            tweets_vectors.append(tweet_vector)
    tweets_vectors = np.array(tweets_vectors)
    return tweets_vectors


def _cal_sentiment_concentration(tweets_vectors, clustering_algo = AgglomerativeClustering, cluster_num=3):
    # clustering tweets
    tweets_clustering = clustering_algo(n_clusters=cluster_num).fit(tweets_vectors)
    tweets_cluster = tweets_clustering.labels_
    cluster_sizes = [np.count_nonzero(tweets_cluster == i) for i in range(cluster_num)]
    max_cluster_size = max(cluster_sizes)
    # the size of the largest cluster implies how many tweets hotly discuss a certain topic
    sentiment_concentration = max_cluster_size / sum(cluster_sizes)

    return sentiment_concentration


def cal_sentiment_concentration(tweets, clustering_algo = AgglomerativeClustering, feature_num=20, cluster_num=3):
    features = identify_key_features(tweets)
    #find most frequently used words and treat it as the 'dimension' of the vector space
    tweets_vector_space_dimension = find_frequently_used_words(features, tweets, topK=feature_num)
    tweets_vectors = generate_tweets_vectors(tweets_vector_space_dimension, tweets)
    concentration = _cal_sentiment_concentration(tweets_vectors, clustering_algo = clustering_algo, cluster_num=cluster_num)
    return concentration, tweets_vector_space_dimension
