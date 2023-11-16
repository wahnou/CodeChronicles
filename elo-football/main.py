import pandas as pd

#Formulas implementation:

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
    matchs = pd.read_csv("int/results.csv")

    # 1. Set-up tournaments k value:
    # 1.1 All tournaments get a default value of 30
    tournaments = matchs['tournament'].unique()
    tournaments = {tournament: 30 for tournament in tournaments}

    # 1.2 Main tournaments get specific values
    tournaments['FIFA World Cup qualification'] = 40
    tournaments['FIFA World Cup'] = 60
    tournaments['Friendly'] = 20
    confederation_tournaments=['AFC Asian Cup','African Cup of Nations','UEFA Euro','Copa América','CONCACAF Championship', 'Oceania Nations Cup']
    for t in tournaments:
        if t in confederation_tournaments:
            tournaments[t] = 50
        elif t.replace(' qualification', '') in confederation_tournaments:
            tournaments[t] = 40

    # 2. Retriving all exsting teams with a starting ranking of 1000
    teams = pd.concat([matchs['home_team'], matchs['away_team']]).unique()
    teams = {team: 1000 for team in teams}

    # Apply Elo
    for index, match in matchs.iterrows():
        var = P(match, tournaments[match['tournament']])
        teams[match['home_team']] += var
        teams[match['away_team']] -= var

    i=1
    for team, ranking in sorted(teams.items(), key=lambda x: x[1], reverse=True):
        print(str(i)+' - '+team+' ('+str(ranking)+')')
        i+=1