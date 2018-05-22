import tweepy
from twitter_access_stuff import consumer_key, consumer_secret, access_token, access_token_secret


# Authorisation:
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creating api object:
api = tweepy.API(auth)


# Finding user:
user = api.get_user("realDonaldTrump")
# Name of the user:
print("Name:", user.screen_name)
# Amount of followers of the user:
print("Amount of followers:", user.followers_count)
# Friends of the user:
print("Friends:")
for friend in user.friends():
    print(friend.screen_name)
