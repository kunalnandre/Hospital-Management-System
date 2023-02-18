# from Route import *
#
#
# if __name__ =="__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://hr:hr@127.0.0.1:1521/xe'
db = SQLAlchemy(app)

secret_key = "BHau ahe tu apla "


class Hospital(db.Model):
    Pno = db.Column(db.Integer(), primary_key=True)
    Pname = db.Column(db.String(20), unique=False, nullable=False)
    PAge = db.Column(db.Integer(), unique=False, nullable=False)
    Pnumber = db.Column(db.Integer(), unique=False, nullable=False)
    Pstatus = db.Column(db.String(10), unique=False, nullable=False)


@app.route("/")
def about():
    return render_template("index.html")


@app.route("/Addinfo.html")
def restapi():
    return render_template("Addinfo.html")


@app.route("/pinfo", methods=['GET', 'POST'])
def stuInfo():
    if request.method == 'POST':
        Pno = request.form.get('Pno')
        Pname = request.form.get('Pname')
        PAge = request.form.get('PAge')
        Pnumber = request.form.get('Pnumber')
        Pstatus = request.form.get('Pstatus')

        entry = Hospital(Pno=Pno, Pname=Pname, PAge=PAge, Pnumber=Pnumber, Pstatus=Pstatus)
        db.session.add(entry)
        db.create_all()
        db.session.commit()

    return render_template("Addinfo.html")


# Pass ALl Entries from Blood table
@app.route("/Selectall.html")
def studata():
    entries = Hospital.query.all()
    # pass entries to the template
    return render_template("Selectall.html", entries=entries)


@app.route("/Search.html/")
def restapi1():
    return render_template("Search.html")


@app.route("/PSearch", methods=['GET', 'POST'])
def PSearch():
    if request.method == 'POST':
        Pname = request.form.get('Pname')
        entries = Hospital.query.filter_by(Pname=Pname).all()
        return render_template("Search.html", entries=entries)


@app.route('/updatepost', methods=['GET', 'POST'])
def updatepost():
    if request.method == 'POST':
        # Get the patient number and new status from the HTML form
        print("Entered into update fun")
        Pno = request.form.get('Pno')
        Pname = request.form.get('Pname')
        PAge = request.form.get('PAge')
        Pnumber = request.form.get('Pnumber')
        Pstatus = request.form.get('Pstatus')
        print(Pno, Pname, PAge, Pstatus)

        # Update the patient status in the database

        hospital = Hospital.query.filter_by(Pno=Pno).first()
        if Hospital:
            hospital.Pno = Pno
            hospital.Pname = Pname
            hospital.PAge = PAge
            hospital.Pnumber = Pnumber
            hospital.Pstatus = Pstatus
            print(hospital.Pno, hospital.Pname, hospital.PAge, hospital.Pnumber, hospital.Pstatus)
            db.session.commit()

        return render_template('/seedata.html')


@app.route("/editpost/<string:id>", methods=['GET', 'POST'])
def editpost(id):
    entry = Hospital.query.get(id)
    print("editpost")
    if request.method == 'POST':
        entry = Hospital.query.filter_by(pno=id)
        entry.Pno = request.form.get('Pno')
        entry.Pname = request.form.get('Pname')
        entry.PAge = request.form.get('PAge')
        entry.Pnumber = request.form.get('Pnumber')
        entry.Pstatus = request.form.get('Pstatus')
        print(entry.Pno, entry.Pname, entry.PAge, entry.Pnumber, entry.Pstatus, )
        db.session.commit()
        return redirect(url_for('Selectall.html'))
    return render_template("Update.html", entry=entry)


@app.route("/removepost/<string:id>")
def removepost(id):
    entry = Hospital.query.filter_by(Pno=id).first()
    print("deletepost!!!!!!!!!!!!!!!!")
    db.session.delete(entry)
    db.session.commit()
    return render_template("seedata.html")


# Pass ALl Entries from Blood table
@app.route("/seedata.html")
def seedata():
    entries = Hospital.query.all()
    # pass entries to the template
    return render_template("Selectall.html", entries=entries)


if __name__ == "__main__":
    app.run(debug=True)
