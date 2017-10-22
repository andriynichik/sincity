Документы в бд

# verified

документ который по нашим соображениям включает в себя максимально точные заначения(названия без шума, полная админ структура, дополнительные свойства местоположения, указатели ни источники)

code - string уникальный идентификатор получаемый из названия, админ уровня и иерархии админ делений

name - string название админ деления
```text
  Paris
```

type - string уровень местоположения
```text
  ADMIN_LEVEL_1
```

У каждой страны свое число админ делений, по этому тут будет храниться только уровень
Но уровень можно сопоставить с названием при внедрении в другую систему
Всего на данный момент будет 8 уровней админ делений, при необходимости список расширим
ADMIN_LEVEL_1 ADMIN_LEVEL_2 ADMIN_LEVEL_3 ADMIN_LEVEL_4
ADMIN_LEVEL_5 ADMIN_LEVEL_6 ADMIN_LEVEL_7 ADMIN_LEVEL_8

i18n - dict названия на разных языках
```text
  {
	en: Paris,
	ru: Париж
  }
```

admin_hierarchy - dict список в порядке убывания  всех уровней админ делений до этого пункта, названия на родном языке (позволит миксовать запросы к тому-же гуглу)
```text
  {
    ADMIN_LEVEL_1: {name:France},
    ADMIN_LEVEL_2: {name:Île-de-France},
    ADMIN_LEVEL_3: {name:Paris},
    ADMIN_LEVEL_5: {...},
    ADMIN_LEVEL_5: {name:Paris}
    ADMIN_LEVEL_N: {...},
  }
```

capital - string имя центра админ деления
```text
  CapitalName
```

center - dict позиция центра админ единицы
```text
  {
    lat - float
    lng - float
  }
```
borders - list граница админ единицы - поможет определять, тот ли еэто пункт (позиция пункта из других источников должна входить в границы)
```text
  [
    {lat:23.324, lng:34.532},
    {lat:24.324, lng:35.532},
    {lat:25.324, lng:36.532},
    {lat:23.324, lng:34.532},
  ]
```

bounds - dict границы окна карты для просмотре этого пункта на карте
```text
  {
    left: {lat:23.32, lng: 35.35},
    right: {lat:32.54, lng: 33.45}
  }
```

altitude - dict средняя высота над уровнем моря (в метрах)
```text
  {
  	min: 234
  	max: 333
  	mean: 276 - среднее арифметическое
    median: 244 - медиана
  }
```

population - unsigned integer
```text
  16579
```

density - unsigned integer плотность населения на квадратный км
```text
  156
```

area - площадь в квадратных километрах
```text
  11254
```

postal_codes - tuple список почтовых кодов
```text
  (
    52435,
    54364,
    67543
  )
```

time - dict данные вмени в админ еденицы
```text
  {
    timezone: 'France/Paris',
    UTC: '+1',
    DST: '+2'
  }
```

other - dict данные которые отличаются в зависимости от страны
```text
  {
    commune_codes: [1254, 4898],
    bla_bla: foo
  }
```


sources - dict - список ключей на связаные данные из других источников (wiki, gmaps, osm, ...) позволит понимать откуда такие данные
```text
  {
    wiki: gdfkslgjreirehgdsjfk,
    gmap: asdfasdfewpfgdsg,
    osm: safdfgsdfgasg,
    insee: asdgasha
  }
```

## файл импорта/экспорта

Плоская таблица с данными, в формате csv с разделителем полей \t
и разделителем строк \n

* обязательно к заполнению

Поле в csv -> поле в документе на сервере

code -> code - если код отсутсвует, то он будет сгенерирован автоматически
name -> name - *
type -> type - *
i18n -> i18n - поле будет записано в формате lang:name|lang:name|...
ADMIN_LEVEL_1 -> admin_hierarchy[0].name - *
ADMIN_LEVEL_2 -> admin_hierarchy[1].name
ADMIN_LEVEL_3 -> admin_hierarchy[2].name
ADMIN_LEVEL_4 -> admin_hierarchy[3].name
ADMIN_LEVEL_5 -> admin_hierarchy[4].name
ADMIN_LEVEL_6 -> admin_hierarchy[5].name
ADMIN_LEVEL_7 -> admin_hierarchy[6].name
ADMIN_LEVEL_8 -> admin_hierarchy[7].name
capital -> capital
lat -> center.lat
lng -> center.lng
borders -> borders - границы будут заполнены в одно поле в формате (lat,lng),(lat,lng),(lat,lng)
bounds -> bounds - область окна карты будет записана в одну ячейку (lat,lng),(lat,lng)
altitude_min -> altitude.min
altitude_max -> altitude.max
altitude_mean -> altitude.mean
altitude_median -> altitude.median
population -> population
density -> density
area -> area
postal_codes -> postal_codes - формат записи в csv будет через запятую 45684,46465,45654
timezone -> time.timezone
UTC -> time.UTC
DST -> time.DST
other -> other.raw - сюда просто вставится строка как есть, без какой либо обработки

# page_cache

кешированые страницы собранные из разных источников (wiki, gmaps, ...) позволит быстро повторить арсинг если вдруг при разработке была допущена ошибка или понадобятся дополнительные данные#

code - string хеш код запроса для извлечения результатов из куша и не отправля запрос на сайт донор
```text
  dfjastwqhsaddglkjasdgewghsaghasvasdverhas
```

request - dict сам запрос который отпраляли для получения этих данных
```text
  {
    url: http://fr.wiki....
    headers: {
      User-agent: Gecko
    }
  }
```

response - string ответ
```text
  <html>...</html>
```

timestamp - timestamp время получения результата
```text
15096456541
```

status - int http статус
```text
  200
```


# wiki

данные из википедии

code - string хеш админ единицы, для идентификации, хеш ссылки на википедии(вместе с хостом) 
```text
dsgasdhgasdfhadfhdfb
```

requests - tuple запросы по которым получили эту информацию, 
получили из странци поиска, есть ссылка с другого населенного пункта
```text
  (
    'issee 25325',
    'Commune 25325',
    'Frace, Paris'
  )
```

url - string ссылка на страницу на основном языке страны
```text
  http://fr.wiki...
```

name - string имя админ единицы записаное в заголовке страницы на основном языке страны
```text
  Paris
```

type - string уровень местоположения
```text
  ADMIN_LEVEL_3
```

i18n - dict названия на разных языках
```text
  {
	en:{name: Paris, url:http://en.wiki...},
	ru:{name: Париж, url:http://ru.wiki...}
  }
```

admin_hierarchy - dict список в порядке убывания  всех уровней админ делений до этого пункта (позволит миксовать запросы к тому-же гуглу)
```text
  [
    ADMIN_LEVEL_1: {name:France, type:country, url:'http://fr.wiki....'},
    ADMIN_LEVEL_2: {...},
    ADMIN_LEVEL_3: {name:Île-de-France, type:region, url:'http://fr.wiki....'},
    ADMIN_LEVEL_4: {name:Paris, type:department, url:'http://fr.wiki....'},
    ADMIN_LEVEL_5: {...},
    ADMIN_LEVEL_6: {name:Paris, type:district, url:'http://fr.wiki....'}
    ADMIN_LEVEL_N: {...}
  ]
```

capital - dict Название центра и ссылка на страницу центра
```text
  {name:CapitalName, url:UrlToCapitalPage}
```

center - dict позиция админ единицы
```text
  {
    lat - float
    lng - float
  }
```

altitude - dict средняя высота над уровнем моря (в метрах)
```text
  {
  	min: 234
  	max: 333
  	mean: 276 - среднее арифметическое
    median: 244 - медиана
  }
```

population - unsigned integer
```text
  16579
```

density - unsigned integer плотность населения на квадратный км
```text
  156
```

area - площадь в квадратных километрах
```text
  11254
```

postal_codes - tuple список почтовых кодов
```text
  (
    52435,
    54364,
    67543
  )
```

time - dict данные вмени в админ еденицы
```text
  {
    timezone: 'France/Paris',
    UTC: '+1',
    DST: '+2'
  }
```

other - dict данные которые отличаются в зависимости от страны
```text
  {
    commune_codes: [1254, 4898],
    bla_bla: foo
  }
```

# Google Maps

code string уникальный идентификатор, берется из place_id
```text
ChIJkdDO-yFu5kcRk04wCbaedQQ
```

requests - tuple запросы по которым получили эту информацию
```text
  (
    'issee 25325',
    'Commune 25325',
    (23.435436, 53.62223) # lat, lng
  )
```

name string вставляется из long name
```text
France
```

short_name вставляется из поля short name
```text
FR
```

type - string тип админ единицы
```text
administrative_area_level_1
```

lang - string язык названий
```text
en
```

admin_hierarchy - dict список в порядке убывания всех уровней админ до этого пункта
```text
[
    ADMIN_LEVEL_1: {name:France, short_name: FR, type:country},
    ADMIN_LEVEL_2: {name:Île-de-France, short_name: Île-de-France, type:administrative_area_level_1},
    ADMIN_LEVEL_3: {name:Paris, short_name: Paris, type:administrative_area_level_2},
    ADMIN_LEVEL_N: {...}
]
```

center - dict позиция админ единицы
```text
  {
    lat - float
    lng - float
  }
```
bounds - dict границы окна карты для просмотре этого пункта на карте
```text
  {
    left: {lat:23.32, lng: 35.35},
    right: {lat:32.54, lng: 33.45}
  }
```

postal_code - string почтовый код для текущего адреса или точки
```text
75001
```