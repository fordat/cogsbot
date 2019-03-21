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

TEXT2 = nltk.corpus.gutenberg.words('austen-emma.txt')

TEXT = nltk.word_tokenize('the quick brown fox jumped over the lazy red cat and I ate a watermelon and watched the whole thing happen ' 
    + 'I never thought it would go this far '
    + 'Im thinking about texting you '
    + 'the quick fox learned how to eat watermelon '
    + 'Im not sure what you want me to do '
    + 'Im not thinking about what you want me to do '
    + 'the brown fox and the red cat learned how far it would go '
    + 'lets see the fox and the cat do something new '
    + 'how far can the dog go '
    + 'can the cat eat the watermelon '
    + 'Im thinking about that watermelon ')

# NLTK shortcuts
bigrams = nltk.bigrams(TEXT2)
cfd = nltk.ConditionalFreqDist(bigrams)


# protoype for status updates. this function
# will print a random 30 word string created 
# from jane austen texts.
def print_austen():
# pick a random word from the corpus to start with
    word = random.choice(TEXT2)
# generate 15 more words
    for i in range(30):
        print(word + ' ', end='')
        if word in cfd:
            word = random.choice(list(cfd[word].keys()))
        else:
            break

def print_new(word):
    acc = ""
    for i in range(30):
        acc += word + ' '
        if word in cfd:
            word = random.choice(list(cfd[word].keys()))
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
        if '#austen' in mention.full_text.lower():
            word = random.choice(TEXT2)
            print('found austen!', flush=True)
            print('responding back...', flush=True)
            api.update_status('@' + mention.user.screen_name + ' ' 
                + print_new(word), mention.id)


while True:
    reply_to_tweets()
    time.sleep(15)
