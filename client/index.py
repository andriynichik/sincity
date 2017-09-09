from flask import Flask
from flask import render_template
from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.config.Yaml import Yaml as Config
from lib.job.storage.MongoDB import MongoDB as JobStorage
from pymongo import MongoClient
import re
from lib.location.Wiki import Wiki
from lib.location.GMap import GMap


app = Flask(__name__)


def escape(val):
    return re.escape(str(val))


@app.route("/")
def index():
    return render_template('admin/index.html')


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


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


@app.route('/gmaps/test')
def gmaps_test():
    return render_template('admin/gmap/test.html')


@app.route('/wiki/')
@app.route('/wiki/<string:country>')
def wiki_list(country=None):
    return render_template('admin/wiki/list.html', country=country)


@app.route('/wiki/test')
def wiki_test():
    return render_template('admin/wiki/test.html')


@app.route('/tasks/<string:jornal_id>')
@app.route('/tasks/<string:jornal_id>/<string:status>')
def tasks_list(jornal_id, status='active'):
    config = Config('./config/config.yml')
    storage = JobStorage(job_name=jornal_id,storage_config=config.get('mongodb'))

    if status == storage.STATUS_COMPLETE:
        tasks = storage.get_complete()
    elif status == storage.STATUS_IN_PROGRESS:
        tasks = storage.get_in_progress()
    else:
        tasks = storage.get_active()

    return render_template('admin/tasks/list.html',
                           name=jornal_id,
                           tasks=tasks
                           )


@app.route('/logs/')
def logs():
    config = Config('./config/config.yml').get('mongodb')
    connection = MongoClient(config['host'], config['port'])
    collection = connection.log['wiki_request']
    return render_template('admin/logs/list.html', logs=collection.find({'message': {'$exists': True}}))