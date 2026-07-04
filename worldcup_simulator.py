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
        Initialize a Team object.

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
    
    def add_match_result(self, goals_scored: int, goals_conceded: int) -> None:
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
            
    def __str__(self) -> str:
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


# ==================== GROUP CLASS ===========================


# ==================== NOCKOUT STAGE CLASS ===================


# ============== WORLD CUP SIMULATOR CLASS ===================


# ===================== MAIN FUNCTION ========================

# =============   TEST(temp)
bad_team = Team("Mars", 150, 90, 1)