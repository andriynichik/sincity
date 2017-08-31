from lib.job.storage.MongoDB import MongoDB as Storage
from lib.job.wiki.RequestTask import RequestTask
from lib.config.Yaml import Yaml as Config
import pandas as pd

config = Config('./config/config.yml')

job_list = Storage(RequestTask.TYPE, config.get('mongodb'))

df = pd.read_csv('./WorkBaseFile/BaseCommuneInInseeFR', delimiter="\t")
for index, row in df.iterrows():
    insee = row[0]
    job_list.add("insee+{insee}".format(insee=insee))