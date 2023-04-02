from flask import render_template, Blueprint, request
from . import db
import pandas as pd
from .handicap_calculate import *

routes = Blueprint('routes', __name__)

@routes.route('/')
def homepage():
    return render_template('homepage.html')

@routes.route('/players')
def players():
    hdcps = {}
    for i in range(1,13):
        scores = pd.read_sql("""
                            SELECT *
                            FROM round
                            JOIN player ON player.id = round.player_id
                            WHERE player.id =
                            """ + str(i), db.engine).convert_dtypes()
        scores = scores.astype({'score': float, 'rating': float, 'slope': float})
        try:
            hdcps[i] = calculateHandicap(scores)
        except:
            hdcps[i] = 0

    table = pd.read_sql("""
                        SELECT 
                        CONCAT_WS(' ', first_name, last_name) AS "Name",
                        SUM(CASE WHEN ROUND.DATE < '2022-12-31' THEN 1 ELSE 0 END) AS "2022 Rounds",
                        SUM(CASE WHEN ROUND.DATE > '2022-12-31' THEN 1 ELSE 0 END) AS "2023 Rounds"
                        FROM player
                        LEFT JOIN round ON player.id = round.player_id
                        GROUP BY player.id
                        ORDER BY player.id
                        """, db.engine)
    table['Handicap'] = [round(i,1) for i in hdcps.values()]
    table['Handicap: Atunyote'] = [round(max(0,(i*127)/113 + (69.5-72)),1) for i in hdcps.values()]
    table['Handicap: Kaluhyat'] = [round(max(0,(i*135)/113 + (71-72)),1) for i in hdcps.values()]
    table['Handicap: Shenandoah'] = [round(max(0,(i*128)/113 + (69.9-72)),1) for i in hdcps.values()]


    return render_template('players.html', tables = [table.to_html(classes = 'table',justify = 'justify-all', index=False)])

@routes.route('/rounds', methods = ['POST', 'GET'])
def rounds():
    if request.method == 'POST':
        from .schema import Player, Round
        roundData = request.form.to_dict()
        roundToAdd = Round(
            course = roundData['course'],
            score = roundData['score'],
            rating = roundData['courseRating'],
            slope = roundData['courseSlope'],
            player_id = roundData['player'],
            tees = roundData['tees']
        )
        db.session.add(roundToAdd)
        db.session.commit()

    table = pd.read_sql("""SELECT
                        CONCAT_WS(' ', first_name, last_name) AS name, course, score, rating, slope
                        FROM player
                        JOIN round ON player.id = round.player_id
                        WHERE round.date > '2022-12-31'
                        ORDER BY round.id DESC
                        """, db.engine)

    return render_template('players.html', tables = [table.to_html(classes = 'table',justify = 'justify-all', index=False)])


@routes.route('/details')
def details():
    return render_template('details.html')