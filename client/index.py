from flask import Flask
from flask import render_template
from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.config.Yaml import Yaml as Config
from lib.job.storage.MongoDB import MongoDB as JobStorage


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('admin/index.html')


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/home/')
@app.route('/home/<name>')
def home(name=None):
    return render_template('home.html', name=name)

@app.route('/gmaps/')
@app.route('/gmaps/<string:country>')
def gmaps_list(country=None):
    config = Config('./config/config.yml')

    factory = DocFactory(config.get('mongodb'))
    gmaps = factory.gmaps_collection()
    if country:
        filter = {
            'name': { '$exists': True, '$not': {'$size': 0}},
            'admin_hierarchy.0.name': '/^{}$/i'.format(country)
        }
    else:
        filter = {'name': { '$exists': True, '$not': {'$size': 0}}}

    objects = gmaps.find(filter)
    count = objects.count()
    return render_template('admin/gmaps/list.html', items=objects, filter=filter)


@app.route('/gmaps/test')
def gmaps_test():
    return render_template('admin/gmaps/test.html')


@app.route('/wiki/')
@app.route('/wiki/<string:country>')
def wiki_list(country=None):
    config = Config('./config/config.yml')

    factory = DocFactory(config.get('mongodb'))
    wiki = factory.wiki_collection()
    if country:
        filter = {
            'name': { '$exists': True, '$not': {'$size': 0}},
            'admin_hierarchy.0.name': '/^{}$/i'.format(country)
        }
    else:
        filter = {'name': { '$exists': True, '$not': {'$size': 0}}}
    objects = wiki.find(filter)
    count = objects.count()
    return render_template('admin/wiki/list.html', items=objects, count=count)


@app.route('/wiki/test')
def wiki_test():
    return render_template('admin/wiki/test.html')


@app.route('/tasks/<string:jornal_id>')
def tasks_list(jornal_id):
    config = Config('./config/config.yml')
    storage = JobStorage(job_name=jornal_id,storage_config=config.get('mongodb'))
    return render_template('admin/tasks/list.html',
                           active=storage.get_active(),
                           in_progress=storage.get_in_progress(),
                           complete=storage.get_complete()
                           )


@app.route('/logs/')
def logs(id):
    return render_template('admin/logs/entity.html')