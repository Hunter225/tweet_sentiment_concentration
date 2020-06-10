def read_tweet_accounts():
    tweet_accounts = []
    with open('settings/twitter_accounts.txt') as tweet_accounts_file:
        tweet_accounts = tweet_accounts_file.read().split('\n')
    return tweet_accounts


def is_en_word_in_string(word, string):
    if ' ' + word + ' ' in string:
        return True
    return False


def count_en_word_in_string(word, string):
    space_b4 = string.count(' ' + word)
    space_after = string.count(word + ' ')
    space_b4_and_after = string.count(' ' + word + ' ')

    return space_b4 + space_after - space_b4_and_after