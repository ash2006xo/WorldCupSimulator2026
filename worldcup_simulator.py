# ============================================================
# Student : Narges Farhangi                       
# Student ID : [ 404131043 ]                      
# Project : World Cup Simulator 2026
# Date : *****
# ============================================================

"""
World Cup 2026 Simulator

This project simulates the FIFA World Cup using
Object-Oriented Programming.

Main Features:
- Team loading
- Group draw
- Match simulation
- Knockout stage
- Tournament statistics
- Multiple tournament simulations
"""

# ===================== IMPORTS ==============================
import csv
import random
import os

import numpy as np

#===================== CONSTANTS =============================
NUMBER_OF_TEAMS = 32
NUMBER_OF_GROUPS = 8
TEAMS_PER_GROUP = 4

GROUP_STAGE_MATCHES = 6

MATCH_DURATION = 90
EXTRA_TIME_DURATION = 30

WIN_POINTS = 3
DRAW_POINTS = 1
LOSS_POINTS = 0

PENALTY_SHOTS = 5

MINIMUM_LAMBDA = 0.05

# =================== HELPER FUNCTIONS =======================



# ===================== TEAM CLASS ===========================
class Team:
    """ Represents a national football team participating in the World Cup tournament. """
    def __init__(self, name: str, attack: int, defense: int, rank: int)-> None:
        """
        Initializes a Team object.

        Args:
            name (str): Team name.
            attack (int): Attack rating (0-100).
            defense (int): Defense rating (0-100).
            rank (int): FIFA ranking.
        """
         
        if not 0 <= attack <= 100:
            raise ValueError("Attack must be between 0 and 100.")

        if not 0 <= defense <= 100:
            raise ValueError("Defense must be between 0 and 100.")

        if rank <= 0:
            raise ValueError("Rank must be greater than zero.")
        
        self.name = name
        self.attack = attack
        self.defense = defense
        self.rank = rank
          
        self.group = None
         
        self.wins = 0
        self.draws = 0
        self.losses = 0
        
        self.points = 0
        self.goals_for = 0
        self.goals_against = 0
         
    def reset_stats(self)-> None:
        """
         Resets all tournament statistics before starting
         a new tournament simulation.
        """
        self.wins = 0
        self.draws = 0
        self.losses = 0
        
        self.points = 0
        self.goals_for = 0
        self.goals_against = 0
        
    def goal_difference(self)-> int:
        """ Returns the team's goal difference. """
        return self.goals_for - self.goals_against
    
    def add_match_result(self, goals_scored: int, goals_conceded: int) -> None:      # will be added to team/match class
        """
        Updates the team's statistics after a match.

        Args:mb,d
            goals_scored (int): Goals scored by the team.
            goals_conceded (int): Goals conceded by the team.
        """

        self.goals_for += goals_scored
        self.goals_against += goals_conceded

        if goals_scored > goals_conceded:
            self.wins += 1
            self.points += WIN_POINTS

        elif goals_scored == goals_conceded:
            self.draws += 1
            self.points += DRAW_POINTS

        else:
            self.losses += 1
            self.points += LOSS_POINTS
    
    def __str__(self)-> str:
        """ Returns a readable string representation of the team. """
        return (
            f"{self.name} | "
            f"Rank: {self.rank} | "
            f"Attack: {self.attack} | "
            f"Defense: {self.defense} | "
            f"Points: {self.points} | "
            f"GD: {self.goal_difference()}"
        )

# ===================== MATCH CLASS ==========================
class Match:
    """ Represents a football match between two teams. """
    def __init__(self, team1: Team, team2: Team, is_knockout: bool = False)-> None:
        """
        Initializes a Match object.

        Args:
            team1 (Team): First team.
            team2 (Team): Second team.
            is_knockout (bool): True if this is a knockout-stage match.
        """
        self.team1 = team1
        self.team2 = team2
        
        self.goals1 = 0
        self.goals2 = 0

        self.is_knockout = is_knockout

        self.winner = None

        self.penalties1 = None
        self.penalties2 = None
        
    def play(self)-> None:
        """
        Plays the whole match.

        This method:
        1. Simulates the normal 90 minutes.
        2. If this is a knockout match and the score is tied,
        simulates extra time.
        3. If still tied, simulates a penalty shootout.
        4. Determines the winner.
        5. Updates both teams' tournament statistics.
        """
        # Play the normal 90 minuets match
        self._simulate_normal_time()
        
        # Knockout stage
        if self.is_knockout and self.goals1 == self.goals2:
            self._simulate_extra_time()
        
        if self.is_knockout and self.goals1 ==  self.goals2:
            self._simulate_penalties()
            
        # Determine the winner
        self._determine_winner()
        
        # Update statistics
        self._update_statistics()
            
    def _calculate_lambda(self, team: Team, opponent: Team)-> float:
        """ Calculates the expected number of goals (lambda) for a team using the assignment formula. """
        return ((team.attack / 100) * 1.5 + (1 - opponent.defense / 100) * 0.8)
        
    def _simulate_normal_time(self)-> None:
        """ Simulates the 90-minute match using a Poisson distribution. """
        lambda1 = self._calculate_lambda(self.team1, self.team2)
        lambda2 = self._calculate_lambda(self.team2, self.team1)
        
        self.goals1 = np.random.poisson(lambda1)
        self.goals2 = np.random.poisson(lambda2)
        
    def _simulate_extra_time(self)-> None:
        """ Simulates 30 minutes of extra time."""

        lambda1 = self._calculate_lambda(self.team1, self.team2) * 0.33
        lambda2 = self._calculate_lambda(self.team2, self.team1) * 0.33

        self.goals1 += np.random.poisson(lambda1)
        self.goals2 += np.random.poisson(lambda2)
    
    def _penalty_probability(self, team: Team, opponent: Team)-> float:
        """ Calculates the probability that a penalty kick is scored. """
        probability = (0.75 + (team.attack - opponent.defense) / 250)
        return max(0.6, min(0.9, probability))

    def _simulate_penalties(self)-> None:
        """ Simulates a penalty shootout including sudden death. """
        self.penalties1 = 0
        self.penalties2 = 0
        
        probability1 = self._penalty_probability(self.team1, self.team2)
        probability2 = self._penalty_probability(self.team2, self.team1)
        
        # First five penalties
        for _ in range(5):
            if random.random() < probability1:
                self.penalties1 += 1
            if random.random() < probability2:
                self.penalties2 += 1

        # Sudden death
        while self.penalties1 == self.penalties2:
            scored1 = random.random() < probability1
            scored2 = random.random() < probability2

            if scored1:
                self.penalties1 += 1
            if scored2:
                self.penalties2 += 1   
                
    def _determine_winner(self)-> None:
        """ Determines the winner of the match. """
        if self.goals1 > self.goals2:
            self.winner = self.team1
            
        elif self.goals2 > self.goals1:
            self.winner = self.team2
            
        elif self.is_knockout :
            if self.penalties1 > self.penalties2:
                self.winner = self.team1
            else:
                self.winner = self.team2

        else:
            self.winner = None
             
    def _update_statistics(self)-> None:
        """  Update both teams' tournament statistics. """
        self.team1.add_match_result(self.goals1, self.goals2)
        self.team2.add_match_result(self.goals2, self.goals1)
        
    def __str__(self)-> str:
        """ Return a readable representation of the match. """
        result = (
            f"{self.team1.name} {self.goals1} - "
            f"{self.goals2} {self.team2.name}"
        )

        if self.penalties1 is not None and self.penalties2 is not None:
            result += f" (Penalties: {self.penalties1}-{self.penalties2})"

        if self.winner is not None:
            result += f"\nWinner: {self.winner.name}"

        return result
        
# ==================== GROUP CLASS ===========================
class Group:
    """
    Represents a World Cup group containing four teams.

    A Group is responsible for managing the group-stage matches,
    ranking the teams based on the tournament rules, and determining
    which two teams advance to the knockout stage.
    """
    def __init__(self, name: str, teams: list[Team]) -> None:
        """
        Initializes a Group object.

        Args:
            name (str): The name of the group (e.g., "A", "B", ..., "H").
        """
        if len(teams) != 4:
            raise ValueError("A group must contain exactly four teams.")
        
        self.name = name
        self.teams = teams
        self.matches = []

        for team in self.teams:
            team.group = self.name
            
    def play_all_matches(self)-> None:
        """
        Plays every match in the group.

        Each team plays exactly one match against every
        other team, resulting in six matches.
        """
        self.matches.clear()
         
        # Each team plays with the team after it    
        for i in range(len(self.teams)):
            for j in range(i + 1, len(self.teams)):
                match = Match(self.teams[i], self.teams[j])
                    
                match.play()
                self.matches.append(match)
            
    def _head_to_head_winner(self, team_a, team_b)-> None:  # Extra
        """
        Finds the direct group-stage match between two teams and returns
        the team that won it.

        Args:
            team_a (Team): first team.
            team_b (Team): second team.
            
        Returns:
            Team or None: the winner of their direct match, or none if
            the match was a draw.
            """
        for match in self.matches:
            if {match.team1, match.team2} == {team_a, team_b}:
                return match.winner
        return None
            
    def get_ranking(self)-> list[Team]:
        """
        Returns the teams ranked from first to fourth.

        Teams are ranked by:
        1. Points
        2. Goal difference
        3. Goals scored
        4. Random draw if still tied
        """
        # Sort the teams according to the World Cup ranking rules.
        ranking = sorted(
            self.teams,
            key=lambda team:(
                team.points,
                team.goal_difference(),
                team.goals_for
            ),
            reverse=True   # Higher values should come first.
        ) 
            
        # Check for teams that are still completely tied after sorting
        for i in range(len(ranking) - 1):   # We compare each team with the one after it (i + 1), so stopping one position early prevents an IndexError.
            current = ranking[i]
            next_team = ranking[i + 1]

            if (
                current.points == next_team.points
                and current.goal_difference() == next_team.goal_difference()
                and current.goals_for == next_team.goals_for
            ):
                head_to_head_winner = self._head_to_head_winner(current, next_team)
                
                if head_to_head_winner is next_team:
                    # next_team beat current directly -> it should rank higher
                    ranking[i], ranking[i + 1] = ranking[i + 1], ranking[i]
                    
                elif head_to_head_winner is current:
                    continue  # current already beat next_team directly -> order stays as is
                
                else:
                    # Their direct match was also a draw -> fall back to random
                    if random.choice([True, False]):
                        ranking[i], ranking[i + 1] = ranking[i + 1], ranking[i]

        return ranking      
        
    def advance_teams(self)-> tuple[Team, Team]:
        """
        Returns the two teams that advance to the knockout stage.

        Returns:
        tuple[Team, Team]: The first-place and second-place teams.
        """
        ranking = self.get_ranking()
        
        first_team = ranking[0]
        second_team = ranking[1]
        
        return first_team, second_team
    
    def __str__(self)-> str:
        """ Returns a readable string representation of the group standings. """
        ranking = self.get_ranking()

        result = f"\n========== Group {self.name} ==========\n"
        # Display each team's position and statistics.
        for position, team in enumerate(ranking, start=1):
            result += (
                f"{position}. {team.name:<15}"
                f"Pts: {team.points:<2} | "
                f"GD: {team.goal_difference():+3} | "
                f"GF: {team.goals_for}\n"
            )

        return result
            
# ==================== KNOCKOUT STAGE CLASS ===================
class KnockoutStage:
    """
    Represents one knockout round of the World Cup.

    A KnockoutStage object contains all matches for a
    specific round (e.g., Round of 16, Quarter-finals,
    Semi-finals, or Final).
    """
    def __init__(self, round_name: str, matches: list[Match])-> None:
        """
        Initializes a knockout stage.

        Args:
            round_name (str): Name of the knockout round.
            matches (list[Match]): List of matches in this round.
        """
        self.round_name = round_name
        self.matches = matches
        
    def play_round(self)-> None:
        """ Plays every match in the current knockout round. """
        for match in self.matches:
            match.play()
            
    def get_winners(self)-> list[Team]:
        """
        Returns the winners of all matches in the current round.

        Returns:
            list[Team]: Teams that advance to the next round.
        """
        winners = []

        for match in self.matches:
            winners.append(match.winner)

        return winners
        
    def display_results(self)-> None:
        """ Displays the results of every match in the current round. """
        print(f"\n========== {self.round_name} ==========")
        
        for match in self.matches:
            print(match)

# ============== WORLD CUP SIMULATOR CLASS ===================
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
        print("Championship percentages: ")
        for name, count in sorted(counts.items(), key = lambda x: x[1], reverse = True):
            if count > 0:
                print(f"{name}: {count / num_simulations * 100:.1f}%")
                
    def display_bracket(self)-> None:
        """ Displays the knockout bracket from the most recent simulation. """
        if self.round_of_16 is None:
            print("No simulation has been run yet.")
            return
        
        print("============== Knockout Bracket ================")
        for stage in (self.round_of_16, self.quarterfinals, self.semifinals, self.final):
            stage.display_results()
    
# ===================== MAIN FUNCTION ========================
# =============   TEST(temp)
def main():
    """Temporary demo menu so we can run the whole project end-to-end and
    confirm every stage works before polishing the real menu."""
    sim = WorldCupSimulator()
    groups_drawn = False

    while True:
        print("\n===== World Cup Simulator =====")
        print("1) Load teams from CSV")
        print("2) Draw groups (automatic seeding)")
        print("3) Run group stage and show tables")
        print("4) Run full tournament and show champion")
        print("5) Run 1000-time simulation and show percentages")
        print("6) Show last simulation's knockout bracket")
        print("7) Exit")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            sim.load_teams_from_csv("worldcup_2026_teams.txt")
        
        elif choice == "2":
            if not sim.teams:
                print("Please load teams first (option 1).")
                continue
            sim.create_seeds()
            sim.draw_groups()
            groups_drawn = True
            print("Groups drawn successfully.")

        elif choice == "3":
            if not groups_drawn:
                print("Please draw groups first (option 2).")
                continue
            
            sim.run_group_stage()
            for group in sim.groups:
                print(group)

        elif choice == "4":
            if not sim.teams:
                print("Please load teams first (option 1).")
                continue
            champion = sim.run_full_simulation()
            print(f"\nChampion: {champion.name}")

        elif choice == "5":
            if not sim.teams:
                print("Please load teams first (option 1).")
                continue
            raw = input("Number of simulations (default 1000): ").strip()
            try:
                num = int(raw) if raw else 1000
            except ValueError:
                print("Invalid number, using default 1000.")
                num = 1000
            sim.most_likely_champion(num)

        elif choice == "6":
            sim.display_bracket()

        elif choice == "7":
            print("Goodbye.")
            break

        else:
            print("Invalid option, please choose 1-7.")


if __name__ == "__main__":
    main()
