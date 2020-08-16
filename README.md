# Tweet Sentiment Concentration calculator
> It helps calculate to what extent how general public is discussing towards a certain topic.

The module consists of 2 parts.
1. Scarpe tweets over 30+ twitter accounts in past 24 hours.
2. Extract features from tweets, vectorize the tweets, and clustering the tweets.

The size of the largest cluster should be concerned becuase it may be a topic that people hottly discussing.

![](header.png)

## Installation

OS X:

```sh
brew install elastic/tap/elasticsearch-full
cd ~/{{dir}}/tweet_sentiment_concentration
pip install -r requirements.txt
```

## Usage example

Start an elastic service first. 

```sh
elasticsearch -d
```

Scrape some tweets - refer to "scrape_tweets_of_last_24_hours.py" under exmaples folder

Calculate the sentiment concentration of tweets:
```py
from tweet_sentiment_concentration.calculation.sentiment_concentration import cal_sentiment_concentration
...
tweets = GET_SOME_TWEETS
...
concentration_coefficient = cal_sentiment_concentration(tweets)
```

It is NOT a must to start an elastic service to do the concentration calculation, you can maintain your own db on mysql or mongdb and then pass an array of tweets string to the function ```cal_sentiment_concentration```


## Parameter Tuning

There are three optional parameter parts in cal_sentiment_concentration:
1. clustering_algo - it is the clustering algorithm provided by scikit learn. By default, AgglomerativeClustering is used

2. feature_num - the number of topK most frequently used words extracted from tweets to be used as the dimension of the vectors space, by default, it is 20

3. cluster_num - the number of clusters assumed in the vectors space.

```py
cal_sentiment_concentration(tweets, clustering_algo = AgglomerativeClustering, feature_num=20, cluster_num=3)
```