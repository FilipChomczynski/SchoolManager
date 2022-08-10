from school_manager import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    surname = db.Column(db.String(60), unique=False, nullable=False)
    birth_date = db.Column(db.String(12), unique=False, nullable=False)
    class_ = db.Column(db.Integer, unique=False, nullable=False)
    address = db.Column(db.String(70), unique=False, nullable=False)
    school = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Student %r>' % self.surname


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Integer, unique=False, nullable=False)
    weight = db.Column(db.Integer, unique=False, nullable=False)
    name = db.Column(db.String(35), unique=False, nullable=False)
    origin_user = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Grade %r>' % self.grade


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    surname = db.Column(db.String(60), unique=False, nullable=False)
    birth_date = db.Column(db.String(12), unique=False, nullable=False)
    salary = db.Column(db.Integer, unique=False, nullable=False)
    date_of_employment = db.Column(db.String(12), unique=False, nullable=False)
    address = db.Column(db.String(70), unique=False, nullable=False)
    school = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Teacher %r>' % self.surname


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True, nullable=False)
    address = db.Column(db.String(70), unique=False, nullable=False)
    password = db.Column(db.String(30), unique=False, nullable=False)

    def __repr__(self):
        return '<School %r>' % self.name


class Class_(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=False, nullable=False)
    supervising_teacher = db.Column(db.Integer, unique=False, nullable=False)
    school = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Class %r>' % self.name

