#!/usr/bin/env python3
import multiprocessing
import itertools
import requests
from lxml import etree
import csv

allTeams: list[str] = [
    'arizona-cardinals',
    'atlanta-falcons',
    'baltimore-ravens',
    'buffalo-bills',
    'carolina-panthers',
    'chicago-bears',
    'cincinnati-bengals',
    'cleveland-browns',
    'dallas-cowboys',
    'denver-broncos',
    'detroit-lions',
    'green-bay-packers',
    'houston-texans',
    'indianapolis-colts',
    'jacksonville-jaguars',
    'kansas-city-chiefs',
    'las-vegas-raiders',
    'los-angeles-chargers',
    'los-angeles-rams',
    'miami-dolphins',
    'minnesota-vikings',
    'new-england-patriots',
    'new-orleans-saints',
    'new-york-giants',
    'new-york-jets',
    'philadelphia-eagles',
    'pittsburgh-steelers',
    'san-francisco-49ers',
    'seattle-seahawks',
    'tampa-bay-buccaneers',
    'tennessee-titans',
    'washington-commanders'
]

teams = itertools.combinations(allTeams, 3)

def get_team_from_mut_gg(teams: list[str]) -> float:
  team_str = ','.join(teams)
  hybrid_url = 'https://mut.gg/theme-teams/hybrid'
  request_response = requests.get(hybrid_url, params={'teams': team_str})
  response_content = request_response.content
  tree = etree.HTML(response_content)
  r = tree.xpath('//h3[text()="Overall Ratings"]')
  rating = r[0].getnext().xpath('//div[contains(@class, "text-end")]')
  rating_text = rating[0].text
  print(f"{team_str} done!")
  return {
    'teams': team_str,
    'rating': rating_text
  }


with multiprocessing.Pool() as pool:
    combos_dict = {}
    for team_set in pool.map(
        get_team_from_mut_gg, teams
    ):
        combos_dict[team_set.get('teams', '')] = team_set.get('rating', '')
    sorted_combos_dict = dict(sorted(combos_dict.items(), key=lambda kv: (kv[1], kv[0])))
    with open('./files/combos.csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(['Teams', 'Rating'])
        for teams, rating in sorted_combos_dict.items():
            spamwriter.writerow([teams, rating])
    