
from dataclasses import dataclass
from math import floor
from random import randint, choice
from time import sleep
from typing import Union
from libs.utils import alignment_emoji, progress_bar, GOOD, BAD, HEROE_POWERSTATS, SLOW_EXECUTION

@dataclass
class SuperHero():
    name: str
    intelligence: int
    strength: int
    speed: int
    durability: int
    power: int
    combat: int
    alignment: str
    picture: str
    _health: int = 0

    def __post_init__(self) -> None:
        self.attacks = [self._mental_attack, self._strong_attack, self._fast_attack]

    @property
    def is_alive(self) -> bool:
        return bool(self._health)

    @property
    def is_good(self) -> bool:
        return (self.alignment == GOOD)

    @property
    def dni(self) -> dict:
        return {'name': self.name, 'picture': self.picture}

    @property
    def health(self) -> int:
        return self._health

    @health.setter
    def health(self, value: int) -> None:
        self._health = value if value > 0 else 0

    def __str__(self) -> str:
        return f""" 
            {alignment_emoji(self.is_good)} | {self.name}{' ' * (51 - len(self.name))}
            {'⎯' * 46}{' ' * 10}
            ❤️  {progress_bar(self.health)}
            🧠 {progress_bar(self.intelligence)}
            💪🏼 {progress_bar(self.strength)}
            ⚡️ {progress_bar(self.speed)}
            🛡  {progress_bar(self.durability)}
            🔥 {progress_bar(self.power)}
            ⚔️  {progress_bar(self.combat)}
            {'⎯' * 46}{' ' * 10}
        """

    def apply_team_filiation(self, team_alignment: Union[GOOD, BAD]) -> None:
        self._get_filiation_coefficient(team_alignment)
        self._update_powerstats()
        self._update_health()

    def attack(self, opponent: 'SuperHero') -> None:
        if self.is_alive and opponent.is_alive:
            opponent.health -= choice(self.attacks)()
            print(f"\t\t\t {opponent.name}'s ❤️  : {opponent.health}\n")

    def _get_filiation_coefficient(self, team_alignment: Union[GOOD, BAD]) -> None:
        coefficient = 1 + randint(0, 10)
        power = 1 if team_alignment == self.alignment else -1
        self.filiation_coefficient = (coefficient ** power)
    
    def _update_powerstats(self) -> None:
        for powerstat in HEROE_POWERSTATS:
            stamina = randint(0, 10)
            update_powerstat = lambda base: floor(self.filiation_coefficient * (2 * base + stamina) / 1.1)
            setattr(self, powerstat, update_powerstat(getattr(self, powerstat)))

    def _update_health(self) -> None:
        stamina = randint(0, 10)
        self.health = floor((1 + stamina / 10) * (self.strength * 0.8 + self.durability * 0.7 + self.power) / 2) + 100

    def _mental_attack(self) -> int:
        attack = (self.intelligence * 0.7 + self.speed * 0.2 + self.combat * 0.1) * self.filiation_coefficient
        print(f"\n\t\t 🔮 {self.name} USES MENTAL ATTACK")
        if SLOW_EXECUTION: sleep(1)
        print(f"\t\t\t 💢 YIELDED DAMAGE : {floor(attack)}")
        return floor(attack)

    def _strong_attack(self) -> int:
        attack = (self.strength * 0.6 + self.power * 0.2 + self.combat * 0.2) * self.filiation_coefficient
        print(f"\n\t\t 👊🏼 {self.name} USES STRONG ATTACK")
        if SLOW_EXECUTION: sleep(1)
        print(f"\t\t\t 💢 YIELDED DAMAGE : {floor(attack)}")
        return floor(attack)

    def _fast_attack(self) -> int:
        attack = (self.speed * 0.55 + self.durability * 0.25 + self.strength * 0.1) * self.filiation_coefficient
        print(f"\n\t\t 💫 {self.name} USES FAST ATTACK")
        if SLOW_EXECUTION: sleep(1)
        print(f"\t\t\t 💢 YIELDED DAMAGE : {floor(attack)}")
        return floor(attack)
