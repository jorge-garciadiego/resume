from hello_im_jorge import db
from hello_im_jorge.models import Skills, Users, Education, Experience, Bullet
from flask import render_template, request, Blueprint
from datetime import datetime, date

core = Blueprint('core', __name__)

def date_diff(date1, date2):
    date_format = "%B %Y"
    return (datetime.strptime(date1, date_format) - datetime.strptime(date2,date_format))


@core.route('/', methods=['GET'])
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
        
    
    # create a dictionary with the bullets for each job the key is the id of the experience table
    
    return render_template('index.html', user=user, skill_cats=skill_cats, skills=skills, edu=edu, exp = experience, bullets=exp_bullets, icons=icons, exp_years = exp_years)