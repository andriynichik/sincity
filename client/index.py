from flask import Flask
from flask import render_template
from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.config.Yaml import Yaml as Config
from lib.job.storage.MongoDB import MongoDB as JobStorage
from pymongo import MongoClient
import re
from lib.location.Wiki import Wiki
from lib.location.GMap import GMap
from lib.logger.MongoDB import MongoDB as MongoDBLog
import hashlib
from bson.objectid import ObjectId
from flask import request
from flask import redirect
from flask import url_for
from urllib.parse import unquote_plus
from lib.factory.Loader import Loader as LoaderFactory
from lib.parser.map.google.GMapFactory import GMapFactory as MapFactory
from lib.compare.Comparison import Comparison
from lib.spider.Spider import Spider


app = Flask(__name__)


def escape(val):
    return re.escape(str(val))


@app.route("/")
def index():
    return render_template('admin/index.html')


@app.route('/internal')
@app.route('/internal/<string:country>')
def internal_list(country=None):
    return render_template('admin/internal/list.html', country=country)


@app.route('/internal/unit/<string:id>')
def internal_unit(id):
    config = Config('./config/config.yml')
    api_key = config.get('googlemaps').get('geocoding')
    factory = DocFactory(config.get('mongodb'))
    collection = factory.internal_collection()
    obj = collection.find_one({'_id': ObjectId(id)})
    return render_template('admin/internal/unit.html', data=obj, api_key=api_key)

@app.route('/internal/edit')
@app.route('/internal/edit/<string:id>')
@app.route('/internal/edit/<string:id>/<string:saved>')
def internal_edit(id=None, saved=0):
    config = Config('./config/config.yml')
    api_key = config.get('googlemaps').get('geocoding')
    obj = {}
    if id:
        factory = DocFactory(config.get('mongodb'))
        collection = factory.internal_collection()
        obj = collection.find_one({'_id': ObjectId(id)})

    admin_levels = ['ADMIN_LEVEL_1', 'ADMIN_LEVEL_2', 'ADMIN_LEVEL_3', 'ADMIN_LEVEL_4', 'ADMIN_LEVEL_5', 'ADMIN_LEVEL_6', 'ADMIN_LEVEL_7', 'ADMIN_LEVEL_8']

    languages = ['en', 'it', 'fr']

    if obj:
        levels = []
        for level in admin_levels:
            if obj.get('type') == level:
                break
            levels.append(level)
        old_postal = obj.get('postal_codes', [])
        new_postal = (str(x) for x in old_postal)
        obj.update(postal_codes=new_postal)
    else:
        obj = {}
        levels = admin_levels

    return render_template('admin/internal/edit.html',
                           admin_levels=admin_levels,
                           levels=levels,
                           data=obj,
                           api_key=api_key,
                           languages=languages,
                           saved=saved
                           )


@app.route('/internal/save', methods=['POST'])
def internal_save():
    post = request.form.copy()
    config = Config('./config/config.yml')
    factory = DocFactory(config.get('mongodb'))
    collection = factory.internal_collection()
    obj = {}
    data = internal_form_mapping(post)
    if post.get('id'):
        obj = collection.find_one({'_id': ObjectId(post.get('id'))})
        if obj:
            collection.update_one({'_id': ObjectId(post.get('id'))}, {'$set': data})
    else:
        result = collection.insert_one(data)
        obj.update(_id=result.inserted_id)
    return redirect(url_for('internal_edit', id=obj.get('_id'), saved=1))


def internal_form_mapping(data):
    obj = {
        'name': data.get('name', ''),
        'capital': data.get('capital', ''),
        'type': data.get('type', ''),
        'admin_hierarchy': {
            'ADMIN_LEVEL_1': data.get('ADMIN_LEVEL_1', ''),
            'ADMIN_LEVEL_2': data.get('ADMIN_LEVEL_2', ''),
            'ADMIN_LEVEL_3': data.get('ADMIN_LEVEL_3', ''),
            'ADMIN_LEVEL_4': data.get('ADMIN_LEVEL_4', ''),
            'ADMIN_LEVEL_5': data.get('ADMIN_LEVEL_5', ''),
            'ADMIN_LEVEL_6': data.get('ADMIN_LEVEL_6', ''),
            'ADMIN_LEVEL_7': data.get('ADMIN_LEVEL_7', ''),
            'ADMIN_LEVEL_8': data.get('ADMIN_LEVEL_8', ''),
        },
        'altitude': data.get('altitude', ''),
        'population': data.get('population', ''),
        'area': data.get('area', ''),
        'density': data.get('density', ''),
        'postal_codes': data.get('postal_codes', '').split(','),
        'time': data.get('time', ''),
        'center': {
            'lat': data.get('latitude', ''),
            'lng': data.get('longitude', ''),
        },
        'bounds': {
            'left': {
                'lat': data.get('left_latitude', ''),
                'lng': data.get('left_longitude', '')
            },
            'right': {
                'lat': data.get('right_latitude', ''),
                'lng': data.get('right_longitude', '')
            }
        },
        'i18n': {
            'en': data.get('en', ''),
            'fr': data.get('fr', ''),
            'it': data.get('it', '')
        }
    }
    return obj


@app.route('/internal/delete/<string:id>')
def internal_delete(id):
    config = Config('./config/config.yml')
    factory = DocFactory(config.get('mongodb'))
    collection = factory.internal_collection()
    result = collection.delete_many({'_id': ObjectId(id)})
    return render_template('admin/empty.html', data='ok', auto_close=True)


@app.route('/data/<string:provider_type>.js')
@app.route('/data/<string:provider_type>/<string:country>.js')
def data_provider(provider_type, country=None):
    config = Config('./config/config.yml')

    factory = DocFactory(config.get('mongodb'))
    document_filter = {}

    if provider_type == Wiki.TYPE:
        data = factory.wiki_collection()
        if country:
            document_filter = {
                'name': {'$exists': True, '$not': {'$size': 0}},
                'admin_hierarchy.ADMIN_LEVEL_1.name': country
            }
    elif provider_type == GMap.TYPE:
        data = factory.gmaps_collection()
        if country:
            document_filter = {
                'name': {'$exists': True, '$not': {'$size': 0}},
                'admin_hierarchy.ADMIN_LEVEL_1.name': country
            }
    else:
        data = factory.internal_collection()
        if country:
            document_filter = {
                'admin_hierarchy.ADMIN_LEVEL_1.name': country
            }

    if not document_filter:
        document_filter = {'name': {'$exists': True, '$not': {'$size': 0}}}

    objects = data.find(document_filter)
    return render_template('admin/{}/list.js'.format(provider_type), e=escape, items=objects)


@app.route('/data/matching-france-<string:region>.js')
def matching_france_js(region):
    region = unquote_plus(region)
    #mode = request.args.get('mode', 'none')
    config = Config('./config/config.yml')

    factory = DocFactory(config.get('mongodb'))
    internal = factory.internal_collection()
    wiki = factory.wiki_collection()
    gmap = factory.gmaps_collection()
    insee = factory.insee_collection()
    objects = internal.find({
        'name': {'$exists': True, '$not': {'$size': 0}},
        '$and': [{'admin_hierarchy.ADMIN_LEVEL_1.name': 'France'}, {'admin_hierarchy.ADMIN_LEVEL_2.name': region}],
    })
    result = []
    for item in objects:
        dic = {
            'internal': item
        }

        wiki_res = {}
        if item.get('source', {}).get('wiki'):
            wiki_res = wiki.find_one({'code': item.get('source', {}).get('wiki')})

        dic.update(wiki=wiki_res)

        gmap_res = {}
        if item.get('source', {}).get('gmap'):
            gmap_res = gmap.find_one({'code': item.get('source', {}).get('gmap')})

        dic.update(gmap=gmap_res)

        insee_res = {}
        if item.get('source', {}).get('insee'):
            insee_res = insee.find_one({'code': item.get('source', {}).get('insee')})

        dic.update(insee=insee_res)

        compare_res = {}
        compare_res.update({'insee_code!=wiki_code': 1 if not (insee_res.get('InseeXls_CodeCommune') == wiki_res.get('commune_codes')) else 0})
        compare_res.update({'insee_name!=wiki_name': 1 if not (insee_res.get('InseeXls_NameCommune') == wiki_res.get('name')) else 0})
        compare_res.update({'wiki_name!=gmaps_name': 1 if not (wiki_res.get('true_name', wiki_res.get('name')) == gmap_res.get('true_name', gmap_res.get('name'))) else 0})
        compare_res.update({'wiki_post!=gmaps_post': 1 if not (str(wiki_res.get('postal_codes')) == str(gmap_res.get('postal_code'))) else 0})
        compare_res.update({'wiki_admin!=gmaps_admin': 1 if not (str(wiki_res.get('admin_hierarchy')) == str(gmap_res.get('admin_hierarchy'))) else 0})
        try:
            max_meters_in_distance = 5000
            compare_res.update({'wiki_posinion>gmaps_position': 1 if Comparison.by_distance(wiki_res.get('center'), gmap_res.get('center')) > max_meters_in_distance else 0})
        except:
            compare_res.update({'wiki_posinion>gmaps_position': 1})
        dic.update(compare=compare_res)

#        if mode != 'none':
#            if mode == 'wiki_adapte':
#                if dic.get('wiki', {}).get('name', '').lower() != dic.get('insee', {}).get('name', '').lower():
#                    result.append(dic)
#            elif mode == 'gmap_adapte':
#                if dic.get('gmap', {}).get('name', '').lower() != dic.get('insee', {}).get('name', '').lower():
#                    result.append(dic)
#        else:
#            result.append(dic)

        result.append(dic)

    return render_template('admin/matching-france/list.js', e=escape, items=result)

@app.route('/matching/france/')
@app.route('/matching/france/<string:region>')
def matching_france(region=None):
    mode = request.args.get('mode', 'none')
    if region is None:
        config = Config('./config/config.yml')

        factory = DocFactory(config.get('mongodb'))
        internal = factory.internal_collection()
        objects = internal.aggregate([
        {'$match':
            {
                'name': {'$exists': True, '$not': {'$size': 0}},
                '$and': [{'admin_hierarchy.ADMIN_LEVEL_1.name': 'France'}]
            }
        },
        {'$group': {'_id': '$admin_hierarchy.ADMIN_LEVEL_2.name', 'count': {'$sum': 1}}}
        ])
        return render_template('admin/matching-france/region-list.html', data=objects, mode=mode)
    else:
        return render_template('admin/matching-france/list.html', region=region, mode=mode)


@app.route('/matching/spain/')
@app.route('/matching/spain/<string:region>')
def matching_spain(region=None):
    mode = request.args.get('mode', 'none')
    Provincia = {
                '01' : 'Araba (Álava)',
                '02' : 'Abacente ',
                '03' : 'Alicante ',
                '04' : 'Almería ',
                '05' : 'Avila ',
                '06' : 'Badajoz ',
                '07' : 'Balears, Illes', 
                '08' : 'Barcelona ',
                '09' : 'Burgos ',
                '10' : 'Cáceres ',
                '11' : 'Cádiz ',
                '12' : 'Castellón', 
                '13' : 'Ciudad Real', 
                '14' : 'Córdoba ',
                '15' : 'Coruña, A ',
                '16' : 'Cuenca ',
                '17' : 'Girona ',
                '18' : 'Granada ',
                '19' : 'Guadalajara ', 
                '20' : 'Guipuzcoa ',
                '21' : 'Huelva ',
                '22' : 'Huesca ',
                '23' : 'Jaén ',
                '24' : 'León ',
                '25' : 'Lleida ',
                '26' : 'Rioja, La ',
                '27' : 'Lugo ',
                '28' : 'Madrid ',
                '29' : 'Málaga ',
                '30' : 'Murcia ',
                '31' : 'Navarra ',
                '32' : 'Ourense ',
                '33' : 'Asturias ',
                '34' : 'Palencia ',
                '35' : 'Las Palmas ',
                '36' : 'Pontevedra ',
                '37' : 'Salamanca ',
                '38' : 'Santa Cruz de Tenerife', 
                '39' : 'Cantabria ',
                '40' : 'Segovia ',
                '41' : 'Sevilla ',
                '42' : 'Soria ',
                '43' : 'Tarragona ',
                '44' : 'Teruel ',
                '45' : 'Toledo ',
                '46' : 'Valencia ',
                '47' : 'Valladolid ',
                '48' : 'Bizkaia ',
                '49' : 'Zamora ',
                '50' : 'Zaragoza ',
                '51' : 'Ceuta ',
                '52' : 'Melilla ',
            }
    if region is None:
 


        return render_template('admin/matching-spain/region-list.html', data=Provincia)
    else:
        config = Config('./config/config.yml')
        mongo_config = config.get('mongodb')
        connection = MongoClient(mongo_config['host'], mongo_config['port'])
        db = connection.location
        data =  db.internal.find({'20_SNIG_COD_PROV': int(region)})
        return render_template('admin/matching-spain/list.html', region=Provincia[str(region)], data=data)



@app.route('/gmaps/')
@app.route('/gmaps/<string:country>')
def gmaps_list(country=None):
    return render_template('admin/gmap/list.html', country=country)


@app.route('/gmaps/unit/<string:id>')
def gmaps_unit(id):
    config = Config('./config/config.yml')
    api_key = config.get('googlemaps').get('geocoding').get('key')
    factory = DocFactory(config.get('mongodb'))
    collection = factory.gmaps_collection()
    obj = collection.find_one({'_id': ObjectId(id)})
    return render_template('admin/gmap/unit.html', data=obj, api_key=api_key)


@app.route('/gmaps/unit/code/<string:id>')
def gmap_code_unit(id):
    config = Config('./config/config.yml')
    api_key = config.get('googlemaps').get('geocoding').get('key')
    factory = DocFactory(config.get('mongodb'))
    collection = factory.gmaps_collection()
    obj = collection.find_one({'code': id})
    return render_template('admin/gmap/unit.html', data=obj, api_key=api_key)


@app.route('/wiki/')
@app.route('/wiki/<string:country>')
def wiki_list(country=None):
    return render_template('admin/wiki/list.html', country=country)


@app.route('/wiki/unit/<string:id>')
def wiki_unit(id):
    config = Config('./config/config.yml')
    api_key = config.get('googlemaps').get('geocoding').get('key')
    factory = DocFactory(config.get('mongodb'))
    collection = factory.wiki_collection()
    obj = collection.find_one({'_id': ObjectId(id)})
    return render_template('admin/wiki/unit.html', data=obj, api_key=api_key)


@app.route('/wiki/unit/code/<string:id>')
def wiki_code_unit(id):
    config = Config('./config/config.yml')
    api_key = config.get('googlemaps').get('geocoding').get('key')
    factory = DocFactory(config.get('mongodb'))
    collection = factory.wiki_collection()
    obj = collection.find_one({'code': id})
    return render_template('admin/wiki/unit.html', data=obj, api_key=api_key)


@app.route('/insee/unit/code/<string:id>')
def insee_code_unit(id):
    config = Config('./config/config.yml')
    factory = DocFactory(config.get('mongodb'))
    collection = factory.insee_collection()
    obj = collection.find_one({'code': id})
    return render_template('admin/other/unit.html', data=obj)


@app.route('/tasks/<string:journal_id>')
@app.route('/tasks/<string:journal_id>/<string:status>')
def tasks_list(journal_id, status='active'):
    config = Config('./config/config.yml')
    storage = JobStorage(job_name=journal_id, storage_config=config.get('mongodb'))

    if status == storage.STATUS_COMPLETE:
        tasks = storage.get_complete()
    elif status == storage.STATUS_IN_PROGRESS:
        tasks = storage.get_in_progress()
    else:
        tasks = storage.get_active()

    return render_template('admin/tasks/list.html',
                           name=journal_id,
                           tasks=tasks
                           )


@app.route('/tasks/remove/<string:journal_id>')
def clear_tasks(journal_id):
    config = Config('./config/config.yml')
    storage = JobStorage(job_name=journal_id, storage_config=config.get('mongodb'))
    storage.clear()
    return render_template('admin/empty.html', data='ok', auto_close=True)


@app.route('/logs/<string:name>/<int:status>')
def logs(name, status=None):
    config = Config('./config/config.yml').get('mongodb')
    connection = MongoClient(config['host'], config['port'])
    collection = connection.log[name]
    if status == 1:
        query = {'$and': [{
            'message': {'$exists': True}},
            {'$or': [{'status': status}, {'status': {'$exists': False}}]}
        ]}
    elif status:
        query = {'message': {'$exists': True}, 'status': status}
    else:
        query = {'message': {'$exists': True}}
    return render_template('admin/logs/list.html', logs=collection.find(query), name=name)


@app.route('/logs/remove/<string:name>')
def clear_logs(name):
    config = Config('./config/config.yml').get('mongodb')
    connection = MongoClient(config['host'], config['port'])
    connection.log[name].delete_many({})
    return render_template('admin/empty.html', data='ok', auto_close=True)


@app.route('/logs/close/<string:name>/<string:id>')
def log_close(name, id):
    config = Config('./config/config.yml').get('mongodb')
    log = MongoDBLog(log_name=name, config=config)
    return 'Ok' if log.close(id) else 'Not'


@app.route('/clear/wiki/<string:name>')
def clear_wiki_country(name):
    config = Config('./config/config.yml').get('mongodb')
    factory = DocFactory(config)
    collection = factory.wiki_collection()
    result = collection.delete_many({'admin_hierarchy.ADMIN_LEVEL_1.name': name})
    return render_template('admin/empty.html', data=['ok', result.deleted_count], auto_close=True)


@app.route('/clear/gmaps/<string:name>')
def clear_gmaps_country(name):
    config = Config('./config/config.yml').get('mongodb')
    factory = DocFactory(config)
    collection = factory.gmaps_collection()
    result = collection.delete_many({'admin_hierarchy.ADMIN_LEVEL_1.name': name})
    return render_template('admin/empty.html', data=['ok', result.deleted_count], auto_close=True)


@app.route('/test/wiki')
def test_wiki():
    pass


@app.route('/test/gmap')
def test_gmap():
    get = request.args.copy()
    raw = {}
    parsed = []
    if get:
        use_cache = bool(get.get('use_cache', True))
        method = get.get('method', 'address')
        language = get.get('lang', 'en')
        config = Config('./config/config.yml')
        gmap_config = config.get('googlemaps')
        gmap_config.update(language=language)

        gmap_loader = LoaderFactory.loader_gmaps_with_cache(gmaps_config=gmap_config,
                                                            storage_config=config.get('mongodb'))
        spider = Spider(
            loader_factory=LoaderFactory,
            gmap_parser=MapFactory.france,
            language=language,
            config=config,
            use_cache=use_cache
        )

        if method == 'address':
            address = get.get('address', 'Magadan')
            raw = gmap_loader.by_address(address, use_cache=use_cache)
        elif method == 'position':
            lat = get.get('latitude', 59.558208)
            lng = get.get('longitude', 150.822794)
            raw = gmap_loader.by_position(lat=lat, lng=lng, use_cache=use_cache)
        elif method == 'place_id':
            place_id = get.get('place_id', 'ChIJ6UpSLYGEaVkROrwiAnFmzXw')
            raw = gmap_loader.by_place_id(place_id=place_id, use_cache=use_cache)
        elif method == 'address_type':
            address = get.get('address', 'Magadan')
            type = get.get('type', 'locality')
            raw = spider.gmap_loader.by_places(address=address, use_cache=spider.use_cache)
            parsed = spider.get_place_ids_by_address_for_type(address=address, type=type)

        if method in ['address', 'position', 'place_id']:
            objects = MapFactory.france(raw)

            for element in objects:
                parsed.append(element.as_dictionary())

    return render_template('admin/gmap/test.html', form_data=get, raw=raw, parsed=parsed)


@app.route('/recursive/parsed_page/<string:name>')
def recursive_parsed_page_cache(name):
    config = Config('./config/config.yml').get('mongodb')
    connection = MongoClient(config['host'], config['port'])
    objects = connection.parsed_page[name].find()

    return render_template('admin/recursive/list.html', items=objects, name='Parsed page')


@app.route('/recursive/parsed_page/drop/<string:name>')
def recursive_parsed_page_drop(name):
    config = Config('./config/config.yml').get('mongodb')
    connection = MongoClient(config['host'], config['port'])
    connection.parsed_page[name].drop()

    return render_template('admin/empty.html', data='ok', auto_close=True)


@app.route('/recursive/url_pool/drop/<string:name>')
def recursive_url_pool_drop(name):
    config = Config('./config/config.yml').get('mongodb')
    connection = MongoClient(config['host'], config['port'])
    connection.url_pool[name].drop()

    return render_template('admin/empty.html', data='ok', auto_close=True)


@app.route('/recursive/url_pool/<string:name>')
def recursive_url_pool_cache(name):
    config = Config('./config/config.yml').get('mongodb')
    connection = MongoClient(config['host'], config['port'])
    objects = connection.url_pool[name].find({})

    return render_template('admin/recursive/list.html', items=objects, name='Url pool')


@app.route('/recursive')
def recursive_cache_list():
    config = Config('./config/config.yml').get('mongodb')
    connection = MongoClient(config['host'], config['port'])
    parsed_page = connection.parsed_page
    parsed_page_names = parsed_page.collection_names(False)

    url_pool = connection.url_pool
    url_pool_names = url_pool.collection_names(False)

    return render_template('admin/recursive/link_list.html',
                           parsed_page=parsed_page,
                           url_pool=url_pool,
                           parsed_page_names=parsed_page_names,
                           url_pool_names=url_pool_names
                           )


@app.route('/worth-it/<string:word>')
def secret_page(word):
    md5 = hashlib.md5()
    md5.update(word.encode('utf-8'))
    code = md5.hexdigest()
    if code != 'e37d7c242913151ee9d7d794f2027128':
        return render_template('admin/empty.html', data=403)

    return render_template('admin/worth-it/debug.html')
