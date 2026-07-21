from colorama import Fore, Style, init
from src.Match import Match
from src.Team import Team

init(autoreset=True)

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
        print()
        print(Fore.YELLOW + "=" * 50)
        print(Fore.CYAN + Style.BRIGHT + self.round_name.center(50))
        print(Fore.YELLOW + "=" * 50)
        
        for match in self.matches:
            print(
                Fore.BLUE + match.team1.name +
                Fore.WHITE + f" {match.goals1} - {match.goals2} " +
                Fore.RED + match.team2.name
            )

            if match.penalties1 is not None:
                print(
                    Fore.MAGENTA +
                    f"Penalties: {match.penalties1}-{match.penalties2}"
                )

            print(
                Fore.GREEN +
                f"Winner: {match.winner.name}"
            )

            print()
