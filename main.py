"""
Determinization of a Finite Paraconsistent Non-Deterministic Automaton (FPNA)

This script implements the determinization method for FPNA whose transition
are taken from the unit square [0,1]^2. It includes the determinization
examples of Section 3 and prints the resulting deterministic automaton (FPDA).
"""

# -------------------------------
# Define a Paraconsistent Automaton
#           (Example 5)
# -------------------------------

# Alphabet
Sigma = ['a', 'b']

# States
Q = {0, 1, 2, 3}

# Initial state
initial = 0

# Final states
F = [0, 3]

# Transitions:
# delta[(q1, a, q2)] = (tt,ff)
delta = {
    (0, 'b', 0): (1, 0),
    (0, 'a', 1): (0.5, 0.6),
    (0, 'a', 2): (0.4, 0.8),
    (2, 'b', 0): (1, 0),
    (1, 'b', 3): (0.8, 1)
}

# Other examples (uncomment to test):
"""
# Example 6
Sigma = ['a', 'b']
Q = {0, 1, 2, 3, 4}
initial = 0
F = [3]
delta = {
    (0, 'a', 1): (0, 0.2),
    (1, 'b', 3): (1, 1),
    (0, 'a', 2): (1, 0),
    (2, 'b', 4): (1, 0)
}
"""

"""
# Example 7
Sigma = ['a', 'b']
Q = {0, 1, 2, 3, 4, 5}
initial = 0
F = [5]
delta = {
    (0, 'a', 1): (0, 0.2),
    (1, 'b', 3): (1, 1),
    (0, 'a', 2): (1, 0),
    (2, 'b', 4): (1, 0),
    (1, 'b', 5): (0.5, 0.5)
}
"""

# -------------------------------
# Algebraic Operators in [0,1]^2
# -------------------------------

def TwistAnd(pair1,pair2):
    return (min(pair1[0],pair2[0]),max(pair1[1],pair2[1]))

def TwistOr(pair1,pair2):
    return (max(pair1[0],pair2[0]),min(pair1[1],pair2[1]))


# -------------------------------
# Complete the transition function
# -------------------------------

def complete():
    for q1 in Q:
        for q2 in Q:
            for a in Sigma:
                if (q1,a,q2) not in delta:
                    delta[(q1,a,q2)]=(0,1)
    return delta

delta=complete()


# -------------------------------
# Extended Transition function
# -------------------------------

def deltastar(q1, w, q2):
    """Compute the truth value of reaching q2 from q1 by reading word w"""
    if w == '':
        return (1, 0) if q1 == q2 else (0, 1)

    result = (0, 1)
    for r in Q:
        aux = TwistAnd(delta[(q1, w[0], r)], deltastar(r, w[1:], q2))
        result = TwistOr(result, aux)
    return result


# -------------------------------
# Reachability function
# -------------------------------

def reach(p, w):
    """Return the set of states reachable from p with colapsing to false, i.e. (0,1)"""
    return {q for q in Q if deltastar(p, w, q) != (0, 1)}


# -------------------------------
# Auxiliary functions
# -------------------------------

def add_letter(W):
    """Generate all possible words formed by appending one letter from Sigma to each word in W."""
    return [w + a for w in W for a in Sigma]

def to_state(set_states):
    """Convert a subset of states of Q to a string"""
    return ''.join(map(str, sorted(set_states)))

def is_final(set_states):
    """Return the set of final states of the determinized automaton"""
    return {state for state in set_states if any(int(s) in F for s in state)}


# -------------------------------
# Determinization Algorithm
# -------------------------------

def step1():
    """Compute all unweighted transitions of the determinized automaton."""
    
    # Store transitions found
    transitions = set()

    # Store next words to be read from the initial state
    next_words = Sigma.copy()

    # This version slightly differs from the paper's pseudocode for
    # optimization reasons: it stores the reachable states of previously
    # read words, rather than just the discovered states.
    words_states = dict()

    while next_words != []:
        words = next_words.copy()

        for w in next_words:
            # Check if we already know the previous state, otherwise compute it
            if w[:len(w) - 1] in words_states:
                prev_state = words_states[w[:len(w) - 1]]
            else:
                prev_state = to_state({initial})

            # Compute the next state reachable from the initial by reading w
            new_state = to_state(reach(initial, w))

            # If a new transition is found, add it
            if ((prev_state, w[-1], new_state) not in transitions) and (new_state != ''):
                transitions.add((prev_state, w[-1], new_state))

            # Remove word if it leads to a known state or a deadlock
            if (new_state in words_states.values()) or (new_state == ''):
                words.remove(w)

            # Store reachable state for word w
            words_states[w] = new_state

        # Generate next words by appending one letter
        next_words = add_letter(words)

    return transitions


def step2(transitions):
    """Compute the transition weights, set of states, and final states
    of the determinized automata"""
    QD = set()
    deltaD = dict()

    for (S1, a, S2) in transitions:
        QD.update([S1, S2])
        value = (0, 1)
        for p in S1:
            for q in S2:
                value = TwistOr(value, delta[(int(p), a, int(q))])
        deltaD[(S1, a, S2)] = value

    print(f"\nThe initial state is '{initial}'")
    print("The set of all states:", QD)
    print("The set of final states:", is_final(QD))

    for t in deltaD:
        print("Transition", t, "has weight", deltaD[t])


def determinization():
    """Run the full determinization procedure and print the result"""
    print("Constructing the determinization of the FPNA...")
    step2(step1())


# -------------------------------
# Run
# -------------------------------

if __name__ == "__main__":
    determinization()
