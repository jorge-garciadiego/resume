import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_mail import Mail
# from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

app = Flask(__name__)

with app.app_context():
    app.config['SECRET_KEY'] = os.getenv('SEC_KEY')

    ##########################################
    ########### DATABASE SETUP  ##############
    ##########################################
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.db')
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app)
    # migrate = Migrate(app, db)
    Base = automap_base()
    Base.prepare(db.engine, reflect=True)

    from hello_im_jorge.core.views import core

    app.register_blueprint(core)