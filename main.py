from models.simulation import Simulation
from libs.superhero_interface import SuperHeroInterface

if __name__ == '__main__':
    teams = SuperHeroInterface.get_teams()
    Simulation(*teams).start()
