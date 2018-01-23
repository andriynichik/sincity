from application import app
from flask.ext.login import login_user, logout_user, login_required
from lib.config.Yaml import Yaml as Config
from lib.factory.StorageLocation import StorageLocation as DocFactory
from flask import render_template
from urllib.parse import unquote_plus
from lib.compare.Comparison import Comparison
from re import escape
from flask import request, redirect, render_template, url_for, flash, session, abort

@app.route('/data/matching-france-<string:region>.js')
@login_required
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
@login_required
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


@app.route('/insee/unit/code/<string:id>')
@login_required
def insee_code_unit(id):
    config = Config('./config/config.yml')
    factory = DocFactory(config.get('mongodb'))
    collection = factory.insee_collection()
    obj = collection.find_one({'code': id})
    return render_template('admin/other/unit.html', data=obj)