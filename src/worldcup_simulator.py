import csv
import os
import random
import matplotlib.pyplot as plt
from colorama import Fore, Style, init

from src.Team import Team
from src.Match import Match
from src.Group import Group
from src.Knockout_stage import KnockoutStage

init(autoreset=True)

class WorldCupSimulator:
    """
    Main simulator class for the worldcup.
    Manages the entire tournament cycle: 
    loading teams, group seeding snd draws,
    group stage, knockout stagec, and repeated simulations
    """
    KNOCKOUT_PAIRS = [
        ("A",1,"B",2), ("C",1,"D",2), ("E",1,"F",2), ("G",1,"H",2),
        ("B",1,"A",2), ("D",1,"C",2), ("F",1,"E",2), ("H",1,"G",2)
    ]
    
    def __init__(self)-> None:
        self.teams = []
        self.groups = []
        self.seeds = []
        self.round_of_16 = None
        self.quarterfinals = None
        self.semifinals =  None
        self.final = None
        self.champion = None
    
    def load_teams_from_csv(self, filename: str)-> None:
        """
        Loads all teams from the CSV file.

        Args:
            filename (str): Path to the team data file.
        """
        if not os.path.exists(filename):
            print(f"Error: file'{filename}'not found")
            return
            
        self.teams.clear()
        
        try:
            with open(filename,  "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    name = row["name"]
                    attack = int(row["attack"])
                    defense = int(row["defense"])
                    rank = int(row["rank"])
                    
                    team = Team(name, attack, defense, rank)
                    self.teams.append(team)
                if len(self.teams) != 32:
                    raise ValueError("Tournament must contain exactly 32 teams.")
                
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{filename}' was not found.")

        except KeyError as error:
            raise KeyError(f"Missing column in file: {error}")

        except ValueError as error:
            raise ValueError(f"Invalid data in file: {error}")
    
    def create_seeds(self) -> None:
        """
        Sort teams by FIFA ranking and divide them
        into four seeds.
        """
        self.seeds.clear()
        # Sort teams by FIFA ranking.
        self.teams.sort(key=lambda team: team.rank)

        # Create four seeds, each containing eight teams.
        for i in range(0, len(self.teams), 8):
            seed = self.teams[i:i + 8]
            self.seeds.append(seed)
            
    def draw_groups(self) -> None:
        """
        Randomly draws the teams into eight World Cup groups.
        Each group receives exactly one team from each seed.
        """
        self.groups.clear()

        group_names = "ABCDEFGH"
        group_teams = {name: [] for name in group_names}

        # Give one team from each seed to each group
        for seed in self.seeds:
            random.shuffle(seed)

            for index, team in enumerate(seed):
                group_teams[group_names[index]].append(team)

        # Create Group objects
        for name in group_names:
            group = Group(name, group_teams[name])
            self.groups.append(group)
                
    def run_group_stage(self)-> None:
        """ Simulate all matches in the World Cup group stage. """
        for team in self.teams:
            team.reset_stats()
        for group in self.groups:
            group.play_all_matches()  
            
    def setup_knockout_bracket(self)->None:
        """ Build the round-of-16 bracket followong the fixed FIFA pairing rule. """
        advance = {group.name: group.advance_teams() for group in self.groups}
        matches = []
        
        for group1,pos1,group2,pos2 in self.KNOCKOUT_PAIRS:
            team1 = advance[group1][pos1 - 1]
            team2 = advance[group2][pos2 - 1]
            matches.append(Match(team1, team2, is_knockout = True))
            
        self.round_of_16 = KnockoutStage("Round of 16", matches)
            
    def run_knockout_stage(self)-> None:
        """ Simulate all knockout rounds and determine the champion. """
        self.round_of_16.play_round()
        
        qf_matches = [
            Match(w1, w2, is_knockout = True)
            for w1, w2 in zip(
                self.round_of_16.get_winners()[0::2],
                self.round_of_16.get_winners()[1::2])
        ]            
        self.quarterfinals = KnockoutStage("Quarterfinals", qf_matches)
        self.quarterfinals.play_round()
        
        qf_winners = self.quarterfinals.get_winners()

        sf_matches = [
            Match(qf_winners[0], qf_winners[1], is_knockout=True),
            Match(qf_winners[2], qf_winners[3], is_knockout=True)
        ]
        self.semifinals = KnockoutStage("Semifinals", sf_matches)
        self.semifinals.play_round()
        
        
        final_winners = self.semifinals.get_winners()
        final_match = Match(final_winners[0], final_winners[1], is_knockout = True)
        self.final = KnockoutStage("Final", [final_match])
        self.final.play_round()
        
        self.champion = self.final.matches[0].winner
    
    def run_full_simulation(self)-> Team:
        """ 
        Runs one complete World Cup tournament.
        
        Returns:
            Team: the champion of this run
        """
        for t in self.teams:
            t.reset_stats()
            
        self.create_seeds()
        self.draw_groups()
        self.run_group_stage()
        self.setup_knockout_bracket()
        self.run_knockout_stage()
        return self.champion
    
    def most_likely_champion(self, num_simulations=1000):
        """
        Runs the simulation the given number of times and repeat each
        team's championship percentage.

        Args:
            num_simulations (int): number of simulations. Defaults to 1000.
        """
        if num_simulations <= 0:
            print("Error: number of simulations must be a positive integer")
            return
        
        counts = {team.name: 0 for team in self.teams}
        for _ in range(num_simulations):
            champ = self.run_full_simulation()
            counts[champ.name] += 1
            
        print(f"Simulation ran {num_simulations} times.")
        print(Fore.YELLOW + Style.BRIGHT + "========== Championship Percentages ==========\n")
        for name, count in sorted(counts.items(), key = lambda x: x[1], reverse = True):
            if count > 0:
                percentage = count / num_simulations * 100

            if percentage >= 5:
                color = Fore.GREEN
            elif percentage >= 2:
                color = Fore.CYAN
            else:
                color = Fore.RED

            print(color + f"{name:<15} {percentage:>5.1f}%")
                
                
        self.plot_championship_chances(counts, num_simulations)
                
    def plot_championship_chances(self, counts: dict, num_simulations: int)-> None:  #Extra
        """ 
        Draws a bar chart of the top 10 teams by championship percentages
        and saves it as an image file

        Args:
            counts (dict): mapping of team name to number of championships won.
            num_simulations (int): total number of simulations run.
        """
        top_teams = sorted(counts.items(), key = lambda x: x[1], reverse = True)[:10]
        names = [name for name, count in top_teams if count > 0]
        percentages = [count / num_simulations * 100 for name, count in top_teams if count > 0]
        
        if not names:
            print("No championship data plot.")
            return
        
        plt.figure(figsize = (10,6))
        plt.bar(names, percentages, color = "#2E7D32")
        plt.xlabel("Team")
        plt.ylabel("Championship Probability(%)")
        plt.title(f"Championship Changes({num_simulations} Simulations)")
        plt.xticks(rotation = 45, ha = "right")
        plt.tight_layout()
        plt.savefig("championship_chances.png")
        plt.close()
        print(Fore.GREEN + "\n✓ Chart saved as championship_chances.png")
        
    def display_bracket(self)-> None:
        """ Displays the knockout bracket from the most recent simulation. """
        if self.round_of_16 is None:
            print("No simulation has been run yet.")
            return
        
        print()
        print(Fore.YELLOW + "=" * 60)
        print(Fore.CYAN + Style.BRIGHT + "🏆 KNOCKOUT BRACKET 🏆".center(60))
        print(Fore.YELLOW + "=" * 60)
        
        for stage in (self.round_of_16, self.quarterfinals, self.semifinals, self.final):
            stage.display_results()
    
