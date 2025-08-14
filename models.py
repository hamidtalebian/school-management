from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(100))

    classes = db.relationship('Class', backref='teacher', lazy=True)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    grade = db.Column(db.String(50))

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    schedule = db.Column(db.String(100))  # مثلا: شنبه‌ها 16-18

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_type = db.Column(db.String(10), nullable=False)  # 'teacher' یا 'student'
    person_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(50))  # YYYY-MM-DD
    note = db.Column(db.String(200))
