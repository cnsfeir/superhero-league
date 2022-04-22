
from dataclasses import dataclass
from typing import List
from models.superhero import SuperHero
from libs.utils import GOOD, BAD, alignment_emoji, strike


@dataclass
class Team():
    members: List[SuperHero]
    identifier: int = 1

    def __post_init__(self) -> None:
        self._get_alignment()
        self._apply_team_filiation()
        print(self)

    @property
    def is_good(self) -> bool:
        return (self.alignment == GOOD)
    
    @property
    def is_alive(self) -> bool:
        return any([member.is_alive for member in self.members])

    @property
    def available_members(self) -> List[SuperHero]:
        return [member for member in self.members if member.is_alive]

    @property
    def members_dni(self) -> dict:
        return [member.dni for member in self.members]

    def __str__(self) -> str:
        team = f"\n\t{alignment_emoji(self.is_good)} | TEAM Nº{self.identifier}{' ' * 12} \n\t{'⎯' * 25}"
        for member in self.members:
            status = alignment_emoji(member.is_good) if member.is_alive else "❌"
            name = member.name if member.is_alive else strike(member.name)
            team += f"\n\t{status} | {name}{' ' * (25 - len(str(member.name)))}"
        team += f"\n\t{'⎯' * 25}"
        return team

    def _get_alignment(self) -> None:
        good_ones = [member for member in self.members if member.is_good]
        self.alignment = GOOD if len(good_ones) > (len(self.members) // 2) else BAD

    def _apply_team_filiation(self) -> None:
        for member in self.members:
            member.apply_team_filiation(self.alignment)
