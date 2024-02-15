import pandas as pd
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import json
import operator

#Formulas:

# The expected result:
def We(match):
    dr = (teams[match['home_team']] - teams[match['away_team']]) + (100 if not match['neutral'] else 0)
    return 1 / (10**float(-dr/400)+1)

# The result of the match:
def W(match):
    if match['home_score'] == match['away_score']:
        return 0.5
    if match['home_score'] > match['away_score']:
        return 1
    return 0

# A number from the index of goal differences
def G(match):
    gd = abs(match['home_score'] - match['away_score'])
    if gd == 0 or gd == 1:
        return 1
    if gd == 2:
        return float(3/2)
    return float((11+gd)/8)

# Points change:
def P(match, k):
    return round(k * G(match) * (W(match) - We(match)))


if __name__ == "__main__":
    # You can download this dataset here: https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017?select=results.csv
    matchs = pd.read_csv("datasets/2024_02_15/results.csv")

    # 1. Set-up tournaments k value:
    # 1.1 All tournaments get a default value of 30
    tournaments = matchs['tournament'].unique()
    tournaments = {tournament: 30 for tournament in tournaments}

    # 1.2 Init other tournaments:
    confederation_tournaments=[
        'AFC Asian Cup',
        'African Cup of Nations',
        'CONCACAF Championship',
        'Copa América',
        'UEFA Euro',
        'Oceania Nations Cup',
    ]
    
    for t in tournaments:
        if t in confederation_tournaments:
            tournaments[t] = 50 #Main tournaments k=50
        elif (t.replace(' qualification', '') in confederation_tournaments):
            tournaments[t] = 40 #Main tournament qualifiers k=40
    
    # 1.3 Special cases in the dataset:
    tournaments['FIFA World Cup qualification'] = 40
    tournaments['FIFA World Cup'] = 60
    tournaments['Friendly'] = 20
    
    # 1.4 Creating a list of tuples (tournament, rating) and stored them in a tournaments.json file to check tournaments k values:
    sorted_tournaments = sorted(tournaments.items(), key=operator.itemgetter(1), reverse=True)
    with open("tournaments.json","w") as file:
        file.write(json.dumps(sorted_tournaments, indent=4))

    # 2. Retriving all exsting teams and initiat all ranking at 1000
    teams = pd.concat([matchs['home_team'], matchs['away_team']]).unique()
    teams = {team: 1000 for team in teams}
    
    # Appling Elo
    for index, match in matchs.iterrows():
        var = P(match, tournaments[match['tournament']])
        teams[match['home_team']] += var
        teams[match['away_team']] -= var

    # Plot top teams:
    top = 25
    teams = dict(sorted(teams.items(), key=lambda x: x[1], reverse=True)[:top])
    print(teams)

    plt.figure(figsize=(8, 6))

    # Plotting the bars
    plt.barh(range(len(teams)), list(teams.values()), align='center', label='Rating')

    # Adding labels to the bars
    for i, (team, rating) in enumerate(teams.items()):
        plt.text(i, rating + 1, str(rating), ha='center')

    # Adding x-axis labels and rotating for better readability
    plt.yticks(range(len(teams)), teams.keys(), rotation=45)
    plt.ylabel('National teams')
    plt.xlabel('Rating')
    plt.title(f'Top {top} teams')
    
    plt.gca().invert_yaxis() 

    # Displaying the plot
    plt.legend()
    plt.tight_layout()
    plt.show()
