import random
import numpy as np

from src.Team import Team
from constants import *


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