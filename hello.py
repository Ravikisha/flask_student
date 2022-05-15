from flask import Flask, redirect,render_template, request, url_for
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

basedir = "./"

app = Flask(__name__)

#database init
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    desc = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<Student {self.firstname}>'



#app routes
#home route/ data route
@app.route("/")
def home():
    students = Student.query.all()
    return render_template("data.html",students=students)

#form route
@app.route("/form",methods=["GET","POST"])
def form():
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        desc = request.form.get("desc")
        new_student = Student(firstname=fname,lastname=lname,email=email,desc=desc)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('form.html')
#dyamic route for student edit
@app.route('/<int:student_id>/edit/', methods=('GET', 'POST'))
def edit(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        firstname = request.form['fname']
        lastname = request.form['lname']
        email = request.form['email']
        desc = request.form['desc']

        student.firstname = firstname
        student.lastname = lastname
        student.email = email
        student.desc = desc

        db.session.add(student)
        db.session.commit()

        return redirect(url_for('student', student_id=student.id))

    return render_template('edit.html', student=student)

#dyamic route for get student data
@app.route('/<int:student_id>/')
def student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student.html',student=student)

#delete a student record
@app.post('/<int:student_id>/delete/')
def delete(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('home'))

#non valid route
@app.errorhandler(404)
def not_found(e):
    return "<p>Link Not Found</p>"
#main function call
if __name__ == "__main__":
    app.run(debug=True)