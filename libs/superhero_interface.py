import os, requests, random
from dotenv import load_dotenv
from typing import Optional, Tuple
from models.superhero import SuperHero
from models.team import Team
from libs.utils import is_numeric, TOTAL_HEROS, HEROS_PER_TEAM, GOOD


load_dotenv()
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
BASE_URL = f'https://superheroapi.com/api/{ACCESS_TOKEN}/'

class SuperHeroInterface():

    @classmethod
    def get_teams(cls) -> Tuple[Team, Team]:
        print(f'\n CREATING TEAMS ...')
        superheros = random.sample(range(1, TOTAL_HEROS), HEROS_PER_TEAM * 2)
        members = [cls._get_superhero(id_) for id_ in superheros]
        team_1 = Team(members=members[HEROS_PER_TEAM:], identifier=1)
        team_2 = Team(members=members[:HEROS_PER_TEAM], identifier=2)
        return team_1, team_2

    @classmethod
    def _get_superhero(cls, identifier: int) -> Optional[SuperHero]:
        print(f'\t ⤵️  IMPORTING SUPERHERO Nº{identifier}')
        url = f'{BASE_URL}{identifier}'
        response = requests.get(url)
        if response.status_code == 200:
            data = cls._get_superhero_data(requests.get(url))
            if data: return SuperHero(**data)
        raise Exception(f'\n\t ❌ RESPONSE ERROR: {response.status_code}')

    @classmethod
    def _get_superhero_data(cls, response: requests.Response) -> Optional[dict]:
        if 'application/json' in response.headers.get('Content-Type'):
            content = response.json()
            data = cls._format_powerstats(content['powerstats'])
            data.update({
                'name': content.get('name', ''),
                'picture': content.get('image', {}).get('url', ''),
                'alignment': content.get('biography', {}).get('alignment', GOOD)
            })
            return data
        raise Exception(f'\n\t ❌ RESPONSE ERROR: JSON VERSION NOT AVAILABLE')

    @staticmethod
    def _format_powerstats(powerstats: dict) -> dict:
        for powerstat, value in powerstats.items():
            if isinstance(value, int): continue
            powerstats[powerstat] = int(value) if is_numeric(value) else 0
        return powerstats
