import pandas as pd
import numpy as np
from sqlalchemy import table
from statistics import mean

def cutOff(df):
    """
    cuts off dataframes with over 20 rounds of data to last 20 rounds
    """
    df = df.tail(20)
    df.index = [i for i in range(1,21)]
    return df

def courseDifferential(r):
    """
    get course differentials from source data
    """
    return (r['score'] - r['rating']) * 113 / r['slope']


def calculateHandicap(tableOfRounds):
    data = {
        'rounds': [i for i in range(1,21)],
        'nToUse': [1,1,1,1,1,2,2,2,3,3,3,4,4,4,5,5,6,6,7,8],
        'adjustment': [0,0,-2,-1,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 
    }
    diffReference = pd.DataFrame(data = data)
    diffReference.set_index('rounds', inplace = True)

    if len(tableOfRounds) > 20:
        tableOfRounds = cutOff(tableOfRounds)
    
    tableOfRounds['roundDifferential'] = tableOfRounds.apply(lambda x: courseDifferential(x), axis = 1)

    sortedDiffs = np.sort(tableOfRounds['roundDifferential'])

    handicapIndex = mean(sortedDiffs[0 : diffReference.loc[len(sortedDiffs)].nToUse]) * 0.96 + diffReference.loc[len(sortedDiffs)].adjustment

    return round(handicapIndex, 2)


