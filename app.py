# from Route import *
# if __name__ =="__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__,template_folder="template")

app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://hr:hr@127.0.0.1:1521/xe'
db = SQLAlchemy(app)


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


# Pass ALl Entries from Hospital table
@app.route("/Search.html")
def studata():
    entries = Hospital.query.all()
    # pass entries to the template
    return render_template("Search.html", entries=entries)

@app.route("/Update.html/")
def restapi1():
    return render_template("Update.html")

# For Updating Info
# @app.route("/stuInfo/update/<int:Pno>", methods=['GET', 'POST'])
# def update_entry(Pno):
#     entry = Hospital.query.get(Pno)
#     if request.method == 'POST':
#         entry.Pname = request.form.get('Pname')
#         entry.PAge = request.form.get('PAge')
#         entry.Pnumber = request.form.get('Pnumber')
#         entry.Pstatus = request.form.get('Pstatus')
#         db.session.commit()
#         return redirect(url_for('update.html'))
#     return render_template("Update.html", entry=entry)

@app.route('/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    patients = Hospital.query.filter_by(id=id).first()
    if request.method == 'POST':
            if patients:
                db.session.delete(patients)
                db.session.commit()
                return redirect('/')
                abort(404)
            return render_template('Delete.html')

        //
if __name__ == "__main__":
    app.run(debug=True)
