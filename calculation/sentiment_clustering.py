from models.getter import Getter
from datetime import datetime
from util import preprocess, lcs, nlp_math, util
from datetime import datetime
import random
import numpy as np
from sklearn.cluster import AgglomerativeClustering

def cal_sentiment_clustering_size(start_time, end_time):

    # __init__ time range
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S")

    # get tweets within the time range
    getter = Getter()
    tweets = getter.get_by_time_range(start_time_str, end_time_str)
    tweets = [preprocess.prepro_for_en(tweet.full_text) for tweet in tweets]
    triangular_combinations = nlp_math.triangular_combinations(tweets)


    # retrieve features from tweets
    features = []
    #for pair in random_pairs_sample:
    for pair in triangular_combinations:
        feature = lcs.lcs_for_en(pair[0], pair[1])
        if not feature:
            continue
        if feature not in features and len(feature.split(' ')) > 2:
            features.append(feature)


    #find most frequently used words
    bow = set()
    for corpus in features:
        words = corpus.split(' ')
        for word in words:
            if word not in  ['', '-']:
                bow.add(word)

    doc_frequency = []
    for word in bow:
        word_count = 0
        for tweet in tweets:
            if util.is_en_word_in_string(word, tweet):
                word_count = word_count + 1
        doc_frequency.append({"word":word, "doc_frequency":word_count})
    doc_frequency = sorted(doc_frequency, key = lambda i: i['doc_frequency'],reverse=True)
    doc_frequency = doc_frequency[:20]
    '''
    if int(len(doc_frequency) * 0.02) > 5:
        doc_frequency = doc_frequency[:int(len(doc_frequency) * 0.02)]
    else:
        doc_frequency = doc_frequency[:5]
    '''
    print(start_time)
    print(len(tweets))
    print(doc_frequency)

    #generate bags of words(bow) vector space
    word_to_vec_dict = {}
    vec_to_word_dict = {}
    cardinality = 0
    for pair in doc_frequency:
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

    #clustering tweets
    num_of_cluster = 3
    #num_of_cluster = int(len(tweets) * 0.02) if int(len(tweets) * 0.02) > 3 else 3
    tweets_clustering = AgglomerativeClustering(n_clusters=num_of_cluster).fit(tweets_vectors)
    tweets_cluster = tweets_clustering.labels_
    cluster_sizes = [np.count_nonzero(tweets_cluster == i) for i in range(num_of_cluster)]
    max_cluster_size = max(cluster_sizes)
    portion_of_max_cluster = max_cluster_size / sum(cluster_sizes)

    return portion_of_max_cluster
