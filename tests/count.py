from lib.Counter.Counter import Counter
from time import sleep

counter = Counter(start=1, end=10, step=1, ttl=10)

while True:
    print('Repeat')
    while counter.is_can():
        print('Step')
        counter.step()
    sleep(1)