from cx_Oracle import IntegrityError
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import model
from hosp_class import *


@app.route("/")
def about():
    return render_template("FLStack.html")


@app.route("/add.html")
def rest1():
    return render_template("/add.html")


@app.route("/pinfo", methods=['GET', 'POST'])
def pinfo():
    if request.method == 'POST':
        pno = request.form.get('pno')
        pname = request.form.get('pname')
        pgender = request.form.get('pgender')
        page = request.form.get('page')
        pward = request.form.get('pward')
        pstatus = request.form.get('pstatus')

        entry = Hospital(pno=pno, pname=pname, pgender=pgender, page=page, pward=pward,pstatus=pstatus)
        db.session.add(entry)
        db.create_all()
        db.session.commit()

    return render_template("add.html")

# for searching a patient
@app.route("/search.html")
def rest2():
    return render_template("/search.html")

@app.route("/psearch", methods=['GET', 'POST'])
def psearch():
    if request.method == 'POST':
        pname = request.form.get('pname')
        entries = Hospital.query.filter_by(pname=pname).all()
        return render_template('search.html', entries=entries)

@app.route('/updatefun', methods=['GET', 'POST'])
def updatefun():
    if request.method == 'POST':
        # Get the patient number and new status from the HTML form
        print("Entered into update fun")
        pno = request.form.get('pno')
        pname = request.form.get('pname')
        pgender = request.form.get('pgender')
        page = request.form.get('page')
        pward = request.form.get('pward')
        pstatus = request.form.get('pstatus')

# Update the patient status in the database
        hospital = Hospital.query.filter_by(pno=pno).first()
        if hospital:
            hospital.pno = pno
            hospital.pname = pname
            hospital.gender = pgender
            hospital.page = page
            hospital.pward = pward
            hospital.pstatus = pstatus
            db.session.commit()

# Redirect the user to the selectall.html page
        return redirect(url_for('selectall'))

# Pass ALl Entries from Blood table
@app.route("/selectall.html")
def selectall():
    entries = Hospital.query.all()
    # pass entries to the template
    return render_template("selectall.html", entries=entries)


@app.route("/editpost/<string:id>", methods=['GET', 'POST'])
def editpost(id):
    entry = Hospital.query.get(id)
    print("editpost")
    if request.method == 'POST':
        entry = Hospital.query.filter_by(pno=id)
        entry.pno = request.form.get('pno')
        entry.pname = request.form.get('pname')
        entry.pgender = request.form.get('pgender')
        entry.page = request.form.get('page')
        entry.pward = request.form.get('pward')
        entry.pstatus = request.form.get('pstatus')
        db.session.commit()
        # return redirect(url_for('selectall.html'))
    return render_template("update.html", entry=entry)



@app.route('/deleterow/<int:id>', methods=['GET', 'POST'])
def deleterow(id):
    hospital = Hospital.query.get(id)
    if hospital:
        db.session.delete(hospital)
        db.session.commit()
    return redirect(url_for('selectall'))
