from hello_im_jorge import db
from hello_im_jorge.models import Skills, Users, Education, Experience, Bullet
from flask import render_template, request, Blueprint
from datetime import datetime, date
from flask_mail import Message
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from flask import current_app
import os

core = Blueprint('core', __name__)


def date_diff(date1, date2):
    date_format = "%B %Y"
    return (datetime.strptime(date1, date_format) - datetime.strptime(date2,date_format))

# Contact me Form
class ContactMeForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email(message='Invalid email address')])
    subject = StringField("Subject", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send Message")


@core.route('/', methods=['GET', 'POST'])
def index():
    
    icons = {'Data Science': 'uil uil-brain', 'Data Visualization':'uil uil-chart-line', 'Frontend developer': 'uil uil-brackets-curly', 'Languages': 'uil uil-language'}
    
    user = db.session.query(Users).all()
    
    # Get skills categories
    skill_cats = db.session.query(Skills.category).distinct().all()
    skill_cats = [item[0] for item in skill_cats]
    
    skills = db.session.query(Skills).all()
    
    edu = db.session.query(Education).all()
    
    experience = db.session.query(Experience).all()
    
    bullet = db.session.query(Bullet).all()
    
    exp_bullets = {}
    
    exp_years = 0
    
    for e in experience:
        if e.end_date == None:
            exp_years += date_diff(datetime.today().strftime("%B %Y"), e.start_date).days/365.25
            print(exp_years)
        else:
            exp_years += date_diff(e.end_date, e.start_date).days/365.25
            print(exp_years)
    
    exp_years = int(exp_years)
    
    if exp_years < 10:
        exp_years = f"0{exp_years}+"
    else:
        exp_years = f"{exp_years}+"
    
    for i in experience:
        exp_bullets[i.id] = [b.description for b in bullet if b.experience_id == i.id]
    
    form = ContactMeForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            subject = form.subject.data
            body = form.message.data
            
            
            msg = Message(subject=f"{name} - sent by {subject}", body=f"Sent by {name}: {email}\n\nSubject: {subject}\n\n{body}", sender='me.garciadiego@gmail.com', recipients=['jorge.garciadiego@icloud.com'])
            mail = current_app._get_current_object().extensions.get('mail')
            mail.send(msg)
            
            form.name.data = ''
            form.email.data = ''
            form.subject.data = ''
            form.message.data = ''
                 
    # create a dictionary with the bullets for each job the key is the id of the experience table
    
    return render_template('index.html', user=user, skill_cats=skill_cats, skills=skills, edu=edu, exp = experience, bullets=exp_bullets, icons=icons, exp_years = exp_years, form=form)