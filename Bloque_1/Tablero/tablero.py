import random

# 3x3
# boardstate = {
#     1: {'r': [2, 4], 'b': [5]},
#     2: {'r': [4, 6], 'b': [1, 3, 5]},
#     3: {'r': [2, 6], 'b': [5]},
#     4: {'r': [2, 8], 'b': [1, 5, 7]},
#     5: {'r': [2, 4, 6, 8], 'b': [1, 3, 7, 9]},
#     6: {'r': [2, 8], 'b': [3, 5, 9]},
#     7: {'r': [4, 8], 'b': [5]},
#     8: {'r': [4, 6], 'b': [5, 7, 9]},
#     9: {'r': [6, 8], 'b': [5]}
# }


# 5x5
boardstate = {
    1:  {'r': [2, 6], 'b': [7]},
    2:  {'r': [6, 8], 'b': [1, 3, 7]},
    3:  {'r': [2, 8, 4], 'b': [7, 9]},
    4:  {'r': [8, 10], 'b': [3, 5, 9]},
    5:  {'r': [4, 10], 'b': [9]},
    
    6:  {'r': [2, 12], 'b': [1, 7, 11]},
    7:  {'r': [2, 6, 8, 12], 'b': [1, 3, 11, 13]},
    8:  {'r': [2, 4, 12, 14], 'b': [3, 7, 9, 13]},
    9:  {'r': [4, 8, 10, 14], 'b': [3, 5, 13, 15]},
    10: {'r': [4, 14], 'b': [5, 9, 15]},
    
    11: {'r': [6, 12, 16], 'b': [7, 17]},
    12: {'r': [6, 8, 16, 18], 'b': [7, 11, 13, 17]},
    13: {'r': [8, 12, 14, 18], 'b': [7, 9, 17, 19]},
    14: {'r': [8, 10, 18, 20], 'b': [9, 13, 15, 19]},
    15: {'r': [10, 14, 20], 'b': [9, 19]},
    
    16: {'r': [12, 22], 'b': [11, 17, 21]},
    17: {'r': [12, 16, 18, 22], 'b': [11, 13, 21, 23]},
    18: {'r': [12, 14, 22, 24], 'b': [13, 17, 19, 23]},
    19: {'r': [14, 18, 20, 24], 'b': [13, 15, 23, 25]},
    20: {'r': [14, 24], 'b': [15, 19, 25]},
    
    21: {'r': [16, 22], 'b': [17]},
    22: {'r': [16, 18], 'b': [17, 21, 23]},
    23: {'r': [18, 22, 24], 'b': [17, 19]},
    24: {'r': [18, 20], 'b': [19, 23, 25]},
    25: {'r': [20, 24], 'b': [19]},
}



def nfa_transition(state, char):
    """Returns the next possible states from the current state based on the input character."""
    return boardstate.get(state, {}).get(char, [])


def find_all_paths(current_states, input_string, current_path, all_paths):
    """Recursively finds all the paths based on the input string."""
    if not input_string:  # If the input string is empty, add the current path to all paths
        all_paths.append(current_path)
        return
    
    char = input_string[0]
    next_input = input_string[1:]
    
    for state in current_states:
        next_states = nfa_transition(state, char)
        for next_state in next_states:
            # Recursively find paths from the next state
            find_all_paths([next_state], next_input, current_path + [next_state], all_paths)


def nfa_find_all_paths(input_string, start_state=1):
    """Find all possible paths for the input string, regardless of acceptance."""
    current_states = [start_state]  # Start from state 1
    all_paths = []
    
    # Find all paths that the NFA can take for the input string
    find_all_paths(current_states, input_string, [start_state], all_paths)
    
    return all_paths


def write_paths_to_file(paths, filename):
    """Write the list of paths to a text file."""
    with open(filename, 'w') as file:
        for path in paths:
            file.write(','.join(map(str, path)) + '\n')


def verify_routes(filename="Bloque_1\\Tablero\\routes.txt", write_win_path="Bloque_1\\Tablero\\win_routes.txt", target_state=9):
    """Read the routes from the file and verify if they contain the target state."""
    valid_routes = []
    
    try:
        with open(filename, 'r') as file:
            routes = file.readlines()
            
            for route in routes:
                path = list(map(int, route.strip().split(',')))
                # Check if the target state is in the path
                if target_state in path:
                    # Create a new path without the occurrences of target state after the first one
                    new_path = []
                    found_target = False
                    
                    for state in path:
                        if state == target_state:
                            if not found_target:  # Keep the first occurrence
                                new_path.append(state)
                                found_target = True
                        else:
                            new_path.append(state)
                    
                    valid_routes.append(new_path)

        if valid_routes:
            # Write successful routes to a new file
            write_paths_to_file(valid_routes, write_win_path)
        else:
            print(f"No routes contain the target state {target_state}.")
    
    except FileNotFoundError:
        print(f"File '{filename}' not found.")


def main():
    cadena = str(input("Write the string: "))

    start_state1 = 1
    start_state2 = 5
    target1 = 25
    target2 = 21

    all_routes_player1 = "Bloque_1\\Tablero\\all_routes_player1.txt"
    all_routes_player2 = "Bloque_1\\Tablero\\all_routes_player2.txt"
    win_routes_player1 = "Bloque_1\\Tablero\\win_routes_player1.txt"
    win_routes_player2 = "Bloque_1\\Tablero\\win_routes_player2.txt"

    player1 = nfa_find_all_paths(cadena, start_state1) # Start from state 1
    player2 = nfa_find_all_paths(cadena, start_state2)
    

    write_paths_to_file(player1, all_routes_player1)
    write_paths_to_file(player2, all_routes_player2)
    verify_routes(all_routes_player1, win_routes_player1, target1)
    verify_routes(all_routes_player2, win_routes_player2, target2)
    print(f"Writing routes for '{cadena}' to both players")

if __name__ == "__main__":
    main()
