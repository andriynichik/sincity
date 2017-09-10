from lib.factory.Loader import Loader as Factory


loader = Factory.loader()

url = 'https://it.wikipedia.org/wiki/Roma'
headers = {'User-Agent': 'Mozilla/5.0'}

content, code = loader.load(url, headers=headers)

if code == 200 and len(content) > 0:
    print('.', end='')
else:
    print('E', end='')