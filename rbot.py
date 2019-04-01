import nltk
import random
import ssl
import tweepy
import time

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

from nltk import word_tokenize,sent_tokenize


print('this is my twitter bot')

CONSUMER_KEY = 'cRQIM9wXVlcTPP7PK9TS0l6ha'
CONSUMER_SECRET = 'nxe4JwHxluk0Cf7E7CWko1nGyMvlCP3Zy5AhFtN5htwf6NBU8o'
ACCESS_KEY = '1106272251651854336-Hz6Fxxmx0FqNuR7qjaXmu4URJFAnRA'
ACCESS_SECRET = 'ym83aFQGDKsnYUYaI0FzZHf6qOMv8JMa3DN9rLLI4POOW'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'

announcements = open('marton.txt','r').read()

MARTON = nltk.word_tokenize(announcements)

AUSTEN = nltk.corpus.gutenberg.words('austen-emma.txt')

# MARTON'S BIGRAMS
ms_bigrams = nltk.bigrams(MARTON)
ms_cfd = nltk.ConditionalFreqDist(ms_bigrams)

# AUSTEN'S BIGRAMS
ja_bigrams = nltk.bigrams(AUSTEN)
ja_cfd = nltk.ConditionalFreqDist(ja_bigrams)


# print things marton would say, using data from his announcements.
def print_marton(word):
    acc = ""
    for i in range(30):
        acc += word + ' '
        if word in ms_cfd:
            word = random.choice(list(ms_cfd[word].keys()))
        else:
            break
    return acc

# print things Jane Austen would write, using data from her book Em.
def print_austen(word):
    acc = ""
    for i in range(30):
        acc += word + ' '
        if word in ja_cfd:
            word = random.choice(list(ja_cfd[word].keys()))
        else:
            break
    return acc

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
    # DEV NOTE: use 1060651988453654528 for testing.
    last_seen_id = retrieve_last_seen_id(FILE_NAME)

    
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#announcements' in mention.full_text.lower():
            word = random.choice(MARTON)
            print('found announcements!', flush=True)
            print('responding back...', flush=True)
            api.update_status('@' + mention.user.screen_name + ' ' 
                + 'Hi all,\n\n' 
                + print_marton(word) 
                + '\n\nAll the best,\n\nMarton', mention.id)        
        if '#austen' in mention.full_text.lower():
            word = random.choice(AUSTEN)
            print('found austen!', flush=True)
            print('responding back...', flush=True)
            api.update_status('@' + mention.user.screen_name + ' ' 
                + print_austen(word), mention.id)



while True:
    reply_to_tweets()
    time.sleep(15)
