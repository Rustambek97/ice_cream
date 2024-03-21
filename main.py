import os
from flask import Flask, render_template, request, redirect
from database.mydb import mydb
from datetime import date
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/media-files'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/hodimlar', methods=['GET', 'POST'])
def HodimlarRuyxati():
    if request.method == 'GET':
        hodimlar = mydb.hodimlar()
        return render_template("hodimlar/hodimlar.html", hodimlar=hodimlar)
    elif request.method == 'POST':
        matn = request.form['qidiruv']
        natijalar = mydb.search(matn)
        return render_template("hodimlar/hodimlar.html", hodimlar=natijalar)


@app.route('/muzqaymoqlar')
def MuzqaymoqlarRuyxati():
    muzqaymoqlar = mydb.muzqaymoqlar()
    return render_template("muzqaymoqlar/muzqaymoqlar.html", muzqaymoqlar=muzqaymoqlar)

@app.route('/mijozlar')
def MijozlarRuyxati():
    mijozlar = mydb.mijozlar()
    return render_template("mijozlar/mijozlar.html", mijozlar=mijozlar)

@app.route('/hodimlar/<id>')
def TanlanganHodim(id):
    a = mydb.hodim(int(id))
    t = date.today() - a[4]
    b = {
        'hodim':a,
        'vaqt':date.today(),
        'farq':t.days
    }
    return render_template("hodimlar/hodim.html", b=b)

@app.route('/hodimqushish', methods = ['GET', 'POST'])
def Add():
    if request.method == 'GET':
        return render_template('hodimqushish.html')
    elif request.method == 'POST':
        ism = request.form['ism']
        familiya = request.form['familiya']
        tel = request.form['tel']
        sana = request.form['ish_boshlash_sana']
        karta = request.form['karta']

        mydb.hodimqushish(ism, familiya, tel, sana, karta)

        return redirect('/hodimlar')

@app.route("/muzqaymoqqushish", methods=['GET', 'POST'])
def muzqaymoqadd():
    if request.method == 'GET':
        turlar = mydb.muzqaymoqturlari()
        return render_template("muzqaymoqlar/muzqaymoqqushish.html", turlar=turlar)
    elif request.method == 'POST':
        nomi = request.form['nomi']
        narxi = request.form['narxi']
        tur_id = request.form['turi']
        chiqqan_sana = request.form['createdate']
        tugash_sana = request.form['deletedate']
        soni = request.form['soni']

        rasm = request.files['rasm']
        mydb.muzqaymoqqushish(nomi, narxi, tur_id, chiqqan_sana, tugash_sana, soni, rasm.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], rasm.filename)
        rasm.save(file_path)
        return redirect("/muzqaymoqlar")

@app.route("/hodim/tahrir/<id>", methods=['GET', 'POST'])
def HodimTahrir(id):
    if request.method == 'GET':
        hodim = mydb.hodimid(id)
        return render_template("hodimlar/hodimtahrirlash.html", hodim=hodim)
    elif request.method == 'POST':
        ism = request.form['ism']
        familiya = request.form['familiya']
        tel = request.form['tel']
        ish_boshlash = request.form['ish_boshlash']
        karta = request.form['karta']
        mydb.hodimTahrir(id, ism, familiya, tel, ish_boshlash, karta)
        return redirect("/hodimlar")

@app.route("/hodim/del/<id>/", methods=['GET', 'POST'])
def HodimDel(id):
    if request.method == 'GET':
        hodimlar = mydb.hodimid(id)
        return render_template("hodimlar/hodimdel.html", hodimlar=hodimlar)
    elif request.method == 'POST':
        mydb.hodimdel(id)
        return redirect("/hodimlar")

if __name__=="__main__":
    app.run(debug=True)