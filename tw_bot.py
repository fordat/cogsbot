import tweepy
import time

print('this is my twitter bot')

CONSUMER_KEY = 'cRQIM9wXVlcTPP7PK9TS0l6ha'
CONSUMER_SECRET = 'nxe4JwHxluk0Cf7E7CWko1nGyMvlCP3Zy5AhFtN5htwf6NBU8o'
ACCESS_KEY = '1106272251651854336-Hz6Fxxmx0FqNuR7qjaXmu4URJFAnRA'
ACCESS_SECRET = 'ym83aFQGDKsnYUYaI0FzZHf6qOMv8JMa3DN9rLLI4POOW'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'

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
        if 'love' in mention.full_text.lower():
            print('found love!', flush=True)
            print('responding back...', flush=True)
            api.update_status('@' + mention.user.screen_name +
                    ' i love you as a friend', mention.id)
        elif 'friend' in mention.full_text.lower():
            print('found friend!', flush=True)
            print('responding back...', flush=True)
            api.update_status('@' + mention.user.screen_name +
                    ' lets be friends', mention.id)

while True:
    reply_to_tweets()
    time.sleep(15)

