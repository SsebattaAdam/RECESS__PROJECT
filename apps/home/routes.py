# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.authentication.models import JobPosted, Contact,InternshipJob
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound



@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')






@blueprint.route('/All_jobs.html', methods=['GET'])
@login_required
def vialljobs():
    jobs = JobPosted.query.all()
    jobs2 = InternshipJob.query.all()
    return render_template('home/All_jobs.html', jobs=jobs, jobs2=jobs2)


@blueprint.route('/<template>')
@login_required

def route_template(template):
    contacts = Contact.query.all()

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)
        # jobs = JobPosted.query.all()
        # print(jobs)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment,  contacts = contacts,)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None


