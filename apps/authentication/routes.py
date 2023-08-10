# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import app, jsonify, render_template, redirect, request, send_file, send_from_directory, url_for, flash
from flask_login import (
    current_user,
    login_user,
    logout_user
)
import os
from werkzeug.utils import secure_filename 
from .models import JobPosted, JobApplication,Contact,  InternshipJob
from datetime import datetime
from apps.home import blueprint
from flask import render_template, request, current_app
from flask_login import login_required
from flask import send_from_directory

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users

from apps.authentication.util import verify_pass

  


@blueprint.route('/')
def home():
    jobs =JobPosted.query.all()
    print(jobs)
    return render_template('index.html', jobs=jobs)


@blueprint.route('/about')
def about():
    return render_template('about.html')

@blueprint.route('/Apply')
def Apply():
    return render_template('Apply.html')


@blueprint.route('/')
def route_default():
    jobs =JobPosted.query.all()
    return redirect(url_for('authentication_blueprint.login'),jobs=jobs)


@blueprint.route('/internjobs')
def internjobs():
    jobs = InternshipJob.query.all()
    return render_template('internjobs.html', jobs=jobs)


    
@blueprint.route('/about')
def route_about():
    render_template('about.html')


@blueprint.route('/home/index')
def adminhome():
    return render_template('/home/index.html')


# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    jobs =JobPosted.query.all()
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']
        

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):
            

            login_user(user)
            if user.status == 1:
                return redirect(url_for('home_blueprint.index'))
            else:
                
                return render_template('index.html',jobs=jobs)

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return render_template('index.html')


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()
        
        return render_template('index.html',
                               msg='Account created successfully.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)
@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.home'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500

@blueprint.route('/home/postJob', methods=['POST', 'GET'])
def add_job():
    if request.method == 'POST':
        # Ensure all the required fields are present in the form data
        required_fields = ['title', 'date_posted', 'deadline_date', 'description', 'requirement','location','job_type','company_name' ]
        if all(field in request.form for field in required_fields):
            # Retrieve form data from the request.form object
            title = request.form['title']
            date_posted_str = request.form['date_posted']
            deadline_date_str = request.form['deadline_date']
            description = request.form['description']
            requirement = request.form['requirement']
            location = request.form['location']
            job_type = request.form['job_type']
            company_name = request.form['company_name']

            # Convert date strings to Python date objects
            from datetime import datetime
            date_posted = datetime.strptime(date_posted_str, '%Y-%m-%d').date()
            deadline_date = datetime.strptime(deadline_date_str, '%Y-%m-%d').date()

            # Create a new JobPosted object and add it to the database
            new_job = JobPosted(title=title, date_posted=date_posted, deadline_date=deadline_date, description=description, requirement=requirement, location=location,  job_type=job_type ,company_name=company_name)

            db.session.add(new_job)
            db.session.commit()

            # Flash a success message
            flash('Job added successfully!', 'success')
        else:
            # Flash an error message for missing fields
            flash('Please fill in all the required fields.', 'error')

    # Regardless of the request method, render the template with the form
    return render_template('/home/postJob.html')

   
#EXTRACTING DATA FROM THE JobPosted table

@blueprint.route('/jobs', methods=['GET'])
def jobs():
    jobs =JobPosted.query.all()
    jobs2 = InternshipJob.query.all()
    print(jobs)
    return render_template('jobs.html', jobs=jobs,  jobs2=jobs2)



@blueprint.route('/home.tables', methods=['GET'])
def another_page():
    jobs = JobPosted.query.all()
    return render_template('/postJob.html', jobs=jobs)


from datetime import datetime
# Other imports and code...

@blueprint.route('/update/<int:id>', methods=['POST', 'GET'])
@login_required
def updatefunc(id):
    job = JobPosted.query.get_or_404(id)
    if request.method == 'POST':
        # Ensure all the required fields are present in the form data
        required_fields = ['title', 'date_posted', 'deadline_date', 'description', 'requirement', 'location', 'job_type', 'company_name']
        if all(field in request.form for field in required_fields):
            # Update the job attributes with form data
            job.title = request.form['title']
            job.date_posted = datetime.strptime(request.form['date_posted'], '%Y-%m-%d').date()
            job.deadline_date = datetime.strptime(request.form['deadline_date'], '%Y-%m-%d').date()
            job.description = request.form['description']
            job.requirement = request.form['requirement']
            job.location = request.form['location']
            job.job_type = request.form['job_type']
            job.company_name = request.form['company_name']

            # Commit the changes to the database
            db.session.commit()

            # Flash a success message
            flash('Job updated successfully!', 'success')
        else:
            # Flash an error message for missing fields
            flash('Please fill in all the required fields.', 'error')

    return render_template('/home/updateJobs.html', job=job)


@blueprint.route('/delete/<int:id>', methods=['POST', 'GET'])
def deletejob(id):
    job = JobPosted.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    flash("Job deleted successfully.")
    
    return redirect(request.referrer)
    
 
UPLOAD_FOLDER = '/static/application'
@blueprint.route('/appl2', methods=['GET', 'POST'])

def job_application_form():
   
    if request.method == 'POST':
        
        first_name = request.form['First name']
        surname = request.form['Surname']
        citizenship = request.form['Citizenship']
        date_of_birth = request.form['Date of birth']
        address = request.form['Address']
        city = request.form['City']
        phone = request.form['Phone']
        email = request.form['Email']

        cv_file = request.files['Curriculum vitae']
        if cv_file:
            cv_filename = secure_filename(cv_file.filename)
            # Create the directory if it doesn't exist
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            cv_file.save(os.path.join(UPLOAD_FOLDER, cv_filename))
        else:
            cv_filename = None

        job_application = JobApplication(
            first_name=first_name,
            surname=surname,
            citizenship=citizenship,
            date_of_birth=date_of_birth,
            address=address,
            city=city,
            phone=phone,
            email=email,
            cv_filename=cv_filename
        )
        db.session.add(job_application)
        db.session.commit()
        flash('Your job application has been submitted successfully!', 'success')  # Adding a flash message


    return render_template('/Apply.html')




@blueprint.route('/job_applications')
def job_applications():
    job_applications = JobApplication.query.all()
    return render_template('/home/Applications.html', job_applications=job_applications)



@blueprint.route('/download_cv/<string:filename>')
def download_cv(filename):
    return send_from_directory(os.path.join(os.getcwd(), UPLOAD_FOLDER), filename, as_attachment=True)



@blueprint.route('/delete_application/<int:application_id>', methods=['POST'])
def delete_application(application_id):
    # Find the job application with the given ID
    job_application = JobApplication.query.get(application_id)

    if job_application:
        # Delete the CV file if it exists
        if job_application.cv_filename:
            cv_path = os.path.join(UPLOAD_FOLDER, job_application.cv_filename)
            if os.path.exists(cv_path):
                os.remove(cv_path)

        # Delete the job application from the database
        db.session.delete(job_application)
        db.session.commit()

    return redirect(request.referrer)


#getting data from the conatct form
@blueprint.route('/contact', methods=['GET', 'POST'])

def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        # Create a new contact record and save it to the database
        new_contact = Contact(name=name, email=email, subject=subject, message=message)
        db.session.add(new_contact)
        db.session.commit()

        # Redirect to the homepage after submitting the form
        return redirect('/')
    flash("Contact submitted  successfully!")

    return render_template('contact.html')



#deleting the contact

@blueprint.route('/deletecontact/<int:id>', methods=['POST', 'GET'])
def deletecontact(id):
    contact = Contact.query.get(id)  # Retrieve the specific contact by its ID
    if contact:
        db.session.delete(contact)  # Delete the specific contact
        db.session.commit()  # Commit the transaction to apply the delete operation
        flash("Contact deleted successfully.")
    else:
        flash("Contact not found.")
    
    return redirect(request.referrer)




@blueprint.route('/interjobposted', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        date_posted = datetime.strptime(request.form['date_posted'], '%Y-%m-%d').date()
        deadline_date = datetime.strptime(request.form['deadline_date'], '%Y-%m-%d').date()
        description = request.form['description']
        company_name = request.form['company_name']
        location = request.form['location']
        requirement = request.form['requirement']
        job_type = request.form['job_type']

        job = InternshipJob(
            title=title,
            date_posted=date_posted,
            deadline_date=deadline_date,
            description=description,
            company_name=company_name,
            location=location,
            requirement=requirement,
            job_type=job_type
        )

        db.session.add(job)
        db.session.commit()
        
        flash('job  has been posted successfully!', 'success') 

       

    return render_template('/home/interjobposted.html')



#intern job thing

@blueprint.route('/delete2/<int:id>', methods=['POST', 'GET'])
def deletejobintern(id):
   
    jobs2 = InternshipJob.query.get_or_404(id)
    db.session.delete(jobs2)
    db.session.commit()
    flash("Job deleted successfully.")
    
    return redirect(request.referrer)


@blueprint.route('/view_jobs')
def view_jobs():
    jobs = InternshipJob.query.all()
    return render_template('home/updateinternjob.html', jobs=jobs)


@blueprint.route('/update2/<int:job_id>', methods=['GET', 'POST'])
def update_job(job_id):
    job = InternshipJob.query.get(job_id)
    if job is None:
        return redirect(url_for('view_jobs'))

    if request.method == 'POST':
        # Convert the date strings to Python date objects
        date_posted = datetime.strptime(request.form['date_posted'], '%Y-%m-%d').date()
        deadline_date = datetime.strptime(request.form['deadline_date'], '%Y-%m-%d').date()

        # Update the job data in the database based on the form submission
        job.title = request.form['title']
        job.date_posted = date_posted
        job.deadline_date = deadline_date
        job.description = request.form['description']
        job.requirement = request.form['requirement']
        job.location = request.form['location']
        job.company_name = request.form['company_name']
        job.job_type = request.form['job_type']

        db.session.commit()

        flash('job  has been updated successfully!', 'success') 

    return render_template('home/updateinternjob.html', job=job)





@blueprint.route('/index_counts')
def index_counts():
    user_count = Users.query.count()
    job_posted_count = JobPosted.query.count()
    job_application_count = JobApplication.query.count()
    contact_count = Contact.query.count()
    internship_job_count = InternshipJob.query.count()

    return jsonify({
        'user_count': user_count,
        'job_posted_count': job_posted_count,
        'job_application_count': job_application_count,
        'contact_count': contact_count,
        'internship_job_count': internship_job_count
    })
