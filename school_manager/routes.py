from school_manager import app, db
from flask import render_template, request, redirect, session, url_for
from school_manager.models import School, Teacher, Class_, Student
from school_manager.forms import (
    RegistrationForm,
    CreateTeacherForm,
    CreateClassForm,
    CreateStudentForm,
    LoginForm)


def make_teacher_list():
    teacher_list = Teacher.query.filter_by(school=session['id']).all()
    teachers = list()
    for teacher in teacher_list:
        teachers.append(f"{teacher.name} {teacher.surname} | {teacher.id}")
    return teachers


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        if School.query.filter_by(password=form.password.data).first() is not None:
            session['password'] = form.password.data
            session['id'] = School.query.filter_by(password=form.password.data).first().id

            return redirect(url_for('main_panel'))
    return render_template("login.html", form=form)


@app.route('/create-school', methods=['GET', 'POST'])
def create_account():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            school = School(name=form.name.data,
                            address=form.address.data,
                            password=form.password.data)
            db.session.add(school)
            db.session.commit()
            session['password'] = form.password.data
            session['id'] = School.query.filter_by(password=form.password.data).first().id
            return redirect(url_for('main_panel'))
        except Exception as e:
            return render_template('create_account.html', msg="School with this name already exist.", form=form)

    return render_template("create_account.html", form=form)


@app.route('/main-panel')
def main_panel():
    try:
        session['password']
    except KeyError:
        return redirect('/')

    classes = Class_.query.filter_by(school=session['id']).all()
    students = Student.query.filter_by(school=session['id']).all()
    teachers = Teacher.query.filter_by(school=session['id']).all()

    return render_template('main_panel.html', classes=classes, teachers=teachers, students=students)


@app.route('/create-teacher', methods=['GET', 'POST'])
def create_teacher():
    try:
        session['password']
    except KeyError:
        return redirect('/')

    form = CreateTeacherForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            teacher = Teacher(name=form.name.data,
                              surname=form.surname.data,
                              birth_date=form.birth_date.data,
                              salary=form.salary.data,
                              date_of_employment=form.date_of_employment.data,
                              address=form.address.data,
                              school=session['id'])
            db.session.add(teacher)
            db.session.commit()
            return redirect('/create-teacher')
        except Exception as e:
            return redirect('/create-teacher')

    return render_template('create/create_teacher.html', form=form)


@app.route('/create-class', methods=['GET', 'POST'])
def create_class():
    try:
        session['password']
    except KeyError:
        return redirect('/')

    form = CreateClassForm(request.form)
    form.supervising_teacher.choices = make_teacher_list()

    if request.method == 'POST' and form.validate():
        class_ = Class_(name=form.name.data,
                        supervising_teacher=form.supervising_teacher.data.split()[-1],
                        school=session['id'])
        db.session.add(class_)
        db.session.commit()
        return redirect('/create-class')
    return render_template('create/create_class.html', form=form)


@app.route('/create-student', methods=['GET', 'POST'])
def create_student():
    try:
        session['password']
    except KeyError:
        return redirect('/')

    form = CreateStudentForm(request.form)
    classes_list = Class_.query.filter_by(school=session['id']).all()
    for class_ in classes_list:
        form.class_.choices.append(f"{class_.name} | {class_.id}")

    if request.method == "POST" and form.validate():
        student = Student(name=form.name.data,
                          surname=form.surname.data,
                          address=form.address.data,
                          birth_date=form.birth_date.data,
                          class_=form.class_.data.split()[-1],
                          school=session['id'])
        db.session.add(student)
        db.session.commit()
        return redirect('/create-student')

    return render_template('create/create_student.html', form=form)


@app.route('/teacher/<id>', methods=['GET', 'POST'])
def teacher_profile(id):
    try:
        var = session['password']
        teacher = Teacher.query.filter_by(id=id).first()
    except KeyError:
        return redirect('/')

    form = CreateTeacherForm(request.form)
    if request.method == 'POST' and form.validate():
        teacher.name = form.name.data
        teacher.surname = form.surname.data
        teacher.birth_date = form.birth_date.data
        teacher.salary = form.salary.data
        teacher.date_of_employment = form.date_of_employment.data
        teacher.address = form.address.data

        db.session.commit()
        return redirect('/main-panel')
    return render_template('profiles/teacher_profile.html', teacher=teacher, form=form)


@app.route('/student/<id>', methods=['GET', 'POST'])
def student_profile(id):
    try:
        var = session['password']
        student = Student.query.filter_by(id=id).first()
    except KeyError:
        return redirect('/')

    form = CreateStudentForm(request.form)
    classes_list = Class_.query.filter_by(school=session['id']).all()
    for class_ in classes_list:
        form.class_.choices.append(f"{class_.name} | {class_.id}")

    if request.method == "POST" and form.validate():
        student.name = form.name.data
        student.surname = form.surname.data
        student.birth_date = form.birth_date.data
        student.address = form.address.data
        student.class_ = form.class_.data.split()[-1]

        db.session.commit()
        return redirect('/main-panel')

    return render_template('/profiles/student_profile.html', student=student, form=form)


@app.route('/class/<id>', methods=['GET', 'POST'])
def class_profile(id):
    try:
        var = session['password']
        class_ = Class_.query.filter_by(id=id).first()
    except KeyError:
        return redirect('/')

    form = CreateClassForm(request.form)
    form.supervising_teacher.choices = make_teacher_list()
    students = Student.query.filter_by(school=session['id'], class_=class_.id).all()

    if request.method == "POST" and form.validate():
        class_.name = form.name.data
        class_.supervising_teacher = form.supervising_teacher.data.split()[-1]
        db.session.commit()

    return render_template('/profiles/class_profile.html', class_=class_, form=form, students=students)


@app.route('/delete/<type>/<id>')
def delete(type, id):
    if type == "class":
        record_to_delete = Class_.query.filter_by(id=id).first()
    elif type == "teacher":
        record_to_delete = Teacher.query.filter_by(id=id).first()
    elif type == "student":
        record_to_delete = Student.query.filter_by(id=id).first()
    else:
        return redirect('/main-panel')

    db.session.delete(record_to_delete)
    db.session.commit()

    return redirect('/main-panel')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
