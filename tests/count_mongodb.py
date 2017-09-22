from lib.Counter.CounterMongoDB import CounterMongoDB
from time import sleep
from lib.config.Yaml import Yaml as Config
from pymongo import MongoClient


config = Config('./config/config.yml').get('mongodb')
connection = MongoClient(config['host'], config['port'])

counter = CounterMongoDB(counter_name='test', start=1, end=10, step=1, ttl=10, connection=connection)

while True:
    print('Repeat')
    while counter.is_can():
        print('Step')
        counter.step()
    sleep(1)