import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from flask_migrate import Migrate
from dotenv import load_dotenv
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
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app)
    # migrate = Migrate(app, db)
    Base = automap_base()
    Base.prepare(db.engine, reflect=True)


    ##########################################

    ##########################################
    ########### LOGIN CONFIGURATION ##########
    ##########################################
    # login_manager = LoginManager()

    # login_manager.init_app(app)
    # login_manager.login_view = 'core'

    ##########################################

    from hello_im_jorge.core.views import core

    app.register_blueprint(core)