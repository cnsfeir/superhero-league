
import arrow
from dataclasses import dataclass, field
from itertools import permutations
from random import choice, shuffle
from time import sleep
from typing import List, Optional, Tuple
from models.superhero import SuperHero
from models.team import Team
from libs.mailer import Mailer
from libs.utils import VALID_MAILS, SLOW_EXECUTION, ROUNDS_PER_FIGHT, print_fighters, print_teams, bold


@dataclass
class Simulation():
    team_1: Team
    team_2: Team
    fights: List[dict] = field(default_factory=list)

    @property
    def teams(self) -> List[Team]:
        return [self.team_1, self.team_2]

    @property
    def teams_alive(self) -> bool:
        return all(team.is_alive for team in self.teams)

    def start(self) -> None:
        print('\n SIMULATION STARTED!')
        while self.teams_alive:
            if SLOW_EXECUTION: input('\n βΈ  PRESS [ENTER] FOR THE NEXT FIGHT.')
            fighters = self._get_fighters()
            self._fight(fighters)
        
        winner, loser = self._get_results()
        print(f'\n π TEAM {winner.identifier} WINS! π \n')

        mail = self._get_email()
        if mail: Mailer.send_mail(mail, self._build_summary(winner, loser))
        print('\n π SEE YOU IN ANOTHER SIMULATION! \n')

    def _get_results(self) -> Tuple[Team, Team]:
        if SLOW_EXECUTION: sleep(1)
        if self.team_1.is_alive:
            return self.team_1, self.team_2
        return self.team_2, self.team_1
    
    def _get_fighters(self) -> List[SuperHero]:
        fighter_1 = choice(self.team_1.available_members)
        fighter_2 = choice(self.team_2.available_members)
        print_fighters(fighter_1, fighter_2)
        if SLOW_EXECUTION: sleep(1)
        return [fighter_1, fighter_2]

    def _fight(self, fighters: List[SuperHero]) -> None:
        for round_ in range(ROUNDS_PER_FIGHT):
            print(f'\n\t ROUND NΒΊ{round_ + 1}')
            if SLOW_EXECUTION: sleep(1)
            shuffle(fighters)
            for attacker, defender in permutations(fighters):
                attacker.attack(defender)
                if SLOW_EXECUTION: sleep(1)
                if not defender.is_alive:
                    return self._end_fight(attacker, defender)

        print("\n\t βοΈ  IT'S A DRAW!")
        self._register_fight(*fighters)

    def _end_fight(self, attacker: SuperHero, defender: SuperHero) -> None:
        if SLOW_EXECUTION: sleep(1)
        print(f'\t\t π± {defender.name} IS DEAD')
        print(f'\t\t π {attacker.name} WINS!')
        if SLOW_EXECUTION: sleep(2)
        print_teams(self.team_1, self.team_2)
        self._register_fight(attacker, defender, winner=attacker)

    def _build_summary(self, winner: Team, loser: Team) -> dict:
        return {
            'winner_team': winner.identifier,
            'loser_team': loser.identifier,
            'iterable.winner_members': winner.members_dni,
            'iterable.loser_members': loser.members_dni,
            'iterable.fights': self.fights,
            'date': arrow.now().format('D MMMM', locale='es')
        }

    def _register_fight(self, fighter_1: SuperHero, fighter_2: SuperHero, winner: Optional[SuperHero]=None) -> None:
        fight = {'fighter_1': fighter_1.name, 'fighter_2': fighter_2.name, 'is_draw': True}
        if winner: fight.update({'winner': winner.name, 'is_draw': False})
        self.fights.append(fight)

    def _get_email(self) -> Optional[str]:
        option = input(f' ΒΏQUIERES RECIBIR LOS RESULTADOS? π π¨ (Yes/{bold("No")}): ')
        if option.upper() in ['Y', 'YES']:
            mail = input(f' ΒΏA QUE EMAIL LO MANDO? \n π§ : ').lower()
            while mail not in VALID_MAILS:
                print(f"\n NO RECONOZCO ESTE CORREO π§\n INTENTA CON ALGUNO DE LA LISTA: {VALID_MAILS}\n O CANCELA DEJANDOLO VACΓO...")
                mail = input(" π§ : ").lower()
                if not mail: return
            return mail
