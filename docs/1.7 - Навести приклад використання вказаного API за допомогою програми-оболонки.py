import tweepy

auth = tweepy.OAuthHandler("fhPVE6KrLVylkE0YiWILkdDSa", "4KsoAIPdI2cvSXBDKUCHEWqmSsdeWU3DXWjS5PNA7kDuoiIMbE")
auth.set_access_token("964470020024791042-3LT8bPADZwpmTindbazkqmFi0x43b6a",
                      "HXkAdtbsA2pXXWtC7DK1LVUwDSlRjExHszhfd4euZnCfN")

api = tweepy.API(auth)

trump = api.get_user("realDonaldTrump")

print("This will show some information about Donald Trump\n")
print("Twitter Id:", trump.id)
print("Language of Trump's account:", trump.lang)
print("Link to his profile picture:", trump.profile_image_url)
print("Location:", trump.location)
print("Coordinates:", trump.coordinates)
print("Description:", trump.description)
print("Ammount of followers:", trump.followers_count)
print("Ammount of friends:", trump.friends_count)

friends = trump.friends()
print("List of those friends:")
print([friend.name for friend in friends])
print("ID's of those friends:")
print([friend.id for friend in friends])

