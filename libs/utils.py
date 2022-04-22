
import os
from dotenv import load_dotenv
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from models.superhero import SuperHero
    from models.team import Team

load_dotenv()
VALID_MAILS = os.environ.get('VALID_MAILS').split(',')
SLOW_EXECUTION = bool(int(os.environ.get('SLOW_EXECUTION')))

BAD = 'bad'
GOOD = 'good'
TOTAL_HEROS = 731
HEROS_PER_TEAM = 5
ROUNDS_PER_FIGHT = 3
HEROE_POWERSTATS = ['intelligence','strength','speed','durability','power','combat']

def progress_bar(value: int) -> str:
    bar_value = 1900 if value > 1900 else value
    filled = (40 * bar_value // 1900)
    bar = ('◼︎' * filled) + ' ' * (40 - filled)
    return f"| {bar} | {value}{' ' * (8 - len(str(value)))}"

def is_numeric(value: str) -> bool:
    return isinstance(value, str) and value.isdecimal()

def alignment_emoji(is_good: bool) -> str:
    return '😇' if is_good else '😈'

def parallel_print(elements: List[str]) -> None:
    zipped = zip(*[string.split("\n") for string in elements])
    for elements in zipped:
        print("".join(elements))

def print_fighters(fighter_1: 'SuperHero', fighter_2: 'SuperHero') -> None:
    print(f"\n\n {'=' * 60} \n\n")
    print(f'  NEXT FIGHT: {fighter_1.name} 🆚 {fighter_2.name}')
    parallel_print([str(fighter_1), str(fighter_2)])

def print_teams(team_1: 'Team', team_2: 'Team') -> None:
    print(f'\n ℹ️  TEAMS STATUS:')
    parallel_print([str(team_1), str(team_2)])

def strike(text: str) -> str:
    return ''.join([u'\u0336{}'.format(c) for c in text])

def bold(text: str) -> str:
    return '\033[1m' + text + '\033[0m'
