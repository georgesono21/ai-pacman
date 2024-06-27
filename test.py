import subprocess
import re
import argparse
def run(cli):
    command_parts = cli.split()

    with subprocess.Popen(command_parts, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
        stdout, stderr = proc.communicate()
        red_match = re.search(r"Red Win Rate: (\S+ \(\S+\))", stderr)
        blue_match = re.search(r"Blue Win Rate: (\S+ \(\S+\))", stderr)
        return red_match.group(1), blue_match.group(1)

def main(repeat, num_games, red_team, blue_team):
    cli = f"python3 -m pacai.bin.capture --red {red_team} --blue {blue_team}
    --fps 1000 -n {{}}" for i in range(repeat):
        command = cli.format(num_games)
        red, blue = run(command)
        if red and blue:
            with open("win_rates.txt", "a") as file:
                file.write(f"Iteration {i+1}:\n")
                file.write(f"Red Win Rate: {red}\n")
                file.write(f"Blue Win Rate: {blue}\n\n")
            print(f"Win rates for iteration {i+1} written to win_rates.txt")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run PACAI games and extract win rates.')
    parser.add_argument('--repeat', type=int, default=5, help='Number of times to repeat the command.')
    parser.add_argument('--games', type=int, default=50, help='Number of games to play in each command execution.')
    parser.add_argument('--red', type=str, default='pacai.student.myTeam', help='Team to set as Red.')
    parser.add_argument('--blue', type=str, default='pacai.core.baselineTeam', help='Team to set as Blue.')
    args = parser.parse_args()
    main(args.repeat, args.games, args.red, args.blue)


