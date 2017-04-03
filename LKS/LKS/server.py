from flask import Flask, render_template, request, redirect, url_for, session
import json
import postgresql
import random
from flask_wtf import FlaskForm
import wtforms
from flask_wtf.csrf import CsrfProtect
from werkzeug.utils import secure_filename
import os
import string
import hashlib
from wtforms.validators import Required, EqualTo
import Config

class Log_in(FlaskForm):
    login = wtforms.StringField("Login", validators=[Required()])
    password = wtforms.PasswordField("Password", validators=[Required()])
#    submit = wtforms.SubmitField('Log in')

class judgment(FlaskForm):
    technique = wtforms.SelectField('Technique / Техника', choices=[(i, str(10-i/2)) for i in range(0, 21)], default=20)
    production = wtforms.SelectField('Direction / Постановка', choices=[(i, str(10-i/2)) for i in range(0, 21)], default=20)
    teamwork = wtforms.SelectField('Teamwork / Командная работа', choices=[(i, str(10-i/2)) for i in range(0, 21)], default=20)
    artistry = wtforms.SelectField('Artistry / Артистизм', choices=[(i, str(10-i/2)) for i in range(0, 21)], default=20)
    musicality = wtforms.SelectField('Musicality / Музыкальность', choices=[(i, str(10-i/2)) for i in range(0, 21)], default=20)
    show = wtforms.SelectField('Show / Шоу', choices=[(i, str(10-i/2)) for i in range(0, 21)], default=20)
    creativity = wtforms.SelectField('Creativity / Креативность', choices=[(i, str(10-i/2)) for i in range(0, 21)], default=20)
    submit = wtforms.SubmitField('OK')


class comands(FlaskForm):
    name = wtforms.StringField("name", validators=[Required()])
    nomination = wtforms.StringField("nomination", validators=[Required()])
    C_order = wtforms.StringField("C_order", validators=[Required()])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qpwoeiruty'
csrf = CsrfProtect(app)
csrf.init_app(app)



@app.route("/home")
@app.route("/")
def home():
    return redirect(url_for("log_in"))

@app.route("/log_in", methods=["GET", "POST"])
def log_in():
    form = Log_in()
    if session.get('id'):
        return redirect(url_for('mainStr', id=session['id']))
    if request.method == "GET":
        return render_template('log_in.html', form = form)
    elif request.method == "POST" :
        user = get_userWhereLog(form.login.data)
        session['id'] = user.get('user_id')
        session['name'] = user.get('name')
        session['role'] = user.get('role')
        if not get_curCom(session['id']):
            session['orderComand'] = user.get('role')
        else:
            session['orderComand'] = get_curCom(session['id'])+1
        session['order2Comand'] = 1
        return redirect(url_for("mainStr", id=session['id']))

@app.route("/<id>", methods=["GET", "POST"])
def mainStr(id):
    comands = get_allComands(id)
    fcomands = get_allfComands(id)
    if request.method == "GET" and session.get('id') == id:
        return render_template("jProfile.html", user = session, comands = comands, finalComands=fcomands)
    elif request.method == "POST" and session.get('id') == id:
        return "POST", 200
    return redirect(url_for('log_in'))

@app.route("/api/log_in", methods=["GET", "POST"])
def log_in_api():
    if request.method == "POST":
        data = json.loads(request.data.decode('utf-8'))
        if data.get("action") == "ch_login_pass":
            if not check_logIs(data.get("login")):
                return "uncorrect_log", 200
            elif not check_passIs(data.get("login"), data.get("pass")):
                return "uncorrect_pass", 200
            return "Ok", 200
    return redirect(url_for('log_in'))

@app.route("/fjudgment", methods=["GET", "POST"])
def jfComand():
    comand = get_fcomandInfo(session['order2Comand'])
    if not comand:
        return redirect(url_for('mainStr', id = session.get('id')))
    form = judgment()
    if request.method == "GET" and session.get('id') :
        return render_template("judgment.html", form = form, comand = comand, id=session['id'])
    elif request.method == "POST" and session.get('id'):
        session['order2Comand'] +=1
        insert_judgRes(session['id'], comand['comand_id'], form, 1)
        return redirect(url_for('jfComand'))
    return redirect(url_for('log_in'))


@app.route("/judgment", methods=["GET", "POST"])
def jComand():
    comand = get_comandInfo(session['orderComand'])
    if not comand:
        return redirect(url_for('mainStr', id = session.get('id')))
    form = judgment()
    if request.method == "GET" and session.get('id') :
        return render_template("judgment.html", form = form, comand = comand, id=session['id'])
    elif request.method == "POST" and session.get('id'):
        session['orderComand'] +=1
        insert_judgRes(session['id'], comand['comand_id'], form)
        return redirect(url_for('jComand'))
    return redirect(url_for('log_in'))


@app.route("/update/<id>", methods=["GET", "POST"])
def update(id):
    print(id)
    comand = get_comand(id)
    form = judgment()      #Change
    if comand:
        print(comand)
        form.technique.default = int(20-2*comand['technique'])
        form.production.default = int(20-2*comand['production'])
        form.teamwork.default = int(20-2*comand['teamwork'])
        form.artistry.default = int(20-2*comand['artistry'])
        form.musicality.default = int(20-2*comand['musicality'])
        form.show.default = int(20-2*comand['show'])
        form.creativity.default = int(20-2*comand['creativity'])
        form.process()
    else :
        return redirect(url_for('mainStr', id = session['id']))
    if not session.get('id'):
        return redirect(url_for('log_in'))
    if request.method == "GET":
        return render_template("update.html", form = form, comand = comand, jud = session['id'])
    elif request.method == "POST":
        update_judgRes(session['id'], id, request.form)
        return redirect(url_for('mainStr', id = session['id']))

@app.route("/finalupdate/<id>", methods=["GET", "POST"])
def fupdate(id):
    comand = get_comand(id, 1)
    form = judgment()      #Change
    if comand:
        form.technique.default = int(comand['technique'])
        form.production.default = int(comand['production'])
        form.teamwork.default = int(comand['teamwork'])
        form.artistry.default = int(comand['artistry'])
        form.musicality.default = int(comand['musicality'])
        form.show.default = int(comand['show'])
        form.creativity.default = int(comand['creativity'])
        form.process()
    else :
        return redirect(url_for('mainStr', id = session['id']))
    if request.method == "GET":
        return render_template("update.html", form = form, comand = comand, jud = session['id'])
    elif request.method == "POST":
        update_judgRes(session['id'], id, request.form, 1)
        return redirect(url_for('mainStr', id = session['id']))

def get_curCom(id):
    with postgresql.open(Config.dbLog) as db:
        sel = db.prepare("Select MAX(c_order) from comands Natural join judge WHERE user_id=$1;")
        jud = sel(id)
    if jud == [(None,)]:
        print("None")
        return 0
    print(jud)
    return jud[0][0]


def update_judgRes(iduser, idcom, form, final = 0):
    with postgresql.open(Config.dbLog) as db:
        sel = db.prepare("UPDATE judge SET technique=$1, production=$2, teamwork=$3,"+
        "artistry=$4, musicality=$5, show=$6, creativity=$7, sum=$8 WHERE final=$9 and comand_id=$10 and user_id=$11")

        com = sel(10-float(form['technique'])/2, 10-float(form['production'])/2, 10-float(form['teamwork'])/2,
        10-float(form['artistry'])/2, 10-float(form['musicality'])/2, 10-float(form['show'])/2, 10-float(form['creativity'])/2,
        10-float(form['technique'])/2+10-float(form['production'])/2+10-float(form['teamwork'])/2+10-float(form['artistry'])/2+
        10-float(form['musicality'])/2+10-float(form['show'])/2+10-float(form['creativity'])/2, final, idcom, iduser)


def insert_judgRes(iduser, idcom, form, final=0):
    with postgresql.open(Config.dbLog) as db:
        sel = db.prepare("INSERT INTO judge VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)")
        try:
            com = sel(int(random.random()*1000), iduser, idcom, 10-float(form.technique.data)/2,
            10-float(form.production.data)/2, 10-float(form.teamwork.data)/2, 10-float(form.artistry.data)/2,
            10-float(form.musicality.data)/2, 10-float(form.show.data)/2, 10-float(form.creativity.data)/2,
            10-float(form.technique.data)/2+10-float(form.production.data)/2+10-float(form.teamwork.data)/2+10-float(form.artistry.data)/2+
            10-float(form.musicality.data)/2+10-float(form.show.data)/2+10-float(form.creativity.data)/2, final)
        except Exception:
            print('no')

def get_comand(id, final=0):
    with postgresql.open(Config.dbLog) as db:
        sel = db.prepare("SELECT * FROM judge natural join comands where comand_id=$1 and user_id=$2 and final=$3; ")
        jud = sel(id, session['id'], final)
    if jud:
        print(jud)
        return jud[0]
    return []

def get_allComands(id):                                   #Вот она
    with postgresql.open(Config.dbLog) as db:
        sel = db.prepare("SELECT * FROM judge natural join comands where user_id=$1 and final='0'; ")
        jud = sel(id)
    return jud

def get_allfComands(id):
    with postgresql.open(Config.dbLog) as db:
        sel = db.prepare("SELECT * FROM judge natural join comands where user_id=$1 and final='1'; ")
        jud = sel(id)
    if jud:
        return jud
    return []

def get_userWhereLog(log):
    with postgresql.open(Config.dbLog) as db:
        sel = db.prepare("SELECT * FROM log_pass WHERE login=$1;")
        user = sel(log.lower())
    if user:
        return user[0]
    return{}

def update_comand_order(name, order):
    with postgresql.open(Config.dbLog) as db:
        sel = db.prepare("UPDATE comands WHERE name=$1 SET c_order=$2;")
        user = sel(name, order)

def insert_command(id, name, nomination, order):
    with postgresql.open(Config.dbLog) as db:
        sel = db.prepare("INSERT INTO comands (comand_id, name, nomination, c_order) VALUES($1, $2, $3, $4)")
        user = sel(id, name, nomination, order)

def check_logIs(log):
    with postgresql.open(Config.dbLog) as db:
        sel = db.prepare("SELECT * FROM log_pass WHERE login=$1;")
        user = sel(log.lower())
    if user:
        return True
    return False

def check_passIs(log, password):
    with postgresql.open(Config.dbLog) as db:
        sel = db.prepare("SELECT * FROM log_pass WHERE login=$1 AND password=$2;")
        user = sel(log.lower(),hashlib.md5(password.encode('utf8')).hexdigest())
    if user:
        return True
    return False

def get_comandInfo(id):
    with postgresql.open(Config.dbLog) as db:
        sel = db.prepare("SELECT * FROM comands WHERE C_order=$1 ")
        com = sel(id)
    if com:
        return com[0]
    return {}

def get_fcomandInfo(id):
    with postgresql.open(Config.dbLog) as db:
        sel = db.prepare("SELECT * FROM comands WHERE C_order2=$1 ")
        com = sel(id)
    if com:
        return com[0]
    return {}

def get_user(id):
    with postgresql.open(Config.dbLog) as db:
        sel = db.prepare("SELECT * FROM log_pass WHERE user_id=$1 ")
        com = sel(id)
    if com:
        return com[0]
    return {}

if __name__ == "__main__":
    app.run(debug=True ,host="192.168.1.4")
