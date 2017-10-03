from lib.job.storage.MongoDB import MongoDB as Storage
from lib.job.wiki.RequestTask import RequestTask
from lib.config.Yaml import Yaml as Config
import pandas as pd
import urllib.parse

country = 'Italy'
lst_address = []

region_index = 1
provincia_index = 3
comune_index = 5
localita_index = 9


config = Config('./config/config.yml').get('mongodb')

job_list = Storage(RequestTask.get_name(country), config)

df = pd.read_csv('./data/italy/indicatori_2011_localita.csv', delimiter=";", skiprows=[1], encoding='ISO-8859-1')

for index, row in df.iterrows():
    print(index)
    try:
        new_address = 'Italia,'
        if row[1]:
            new_address += row[region_index]
            if new_address not in lst_address:
                lst_address.append(new_address)
                job_list.add(urllib.parse.quote(new_address))
            new_address += ','
            if row[provincia_index]:
                new_address += row[provincia_index]
                if new_address not in lst_address:
                    lst_address.append(new_address)
                    job_list.add(urllib.parse.quote(new_address))
                new_address += ','
                if row[comune_index]:
                    new_address += row[comune_index]
                    if new_address not in lst_address:
                        lst_address.append(new_address)
                        job_list.add(urllib.parse.quote(new_address))
                    new_address += ','
                    if row[localita_index]:
                        new_address += row[localita_index]
                        if new_address not in lst_address:
                            lst_address.append(new_address)
                            job_list.add(urllib.parse.quote(new_address))
    except:
        print('Error in index [{}]'.format(index))