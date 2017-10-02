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


app = Flask(__name__)


def escape(val):
    return re.escape(str(val))


@app.route("/")
def index():
    return render_template('admin/index.html')


@app.route('/internal/<string:country>')
def internal(country=None):
    return render_template('admin/internal/list.html', country=country)


@app.route('/internal/unit/<string:id>')
def internal_unit(id):
    config = Config('./config/config.yml')
    api_key = config.get('googlemaps').get('geocoding')
    factory = DocFactory(config.get('mongodb'))
    collection = factory.gmaps_collection()
    obj = collection.find_one({'_id': ObjectId(id)})
    return render_template('admin/gmap/unit.html', data=obj, api_key=api_key)


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
                'admin_hierarchy': {'$elemMatch': {'name': country}}
            }
    elif provider_type == GMap.TYPE:
        data = factory.gmaps_collection()
        if country:
            document_filter = {
                'name': {'$exists': True, '$not': {'$size': 0}},
                'admin_hierarchy': {'$elemMatch': {'name': country}}
            }
    else:
        data = factory.internal_collection()

    if not document_filter:
        document_filter = {'name': {'$exists': True, '$not': {'$size': 0}}}

    objects = data.find(document_filter)
    return render_template('admin/{}/list.js'.format(provider_type), e=escape, items=objects)


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
    result = collection.delete_many({'admin_hierarchy': {'$elemMatch': {'name': name}}})
    return render_template('admin/empty.html', data=['ok', result.deleted_count], auto_close=True)

@app.route('/clear/gmaps/<string:name>')
def clear_gmaps_country(name):
    config = Config('./config/config.yml').get('mongodb')
    factory = DocFactory(config)
    collection = factory.gmaps_collection()
    result = collection.delete_many({'admin_hierarchy': {'$elemMatch': {'name': name}}})
    return render_template('admin/empty.html', data=['ok', result.deleted_count], auto_close=True)


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
