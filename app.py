from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Teacher, Student, Class, Payment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'change-this-in-production'

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    stats = {
        'teachers': Teacher.query.count(),
        'students': Student.query.count(),
        'classes': Class.query.count(),
        'payments': Payment.query.count()
    }
    return render_template('index.html', stats=stats)

# ---------- Teachers ----------
@app.route('/teachers', methods=['GET', 'POST'])
def teachers():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        if not name:
            flash('نام معلم الزامی است.', 'danger')
        else:
            t = Teacher(name=name, phone=phone, subject=subject)
            db.session.add(t)
            db.session.commit()
            flash('معلم اضافه شد.', 'success')
        return redirect(url_for('teachers'))
    all_teachers = Teacher.query.order_by(Teacher.id.desc()).all()
    return render_template('teachers.html', teachers=all_teachers)

@app.route('/teachers/<int:tid>/delete')
def delete_teacher(tid):
    t = Teacher.query.get_or_404(tid)
    db.session.delete(t)
    db.session.commit()
    flash('معلم حذف شد.', 'info')
    return redirect(url_for('teachers'))

# ---------- Students ----------
@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        grade = request.form.get('grade')
        if not name:
            flash('نام شاگرد الزامی است.', 'danger')
        else:
            s = Student(name=name, phone=phone, grade=grade)
            db.session.add(s)
            db.session.commit()
            flash('شاگرد اضافه شد.', 'success')
        return redirect(url_for('students'))
    all_students = Student.query.order_by(Student.id.desc()).all()
    return render_template('students.html', students=all_students)

@app.route('/students/<int:sid>/delete')
def delete_student(sid):
    s = Student.query.get_or_404(sid)
    db.session.delete(s)
    db.session.commit()
    flash('شاگرد حذف شد.', 'info')
    return redirect(url_for('students'))

# ---------- Classes ----------
@app.route('/classes', methods=['GET', 'POST'])
def classes():
    teachers = Teacher.query.all()
    if request.method == 'POST':
        title = request.form.get('title')
        teacher_id = request.form.get('teacher_id', type=int)
        schedule = request.form.get('schedule')
        if not title or not teacher_id:
            flash('عنوان کلاس و معلم الزامی است.', 'danger')
        else:
            c = Class(title=title, teacher_id=teacher_id, schedule=schedule)
            db.session.add(c)
            db.session.commit()
            flash('کلاس اضافه شد.', 'success')
        return redirect(url_for('classes'))
    all_classes = Class.query.order_by(Class.id.desc()).all()
    return render_template('classes.html', classes=all_classes, teachers=teachers)

@app.route('/classes/<int:cid>/delete')
def delete_class(cid):
    c = Class.query.get_or_404(cid)
    db.session.delete(c)
    db.session.commit()
    flash('کلاس حذف شد.', 'info')
    return redirect(url_for('classes'))

# ---------- Payments ----------
@app.route('/payments', methods=['GET', 'POST'])
def payments():
    teachers = Teacher.query.all()
    students = Student.query.all()
    if request.method == 'POST':
        person_type = request.form.get('person_type')
        person_id = request.form.get('person_id', type=int)
        amount = request.form.get('amount', type=float)
        date = request.form.get('date')
        note = request.form.get('note')
        if person_type not in ('teacher', 'student') or not person_id or amount is None:
            flash('اطلاعات پرداخت نامعتبر است.', 'danger')
        else:
            p = Payment(person_type=person_type, person_id=person_id, amount=amount, date=date, note=note)
            db.session.add(p)
            db.session.commit()
            flash('پرداخت ثبت شد.', 'success')
        return redirect(url_for('payments'))
    all_payments = Payment.query.order_by(Payment.id.desc()).all()
    return render_template('payments.html', payments=all_payments, teachers=teachers, students=students)

@app.route('/payments/<int:pid>/delete')
def delete_payment(pid):
    p = Payment.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    flash('پرداخت حذف شد.', 'info')
    return redirect(url_for('payments'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
