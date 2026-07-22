# ============================================================  
# Student : Narges Farhangi                         
# Student ID : [ 404131043 ]                        
# Project : World Cup Simulator 2026  
# Date : 31.6.1405
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

from colorama import Fore, Style, init
import src.worldcup_simulator

init(autoreset=True)

def main():
    """Temporary demo menu so we can run the whole project and
    confirm every stage works before polishing the real menu."""
    sim = src.worldcup_simulator.WorldCupSimulator()
    groups_drawn = False

    while True:
        print(Fore.YELLOW + "=" * 60)
        print(Fore.CYAN + "🏆 WORLD CUP 2026 SIMULATOR 🏆")
        print(Fore.YELLOW + "=" * 60)
        print(Fore.CYAN + "[1] 📂 Load Teams")
        print(Fore.CYAN + "[2] 🎲 Draw Groups")
        print(Fore.CYAN + "[3] ⚽ Play Group Stage")
        print(Fore.CYAN + "[4] 🏆 Simulate Tournament")
        print(Fore.CYAN + "[5] 📊 Championship Statistics")
        print(Fore.CYAN + "[6] 🥇 Knockout Bracket")
        print(Fore.CYAN + "[7] 🚪 Exit")

        choice = input(Fore.MAGENTA + "Choose an option (1-7): ").strip()

        if choice == "1":
            sim.load_teams_from_csv("worldcup_2026_teams.txt")
        
        elif choice == "2":
            if not sim.teams:
                print(Fore.RED + "Please load teams first.")
                continue
            sim.create_seeds()
            sim.draw_groups()
            groups_drawn = True
            print(Fore.GREEN + "Groups drawn successfully.")

        elif choice == "3":
            if not groups_drawn:
                print(Fore.RED+ "Please draw groups first (option 2).")
                continue
            
            sim.run_group_stage()
            for group in sim.groups:
                print(group)

        elif choice == "4":
            if not sim.teams:
                print(Fore.RED + "Please load teams first.")
                continue
            champion = sim.run_full_simulation()
            print(Fore.YELLOW + "\n" + "="*60)
            print(Fore.CYAN + "              🏆 WORLD CHAMPION 🏆")
            print(Fore.YELLOW + "="*60)
            print()
            print(Fore.GREEN + f"\n   Champion: {champion.name}")
            print()
            print(Fore.YELLOW + "="*60)

        elif choice == "5":
            if not sim.teams:
                print(Fore.RED + "Please load teams first.")
                continue
            raw = input(Fore.MAGENTA + "Number of simulations (default 1000): ").strip()
            try:
                num = int(raw) if raw else 1000
            except ValueError:
                print(Fore.RED + "Invalid number, using default 1000.")
                num = 1000
            sim.most_likely_champion(num)

        elif choice == "6":
            sim.display_bracket()

        elif choice == "7":
            print("Goodbye.")
            break

        else:
            print(Fore.RED + "Invalid option, please choose 1-7.")


if __name__ == "__main__":
    main()