import configparser

config = configparser.ConfigParser()
config.read("config.cfg")

api_key = config['KEYS']['API_KEY']
headers = {'Authorization': 'Bearer %s' % api_key}