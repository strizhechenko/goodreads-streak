"""
Goodreads serverless (yeah, no callbacks!) oauth example.
"""

import urlparse
import yaml
import oauth2


url = 'https://www.goodreads.com'
authorize_url = '%s/oauth/authorize' % url
access_token_url = '%s/oauth/access_token' % url

def make_consumer(config):
    return oauth2.Consumer(key=config['consumer']['key'], secret=config['consumer']['secret'])

def request_token(consumer):
    request_token_url = '%s/oauth/request_token' % url
    client = oauth2.Client(consumer)
    response, content = client.request(request_token_url, 'GET')
    if response['status'] != '200':
        raise Exception('Invalid response: %s' % response['status'])
    return dict(urlparse.parse_qsl(content))

def oauth_token(req_token):
    authorize_link = '%s?oauth_token=%s' % (authorize_url, req_token['oauth_token'])
    print authorize_link
    accepted = 'n'
    while accepted.lower() == 'n':
        accepted = raw_input('Have you authorized me? (y/n) ')
    return oauth2.Token(req_token['oauth_token'], req_token['oauth_token_secret'])


def access_token(consumer, token):
    client = oauth2.Client(consumer, token)
    response, content = client.request(access_token_url, 'POST')
    if response['status'] != '200':
        raise Exception('Invalid response: %s' % response['status'])

    return dict(urlparse.parse_qsl(content))

def final_token(access):
    return oauth2.Token(access['oauth_token'],
                        access['oauth_token_secret'])

def main():
    config = yaml.load(open('config.yml'))
    consumer = make_consumer(config)
    request = request_token(consumer)
    oauth = oauth_token(request)
    access = access_token(consumer, oauth)
    final = final_token(access)
    print final

if __name__ == '__main__':
    main()
