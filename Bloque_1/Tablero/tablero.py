import random
import csv  

# Define the NFA transitions
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

# Define the accepting states
accepting_states = {9}  

def nfa_transition(state, char):
    """Returns the next possible states from the current state based on the input character."""
    return boardstate.get(state, {}).get(char, [])

def nfa_accepts(input_string):
    """Check if the NFA accepts the input string."""
    current_states = {1}  # Start from the initial state, which is state 1

    for char in input_string:
        next_states = set()
        for state in current_states:
            # Get next possible states for each current state and input character
            next_states.update(nfa_transition(state, char))
        
        current_states = next_states  # Move to the next states

    # Check if any of the current states is an accepting state
    return not current_states.isdisjoint(accepting_states)


def main():
    # Test the NFA with some input strings
    # test_strings = ["rb", "rbr", "b", "rrb", "brb", "rbb", "rbbrr"]
    # for string in test_strings:
    #     result = nfa_accepts(string)
    #     print(f"The string '{string}' is {'accepted' if result else 'not accepted'} by the NFA.")

    cadena = str(input("Write the string: "))
    result = nfa_accepts(cadena)
    print(f"The string '{cadena}' is {'accepted' if result else 'not accepted'} by the NFA.")

if __name__ == "__main__":
    main()
