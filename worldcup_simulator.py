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
import math
import csv
import random

import numpy as np
import pandas as pd

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

        Args:
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
                # Perform a random draw with a 50% chance, if True is selected, swap the two teams.
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


# ============== WORLD CUP SIMULATOR CLASS ===================


# ===================== MAIN FUNCTION ========================

# =============   TEST(temp)
if __name__ == "__main__":

    brazil = Team("Brazil", 95, 90, 1)
    france = Team("France", 92, 89, 2)
    japan = Team("Japan", 80, 82, 18)
    mexico = Team("Mexico", 81, 80, 15)

    group = Group("A", [brazil, france, japan, mexico])

    group.play_all_matches()
    for match in group.matches:
        print(match)

    print(group)