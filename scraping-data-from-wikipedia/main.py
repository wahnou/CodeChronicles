from bs4 import BeautifulSoup
import requests
import json

req = requests.get("https://en.wikipedia.org/wiki/Botola")
soup = BeautifulSoup(req.content, 'html.parser')

winners_table = soup.find("th", string="Season").parent.parent

winners_list = []
for winner in winners_table.find_all("tr"):
    season_details = winner.find_all("td")
    if len(season_details):
        winners_list.append({
            'season': season_details[0].text,
            'winner': season_details[1].text
        })

with open("botola_winners.json", "w") as outfile:
    outfile.write(json.dumps(winners_list, indent=4))