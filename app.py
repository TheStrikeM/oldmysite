from flask import Flask, render_template, request, g, flash, abort, make_response
from flask import session, redirect, url_for
from flask_login import LoginManager
from time import sleep
from utils.HDataBase import HDataBase
import os, datetime, requests, sqlite3 as sql

DATABASE = "/tmp/auth.sqlite"
DEBUG = True
SECRET_KEY = '2347uidhfgvbfbhui654+_9548=+0>?'

app = Flask( __name__ )
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'auth.sqlite')))

hdb = None

def privetik(num):
   sum = 0
   while (num != 0):
      sum += num % 10
      num //= 10
   return sum

@app.before_request
def before_req():
    global hdb
    db = get_db()
    hdb = HDataBase(db)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

def connect_db():
    try:
        con = sql.connect(app.config['DATABASE'])
        con.row_factory = sql.Row
        return con
    except Exception as e:
        print(e)
        return False

def create_db():

    db = connect_db()
    cur = db.cursor()
    with app.open_resource('sq_db.sql', mode='r') as f:
        cur.executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db



@app.route( '/' )
def index( ):
    return render_template('index.html')

@app.route('/sources/test', methods=["POST", "GET"])
def privet():
    result = "0"
    if request.method == "POST":
        if len(request.form['number']) >= 2:
            num = int(request.form['number'])
            result = privetik(num)

    return render_template("test.html", result=result)



@app.route('/sources/inst', methods=["POST", "GET"])
def inst():
    result = "0"
    debugstatus = "Disabled"
    if request.method == "POST":
        if request.form['typi'] == "Накрутка подписчиков":
            result = "1"
            if request.form['dbug']:
                debugstatus = "Enabled"
            if request.form['dbug']:
                debugstatus = "Disabled"

        if request.form['typi'] == "Накрутка лайков":
            result = "2"
        if request.form['typi'] == "Накрутка лайков на все посты":
            result = "3"
        if request.form['typi'] == "Накрутка комментариев":
            result = "4"
        if request.form['typi'] == "Спам в директ":
            result = "5"
    return render_template('inst.html', result=result, debugstatus=debugstatus)

@app.route('/sources/phone', methods=["POST", "GET"])
def phone():
    number = "Не указано"
    country = "Нет"
    fullcountry = "Нет"
    language = "Нет"
    id = "Нет"
    code = "Нет"
    iso = "Нет"
    telecode = "Нет"
    city = "Нет"
    telecodec = "Нет"
    area = "Нет"
    lantitude = "Нет"
    longitude = "Нет"
    timezone = "Нет"
    rayon = "Нет"
    post = "Нет"
    mainoper = "Нет"
    peroper = "Нет"
    idoper = "Нет"
    defs = "Нет"

    if request.method == "POST":
        if len(request.form['phone']) >= 4:
                number = request.form[ 'phone' ]
                response = requests.get(f'https://htmlweb.ru/geo/api.php?json&telcod={number}')

                country = response.json()['country']['name']
                fullcountry = response.json()['country']['fullname']
                code = response.json()['country']['country_code3']
                iso = response.json()['country']['iso']
                telecode = response.json()['country']['telcod']
                language = response.json()['country']['lang']
                id = response.json()['country']['id']
                city = response.json()['capital']['name']
                area = response.json()['capital']['area']
                telecodec = response.json()['capital']['telcod']
                lantitude = response.json()['capital']['latitude']
                longitude = response.json()['capital']['longitude']
                timezone = response.json()['time_zone']
                post = response.json()['capital']['post']
                mainoper = response.json()['0']['oper']
                idoper = response.json()['0']['oper_id']
                peroper = response.json()['0']['oper_brand']
                defs = response.json()['0']['def']

    return render_template('phone-checker.html', number=number, country=country, fullcountry=fullcountry, language=language, id=id, code=code, iso=iso, telecode=telecode, telecodec=telecodec, city=city, mainoper=mainoper, peroper=peroper, defs=defs, timezone=timezone, post=post, area=area, lantitude=lantitude, longitude=longitude, rayon=rayon, idoper=idoper)

@app.route('/sources/ip-checker', methods=["POST", "GET"])
def ip_checker():
    ips = "Не указано"
    states = "Нет"
    regions = "Нет"
    stranas = "Нет"
    locations = "Нет"
    providers = "Нет"
    pindexs = "Нет"
    timezones = "Нет"

    if request.method == "POST":
        if len(request.form['ip']) >= 3:
            ips = request.form['ip']
            response = requests.get(f'http://ipinfo.io/{ips}/json')

            states = response.json()['city']
            regions = response.json()['region']
            stranas = response.json()['country']
            locations = response.json()['loc']
            providers = response.json()['org']
            timezones = response.json()['timezone']

    return render_template('ip-checker.html', ips=ips, states=states, regions=regions, stranas=stranas, locations=locations, providers=providers, pindexs=pindexs, timezones=timezones)


if __name__ == '__main__':
    app.run( )
