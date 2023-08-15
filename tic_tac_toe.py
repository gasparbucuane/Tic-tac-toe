def printGrid(grid):
    for row in grid:
        print(" | ".join(row))
        print("-" * 9)

def checkLine(grid, player, row):
    return all(cell == player for cell in grid[row])

def checkColumn(grid, player, col):
    return all(row[col] == player for row in grid)

def checkDiagonal(grid, player):
    diagonal1 = all(grid[i][i] == player for i in range(3))
    diagonal2 = all(grid[i][2 - i] == player for i in range(3))
    return diagonal1 or diagonal2

def winner(grid, player):
    for i in range(3):
        if checkLine(grid, player, i) or checkColumn(grid, player, i):
            return True
    return checkDiagonal(grid, player)

def play(grid, x, y, player):
    if grid[x][y] == ' ':
        grid[x][y] = player
        return True
    else:
        return False

def update_scores(scores_file, player1, player2, winner_index):
    with open(scores_file, 'a') as f:
        f.write(f"{player1}:{player2}:{winner_index}\n")

def get_scores(scores_file):
    scores = {}
    try:
        with open(scores_file, 'r') as f:
            for line in f:
                p1, p2, winner = line.strip().split(":")
                scores[(p1, p2)] = int(winner)
    except FileNotFoundError:
        pass
    return scores

def main():
    scores_file = "scores.txt"
    scores = get_scores(scores_file)

    grid = [[' ' for _ in range(3)] for _ in range(3)]
    players = []
    for i in range(2):
        valid = False
        while not valid:
            name = input(f"Enter name for Player {i + 1}: ")
            if '\n' in name or ':' in name:
                print("Player names cannot contain newline or colon characters. Try again.")
            else:
                players.append(name)
                valid = True

    current_player = 0

    print("Welcome to Tic-Tac-Toe!")
    printGrid(grid)

    for _ in range(9):
        print(f"{players[current_player]}'s turn:")
        row = int(input("Choose a row (0, 1, 2): "))
        col = int(input("Choose a column (0, 1, 2): "))

        if play(grid, row, col, 'X' if current_player == 0 else 'O'):
            printGrid(grid)

            if winner(grid, 'X'):
                print(f"{players[0]} wins!")
                update_scores(scores_file, players[0], players[1], 0)
                break
            elif winner(grid, 'O'):
                print(f"{players[1]} wins!")
                update_scores(scores_file, players[0], players[1], 1)
                break
            elif _ == 8:  # All positions filled
                print("It's a draw!")
                update_scores(scores_file, players[0], players[1], -1)

            current_player = 1 - current_player

    print("\nScores:")
    for player_pair, winner_index in scores.items():
        p1, p2 = player_pair
        if winner_index == 0:
            print(f"{p1} vs {p2}: {p1} wins")
        elif winner_index == 1:
            print(f"{p1} vs {p2}: {p2} wins")
        else:
            print(f"{p1} vs {p2}: Draw")

if __name__ == "__main__":
    main()
