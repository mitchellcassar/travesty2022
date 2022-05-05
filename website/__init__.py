from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

db = SQLAlchemy()
DB_CONN_STRING = 'postgresql://yrbvxdrectywvl:2bd707ad3a9ed5f9e24445fcbaf416a78b29efdbc4891031e6c77a5f79d8da68@ec2-52-5-110-35.compute-1.amazonaws.com:5432/dedih68fbgaf2i'
#DB_CONN_STRING = os.getenv('HEROKU_POSTGRES_URL')

def createDatabase(app):
        db.create_all(app=app)

def createApp():
    app = Flask(__name__)
    app.config['SECURE_KEY'] = 'fkrmmkpgmfkp3emfkpmpampmfpd'
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONN_STRING 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .routes import routes

    app.register_blueprint(routes, url_prefix = '/')

    from .schema import Player, Round
    if 1 == 2:
        createDatabase(app)

    from .listPlayers import players
    if 1==2:
        with app.app_context():
            if len(Player.query.all()) < 12:
                addToDb = [Player(first_name = player[0], last_name=player[1]) for player in players]
                for player in addToDb:
                    db.session.add(player)
                    print(player.first_name + player.last_name + " added to database")
                db.session.commit()
    return app

