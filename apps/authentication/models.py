# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass



class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    status = db.Column(db.Integer, default=0)
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)
    
class JobPosted(db.Model, UserMixin):
    __tablename__ = 'JobPosted'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.Date, nullable=False)
    deadline_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirement = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    job_type = db.Column(db.String(50), nullable=False)
    company_name = db.Column(db.String(50), nullable=False)
    
    
    def __init__(self, title, date_posted, deadline_date, description, requirement, location , job_type, company_name):
        self.title = title
        self.date_posted = date_posted
        self.deadline_date = deadline_date
        self.description = description
        self.requirement = requirement
        self.location = location
        self.job_type = job_type
        self.company_name = company_name
        
        
        
    def __repr__(self):
        return str(self.title) 
    
    
    
class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    citizenship = db.Column(db.String(50))
    date_of_birth = db.Column(db.String(10))
    address = db.Column(db.String(200))
    city = db.Column(db.String(50))
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    cv_filename = db.Column(db.String(100))
    


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None




# Contact model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Contact {self.name}>'
    
    
    
class InternshipJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.Date, nullable=False)
    deadline_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    requirement = db.Column(db.Text, nullable=False)
    job_type = db.Column(db.String(20), nullable=False)