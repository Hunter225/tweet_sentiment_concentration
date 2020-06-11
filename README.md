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

```sh
elasticsearch -d
cd ~/{{dir}}/tweet_sentiment_concentration
python cronjobs.py
```

After completion,  a csv file containing calculation result will be stored in tweet_sentiment_concentration/result/VIX_predictor
