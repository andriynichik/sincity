from lib.job.storage.MongoDB import MongoDB as Storage
from lib.job.wiki.RequestTask import RequestTask
from lib.config.Yaml import Yaml as Config

config = Config('./config/config.yml')

job_list = Storage(RequestTask.TYPE, config.get('mongodb'))

job_list.add('Nice')