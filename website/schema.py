from . import db

class Player(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    rounds = db.relationship('Round')

    def __repr__(self):
        return str(self.__dict__)

class Round(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    course = db.Column(db.String(80))
    score = db.Column(db.String(80))
    rating = db.Column(db.String(80))
    slope = db.Column(db.String(80))

    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    
    def __repr__(self):
        return str(self.__dict__)