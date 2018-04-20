from application import app
from application import lm
from flask import render_template
from lib.factory.StorageLocation import StorageLocation as DocFactory
from lib.config.Yaml import Yaml as Config
from lib.job.storage.MongoDB import MongoDB as JobStorage
from pymongo import MongoClient
import re
from werkzeug.security import generate_password_hash
from lib.location.Wiki import Wiki
from lib.location.GMap import GMap
from lib.logger.MongoDB import MongoDB as MongoDBLog
import hashlib
from bson.objectid import ObjectId
from flask import request
from flask import redirect
from flask import url_for
from lib.factory.Loader import Loader as LoaderFactory
from lib.parser.map.google.GMapFactory import GMapFactory as MapFactory
from lib.spider.Spider import Spider
from application.forms import LoginForm
from application.user import User
from flask.ext.login import login_user, logout_user, login_required
from flask import request, redirect, render_template, url_for, flash, session, abort
from lib.keygen.gmap_keygen import Keygen
from lib.factory.Loader import Loader 
import json
import requests
import random
import os
import urllib.parse



def escape(val):
    return re.escape(str(val))


@app.route("/")
@login_required
def index():
    return render_template('admin/index.html')

def generate_code():
    return str(random.randrange(100000, 999999))

def send_confirmation_code(to_number):
    verification_code = generate_code()
    session['verification_code'] = verification_code
    headers = {'Content-type': 'application/json',  
           'Accept': 'text/plain',
           'Content-Encoding': 'utf-8'}
    data = {"to":str(to_number) , "message":"Код підтвердження авторизації Sinoptik Parser: "+str(verification_code)+""}
    response = requests.post('http://sms-gate.ukr.net/sms/send', data=json.dumps(data), headers=headers)

    # verification_code = generate_code()
    # send_sms(to_number, verification_code)
    # session['verification_code'] = verification_code
    # return verification_code


@app.route("/confirm", methods=['GET', 'POST'] )
def confirm():
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.local
    user = db.users.find_one({"_id": session.get('userphone', '')}) or abort(401)
    print (session.get('userphone', ''))
    if request.method == 'POST':
        is_valid_code = request.form['verification_code'] == session['verification_code']
        is_dev_env = os.environ.get('DEV_ENV')
        if is_valid_code or is_dev_env:
            user_obj = User(user['_id'])
            login_user(user_obj)
            return redirect(url_for('index'))
    return render_template('admin/login/confirm.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.local
    if request.method == 'POST' and form.validate_on_submit():
        user = db.users.find_one({"_id": form.username.data})
        if user and User.validate_login(user['password'], form.password.data):
            # user_obj = User(user['_id'])
            session['userphone'] = user['_id']
            send_confirmation_code(user['_id'])
            return redirect(url_for('confirm'))
            # login_user(user_obj)
            flash("Logged in successfully!", category='success')
            # return redirect(url_for('index'))
        flash("Wrong username or password!", category='error')
    return render_template('admin/login/sign-in.html', form=form)

@lm.user_loader
def load_user(username):
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.local
    u = db.users.find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])


@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))

@app.route('/internal')
@app.route('/internal/<string:country>')
@login_required
def internal_list(country=None):
    return render_template('admin/internal/list.html', country=country)


@app.route('/internal/unit/<string:id>')
@login_required
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
@login_required
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
@login_required
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

@login_required
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
@login_required
def internal_delete(id):
    config = Config('./config/config.yml')
    factory = DocFactory(config.get('mongodb'))
    collection = factory.internal_collection()
    result = collection.delete_many({'_id': ObjectId(id)})
    return render_template('admin/empty.html', data='ok', auto_close=True)


@app.route('/data/<string:provider_type>.js')
@app.route('/data/<string:provider_type>/<string:country>.js')
@login_required
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


@app.route('/matching/belarus')
@app.route('/matching/belarus/<string:region>')
@login_required
def matching_belarus(region=None, provincia=None):
    mode = request.args.get('mode', 'none')
    Provincia = {
            '1':'Брестская', 
            '2':'Витебская', 
            '3':'Гомельская', 
            '4':'Гродненская',
            '5':'Минская', 
            '6':'Могилевская', 
            '7':'Минск',
            }
    if region is None:
        return render_template('admin/belarus/region-list.html', data=Provincia)
    else:
        config = Config('./config/config.yml')
        mongo_config = config.get('mongodb')
        connection = MongoClient(mongo_config['host'], mongo_config['port'])
        db = connection.location
        data =  db.belarus.find({'NAMEDISTR': str(region)})
        return render_template('admin/belarus/list.html', com = 0,  data=data)

##############################################
# SPAIN
##############################################
@app.route('/matching/spain/')
@app.route('/matching/spain/<string:region>/<string:provincia>')
@login_required
def matching_spain(region=None, provincia=None):
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
    types = {"Municipio": ["administrative_area_level_4"],
            "Entidad colectiva" :  ["administrative_area_level_5", "neighborhood"],
            "Otras entidades": ["locality", "neighborhood"],
            "Capital de municipio":["locality"],
            "Entidad singular": ["locality"]}
    if region is None:
 


        return render_template('admin/matching-spain/region-list.html', data=Provincia)
    else:
        config = Config('./config/config.yml')
        mongo_config = config.get('mongodb')
        connection = MongoClient(mongo_config['host'], mongo_config['port'])
        db = connection.location
        data =  db.internal.find({'20_SNIG_COD_PROV': int(region)})
        return render_template('admin/matching-spain/list.html', region=Provincia[str(region)], com = 0, types=types, data=data)

@app.route('/sinoptik_db_confirm', methods=['GET', 'POST'])
@login_required
def sinoptik_db_confirm():

    # return render_template('admin/gmap/list.html', country=country)
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.location
    db.spain_sql_sinoptik.update_one({"_id" : ObjectId(request.form['id']) },{"$set" : {"status":4}})
    return request.form['id'] 

@app.route('/sinoptik_db_delete-confirm', methods=['GET', 'POST'])
@login_required
def sinoptik_db_delete_status_confirm():

    # return render_template('admin/gmap/list.html', country=country)
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.location
    db.spain_sql_sinoptik.update_one({"_id" : ObjectId(request.form['id']) },{"$unset" : {"status":4}})
    return request.form['id'] 

@app.route('/sinoptik_db_reparse', methods=['GET', 'POST'])
@login_required
def sinoptik_db_reparse():

    # return render_template('admin/gmap/list.html', country=country)
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.location

    # db.spain_sql_sinoptik.update_one({"_id" : ObjectId(request.form['id']) },{"$set" : {"status":4}})
    


    row =  db.spain_sql_sinoptik.find_one({"_id" : ObjectId(request.form['sinoptik_id'])})
    
    parce_data =  db.internal.find_one({"_id" : ObjectId(request.form['parser_id'])})
    if parce_data is not None:
        # print(row['city_title'])
        # print (parce_data)
        comparison = getDistance(row['lat'], row['lng'], parce_data['28_SNIG_LATITUD_ETRS89'], parce_data['29_SNIG_LONGITUD_ETRS89'])
        comparison_url =("https://www.google.com.ua/maps/dir/"+str(row['lat'])+","+str(row['lng'])+"/"+str(parce_data['28_SNIG_LATITUD_ETRS89'])+","+str(parce_data['29_SNIG_LONGITUD_ETRS89'])+"")
        db.spain_sql_sinoptik.update_one(
                {"_id": row['_id'] },
                    {
                        "$set": {
                        "parser_id": parce_data['_id'],
                        "comparison": comparison,
                        "SNIG_NOMBRE": parce_data['24_SNIG_NOMBRE'],
                        "comparison_url":comparison_url,
                        
                    }
               }
        )
    status = True
    if comparison >= 2:
        status = False

    responce = {
                # "parser_id": ObjectId(parce_data['_id']),
                "comparison": comparison,
                "SNIG_NOMBRE": parce_data['24_SNIG_NOMBRE'],
                "comparison_url":comparison_url,
                "comparison_status":status,

    }
    return json.dumps(responce)



@app.route('/matching-spain-update_snig', methods=['GET', 'POST'])
@login_required
def update_status_snig():

    # return render_template('admin/gmap/list.html', country=country)
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.location
    db.internal.update_one({"_id" : ObjectId(request.form['id']) },{"$set" : {"status_snig":1}})
    return request.form['id'] 

@app.route('/matching-spain-delete-confirm_snig', methods=['GET', 'POST'])
@login_required
def delete_status_confirm_snig():

    # return render_template('admin/gmap/list.html', country=country)
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.location
    db.internal.update_one({"_id" : ObjectId(request.form['id']) },{"$unset" : {"status_snig":1}})
    return request.form['id'] 




@app.route('/matching-spain-update', methods=['GET', 'POST'])
@login_required
def update_status():

    # return render_template('admin/gmap/list.html', country=country)
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.location
    db.internal.update_one({"_id" : ObjectId(request.form['id']) },{"$set" : {"status":4}})
    return request.form['id'] 

@app.route('/matching-spain-delete-confirm', methods=['GET', 'POST'])
@login_required
def delete_status_confirm():

    # return render_template('admin/gmap/list.html', country=country)
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.location
    db.internal.update_one({"_id" : ObjectId(request.form['id']) },{"$unset" : {"status":4}})
    return request.form['id'] 




def getDistance(lat1,lon1,lat2,lon2):
    Key = Keygen()
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins='+str(lat1)+','+str(lon1)+'&destinations='+str(lat2)+','+str(lon2)+'&key='+str(Key.get_key_distance())+''
    # print(url)
    response = requests.get(url)
    data = response.json()
    try:
        resp = data['rows'][0]['elements'][0]['distance']['value'] / 1000
    except Exception as e:
        resp = 0
    
    print (round(resp, 2))
    return round(resp, 2)

@app.route('/spain-reparse_by_geocode', methods=['GET', 'POST'])
@login_required
def reparse_by_geocode():

    # return render_template('admin/gmap/list.html', country=country)
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    # use_cache = bool(get.get('use_cache', True))
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.location
    doc = db.internal.find_one({"_id" : ObjectId(request.form['id']) })
    doc_factory = DocFactory(config.get('mongodb'))
    Key = Keygen()
    keyAPI =  Key.get_key_place()
    if not keyAPI:
        sys.exit()
    cnf = {'googlemaps':{'geocoding':{'key': keyAPI}}}
    config.set(cnf)
    gmap_config = config.get('googlemaps')
    # gmap_config.update(language=language)
    language = 'es'

    gmap_loader = LoaderFactory.loader_gmaps_with_cache(gmaps_config=gmap_config,
                                                            storage_config=config.get('mongodb'))
    spider = Spider(
            loader_factory=LoaderFactory,
            gmap_parser=MapFactory.spain,
            doc_factory=doc_factory,
            language=language,
            config=config,
            use_cache=True
    )
    if request.form['type'] == "autocomplete":
        raw = gmap_loader.by_places(doc['08_INE_Name_w_Article'] + ', España')
        return json.dumps(raw)
    else:
        objects = spider.get_gmap_place_id(request.form['place_id'])
        gmap = {}
        gmap = objects[0].get_document()
        try:
            if gmap['name'].lower().lstrip().strip() == doc['08_INE_Name_w_Article'].lower().lstrip().strip():
                gmap['comparison'] = True
            else:
                gmap['comparison'] = False
        except Exception as e: 
            gmap['comparison'] = False

        gmap['15_GMap_center_SNIG_comparison'] = getDistance(gmap['center']['lat'], gmap['center']['lng'],doc['28_SNIG_LATITUD_ETRS89'],doc['29_SNIG_LONGITUD_ETRS89'])
        gmap['15_gmap_comparison_url'] =("https://www.google.com.ua/maps/dir/"+str(gmap['center']['lat'])+","+str(gmap['center']['lng'])+"/"+str(doc['28_SNIG_LATITUD_ETRS89'])+","+str(doc['29_SNIG_LONGITUD_ETRS89'])+"")
        db.internal.update_one(
                {"_id": ObjectId(request.form['id']) },
                    {
                        "$set": {
                        "10_gmap_name": gmap.get('name'),
                        "17_gmap_admin_hierarchy": gmap.get('admin_hierarchy', {}),
                        "gmap_center": gmap.get('center'),
                        "gmap_bounds": gmap.get('bounds'),
                        "12_gmap_type": gmap.get('type'),
                        "15_GMap_center_SNIG_comparison": gmap.get('15_GMap_center_SNIG_comparison'),
                        "15_gmap_comparison_url": gmap.get('15_gmap_comparison_url'),
                        "11_gmap_comparison" : gmap['comparison']
                        
                    }
               }
        )
        gmap.pop('_id')
        # gmap['15_GMap_center_SNIG_comparison'] = getDistance(gmap['center']['lat'], gmap['center']['lng'],doc['28_SNIG_LATITUD_ETRS89'],doc['29_SNIG_LONGITUD_ETRS89'])
        if gmap['15_GMap_center_SNIG_comparison'] <= 1:
            gm_comp_status = True
        else:
            gm_comp_status = False

        types = {"Municipio": ["administrative_area_level_4"],
            "Entidad colectiva" :  ["administrative_area_level_5", "neighborhood"],
            "Otras entidades": ["locality", "neighborhood"],
            "Capital de municipio":["locality"],
            "Entidad singular": ["locality"]}
        if gmap.get('type') in types[doc['25_SNIG_TIPO']]:
            gm_type_status = True
        else:
            gm_type_status = False

        raw = {
                "gmap_name": gmap.get('name'),
                "gmap_name_status" : gmap['comparison'],
                "gmap_type": gmap.get('type'),
                "15_GMap_center_SNIG_comparison": gmap.get('15_GMap_center_SNIG_comparison'),
                "15_gmap_comparison_url": gmap.get('15_gmap_comparison_url'),
                "gmap_comp_status":gm_comp_status,
                "gmap_type_status":gm_type_status,

            }
        
        return json.dumps(raw)




@app.route('/sinoptik_db/spain',  methods=['GET', 'POST'])
@login_required
def sinoptik_db():
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.location
    data_db = db.spain_sql_sinoptik.find()
    # data = list()
    # array = dict()
    # for item in data_db:
    #     # array['sinoptik_db'] = item
    #     # print (item['title'])
    #     if 'parser_id' in item:
    #         ntype = db.internal.find_one({"_id" : item['parser_id']})
    #         data_db['type_snig'] = ntype["25_SNIG_TIPO"]
        
        # data.append(array)

    return render_template('admin/matching-spain/sinoptik_db.html', data=data_db)

##############################################
# END SPAIN
##############################################
@app.route('/sinoptik_db/romania',  methods=['GET', 'POST'])
@login_required
def sinoptik_db_romania():
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.location
    data_db = db.sinoplik_romania.find()
    # data = list()
    # array = dict()
    # for item in data_db:
    #     # array['sinoptik_db'] = item
    #     # print (item['title'])
    #     if 'parser_id' in item:
    #         ntype = db.internal.find_one({"_id" : item['parser_id']})
    #         data_db['type_snig'] = ntype["25_SNIG_TIPO"]
        
        # data.append(array)

    return render_template('admin/romania/sinoptik_db.html', data=data_db)


@app.route('/sinoptik_db_confirm_romania', methods=['GET', 'POST'])
@login_required
def sinoptik_db_confirm_romania():

    # return render_template('admin/gmap/list.html', country=country)
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.location
    db.sinoplik_romania.update_one({"_id" : ObjectId(request.form['id']) },{"$set" : {"status":4}})
    return request.form['id'] 

@app.route('/sinoptik_db_delete-confirm_romania', methods=['GET', 'POST'])
@login_required
def sinoptik_db_delete_status_confirm_romania():

    # return render_template('admin/gmap/list.html', country=country)
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.location
    db.sinoplik_romania.update_one({"_id" : ObjectId(request.form['id']) },{"$unset" : {"status":4}})
    return request.form['id'] 

@app.route('/sinoptik_db_reparse_romania', methods=['GET', 'POST'])
def sinoptik_db_reparse_romania():

    # return render_template('admin/gmap/list.html', country=country)
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.location

    # db.spain_sql_sinoptik.update_one({"_id" : ObjectId(request.form['id']) },{"$set" : {"status":4}})
    


    row =  db.sinoplik_romania.find_one({"_id" : ObjectId(request.form['sinoptik_id'])})
    
    parce_data =  db.romania.find_one({"_id" : ObjectId(request.form['parser_id'])})
    if parce_data is not None:
        # print(row['city_title'])
        # print (parce_data)
        
        if 'wiki_center' in parce_data:
            comparison = getDistance(row['lat'], row['lng'], parce_data["wiki_center"]["lat"], parce_data["wiki_center"]["lng"])
            comparison_url =("https://www.google.com.ua/maps/dir/"+str(row['lat'])+","+str(row['lng'])+"/"+str(parce_data["wiki_center"]["lat"])+","+str(parce_data["wiki_center"]["lng"])+"")

        else:
            comparison = False
            comparison_url = '#'

        db.sinoplik_romania.update_one(
                    {"_id": row['_id'] },
                        {
                            "$set": {
                            "parser_id": parce_data['_id'],
                            "comparison": comparison,
                            "SNIG_NOMBRE": parce_data['DENLOC'],
                            "comparison_url":comparison_url,
                            
                        }
                   }
            )

    status = True
    if comparison >= 2:
        status = False

    responce = {
                # "parser_id": ObjectId(parce_data['_id']),
                "comparison": comparison,
                "SNIG_NOMBRE": parce_data['DENLOC'],
                "comparison_url":comparison_url,
                "comparison_status":status,

    }
    return json.dumps(responce)



@app.route('/matching/romania')
@app.route('/matching/romania/<string:region>')
@login_required
def matching_romania(region=None):
    mode = request.args.get('mode', 'none')
    Provincia = {
                '1' : 'NORD-EST',
                '2' : 'SUD-EST',
                '3' : 'SUD  - MUNTENIA',
                '4' : 'SUD-VEST - OLTENIA',
                '5' : 'VEST',
                '6' : 'NORD-VEST',
                '7' : 'CENTRU', 
                '8' : 'BUCURESTI - ILFOV',
      
            }

    if region is None:
 


        return render_template('admin/romania/region-list.html', data=Provincia)
    else:
        TIP_Name ={
            "40":"Judet_admin",
            "1":"Municipiu_admin_resedinta_judet",
            "2":"Oras_admin",
            "3":"Comuna_admin",
            "4":"Municipiu_admin",
            "5":"Oras_admin_resedinta_judet",
            "6":"Sectoarele_Bucuresti",
            "9":"Town_resedinta_municipiu",
            "10":"Town_municipiu",
            "11":"Willage_municipiu",
            "17":"Town_resedinta_orasului",
            "18":"Town_orasului",
            "19":"Willage_orasului",
            "22":"Willage_resedinta_comuna",
            "23":"Willage_comuna",
        }

        types = {
            "40": ["administrative_area_level_1"],
            "1":    ["administrative_area_level_2"],
            "2":    ["administrative_area_level_2"],
            "3":    ["administrative_area_level_2"],    
            "4":    ["administrative_area_level_2"],    
            "5":    ["administrative_area_level_2"],    
            "6":    ["sublocality_level_1"],    
            "9":    ["locality","sublocality_level_1"],
            "10":   ["locality","sublocality_level_1"],
            "11":   ["locality","sublocality_level_1"],
            "17":   ["locality","sublocality_level_1"],
            "18":   ["locality","sublocality_level_1"],
            "19":   ["locality","sublocality_level_1"],
            "22":   ["locality","sublocality_level_1"],
            "23":   ["locality","sublocality_level_1"]
        }
        config = Config('./config/config.yml')
        mongo_config = config.get('mongodb')
        connection = MongoClient(mongo_config['host'], mongo_config['port'])
        db = connection.location
        data =  db.romania.find({'REGIUNE': int(region)})
        return render_template('admin/romania/list.html', region=Provincia[str(region)], types=types, tip_name=TIP_Name,  com = 0, data=data)

@login_required
@app.route('/romania-reparse_wiki', methods=['GET', 'POST'])
def romania_reparse_wik():

    from lib.parser.wiki.romania import Romania as WikiRo
    country = 'Romania'
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    conn =  MongoClient(mongo_config['host'], mongo_config['port'])
    db = conn.location
    doc_factory = DocFactory(config.get('mongodb'))
    loader = Loader.loader_with_mongodb(config.get('mongodb'))
    headers = {'User-Agent': 'Mozilla/5.0'}
    language='ro'
    wiki_url_r = urllib.parse.quote(request.form['wiki_url'], safe=":/")
 

    doc = doc_factory.wiki(wiki_url_r)
    page, code = loader.load(wiki_url_r, headers=headers)
    page_parser = WikiRo(page)
    data = page_parser.as_dictionary()

    doc_mongo = db.romania.find_one({"_id" : ObjectId(request.form['wiki_mongo']) })
    if 'gmap_center' in doc_mongo:
        
        center_gm = doc_mongo['gmap_center']
        center_wiki = data.get('center')
        gmap_comparison_url =  ("https://www.google.com.ua/maps/dir/"+str(center_gm['lat'])+","+str(center_gm['lng'])+"/"+str(center_wiki["lat"])+","+str(center_wiki["lng"])+"")
        # gmap_comparison_url = 
        distance =  getDistance(center_gm["lat"],center_gm["lng"], center_wiki["lat"], center_wiki["lng"])
        db.romania.update_one(
                                {"_id": ObjectId(request.form['wiki_mongo'])},
                                    {
                                        "$set": {
                                        
                                        'wiki_name': data.get('name'),
                                        'wiki_admin_hierarchy': data.get('admin_hierarchy', {}),
                                        'wiki_center': data.get('center'),
                                        'wiki_url': str(request.form['wiki_url']),
                                            'gmap_wiki_distance': distance,
                                        'wiki_postal_code': data.get('postal_codes'),
                                        
                                    }
                               }
                        )

        if distance < 2:
            distance_status = True
        else:
            distance_status = False
    
    else:
        distance_status = False
        distance = False
        gmap_comparison_url = '#'
        db.romania.update_one(
                                {"_id": ObjectId(request.form['wiki_mongo'])},
                                    {
                                        "$set": {
                                        
                                        'wiki_name': data.get('name'),
                                        'wiki_admin_hierarchy': data.get('admin_hierarchy', {}),
                                        'wiki_center': data.get('center'),
                                        'wiki_url': str(request.form['wiki_url']),
                                        'wiki_postal_code': data.get('postal_codes'),
                                        
                                    }
                               }
                        )




    resp = {
        "distance_status":distance_status,
        "distance":distance,
        "gmap_comparison_url":gmap_comparison_url,
        'wiki_name': data.get('name'),
        'wiki_center': data.get('center'),

    }
    return json.dumps(resp)

@app.context_processor
def utility_processor():
    def autocomplete(pid):
        config = Config('./config/config.yml')
        mongo_config = config.get('mongodb')
        connection = MongoClient(mongo_config['host'], mongo_config['port'])
        db = connection.location
        db.romania.update_one({"_id" : ObjectId(pid) },{"$set" : {"status_autoconfirm":1}})
        return str('')
    return dict(autocomplete = autocomplete)


@app.context_processor
def dublicate():
    def isdub(lat, lng):
        config = Config('./config/config.yml')
        mongo_config = config.get('mongodb')
        connection = MongoClient(mongo_config['host'], mongo_config['port'])
        db = connection.location
        cnt = db.internal.find({"28_SNIG_LATITUD_ETRS89":lat, "29_SNIG_LONGITUD_ETRS89":lng}).count()
        if cnt > 1:
            return "True"
        else:
            return "False"
    return dict(isdub = isdub)

@app.route('/matching-romania-confirm', methods=['GET', 'POST'])
@login_required
def romania_confirm():

    # return render_template('admin/gmap/list.html', country=country)
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.location
    db.romania.update_one({"_id" : ObjectId(request.form['id']) },{"$set" : {"status_snig":1}})
    return request.form['id'] 

@app.route('/matching-romania-confirm_ins', methods=['GET', 'POST'])
@login_required
def romania_confirm_ins():

    # return render_template('admin/gmap/list.html', country=country)
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.location
    db.romania.update_one({"_id" : ObjectId(request.form['id']) },{"$set" : {"status_ins":1}})
    return request.form['id'] 


@login_required
def romania_confirm():

    # return render_template('admin/gmap/list.html', country=country)
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.location
    db.romania.update_one({"_id" : ObjectId(request.form['id']) },{"$set" : {"status_autoconfirm":1}})
    return request.form['id'] 



@app.route('/matching-romania-confirm_del_ins', methods=['GET', 'POST'])
@login_required
def romania_confirm_del():

    # return render_template('admin/gmap/list.html', country=country)
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.location
    db.romania.update_one({"_id" : ObjectId(request.form['id']) },{"$unset" : {"status_snig":1}})
    return request.form['id'] 


@app.route('/romania-reparse_by_geocode', methods=['GET', 'POST'])
@login_required
def romania_reparse_by_geocode():

    # return render_template('admin/gmap/list.html', country=country)
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    # use_cache = bool(get.get('use_cache', True))
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.location
    doc = db.romania.find_one({"_id" : ObjectId(request.form['id']) })
    doc_factory = DocFactory(config.get('mongodb'))
    Key = Keygen()
    keyAPI =  Key.get_key_place()
    if not keyAPI:
        sys.exit()
    cnf = {'googlemaps':{'geocoding':{'key': keyAPI}}}
    config.set(cnf)
    gmap_config = config.get('googlemaps')
    # gmap_config.update(language=language)
    language = 'ro'

    gmap_loader = LoaderFactory.loader_gmaps_with_cache(gmaps_config=gmap_config,
                                                            storage_config=config.get('mongodb'))
    spider = Spider(
            loader_factory=LoaderFactory,
            gmap_parser=MapFactory.spain,
            doc_factory=doc_factory,
            language=language,
            config=config,
            use_cache=True
    )
    if request.form['type'] == "autocomplete":
        raw = gmap_loader.by_places(doc['DENLOC'] + ', România')
        return json.dumps(raw)
    else:
        objects = spider.get_gmap_place_id(request.form['place_id'])
        gmap = {}
        gmap = objects[0].get_document()
        try:
            if gmap['name'].lower().replace('ă', 'a').replace('ã', 'a').replace('â', 'a').replace('î', 'i').replace('ș', 's').replace('ş', 's').replace('ț', 't').replace('ţ', 't') == doc['DENLOC'].lower().replace('ă', 'a').replace('ã', 'a').replace('â', 'a').replace('î', 'i').replace('ș', 's').replace('ş', 's').replace('ț', 't').replace('ţ', 't'):
                gmap['comparison'] = True
            else:
                gmap['comparison'] = False
        except Exception as e: 
            gmap['comparison'] = False

        pcs = False
        if 'postal_code' in gmap and gmap.get('postal_code') == doc['CODP']:
            pcs = True
        else:
            pcs = False

        if 'wiki_center' in doc:
            
            distance =  getDistance(gmap['center']['lat'], gmap['center']['lng'], doc["wiki_center"]["lat"],doc["wiki_center"]["lng"])
            # gmap['15_GMap_center_SNIG_comparison'] = getDistance(gmap['center']['lat'], gmap['center']['lng'],doc['28_SNIG_LATITUD_ETRS89'],doc['29_SNIG_LONGITUD_ETRS89'])
            gmap['gmap_comparison_url'] =("https://www.google.com.ua/maps/dir/"+str(gmap['center']['lat'])+","+str(gmap['center']['lng'])+"/"+str(doc["wiki_center"]["lat"])+","+str(doc["wiki_center"]["lng"])+"")
        
        else:
            distance =  False
            # gmap['15_GMap_center_SNIG_comparison'] = getDistance(gmap['center']['lat'], gmap['center']['lng'],doc['28_SNIG_LATITUD_ETRS89'],doc['29_SNIG_LONGITUD_ETRS89'])
            gmap['gmap_comparison_url'] = False
      

        db.romania.update_one(
                {"_id": ObjectId(request.form['id']) },
                    {
                        "$set": {
                                'gmap_name': gmap.get('name'),
                                'gmap_admin_hierarchy': gmap.get('admin_hierarchy', {}),
                                'gmap_center': gmap.get('center'),
                                'gmap_bounds': gmap.get('bounds'),
                                'gmap_type': gmap.get('type'),
                                'gmap_translate': gmap.get('translate'),
                                'gmap_requests': gmap.get('requests'),
                                'gmap_code': gmap.get('code'),
                                'gmap_postal_code': gmap.get('postal_code'),
                                'gmap_wiki_distance':distance

                    }
               }
        )

        if distance < 2:
            distance_status = True
        else:
            distance_status = False
        # gmap.pop('_id')
        # # gmap['15_GMap_center_SNIG_comparison'] = getDistance(gmap['center']['lat'], gmap['center']['lng'],doc['28_SNIG_LATITUD_ETRS89'],doc['29_SNIG_LONGITUD_ETRS89'])
        # if gmap['15_GMap_center_SNIG_comparison'] <= 1:
        #     gm_comp_status = True
        # else:
        #     gm_comp_status = False

        # types = {"Municipio": ["administrative_area_level_4"],
        #     "Entidad colectiva" :  ["administrative_area_level_5", "neighborhood"],
        #     "Otras entidades": ["locality", "neighborhood"],
        #     "Capital de municipio":["locality"],
        #     "Entidad singular": ["locality"]}
        # if gmap.get('type') in types[doc['25_SNIG_TIPO']]:
        #     gm_type_status = True
        # else:
        #     gm_type_status = False

        types = {
            "40": ["administrative_area_level_1"],
            "1":    ["administrative_area_level_2"],
            "2":    ["administrative_area_level_2"],
            "3":    ["administrative_area_level_2"],    
            "4":    ["administrative_area_level_2"],    
            "5":    ["administrative_area_level_2"],    
            "6":    ["sublocality_level_1"],    
            "9":    ["locality","sublocality_level_1"],
            "10":   ["locality","sublocality_level_1"],
            "11":   ["locality","sublocality_level_1"],
            "17":   ["locality","sublocality_level_1"],
            "18":   ["locality","sublocality_level_1"],
            "19":   ["locality","sublocality_level_1"],
            "22":   ["locality","sublocality_level_1"],
            "23":   ["locality","sublocality_level_1"]
        }
        mytypes = types[str(doc['TIP'])]
        if gmap.get('type') in mytypes:
            gmap_type_status = True
        else:
            gmap_type_status = False

            
        raw = {
                "gmap_name": gmap.get('name'),
                "gmap_name_status" : gmap['comparison'],
                "gmap_type": gmap.get('type'),
                "gmap_type_status":gmap_type_status,
                "gmap_postal_code": gmap.get('postal_code'),
                "pcs":pcs,
                "distance":distance,
                "distance_status":distance_status,
                "gmap_comparison_url":gmap['gmap_comparison_url'],
                'gmap_type': gmap.get('type'),

            }
        
        return json.dumps(raw)





@app.route('/users/create',  methods=['GET', 'POST'] )
@login_required
def user_create():
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.local
    if request.method == 'POST':
        pass_hash = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        db.users.insert({"_id": request.form['phone'], "password": pass_hash, "userName": request.form['username'], "userEmail":request.form['email'], "phone": '+'+str(request.form['phone']) })
        return redirect(url_for('user_list'))
    return render_template('admin/users/create.html')

@app.route('/users/list')
@login_required
def user_list():
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.local
    data = db.users.find()

    return render_template('admin/users/list.html', data=data)



@app.route('/gmap/keys')
@login_required
def keys_google():
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.local
    data = db.keygen.find()

    return render_template('admin/gmap/keys.html', data=data)
    # return render_template('admin/users/create.html')


@app.route('/gmaps/')
@app.route('/gmaps/<string:country>')
@login_required
def gmaps_list(country=None):
    return render_template('admin/gmap/list.html', country=country)


@app.route('/gmaps/unit/<string:id>')
@login_required
def gmaps_unit(id):
    config = Config('./config/config.yml')
    api_key = config.get('googlemaps').get('geocoding').get('key')
    factory = DocFactory(config.get('mongodb'))
    collection = factory.gmaps_collection()
    obj = collection.find_one({'_id': ObjectId(id)})
    return render_template('admin/gmap/unit.html', data=obj, api_key=api_key)


@app.route('/gmaps/unit/code/<string:id>')
@login_required
def gmap_code_unit(id):
    config = Config('./config/config.yml')
    api_key = config.get('googlemaps').get('geocoding').get('key')
    factory = DocFactory(config.get('mongodb'))
    collection = factory.gmaps_collection()
    obj = collection.find_one({'code': id})
    return render_template('admin/gmap/unit.html', data=obj, api_key=api_key)


@app.route('/wiki/')
@app.route('/wiki/<string:country>')
@login_required
def wiki_list(country=None):
    return render_template('admin/wiki/list.html', country=country)


@app.route('/wiki/unit/<string:id>')
@login_required
def wiki_unit(id):
    config = Config('./config/config.yml') 
    api_key = config.get('googlemaps').get('geocoding').get('key')
    factory = DocFactory(config.get('mongodb'))
    collection = factory.wiki_collection()
    obj = collection.find_one({'_id': ObjectId(id)})
    return render_template('admin/wiki/unit.html', data=obj, api_key=api_key)


@app.route('/wiki/unit/code/<string:id>')
@login_required
def wiki_code_unit(id):
    config = Config('./config/config.yml')
    api_key = config.get('googlemaps').get('geocoding').get('key')
    factory = DocFactory(config.get('mongodb'))
    collection = factory.wiki_collection()
    obj = collection.find_one({'code': id})
    return render_template('admin/wiki/unit.html', data=obj, api_key=api_key)


@app.route('/tasks/<string:journal_id>')
@app.route('/tasks/<string:journal_id>/<string:status>')
@login_required
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
@login_required
def clear_tasks(journal_id):
    config = Config('./config/config.yml')
    storage = JobStorage(job_name=journal_id, storage_config=config.get('mongodb'))
    storage.clear()
    return render_template('admin/empty.html', data='ok', auto_close=True)


@app.route('/logs/<string:name>/<int:status>')
@login_required
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
@login_required
def clear_logs(name):
    config = Config('./config/config.yml').get('mongodb')
    connection = MongoClient(config['host'], config['port'])
    connection.log[name].delete_many({})
    return render_template('admin/empty.html', data='ok', auto_close=True)


@app.route('/logs/close/<string:name>/<string:id>')
@login_required
def log_close(name, id):
    config = Config('./config/config.yml').get('mongodb')
    log = MongoDBLog(log_name=name, config=config)
    return 'Ok' if log.close(id) else 'Not'


@app.route('/clear/wiki/<string:name>')
@login_required
def clear_wiki_country(name):
    config = Config('./config/config.yml').get('mongodb')
    factory = DocFactory(config)
    collection = factory.wiki_collection()
    result = collection.delete_many({'admin_hierarchy.ADMIN_LEVEL_1.name': name})
    return render_template('admin/empty.html', data=['ok', result.deleted_count], auto_close=True)


@app.route('/clear/gmaps/<string:name>')
@login_required
def clear_gmaps_country(name):
    config = Config('./config/config.yml').get('mongodb')
    factory = DocFactory(config)
    collection = factory.gmaps_collection()
    result = collection.delete_many({'admin_hierarchy.ADMIN_LEVEL_1.name': name})
    return render_template('admin/empty.html', data=['ok', result.deleted_count], auto_close=True)


@app.route('/test/wiki')
@login_required
def test_wiki():
    pass


@app.route('/test/gmap')
@login_required
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
@login_required
def recursive_parsed_page_cache(name):
    config = Config('./config/config.yml').get('mongodb')
    connection = MongoClient(config['host'], config['port'])
    objects = connection.parsed_page[name].find()

    return render_template('admin/recursive/list.html', items=objects, name='Parsed page')


@app.route('/recursive/parsed_page/drop/<string:name>')
@login_required
def recursive_parsed_page_drop(name):
    config = Config('./config/config.yml').get('mongodb')
    connection = MongoClient(config['host'], config['port'])
    connection.parsed_page[name].drop()

    return render_template('admin/empty.html', data='ok', auto_close=True)


@app.route('/recursive/url_pool/drop/<string:name>')
@login_required
def recursive_url_pool_drop(name):
    config = Config('./config/config.yml').get('mongodb')
    connection = MongoClient(config['host'], config['port'])
    connection.url_pool[name].drop()

    return render_template('admin/empty.html', data='ok', auto_close=True)


@app.route('/recursive/url_pool/<string:name>')
@login_required
def recursive_url_pool_cache(name):
    config = Config('./config/config.yml').get('mongodb')
    connection = MongoClient(config['host'], config['port'])
    objects = connection.url_pool[name].find({})

    return render_template('admin/recursive/list.html', items=objects, name='Url pool')


@app.route('/recursive')
@login_required
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
@login_required
def secret_page(word):
    md5 = hashlib.md5()
    md5.update(word.encode('utf-8'))
    code = md5.hexdigest()
    if code != 'e37d7c242913151ee9d7d794f2027128':
        return render_template('admin/empty.html', data=403)

    return render_template('admin/worth-it/debug.html')
