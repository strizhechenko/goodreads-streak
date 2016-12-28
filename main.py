import yaml
from goodreads import client

config = yaml.load(open('config.yml'))
gc = client.GoodreadsClient(config['consumer']['key'], config['consumer']['secret'])
gc.authenticate(config['access']['token'], config['access']['secret'])
# me = 34318778

# user = gc.user(me)
# user.owned_books()
