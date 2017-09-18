from lib.job.storage.MongoDB import MongoDB as Storage
from lib.job.wiki.RequestTask import RequestTask
from lib.config.Yaml import Yaml as Config
import pandas as pd
from lib.job.wiki.PageRecursiveTask import PageRecursiveTask

config = Config('./config/config.yml')

max_dig_level = 4

job_list = Storage(PageRecursiveTask.TYPE, config.get('mongodb'))

df = pd.read_csv('./WorkBaseFile/ItalyUrlMainList', delimiter="\t")
for index, row in df.iterrows():
    link = row[0]
    job_list.add({'link': link, 'level': max_dig_level})