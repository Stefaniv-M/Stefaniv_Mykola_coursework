# This module tests if you can get tags from facebook photos of a person.


import facebook
# Now I will import *.py file with my access token.
import personal_access_stuff


token = personal_access_stuff.access_token

graph = facebook.GraphAPI(access_token=token, version = 2.7)

user = graph.request('/KimKardashian')

albums = graph.request('/' + user['id'] + '/albums')

print(albums)

# Getting biggest photo album of user:
album_id = albums['data'][3]['id']
print(albums['data'][3]['name'])

# Graph with 50 first photos from the album:
photos = graph.request('/' + album_id + '/photos?limit=50')

for i in range(50):
    photo_id = photos['data'][i]['id']
    print(photo_id)
    tags = graph.request('/' + photo_id + '/tags')
    print("THIS IS TAGS DICTIONARY:")
    print(tags)
    print("END OF TAGS")
    print("-----------------------------------------------------------------------------------")



