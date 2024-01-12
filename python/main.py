#!/usr/bin/env python3
import multiprocessing
import itertools
import requests
from lxml import etree

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

def get_team_from_mut_gg(team1: str, team2: str, team3: str) -> float:
  hybrid_url = 'https://mut.gg/theme-teams/hybrid'
  request_response = requests.get(hybrid_url, params={'teams': f"{team1},{team2},{team3}"})
  response_content = request_response.content
  tree = etree.HTML(response_content)
  r = tree.xpath('//h3[text()="Overall Ratings"]')
  rating = r[0].getnext().xpath('//div[contains(@class, "text-end")]')
  rating_text = rating[0].text
  print(f"{team1}-{team2}-{team3}: {rating_text}")
  return rating_text


with multiprocessing.Pool() as pool:
    combos_dict = {}
    for team_set in pool.starmap(
        get_team_from_mut_gg, teams
    ):
      combos_dict[str(teams)]
      print(get_team_from_mut_gg(team_set))