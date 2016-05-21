# import modules
""" how is this accepted as docstring when importing modules? """
import csv
import tweepy

from apikeys import consumer_key, consumer_secret, access_token, access_secret

# Your constants
twitter_user = 'St1Norge'
csvfile = 'tweets.csv'


# Split and extract information from the tweet, and return in a usefull format
def parse_tweet(text):
    """ Split the tweet into something usable. """
    split = text.split('\n')
    gasoline = split[1].split(': ')[1]
    diesel = split[2].split(': ')[1]
    station = split[3]
    time = split[5]
    return time, station, gasoline, diesel


def get_all_tweets(screen_name):
    """Download all tweets for specified screen name"""

    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    # Initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial requst for the most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("Getting Tweets before %s" % (oldest))

        # all subsequent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        #save the most recent tweets
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))

    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = []
    for tweet in alltweets:
        outtweets.append(parse_tweet(tweet.text))

    # write the csv
    with open(csvfile, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["created_at", "tid", "stasjon", "bensin", "diesel"])
        writer.writerows(outtweets)

if __name__ == '__main__':
    # pass in the username of the account you want to download
    get_all_tweets(twitter_user)
