#!/usr/bin/env python3
import multiprocessing
import itertools
import requests
from lxml import etree
import csv

seahawks: str = 'seattle-seahawks'
eagles: str = 'philadelphia-eagles'

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
    'pittsburgh-steelers',
    'san-francisco-49ers',
    'tampa-bay-buccaneers',
    'tennessee-titans',
    'washington-commanders'
]


def get_team_from_mut_gg(teams: tuple[str, str, str]) -> float:
  (team1, team2, team3) = teams
  team_str = f"{team1},{team2},{team3}"
  print(f"looking at {team_str}")
  hybrid_url = 'https://mut.gg/theme-teams/hybrid'
  request_response = requests.get(hybrid_url, params={'teams': team_str})
  response_content = request_response.content
  tree = etree.HTML(response_content)
  r = tree.xpath('//h3[text()="Overall Ratings"]')
  rating = r[0].getnext().xpath('//div[contains(@class, "text-end")]')
  rating_text = rating[0].text
  print(f"{team_str} done!")
  return {
    'team1': team1.replace('-', ' ').title(),
    'team2': team2.replace('-', ' ').title(),
    'team3': team3.replace('-', ' ').title(),
    'rating': rating_text
  }


def main(allTeams: list[str]):
  teams = [(seahawks, eagles, team) for team in allTeams]
  combos = []
  with multiprocessing.Pool() as pool:
      for team_set in pool.map(
          get_team_from_mut_gg, teams
      ):
          combos.append(team_set)
  sorted_combos = sorted(combos, key=lambda kv: (kv.get('rating')), reverse=True)
  with open('./files/combos.csv', 'w') as csvfile:
      spamwriter = csv.writer(csvfile)
      spamwriter.writerow(['Team 1', 'Team 2', 'Team 3', 'Rating'])
      for combo in sorted_combos:
          spamwriter.writerow([combo.get('team1'), combo.get('team2'), combo.get('team3'), combo.get('rating')])
    
if __name__ == "__main__":
  main(allTeams)
