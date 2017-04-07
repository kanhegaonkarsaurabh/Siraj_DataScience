# Authenticate and connect with Twitter API
import time
import json
import re # regular Expression
import tweepy
from textblob import TextBlob
from tweepy.streaming import StreamListener
import matplotlib.pyplot as plt
consumer_key = 'uQtz4x4rwHVdgywMSa1NEPswQ'
consumer_secret = 'm4cCXQuBXzkM9uDymDScIcvygpxcAS584LbkCW6xbHu9kml1aj'

access_token = '790159119558639616-S4MV4jZ8H4PgITaK8wWBhXEawa3yD3D'
access_token_secret = 'oT4u981L2QpXm0gflu6gjf596ouN9j4qsgV5mKsHC5CdF'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token , access_token_secret)



# Define a funtion to calculate the time spent on collecting tweets ( here a is the start time)
def calctime(a):
    return time.time() - a

#initial calues
positive = 0
negative = 0
compound = 0
count = 0
initime = time.time()
plt.ion()

# a Listener class to organize the tweets. This is inheriting from a class in the tweepy library
class listener(StreamListener):

    def on_data(self,data):
        global initime
        # calculate the time that has been spent ( so initime would be initialized in the beginning. passed - initial)
        t = int(calctime(initime))
        # The twitter data is in the form of a data. Load it onto a matrix
        all_data = json.loads(data)
        # Now, with every tweet, several values are associated like the text, username, date when posted. Here, we take
        # whats required
        tweet = all_data["text"].encode('utf-8')
        tweet = " ".join(re.findall("[a-zA-Z]+", tweet))
        blob = TextBlob(tweet.strip())

        # Loop over the tweets and find the resp. positive and g=negative sentiment values
        global positive
        global negative
        global compound
        global count

        count = count + 1
        senti = 0
        for sen in blob.sentences :
            senti = senti + sen.sentiment.polarity
            if sen.sentiment.polarity >= 0:
                positive = positive + sen.sentiment.polarity
            else:
                negative = negative + sen.sentiment.polarity
        compound = compound + senti

        # Print out the details of the tweets onto the terminal
        print count
        print tweet.strip()
        print senti
        print t
        print str(positive) + ' ' + str(negative) + ' ' + str(compound)

        # Plot the tweets' sentiments onto a live graph
        plt.axis([0,70,-20,20])
        plt.xlabel('Time')
        plt.ylabel('Sentiment')
        plt.plot([t],[positive],'go',[t],[negative],'ro',[t],[compound],'bo')
        plt.show()
        plt.pause(0.0001)
        if count==200:
            return False
        else:
            return True

    def on_error(self, status):
        print status


# Listen to the twitter streams and filter them acc. to the parameter
twitterStream = tweepy.Stream(auth, listener(count))
twitterStream.filter(track = ["Donald Trump"])
plt.show()
