Документы в бд

# verified

документ который по нашим соображениям включает в себя максимально точные заначения(названия без шума, полная админ структура, дополнительные свойства местоположения, указатели ни источники)

name - string название админ деления
```text
  Paris
```

type - string уровень местоположения
```text
  Region
```

i18n - dict названия на разных языках
```text
  {
	en: Paris,
	ru: Париж
  }
```

admin_hierarchy - list список в порядке убывания  всех уровней админ делений до этого пункта (позволит миксовать запросы к тому-же гуглу)
```text
  [
    {name:France, type:country, i18n:{en:France, ru:Франция}},
    {...},
    {name:Île-de-France, type:region, i18n:{...}},
    {name:Paris, type:department, i18n:{...}},
    {...},
    {name:Paris, type:district, i18n:{...}}
    {...}
  ]
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

commune_codes - tuple список кодов коммун
```text
  (
    5432345
  )
```

old_commune_codes - tuple список старых кодов которые входят сейчас в новые
```text
  (
    4534623,
    6362346
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


sources - dict - список ключей на связаные данные из других источников (wiki, gmaps, osm, ...) позволит понимать откуда такие данные
```text
  {
    wiki:[
      	gdfkslgjreirehgdsjfk,
      	fwqeoigthyqweruighvs,
      	fwqoietuqjgsadfvasdf
      ],
    gmaps:[
        asdfasdfewpfgdsg,
        fadsklgehwotetvs,
        fasdgewetqgfasdv
      ],
    osm: [
        safdfgsdfgasg,
        gasdhgdshasdg
      ]
  }
```


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

code - string хеш админ единицы, для идентификации
```text
dsgasdhgasdfhadfhdfb
```

requests - tuple запросы по которым получили эту информацию
```text
  (
    'issee 25325',
    'Commune 25325',
    'Frace, Paris'
  )
```

url - string ссылка на страницу на языке страны
```text
  http://fr.wiki...
```

name - string имя админ единицы записаное в заголовке страницы на языке страны
```text
  Paris
```

type - string уровень местоположения
```text
  region
```

i18n - dict названия на разных языках
```text
  {
	en:{name: Paris, url:http://en.wiki...},
	ru:{name: Париж, url:http://ru.wiki...}
  }
```

admin_hierarchy - list список в порядке убывания  всех уровней админ делений до этого пункта (позволит миксовать запросы к тому-же гуглу)
```text
  [
    {name:France, type:country, url:'http://fr.wiki....', i18n:{en:{name:France, url:http://en.wiki...}, ru:{name:Франция, url:http://ru.wiki...}},
    {...},
    {name:Île-de-France, type:region, url:'http://fr.wiki....', i18n:{...}},
    {name:Paris, type:department, url:'http://fr.wiki....', i18n:{...}},
    {...},
    {name:Paris, type:district, url:'http://fr.wiki....', i18n:{...}}
    {...}
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

commune_codes - tuple список кодов коммунн
```text
  (
    5432345
  )
```


old_commune_codes - tuple список старых кодов которые входят сейчас в новые/новый
```text
  (
    4534623,
    6362346
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

admin_hierarchy - list список в порядке убывания всех уровней админ до этого пункта
```text
[
    {name:France, short_name: FR, type:country},
    {name:Île-de-France, short_name: Île-de-France, type:administrative_area_level_1},
    {name:Paris, short_name: Paris, type:administrative_area_level_2},
    {...}
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

