from constants import *


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
