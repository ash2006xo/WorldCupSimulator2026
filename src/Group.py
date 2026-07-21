import random
from colorama import Fore, Style, init

from src.Team import Team
from src.Match import Match

init(autoreset=True)

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

        result = []
        result.append(Fore.YELLOW + "="*55)
        result.append(Fore.CYAN + f"GROUP {self.name}")
        result.append(Fore.YELLOW + "="*55)
        result.append(
            Fore.MAGENTA + f"{'Pos':<5}{'Team':<18}{'Pts':<6}{'GD':<6}{'GF'}"
        )
        
        result.append(Fore.YELLOW + "-"*52)

        for pos, team in enumerate(ranking, start=1):
            result.append(
                f"{pos:<5}"
                f"{team.name:<18}"
                f"{team.points:<6}"
                f"{team.goal_difference():+<6}"
                f"{team.goals_for}"
            )

        result.append("="*55)

        return "\n".join(result)