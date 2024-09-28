import random


boardstate = {
    1: {'r': [2, 4], 'b': [5]},
    2: {'r': [4, 6], 'b': [1, 3, 5]},
    3: {'r': [2, 6], 'b': [5]},
    4: {'r': [2, 8], 'b': [1, 5, 7]},
    5: {'r': [2, 4, 6, 8], 'b': [1, 3, 7, 9]},
    6: {'r': [2, 8], 'b': [3, 5, 9]},
    7: {'r': [4, 8], 'b': [5]},
    8: {'r': [4, 6], 'b': [5, 7, 9]},
    9: {'r': [6, 8], 'b': [5]}
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
    find_all_paths(current_states, input_string, [1], all_paths)
    
    return all_paths

def write_paths_to_file(paths, filename="Bloque_1\\Tablero\\routes.txt"):
    """Write the list of paths to a text file."""
    with open(filename, 'w') as file:
        for path in paths:
            file.write(','.join(map(str, path)) + '\n')


def verify_routes(filename="Bloque_1\\Tablero\\routes.txt", target_state=9):
    """Read the routes from the file and verify if they end in the target state."""
    valid_routes = []
    
    try:
        with open(filename, 'r') as file:
            routes = file.readlines()
            
            for route in routes:
                path = list(map(int, route.strip().split(',')))
                if path[-1] == target_state:  # Check if the last state is the target state
                    valid_routes.append(path)
        
        if valid_routes:
            # Write successful routes to a new file called win_route.txt
            write_paths_to_file(valid_routes, filename="Bloque_1\\Tablero\\win_routes.txt")
        else:
            print(f"No routes end in state {target_state}.")
    
    except FileNotFoundError:
        print(f"File '{filename}' not found.")

def main():
    cadena = str(input("Write the string: "))
    all_paths = nfa_find_all_paths(cadena) # Start from state 1
    
    if all_paths:
        print(f"Writing all possible routes for '{cadena}' to routes.txt")
        write_paths_to_file(all_paths)
        verify_routes()
    else:
        print(f"No paths found for the string '{cadena}'.")

if __name__ == "__main__":
    main()
