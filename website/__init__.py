from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import psycopg2

db = SQLAlchemy()
DB_CONN_STRING = 'postgres://ophjaempldiesk:5ce9b296fd019992f9de770771cbf2b61d558b40ea28fde7c6c50a5715e287bf@ec2-3-217-146-37.compute-1.amazonaws.com:5432/d8t3kaotnthv6u'

def createDatabase(app):
        db.create_all(app=app)

def createApp():
    app = Flask(__name__)
    app.config['SECURE_KEY'] = os.getenv('SECURE_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONN_STRING 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .routes import routes

    app.register_blueprint(routes, url_prefix = '/')

    from .schema import Player, Round
    createDatabase(app)

    from .listPlayers import players
    with app.app_context():
        if len(Player.query.all()) < 12:
            addToDb = [Player(first_name = player[0], last_name=player[1]) for player in players]
            for player in addToDb:
                db.session.add(player)
                print(player.first_name + player.last_name + " added to database")
            db.session.commit()
    return app

