# This module tests if you can get friends of a person on Facebook


import facebook
# Now I will import *.py file with my access token.
import personal_access_stuff


token = personal_access_stuff.access_token

graph = facebook.GraphAPI(access_token=token, version = 2.7)

user = graph.request('/DonaldTrump')

friends = graph.request('/' + user['id'] + '/hours')
print(friends)